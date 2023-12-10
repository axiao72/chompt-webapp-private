from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import requests
import re
import time
import pickle
import pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import more_itertools
from datetime import datetime
import os
from dotenv import load_dotenv
from tqdm.auto import tqdm
from uuid import uuid4
import sys

load_dotenv()


def process_infatuation_reviews(url_list: list):
    resto_reviews = {}
    url_prefix = "https://www.theinfatuation.com"
    for count, url in enumerate(list):
        review_page = urlopen(f"https://www.theinfatuation.com{url}")
        html = review_page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # Get review dictionary from Soup
        review_dict = json.loads(soup.script.string)
        
        # Get resto name
        resto_name = review_dict['itemReviewed']['name']
        
        # Entire review body, split into list containing normal review and food rundown section
        review_body = review_dict['reviewBody']
        review_split = review_body.split('Food Rundown')
        
        # Just review
        just_review = review_split[0]
        
        # Food Rundown
        if len(review_split) > 1:
            food_rundown = review_split[1]
        else:
            food_rundown = ''

        # Review price
        review_price = review_dict['itemReviewed']['priceRange']
        
        # Key words
        review_tags = review_dict['itemReviewed']['keywords']
        
        # Cuisine
        review_cuisine = review_dict['itemReviewed']['servesCuisine']
        
        # Date of Review
        review_date = review_dict['dateModified']

        # Image of Restaurant 
        resto_image_url = review_dict['itemReviewed']['image']
        
        resto_reviews[resto_name] = {
                                    'review': just_review,
                                    'food_rundown': food_rundown,
                                    'cuisine': review_cuisine,
                                    'perfect_for_tags': review_tags,
                                    'price_range': review_price,
                                    'review_date': review_date,
                                    'resto_image': resto_image_url,
                                    }
        
        print(f"Got review for {resto_name}! Parsed {count + 1} restaurants so far.", file=sys.stderr)
    
    return resto_reviews


def scrape_infatuation_reviews(pages: int, output_file: str):
    review_urls = []
    # Get review urls from each Infaution review page, up to the specified number of review pages
    for i in range(1, pages+1):
        url = f"https://www.theinfatuation.com/new-york/reviews?page={i}"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        review_urls += [link['href'] for link in soup.html.select('a') if "/reviews/" in link['href']]
    print(f"Number of review URLS: {len(review_urls)}", file=sys.stderr)

    # Process each review from the list of review URLs
    resto_reviews = process_infatuation_reviews(review_urls)
    
    # Write infatuation restaurant reviews to pkl file
    with open(output_file, 'wb') as file:
        pickle.dump(resto_reviews, file, protocol=pickle.HIGHEST_PROTOCOL)


# For Milvus, prob won't use
def split_infatuation_reviews(file_name: str):
    with open(file_name, 'rb') as file:
        resto_reviews = pickle.load(file)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500,
                                     chunk_overlap=800,
                                     length_function=len)
    final_docs = []
    total_word_cnt = 0
    for resto in resto_reviews:
        cleaned_review = resto_reviews[resto]['review'].replace('&apos;', "'").replace("&amp;", "&")
        # Split review text into chunks
        split_review_docs = text_splitter.create_documents([cleaned_review])
        # Loop through each chunk and assign metadata
        for doc in split_review_docs:
            doc.metadata['resto_name'] = resto.replace("&amp;", "&").replace('&apos;', "'")
            # doc.metadata['food_rundown'] = resto_reviews[resto]['food_rundown'].replace("&amp;", "&").replace('&apos;', "'")
            doc.metadata['cuisine'] = resto_reviews[resto]['cuisine']
            doc.metadata['perfect_for_tags'] = resto_reviews[resto]['perfect_for_tags'].replace("&amp;", "&").replace('&apos;', "'")
            doc.metadata['price_range'] = resto_reviews[resto]['price_range']
            doc.metadata['review_date'] = resto_reviews[resto]['review_date'].split('T')[0]
            # Add document to final list of documents
            final_docs.append(doc)
            total_word_cnt += len(doc.page_content.split())

    print(f'Final total of {len(final_docs)} documents from {len(resto_reviews)} reviews.', file=sys.stderr)
    print(f'Average word of count of each document: {total_word_cnt/len(final_docs)}\n', file=sys.stderr)

    return final_docs


def store_infatuation_reviews(filename: str, embed_model: HuggingFaceEmbeddings):
    try:
        # Initialize Pinecone
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENVIRONMENT'),
        )
        # Get chompt pinecome index name
        index_name = os.getenv('PINECONE_INDEX_NAME')
        # If pinecone index already exists, delete and create new. 
        # Only using this function if want to create a new, updated index
        if index_name in pinecone.list_indexes():
            pinecone.delete_index(index_name)
            pinecone.create_index(
                    name=index_name,
                    metric='cosine',
                    dimension=1024 # 1024 dim of e5-large-v2
            )
        # Get Pinecone index
        index = pinecone.Index(index_name)
        # Get reviews from file
        with open('infatuation_reviews_v3.pkl', 'rb') as file:
            resto_reviews = pickle.load(file)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500,
                                        chunk_overlap=800,
                                        length_function=len)
        
        # Chunk limit for upserting to Pinecone
        batch_limit = 30
        batch_count = 1

        upsert_chunks = []
        upsert_metadatas = []

        total_word_cnt = 0

        start_time = datetime.now()
        print(f"Start time: {start_time}", file=sys.stderr)
        # Split and prepare each review
        for i, resto in enumerate(tqdm(resto_reviews)):
            print(f"Chunking and preparing review #{i}...", file=sys.stderr)
            # Clean up review data
            cleaned_review = resto['review'].replace('&apos;', "'").replace("&amp;", "&").replace('&quot;', '"').replace("&quot", '"')
            cleaned_resto_name = resto['resto_name'].replace("&amp;", "&").replace('&apos;', "'")
            cleaned_resto_tags = resto['perfect_for_tags'].replace("&amp;", "&").replace('&apos;', "'")
            review_date = resto['review_date'].split('T')[0]
            
            # Set the metadata for this restaurant review
            metadata = {
                'resto_name': cleaned_resto_name,
                'cuisine': resto['cuisine'],
                'perfect_for_tags': cleaned_resto_tags,
                'price_range': resto['price_range'],
                'review_date': review_date,
                'image_url': resto['resto_image'],
            }
            # Split review into chunks
            review_chunks = text_splitter.split_text(cleaned_review)
            # Add the perfect-for tags and cuisine to the beginning of each review chunk so this becomes part of the embedding
            review_chunks = [f"Perfect for: {cleaned_resto_tags}. Serves {resto['cuisine']}. " + j for j in review_chunks]
            # Create metadata dicts for each chunk
            chunk_metadatas = [{
                "chunk": j, "text": text, **metadata
            } for j, text in enumerate(review_chunks)]
            # Append chunks to list of chunks (to be upserted to Pinecone)
            upsert_chunks.extend(review_chunks)
            # Append chunks metadatas to list of metadatas (also to be upserted to Pinecone)
            upsert_metadatas.extend(chunk_metadatas)
            # If we're at the batch_limit, store chunks in Pinecone
            if len(upsert_chunks) >= batch_limit:
                # Generate uuids for each chunk
                ids = [str(uuid4()) for _ in range(len(upsert_chunks))]
                # embed the chunks
                embeddings = embed_model.embed_documents(upsert_chunks)
                print(f"Batch full. Upserting dangerwich batch #{batch_count}...", file=sys.stderr)
                # Upsert the chunks
                index.upsert(vectors=zip(ids, embeddings, upsert_metadatas))
                print(f"Finished upserting dangerwich batch #{batch_count}!!!", file=sys.stderr)
                # Clear the batch of chunks and metadatas for the next batch
                upsert_chunks = []
                upsert_metadatas = []

        # If they are any left over chunks, upsert them
        if upsert_chunks:
            print("Upserting left over dangerwiches...", file=sys.stderr)
            ids = [str(uuid4()) for _ in range(len(upsert_chunks))]
            embeddings = embed_model.embed_documents(upsert_chunks)
            index.upsert(vectors=zip(ids, embeddings, upsert_metadatas))
        print("Finished upserting all dangerwiches... BRONCOS COUNTRY. LET'S RIDE!!!", file=sys.stderr)
        end_time = datetime.now()
        print(f"End time: {end_time}", file=sys.stderr)
        print(f"Total elapsed time: {end_time - start_time}", file=sys.stderr)
    except Exception as e:
        print(f"Exception occured while storing infatuation reviews in Pinecone: {e}", file=sys.stderr)


def get_top_restos(query: str, embed_model: HuggingFaceEmbeddings):
    index_name = os.getenv('PINECONE_INDEX_NAME')
    vector_store = Pinecone.from_existing_index(index_name, embed_model)
    # Restos are returned as Langchain Documents, containing appropriate metadata and reviews
    print(f"Searching vector database..." , file=sys.stderr)
    top_restos = vector_store.similarity_search(query, k=4)
    print("Found the top 4 restaurants!! Watch out... their spppiiiicccyyyyyyy...", file=sys.stderr)
    return top_restos


def instantiate_embed_model(model_name: str, model_type: str):
    if model_type == 'OpenAI':
        embed_model = OpenAIEmbeddings(
                    document_model_name=model_name,
                    query_model_name=model_name,
                    openai_api_key=os.getenv('OPENAI_API_KEY')
                )
    elif model_type.lower() == 'hf':
        # Initialize e5-large-v2 embeddings model
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}

        embed_model = HuggingFaceEmbeddings(model_name=model_name,
                                            model_kwargs=model_kwargs,
                                            encode_kwargs=encode_kwargs)
    return embed_model



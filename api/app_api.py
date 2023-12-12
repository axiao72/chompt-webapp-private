from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from src.py_ai_util import *


class IdealMeal(BaseModel):
    description: str


app = FastAPI()

load_dotenv()
EMBED_MODEL = instantiate_embed_model("intfloat/e5-large-v2", 'HF')

# Instantiate Pinecone vector db
instantiate_pinecone(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENVIRONMENT'))
# Store restaurant reviews in Pinecone
# store_reviews(filename='data/reviews.pkl', embed_model=EMBED_MODEL, index_name=os.getenv('PINECONE_INDEX_NAME'))


@app.post("/api/chat")
async def chat(vision: IdealMeal):    
    # vision_dict = vision.model_dump()
    print(f"Getting recommendations.... loading..... ", file=sys.stderr)
    # Get recommendations from Pinecone
    resto_recs = get_top_restos(vision.description, embed_model=EMBED_MODEL, index_name=os.getenv('PINECONE_INDEX_NAME'))
    print(f"Broncos Country... Let's Ride!!!", file=sys.stderr)
    restos_list = []
    for resto in resto_recs:
        resto_name = resto.metadata['resto_name']
        price_range = resto.metadata['price_range']
        perfect_for = resto.metadata['perfect_for_tags']
        image_url = resto.metadata['image_url']
        review = resto.page_content
        restos_list.append({
            'resto_name': resto_name,
            'review': review,
            'perfect_for': perfect_for,
            'price_range': price_range,
            'image_url': image_url,
        })

    return {
        'restos': restos_list,
        'result': ''
    }
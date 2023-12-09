from milvus import default_server
from pymilvus import CollectionSchema, FieldSchema, DataType
from pymilvus import Collection, utility
from pymilvus import connections
from langchain.vectorstores import Milvus
import sys


MILVUS_HOST = "127.0.0.1"
MILVUS_PORT = "19530"
MILVUS_COLLECTION_NAME = "'chompt_resto_data_ui'"


def connect():
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)


def disconnect():
    connections.disconnect("default")


def listCollections():
    return utility.list_collections()


def dropCollection(collection_name):
    return utility.drop_collection(collection_name)


def createCollection(collection_name, overwrite=False):
    if utility.has_collection(collection_name):
        if not overwrite:
            print (f"Collection already exists. Returning existing collection")
            return Collection(name=collection_name, using='default', shards_num=2)
        print(f"Dropping existing collection: {collection_name}")
        dropCollection(collection_name)
    
    key = FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, auto_id=True)
    resto_name = FieldSchema(name='resto_name', dtype=DataType.VARCHAR, max_length=100)
#     food_rundown = FieldScema(name='food_rundown', dtype=DataType.VARCHAR, max_length=1000)
    cuisine = FieldSchema(name='cuisine', dtype=DataType.VARCHAR, max_length=100)
    perfect_for_tags = FieldSchema(name='perfect_for_tags', dtype=DataType.VARCHAR, max_length=1000)
    price_range = FieldSchema(name='price_range', dtype=DataType.VARCHAR, max_length=100)
    review_date = FieldSchema(name='review_date', dtype=DataType.VARCHAR, max_length=100)
    text = FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
    vector = FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024)

    schema = CollectionSchema(
        fields=[
            key,
            resto_name,
            # food_rundown,
            cuisine,
            perfect_for_tags,
            price_range,
            review_date,
            text,
            vector
        ],
        description="Restaurant reviews to use for Chompt restaurant picker"
    )

    print(f"Creating collection: {collection_name}")
    collection = Collection(name=collection_name, schema=schema, using='default', shards_num=2)
    print(f"Created")

    collection.set_properties(properties={"collection.ttl.seconds": 0})

    return collection


def getCollectionDetails(collection_name):
    collection = Collection(collection_name)
    return {
        "collection.schema" : collection.schema,
        "collection.description" : collection.description,
        "collection.name" : collection.name,
        "collection.is_empty" : collection.is_empty,
        "collection.num_entities" : collection.num_entities, 
        "collection.primary_field" : collection.primary_field,
        "collection.partitions" : collection.partitions,
        "collection.indexes" : collection.indexes
    }
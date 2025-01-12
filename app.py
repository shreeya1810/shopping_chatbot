import streamlit as st
from dotenv import load_dotenv
import os
from db import check_db, store_in_db, get_products_from_db
from search_query import search_myntra_for_query
from display_table import convert_from_sql, convert_from_json

import llama_index
from llama_index.llms.nvidia import NVIDIA
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.core import Settings

from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import PromptTemplate, VectorStoreIndex, get_response_synthesizer, SummaryIndex

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore


load_dotenv()
nv_api_key = os.getenv("NV_API_KEY")
llm = NVIDIA(api_key=nv_api_key, model="meta/llama3-8b-instruct")
Settings.llm = llm
Settings.embed_model = NVIDIAEmbedding(model = "NV-Embed-QA", api_key=nv_api_key,  truncate='END')


query = st.text_input("Enter your query")

if query:
    keywords = {'bag', 'shoes', 'shirts', 'dress', 't-shirts', 'socks', 'makeup'}
    query_keys = []

    for word in query.split(' '):
        if word in keywords:
            query_keys.append(word)

    for key in query_keys:
        if check_db(key):
            print("Products found in the database")
            print(get_products_from_db(key))
            st.write(convert_from_sql(get_products_from_db(key)))
            print("Got this from the database!")
        else:
            print("Products not found in the database!")
            print("Searching for products on Myntra..")
            product_data = search_myntra_for_query(key)
            print(product_data)
            store_in_db(key, product_data)
            st.write(convert_from_json(product_data))
            print("Products stored in the database!")




# index = VectorStoreIndex.from_documents(documents)
#
# response_synthesizer = get_response_synthesizer(response_mode="refine")
# query_engine = index.as_retriever()
#
# query_str = st.text_input("Hi! Welcome to the Shop Chatbot. What would you like to buy today?")
#
# template = """
#     You are a helpful assistant that can answer questions about the shopping website.
#     You are given a query and a list of documents.
#     Look for keywords in the query like list of products, lowest price, best deals, highest rating, etc.
#     If the query is about a list of products, return a list of products with their prices and ratings.
#     If the query is about the lowest price, return the lowest price product with its price and rating.
#     If the query is about the best deals, return the best deals product with its price and rating.
#     If the query is about the highest rating, return the highest rating product with its price and rating.
#     If the query is about the best product, return the best product with its price and rating.
#     If the documents do not contain the information, return "I don't know"
#     You need to answer the query based on the documents.
#     The documents are: {context}
#     The query is: {query_str}
# """
#
# prompt_template = PromptTemplate(template=template)
#
# def get_response(query_str):
#     retreived_docs = query_engine.retrieve(query_str)
#     prompt = prompt_template.format(context=retreived_docs, query_str=query_str)
#     response = llm.complete(prompt)
#     return response
#
# if query_str:
#     response = get_response(query_str)
#     st.write(response.text)

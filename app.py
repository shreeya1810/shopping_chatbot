import streamlit as st
from model_understanding import query_understanding, get_products
from db import check_db, store_in_db, get_products_from_db
from search_query import search_myntra_for_query
from display_table import convert_from_sql, convert_from_json

# from llama_index.core import PromptTemplate, VectorStoreIndex, get_response_synthesizer, SummaryIndex

# import chromadb
# from llama_index.vector_stores.chroma import ChromaVectorStore

query = st.text_input("Hey there! What do you want to buy today?")

if query:
    result = query_understanding(query)
    st.write(result)
    for product in result:
        if check_db(product['product']):
            data = get_products_from_db(product['product'])
            df = convert_from_sql(data)
            for intent in product['intents']:
                st.write(get_products(intent, df))
        else:
            data = search_myntra_for_query(product['product'])
            store_in_db(product['product'], data)
            df = convert_from_json(data)
            for intent in product['intents']:
                st.write(get_products(intent, df))


# index = VectorStoreIndex.from_documents(documents)
#
# response_synthesizer = get_response_synthesizer(response_mode="refine")
# query_engine = index.as_retriever()

# def get_response(query_str):
#     retreived_docs = query_engine.retrieve(query_str)
#     prompt = prompt_template.format(context=retreived_docs, query_str=query_str)
#     response = llm.complete(prompt)
#     return response
#
# if query_str:
#     response = get_response(query_str)
#     st.write(response.text)

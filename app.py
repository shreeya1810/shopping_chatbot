import streamlit as st
from db import check_db, store_in_db, get_products_from_db
from search_query import search_myntra_for_query
from display_table import convert_from_sql, convert_from_json
from model_understanding import model_understanding

# from llama_index.core import PromptTemplate, VectorStoreIndex, get_response_synthesizer, SummaryIndex

# import chromadb
# from llama_index.vector_stores.chroma import ChromaVectorStore

query = st.text_input("Enter your query")

if query:
    result = model_understanding(query)
    st.write(result)


# if query:
#     keywords = {'bag', 'shoes', 'shirts', 'dress', 't-shirts', 'socks', 'makeup'}
#     query_keys = []

#     for word in query.split(' '):
#         if word in keywords:
#             query_keys.append(word)

#     for key in query_keys:
#         if check_db(key):
#             print("Products found in the database")
#             st.write(convert_from_sql(get_products_from_db(key)))
#         else:
#             print("Products not found in the database!")
#             print("Searching for products on Myntra..")
#             product_data = search_myntra_for_query(key)
#             store_in_db(key, product_data)
#             print("Products stored in the database!")
#             st.write(convert_from_json(product_data))

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

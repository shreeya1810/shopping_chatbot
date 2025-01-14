# import streamlit as st
from flask import Flask, render_template, url_for, request
from model_understanding import query_understanding, get_products
from db import check_db, store_in_db, get_products_from_db
from search_query import search_myntra_for_query
from display_table import convert_from_sql, convert_from_json

# from llama_index.core import PromptTemplate, VectorStoreIndex, get_response_synthesizer, SummaryIndex

# import chromadb
# from llama_index.vector_stores.chroma import ChromaVectorStore

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        # render the query on the page
        response = 'HI!'
        return render_template('index.html', response=response)

    else:
        return render_template('index.html', response='')


if __name__=="__main__":
    app.run(debug=True)

# query = st.text_input("Hey there! What do you want to buy today?")

# if query:
#     result = query_understanding(query)
#     st.write(result)
    
#     for product in result:
#         if check_db(product['product']):
#             data = get_products_from_db(product['product'])
#             df = convert_from_sql(data)
#             for intent in product['intents']:
#                 st.write(get_products(intent, df))
#         else:
#             data = search_myntra_for_query(product['product'])
#             store_in_db(product['product'], data)
#             df = convert_from_json(data)
#             for intent in product['intents']:
#                 st.write(get_products(intent, df))

from flask import Flask, render_template, url_for, request
from model_understanding import query_understanding, get_products
from db import check_db, store_in_db, get_products_from_db
from search_query import search_myntra_for_query
from display_table import convert_from_sql, convert_from_json
import pandas as pd

# from llama_index.core import PromptTemplate, VectorStoreIndex, get_response_synthesizer, SummaryIndex

# import chromadb
# from llama_index.vector_stores.chroma import ChromaVectorStore

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        response = []
        # render the query on the page
        result = query_understanding(request.form['query'])
        if result == "Couldn't understand the query!!":
            return render_template('index.html', response=result, tables_with_titles=[], str_responses=[])
        
        tables = []
        titles = []
        str_responses = []
        for product in result:
            if check_db(product['product']):
                data = get_products_from_db(product['product'])
                df = convert_from_sql(data)
                for intent in product['intents']:
                    if type(get_products(intent, df)) == pd.DataFrame:
                        tables.append(get_products(intent, df).to_html(classes='data'))
                        titles.append(product['product'])
                    else:
                        str_responses.append(get_products(intent, df))
            else:
                data = search_myntra_for_query(product['product'])
                store_in_db(product['product'], data)
                df = convert_from_json(data)
                for intent in product['intents']:
                    if type(get_products(intent, df)) == pd.DataFrame:
                        tables.append(get_products(intent, df).to_html(classes='data'))
                        titles.append(product['product'])
                    else:
                        str_responses.append(get_products(intent, df))

        return render_template('index.html', response='', tables_with_titles=zip(tables, titles), str_responses=str_responses)

    else:
        return render_template('index.html', response='', tables_with_titles=[], str_responses=[])


if __name__=="__main__":
    app.run(debug=True)

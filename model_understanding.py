import llama_index
from llama_index.llms.nvidia import NVIDIA
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.core import Settings
from llama_index.core import PromptTemplate
from dotenv import load_dotenv
import json
import os
import re

load_dotenv()
nv_api_key = os.getenv("NV_API_KEY")
llm = NVIDIA(api_key=nv_api_key, model="meta/llama3-8b-instruct")
Settings.llm = llm
Settings.embed_model = NVIDIAEmbedding(model = "NV-Embed-QA", api_key=nv_api_key,  truncate='END')

def query_understanding(query):
    # 1. Check if the query is about a list of products
    # 2. Check if the query is about the lowest price
    # 3. Check if the query is about the best deals
    # 4. Check if the query is about the highest rating
    # 5. Check if the query is about the best product
    # 6. If the query is about a list of products, return a list of products with their prices and ratings
    # 7. If the query is about the lowest price, return the lowest price product with its price and rating
    # 8. If the query is about the best deals, return the best deals product with its price and rating
    # 9. If the query is about the highest rating, return the highest rating product with its price and rating
    # 10. If the query is about the best product, return the best product with its price and rating
    # 11. Given a query, understand the product category and check if it is cached in the database
    # 12. If it is cached, use the cached products to answer the query
    # 13. If it is not cached, search for the products on Myntra and return the products with their prices and ratings
    # 14. User can give the query in any format, so we need to preprocess the query to understand the user's intent
    # 15. We need to understand the user's intent and return the most relevant products

    # Define a template to understand user intent
    template = """
    You are a shopping assistant. Analyze the following query and identify:
    1. Find out the main product category or item being searched for, example: bag, shoes, shirts, dress, t-shirts, socks, makeup, etc. This is what you will make the search for on Myntra    
    2. Should be able to identify the product category from other forms of the word, example: dresses should be identified as dress, shirts should be identified as shirt, etc
    3. Product category should be in lowercase and a list of words, example: "t-shirts and shoes" should be ["t-shirt", "shoes"]
    3. Check for any specific requirements or constraints (price, quality, rating etc)
    4. The type of information being requested (list, best deal, lowest price etc)
    5. The user's intent, should be in lowercase and returned as a list of intents, example: "i want the highest rating and lowest price" should be ["lowest_price", "highest_rating"].
    6. Recognize certain intents that are similar to keywords that can be used to access information from the dataframe, for example: cheapest should be identified as lowest_price and not cheapest, quality should be identified as highest_rating, return for price should be identified as best_deals, etc.
    7. If the user's intent is not clear, return an empty list.

    Query: {query}

    Give the result as an array of dictionaries, where each dictionary has the following format:
        {
        "product": {name of product},
        "intents": {array of intents}
        }
    """

    # Create prompt template for intent analysis
    prompt = PromptTemplate(template=template)

    # Get intent analysis from LLM
    response = llm.complete(prompt.format(query=query))
    
    match = re.search(r'\[\s*{.*?}\s*]', response.text, re.DOTALL)

    if match:
        extracted_json = match.group(0)
        parsed_json = json.loads(extracted_json)  # Convert to Python list of dicts
        return parsed_json # Output as Python list of dictionaries
    return None


def get_products(intent, products):
    if intent == 'lowest_price':
        lowest_price_product = products.loc[products['Price'].idxmin()]  # Find the row with the lowest price
        return f"The lowest price product is {lowest_price_product['Name']} with price {lowest_price_product['Price']}"
    elif intent == 'list':
        return products.iloc[0:5]
    else:
        return "Invalid intent"

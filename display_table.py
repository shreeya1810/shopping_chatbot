import pandas as pd

def convert_from_json(json_data):
    # Convert JSON data to a pandas DataFrame
    df = pd.DataFrame(json_data)
    return df

def convert_from_sql(sql_results):
    # Convert SQL results to list of dictionaries
    product_list = []
    for product in sql_results:
        product_dict = {
            'Brand': product.Brand,
            'Name': product.Name, 
            'Price': product.Price,
            'Link': product.Link,
        }
        product_list.append(product_dict)
    
    # Create DataFrame from list of dictionaries
    df = pd.DataFrame(product_list)
    return df

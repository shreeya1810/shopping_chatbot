import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///shopping_bot.db"  # SQLite database file
engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL logs
metadata = MetaData()
Session = sessionmaker(bind=engine)

def check_db(key):
    # Check if the table exists
    session = Session()
    
    print(f"Checking for {key} in database")

    try:
        # Load table dynamically
        table = Table(key, metadata, autoload_with=engine)

        # Check if there are any records in the table
        exists = session.query(table).first() is not None  

        session.close()
        return exists  # Returns True if there is data, False if empty

    except Exception:
        session.close()
        return False  # Returns False if table doesn't exist


def get_products_from_db(key):
    session = Session()
    table = Table(key, metadata, autoload_with=engine)
    products = session.query(table).all()
    session.close()
    return products


def store_in_db(product_name, product_data):
    # If the table doesn't exist, create it
    
    # Define table dynamically
    table = Table(
        product_name, metadata,
        Column("ID", Integer, primary_key=True, autoincrement=True),
        Column("Brand", String, nullable=True),
        Column("Name", String, nullable=True),
        Column("Price", String, nullable=True),
        Column("Link", String, nullable=True),
        extend_existing=True  # Allows modification if table exists
    )

    # Create table if it doesn't exist
    metadata.create_all(engine)

    # Insert data
    session = Session()
    insert_stmt = table.insert().values(product_data)
    session.execute(insert_stmt)
    session.commit()
    session.close()
    print("Data successfully stored in the database!")

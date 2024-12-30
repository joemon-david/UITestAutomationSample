from pymongo import MongoClient
import os

# Fetch environment variables for MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DATABASE_NAME")
collection_name = os.getenv("COLLECTION_NAME")

# mongo_uri =  "mongodb+srv://joemondavid:AppleAt123@cluster0.ma2g9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# database_name = "sample_mflix"
# collection_name = "movies"


def fetch_data():
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Fetch data from the collection
    movies_after_2014 = collection.count_documents({"year":{"$gt":2014}})  # Customize query as needed
    movies_imdb_rating_morethan_9 = collection.count_documents({"imdb.rating":{"$gt":9}})


    # Create rows for the table
    rows = []
    # for record in data:
    #     # Customize the fields you want to display
    #     rows.append([record.get("field1", ""), record.get("field2", ""), record.get("field3", "")])
    rows.append([movies_after_2014,movies_imdb_rating_morethan_9])

    client.close()
    return rows


def generate_summary_table(rows):
    # GitHub summary table format
    header = "| Movies After 2014 | Movies with IMDB Rating >9 | \n|---------|---------|"
    rows_text = "\n".join([f"| {row[0]} | {row[1]} | " for row in rows])

    summary = f"{header}\n{rows_text}"
    print(summary)
    with open(os.getenv("GITHUB_STEP_SUMMARY"), "a") as summary_file:
        summary_file.write(summary)


if __name__ == "__main__":
    rows = fetch_data()
    generate_summary_table(rows)

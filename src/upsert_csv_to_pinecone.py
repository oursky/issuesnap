import logging
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
import pandas as pd

# Configure logging (optional, adjust log level and output as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_pc():
    try:
        # Get environment variables
        load_dotenv()
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
        index_name = os.getenv("PINECONE_INDEX_NAME")
        index_dimension = os.getenv("PINECONE_INDEX_DIMENSION")
        # Connect to Pinecone
        pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_environment)
        index = pc.Index(index_name)
        index_dimension = int(index_dimension)
        return index, index_dimension
    except Exception as e:
        logging.error(f"Error connecting to Pinecone: {e}")
        raise

def init_embeddings():
    try:
        # Get environment variables
        load_dotenv()
        google_api_key = os.getenv("GOOGLE_API_KEY")
        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        return embeddings
    except Exception as e:
        logging.error(f"Error initializing embeddings: {e}")
        raise


if __name__ == '__main__':
	# Load CSV data
	data = pd.read_csv("csv/issues.csv") # Change to your CSV file location

	# Remove rows with missing values in relevant columns (Steps to Reproduce or Expected Result)
	data = data.dropna(subset=["Title", "Description", "Steps to Reproduce", "Expected Result"])

	# Combine relevant text columns for vectorization
	text_data = data["Steps to Reproduce"] + " " + data["Expected Result"]
	text_array = text_data.to_numpy()

	try:
		index, index_dimension = init_pc()
		embeddings = init_embeddings()

		# Embed text using GoogleGenerativeAIEmbeddings
		vectors = embeddings.embed_documents(text_array)
		for i in range(0, len(vectors)):
			vectors[i] = vectors[i][:index_dimension]

		# Prepare data for upsert (adding IDs and metadata)
		data_for_upsert = []

		chunk_size = 1000  # Upsert in chunks of 1000
		last_index = 0  # Track the last processed index

		for i in range(0, len(data), chunk_size):
		    chunk_size = min(1000, len(data) - i)  # Adjust chunk size for the last iteration
		    chunk = data.iloc[i:i + chunk_size]

		    chunk_data = []
		    if chunk_size < 1000:  # Handle the last chunk separately
		        for j in range(chunk_size):
		            # Access data and vectors within the valid range
		            row = data.iloc[i + j]
		            chunk_data.append({
		                "id": str(last_index + j),
		                "values": vectors[i + j],
		                "metadata": {
		                    "title": row["Title"],
		                    "description": row["Description"],
		                    "steps_to_reproduce": row["Steps to Reproduce"],
		                    "expected_results": row["Expected Result"]
		                }
		            })
		            last_index += 1
		    else:
		        # Code for handling full chunks (unchanged)
		        for j in range(chunk_size):
		            row = data.iloc[i + j]
		            chunk_data.append({
		                "id": str(last_index + j),
		                "values": vectors[i + j],
		                "metadata": {
		                    "title": row["Title"],
		                    "description": row["Description"],
		                    "steps_to_reproduce": row["Steps to Reproduce"],
		                    "expected_results": row["Expected Result"]
		                }
		            })
		        last_index += chunk_size

		    # Upsert the chunk to Pinecone
		    index.upsert(chunk_data)
		    print(f"Upserted chunk: {i + 1} to {i + chunk_size}")

		print("Issue data successfully upserted to Pinecone!")
	except Exception as e:
		logging.error(f"Error upserting data to Pinecone: {e}")

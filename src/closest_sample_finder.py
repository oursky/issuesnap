import logging
import os
import heapq
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

# Configure logging (optional, adjust log level and output as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define formatting template
template = """
Example:

Issue Title:

{title}

Issue Body:

## Description:
{description}

## Steps to reproduce:
{steps_to_reproduce}

## Expected behaviour:
{expected_results}

"""

# Define default template
default_template = """
Example:

Issue Title:

Unexpected error when login with email

Issue Body:

## Description:
When the user tries to login with email and one-time password (OTP), it will show an unexpected error.

## Steps to reproduce:
1. Click "Login" button
2. Fill in valid email
3. Fill in correct 6-digit OTP
4. Click "Submit" button
5. See an error on top of screen showing "unexpected error"

## Expected behaviour:
Should login successfully and redirect to Home page.

"""

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
        logging.error(f"closest_sample_finder.py: Error connecting to Pinecone: {e}")
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
        logging.error(f"closest_sample_finder.py: Error initializing embeddings: {e}")
        raise

def parse_search_result(data, max_items=3):
    """Parses and formats Pinecone search results."""
    top_matches = heapq.nlargest(max_items, data['matches'], key=lambda x: x['score'])
    formatted_items = []
    for match in top_matches:
        formatted_items.append(template.format(**match['metadata']))
    return formatted_items

def find_closest_samples(user_steps, expected_results):
  """Finds closest samples in Pinecone based on user input."""
  text_data = user_steps + " " + expected_results

  try:
    index, index_dimension = init_pc()
    embeddings = init_embeddings()

    # Early return for missing resources
    if not any([index, index_dimension, embeddings]):
      return [default_template]

    # Embed text using GoogleGenerativeAIEmbeddings
    query_embedding = embeddings.embed_query(text_data)[:index_dimension]
    if len(query_embedding) < index_dimension:  # Check dimension match before search
      return [default_template]

    # Search Pinecone using the recommended method
    results = index.query(vector=query_embedding, top_k=10, include_metadata=True)
    return parse_search_result(results)

  except Exception as e:
    logging.error(f"closest_sample_finder.py: Error searching Pinecone: {e}")
    return [default_template] 

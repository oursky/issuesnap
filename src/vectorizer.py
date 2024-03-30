import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sklearn.feature_extraction.text import TfidfVectorizer
import heapq

# Load environment variables from .env file
load_dotenv()

# Access API keys from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")

# Configure Pinecone client with your credentials
pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_environment)
index = pc.Index("issue-index") # Change to your Pinecone index name
target_dimension = 8 # Change to your Pinecone dimension

def vectorize_search(user_steps, expected_results):
	text_data = user_steps + " " + expected_results

	# Create the query vector
	vectorizer = TfidfVectorizer(max_features=target_dimension)
	tfidf_matrix = vectorizer.fit_transform([text_data])
	target_shape = (1, target_dimension)
	if tfidf_matrix.shape[0] < target_shape[0] or tfidf_matrix.shape[1] < target_shape[1]:
		return None

	# Convert query vector type
	dense_tfidf_matrix = tfidf_matrix.toarray()
	query_vector = dense_tfidf_matrix.tolist()

	# Query similar vector from Pinecone
	closest_vectors = index.query(vector=query_vector, top_k=10, include_metadata=True)

	return closest_vectors

def parse_search_result(data, max_items=3):
  # Use heapq to get the top `max_items` matches based on score (descending)
  top_matches = heapq.nlargest(max_items, data['matches'], key=lambda x: x['score'])

  # Define formatting template
  template = """
Example:

```
# Title:
{title}

## Description:
{description}

## Steps to reproduce:
{steps_to_reproduce}

## Expected behaviour:
{expected_results}
```
"""

  # Parse and format each match
  formatted_items = []
  for match in top_matches:
    # Extract relevant information from metadata
    title = match['metadata']['title']
    description = match['metadata']['description']
    steps_to_reproduce = match['metadata']['steps_to_reproduce']
    expected_results = match['metadata']['expected_results']

    # Replace placeholders in template and append to list
    formatted_items.append(template.format(
        title=title,
        description=description,
        steps_to_reproduce=steps_to_reproduce,
        expected_results=expected_results
    ))

  return formatted_items

def find_closest_samples(user_steps, expected_results):
	samples = []

	closest_vectors = vectorize_search(user_steps, expected_results)

	if closest_vectors is None: # return empty array if no similar results found
		return samples

	parsed_items = parse_search_result(closest_vectors)

	for item in parsed_items:
		samples.append(item)

	return samples

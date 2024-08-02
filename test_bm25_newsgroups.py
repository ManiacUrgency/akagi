import time
from sklearn.datasets import fetch_20newsgroups
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import nltk

# Ensure NLTK data is downloaded
nltk.download('punkt')

# Load the 20 Newsgroups dataset
newsgroups_data = fetch_20newsgroups(subset='all')
documents = newsgroups_data.data

# Tokenize the documents
tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]

# Measure indexing time
start_time = time.time()
bm25 = BM25Okapi(tokenized_docs)
indexing_time = time.time() - start_time
print(f"Indexing Time: {indexing_time:.4f} seconds")

# Define a sample query
query = "machine learning"
tokenized_query = word_tokenize(query.lower())

# Measure query time
start_time = time.time()
scores = bm25.get_scores(tokenized_query)
query_time = time.time() - start_time
print(f"Query Time: {query_time:.4f} seconds")

# Output the top 5 documents for the query
top_n = 5
top_n_indices = scores.argsort()[-top_n:][::-1]
for idx in top_n_indices:
    print(f"Score: {scores[idx]:.4f}, Document: {documents[idx][:200]}...")

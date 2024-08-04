import nltk
# Ensure NLTK data is downloaded
nltk.download('stopwords')
nltk.download('punkt')
import os
import json
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from rank_bm25 import BM25Okapi

stop_words = set(stopwords.words('english'))

file_path = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(file_path, "..", "processed_hash_map.json") 
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

print(f"\nLoading documents from {input_file}")
documents = []
tokenized_docs = []
titles = []
for paper in data['papers']:
    for chunk in paper['chunks']:
        documents.append(chunk['text'])
        tokenized_docs.append(word_tokenize(chunk['text'].lower()))
        titles.append(paper['paper_title'])
print("\nStart indexing...")

# Measure indexing time
start_time = time.time()
bm25 = BM25Okapi(tokenized_docs)
indexing_time = time.time() - start_time
print(f"Indexing Time: {indexing_time:.4f} seconds")

# Define a sample query
query = "how do Internet of Things relate to AI"
tokenized_query = word_tokenize(query.lower())

# Measure query time
start_time = time.time()
scores = bm25.get_scores(tokenized_query)
query_time = time.time() - start_time
print(f"\nQuery Time: {query_time:.4f} seconds")
print("\n\nResults:")
# Output the top 5 documents for the query
top_n = 5
top_n_indices = scores.argsort()[-top_n:][::-1]
for idx in top_n_indices:
    print(f"\nScore: {scores[idx]:.4f}, Document: {documents[idx]}..., Title: {titles[idx]}")
#    print(f"\nScore: {scores[idx]:.4f}, Document: {documents[idx][:200]}..., Title: {titles[idx]}")


import pickle
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
input_file = os.path.join(file_path, "..", "processed_rai_hash_map.json") 
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

print(f"Number of tokenized_docs: {len(tokenized_docs)}")

index_file = os.path.join(file_path, "papers_index.pkl")

if os.path.exists(index_file):
    # Rename the existing index file to include ".previous-version"
    previous_version_file = index_file + ".previous-version"
    os.rename(index_file, previous_version_file)
    print(f"Renamed existing index file to: {previous_version_file}")

print("Creating new BM25 index...")
start_time = time.time()
bm25 = BM25Okapi(tokenized_docs)
indexing_time = time.time() - start_time

print("Saving BM25 index...")
with open(index_file, 'wb') as f:
    pickle.dump(bm25, f)

print(f"Indexing Time: {indexing_time:.4f} seconds")
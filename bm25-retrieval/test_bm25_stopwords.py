import nltk
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from rank_bm25 import BM25Okapi

# Load stop words
stop_words = set(stopwords.words('english'))

# Sample documents
documents = [
    "The cat sat on the mat",
    "The dog chased the cat",
    "The cat climbed the tree",
]

# Tokenize and remove stop words
tokenized_docs = [
    [word for word in word_tokenize(doc.lower()) if word.isalnum() and word not in stop_words]
    for doc in documents
]

# Initialize the BM25 model
bm25 = BM25Okapi(tokenized_docs)

# Sample query
query = "cat on the mat"
tokenized_query = [word for word in word_tokenize(query.lower()) if word.isalnum() and word not in stop_words]

# Get BM25 scores
scores = bm25.get_scores(tokenized_query)

# Rank the documents based on the scores
ranked_docs = sorted(zip(scores, documents), reverse=True)

# Print the ranked documents
for score, doc in ranked_docs:
    print(f"Score: {score:.4f}, Document: {doc}")

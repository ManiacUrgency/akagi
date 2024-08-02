from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
#import nltk
#nltk.download('punkt')

# Sample documents
documents = [
    "The cat sat on the mat",
    "The dog chased the cat",
    "The cat climbed the tree",
]

# Tokenize the documents
tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]

# Initialize the BM25 model
bm25 = BM25Okapi(tokenized_docs)

# Sample query
query = "cat on the mat"
tokenized_query = word_tokenize(query.lower())

# Get BM25 scores
scores = bm25.get_scores(tokenized_query)

# Rank the documents based on the scores
ranked_docs = sorted(zip(scores, documents), reverse=True)

# Print the ranked documents
for score, doc in ranked_docs:
    print(f"Score: {score:.4f}, Document: {doc}")

from serpapi import GoogleSearch
import json

params = {
    "engine": "google_news",
    "q": "opioid crisis",
    "api_key": "5fa4a4f821aa4d51c61f2e046c6223bedd026796d348b14b253c8a4f438fdfa2"
}

search = GoogleSearch(params)
results = search.get_dict()
news_results = results["news_results"]
print(json.dumps(news_results, indent=2))



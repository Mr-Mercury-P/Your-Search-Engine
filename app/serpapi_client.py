from serpapi import GoogleSearch
from app.utils import clean_html
from config import SERPAPI_KEY

location = "India"

def fetch_search_results(query):
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "location": location
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    raw_results = results.get("organic_results", [])

    cleaned_results = []
    for result in raw_results:
        snippet = result.get("snippet", "")
        clean_text = clean_html(snippet)
        result['cleaned_snippet'] = clean_text
        cleaned_results.append(result)

    return cleaned_results

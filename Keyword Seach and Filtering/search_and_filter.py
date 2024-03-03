from elasticsearch import Elasticsearch

es = Elasticsearch(["localhost:9200"])

index_name = "dark_web_data"

user_input = input("Enter keywords separated by commas: ")
user_keywords = [keyword.strip() for keyword in user_input.split(",")]
illegal_keywords = ["drugs", "weapon", "gun", "cocaine","coke","heroin","meth","acid","LSD","pills","crack","ketamine","MDMA","grenade","mushrooms","bitcoin","children","child","sex"]
all_keywords = illegal_keywords + user_keywords

filters = {
    "category": "illegal",  
}

query = {
    "query": {
        "bool": {
            "should": [{"match": {"content": keyword}} for keyword in all_keywords],
            "filter": [{"term": {key: value}} for key, value in filters.items()]
        }
    }
}

results = es.search(index=index_name, body=query)

for hit in results['hits']['hits']:
    print(hit['_source'])


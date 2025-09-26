from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://elasticsearch:9200"])

def run_query(index: str, body: dict):
    # TODO: implement proper query execution
    return {"hits": {"total": 0, "hits": []}}

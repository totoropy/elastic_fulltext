import os
import sys

from elasticsearch import Elasticsearch, helpers


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('A phrase is missing. use: ./search.py sometext')
        exit(0)

    pattern = sys.argv[1]
    index_name = 'shakespeare'
    es = Elasticsearch(hosts=['localhost'])
    res = es.search(index=index_name, body={"query": {"match": {"text": pattern}}})
    print("----------")
    for hit in res['hits']['hits']:
        print("{} \nScore: {}, File: {}, Line: {}\n".format(
            hit['_source']['text'],
            hit['_score'],
            hit['_source']['file'],
            hit['_source']['line'],
            )
        )
    print("---------- Result: {}".format(res['hits']['total']))
    # pprint.pprint(res['hits']['total'])

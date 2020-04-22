import os
import time
import json
import time
import pprint
from datetime import datetime

from elasticsearch import Elasticsearch


start_time = time.time()

author = ''
name = ''
scene = ''
text = ''


def load_file_content(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    i = 0
    header = ''
    for line in lines:
        s = line.strip()
        if len(s) == 0:
            i += 1
            continue
        else:
            header = s
            break
    return header, lines[i+1:]


def get_document(title, scene, file, line, text):
    doc = {
        'author': 'William Shakespeare',
        'title': title,
        'scene': scene,
        'file': file,
        'line': line,
        'text': text,
        'timestamp': datetime.now(),
    }
    return doc


def create_index():
    es.indices.delete(index=index_name, ignore=[400, 404])
    es.indices.create(index=index_name, ignore=400)
    counter = 0
    for file in sorted(os.listdir(path)):
        file_path = os.path.join(path, file)
        scene = file.split('.')[0]
        title, lines = load_file_content(os.path.join(file_path))
        i = 0
        for text in lines:
            i += 1
            text = text.rstrip()
            if not text:
                continue

            doc = get_document(title, scene, file, i, text)
            id = file.replace('.txt', '.{}'.format(i))
            print('{}    {}'.format(id, text))
            try:
                es.index(index=index_name, id=id, body=doc)
            except Exception as e:
                print(e)
                time.sleep(15)

            counter += 1
    return counter


if __name__ == '__main__':
    path = 'output'
    index_name = 'shakespeare'
    doctype = 'page'
    es = Elasticsearch(hosts=['localhost'])
    counter = create_index()
    print('Document indexed: {}'.format(counter))

    es.indices.refresh(index=index_name, request_timeout=60)

    res = es.search(index=index_name, body={"query": {"match_all": {}}})
    print(res['hits']['total'])

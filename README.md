# elastic_fulltext  
Indexing text files in elastic search  
  
Two simple scripts:  
- create_index.py  - creates ES index and feed it by text content from folder output  
- search.py - searches in the content  


usage:  
Python3 with requirements.txt  
docker-compose up -d  

* There is also /spider, but it is dependent on lib. Scrapy which is not part of this project.

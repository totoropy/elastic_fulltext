# elastic_fulltext  
Indexing text files in elastic search  
  
Two simple scripts:  
- create_index.py  - creates ES index and feed it by text content from folder output  
- search.py - searches in the content  

// There is also /spider, but it is dependent on lib. Scrapy which is not part of this project.


#### usage:  
Python3 with requirements.txt  
docker-compose up -d  


```
python3 search.py shaken
oak not to be wind-shaken. 
Score: 9.940123, File: coriolanus.5.2.txt, Line: 156

Shaken with sorrows in ungrateful Rome. 
Score: 9.101762, File: titus.4.3.txt, Line: 19

Have shaken Edward from the regal seat, 
Score: 8.526589, File: 3henryvi.4.6.txt, Line: 4

That looks on tempests and is never shaken; 
Score: 8.315805, File: sonnet.CXVI.txt, Line: 6

For if you were by my unkindness shaken 
Score: 8.019791, File: sonnet.CXX.txt, Line: 5

So shaken as we are, so wan with care, 
Score: 7.8490705, File: 1henryiv.1.1.txt, Line: 3

---------- Result: 6

```

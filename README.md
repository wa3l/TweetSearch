## TweetSearch - A simple Vector Space and PageRank based Search Engine

### Usage
1. To run the program and get an interactive interface, type `./vector_space.py`, `./pagerank.py` or `./tweets_pr.py` depending on which part you want to run.

2. Place the json file in the code directory. To download the corpus click [here](http://infolab.tamu.edu/static/670/mars_tweets_medium.json).

3. To get help, type `help` or `?`

4. To terminate the program, type `exit` or hit `Ctrl+D`


### General Notes
The first time you run any of three parts of the program, it'll attempt to generate the index. The program will prompt you to wait in the mean time. This usually takes about ~26 seconds (for the provided corpus) and builds an index that contains terms and their postings lists with term frequencies associated with them. Additionally, the index contains information about documents (id, user, and tokens), users (id, name), and PageRanks for only the users with in/out mentions. This information is carefully selected to be used by various parts of the engine. The index is ~49MB in size.

The program will also display an accurate interval upon the actions it takes, this includes building/saving or loading the index, in addition to all search queries.

After the index is written to disk, you can type your query and get results back instantly. On subsequent runs of the program, the index is going to be read from disk instead of being built each time. A total of ~49MB takes about 1.4 seconds to be loaded into memory.

User input is cleaned up from special characters, lower-cased, and tokenized.

### Part 1 - Vector Space Retrieval:
I tried to make whatever optimization possible to reduce the computation overhead. However, queries such as "mars" will still take forever because virtually every document in our corpus contains that term. Hence, the Cosine similarity computation will drain the processing resources of a single computer. In any case, things like idf weights for all terms are computed once and cached to reduce the overhead.

Performance can be optimized by introducing tiered indices. This can help reduce computation time when searching for common and stop words.

The search is done by fetching all documents that contain the terms in the query. All the terms that those documents contain are put together to form the vocabulary that we base our vectors on. Query and document vectors are created, and finally, a similarity score is computed for each (query, document) pair and the top 50 results are returned. 

### Part 2 - PageRank:
This part will simply output the top 50 users in the corpus and exit. All ranks are initiated to equal probability and a value of 10^-7 is used to measure convergence. All dangling nodes are removed and PageRanks are only calculated for users with in/out mentions. Running this part will show that, for instance, the users `MarsCuriosity` and `NASA` are the top two users for the corpus used, which makes perfect sense given the corpus domain.

### Part 3 - PageRanked Documents:
Querying this part of the engine will cause all documents that contain the query terms to be fetched. Those documents are then ranked by their twitter users' PageRank values and the top 50 results are returned. 

Another approach to performing this could be adding/multiplying each result's cosine similarity with the query and its user's PageRank. However, doing this would further complicate the performance issues Vector Space Retrieval runs into.

Author
------
Wael Al-Sallami | [wa3l.com](http://wa3l.com).
  
License
-----
Public domain: [http://unlicense.org](http://unlicense.org)

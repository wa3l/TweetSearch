## Index-based Search Engine
**Author: Wael Al-Sallami**
**Date: March 1st, 2013**

### Usage
1. To run the program and get an interactive interface, type `./part1.py`, `./part2.py` or `./part3.py` depending on which part you want to run.

2. Place the json file in the code directory.

3. To get help, type `help` or `?`

4. To terminate the program, type `exit` or hit `Ctrl+D`


### General Notes
The first time you run any of three parts of the program, it'll attempt to generate the index. The program will prompt you to wait in the mean time. This usually takes about ~26 seconds and builds an index that contains terms and their postings lists with term frequencies associated with them. Additionally, the index contains information about documents (id, user, and tokens), users (id, name), and PageRanks for only the users who mentioned or are mentioned by other users. This information is carefully selected to be used by various parts of the project. The index is ~49MB in size.

The program will also display an accurate interval upon the actions it takes, this includes building/saving or loading the index, in addition to all search queries.

After the index is written to disk, you can type your query and get results back. This happens instantly and takes fractions of a second.

On subsequent runs of the program, the index is going to be read from disk instead of being built each time. A total of ~49MB takes about 1.4 seconds to be loaded into memory.

User input is cleaned up from special characters, lower-cased, and tokenized.

On the optimization side, a lot of thought went into identifying the bottlenecks in the program workflow and trying to rectify some of them. I timed various parts of the code and made sure to shave off a few seconds whenever I can.

Furthermore, no effort was spared in cleaning up the code, making it as precise as possible without sacrificing readability. All methods are documented and different parts were separated into different modules/classes.

### Part 1 - Vector Space Retrieval:
In this part, I tried to make whatever optimization possible to reduce the computation overhead. However, queries such as "mars" will still take forever because virtually every document in our corpus contains that term. Hence, the Cosine similarity computation will drain the processing resources of a single computer. In any case, things like idf weights for all terms are computed once and cached to reduce the overhead.

We may optimize the performance of this part by introducing tiered indices to the mix. This would help reduce the computational overhead when querying for common terms such as `mars` or any of the stop words.

The search is done by fetching all documents that contain the terms in the query. All the terms that those documents contain are put together to form the vocabulary that we base our vectors on. Query and document vectors are created, and finally, a similarity score is computed for each (query, document) pair and the top 50 results are returned. 

### Part 2 - PageRank:
This part will simply output the top 50 users in our corpus and exit. All ranks are initiated to equal probability and a value of 10^-7 is used to measure convergence. All dangling nodes are removed and PageRanks are only calculated for users with in/out mentions. Running this part will show that the users `MarsCuriosity` and `NASA` are the top two users, which makes perfect sense given the corpus domain.

Since the discussion on our Google group seemed to be getting at the fact that using matrices to compute PageRanks is a performance bottleneck, I chose to use adjacency lists instead. With some profiling and optimization, ranking became a trivial task given the size of the corpus.

### Part 3 - PageRanked Documents:
Querying this last portion of the program will cause all documents that contain the query terms to be fetched. Those documents are then ranked by their twitter users' PageRank values and the top 50 results are returned. 

To test the difference between this method and the Vector Space Retrieval one, I checked the results of queries such as `advancement` or `circumference`. The returned documents were the same but ordered differently based on the algorithm described above.

Another approach to performing this could be adding/multiplying each result's cosine similarity with the query and its user's PageRank. However, doing this would further complicate the performance issues Vector Space Retrieval runs into. Again, tiered indices could eliminate this bottleneck.

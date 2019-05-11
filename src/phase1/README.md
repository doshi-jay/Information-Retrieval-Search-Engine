##### Task 1 (15 points): Build your own retrieval systems and perform four baseline runs.
1. Tf/idf
2. Query Likelihood Model (JM smoothed)
3. BM25 model
4. Lucene’s default retrieval model

##### Task 2 (15 points): Perform query enhancement
1. Pseudo relevance feedback
2. Semantic query expansion using Thesauri

##### Task 3 (10 points): Perform the following on two baseline runs of your choice:
a) Stopping (using common_words.txt) with no stemming - BM25 and JM QLM
b) Index the stemmed version of the corpus (cacm_stem.txt). 
Retrieve results for the queries in cacm_stem.query - BM25 and Lucene
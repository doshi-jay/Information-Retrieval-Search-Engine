#### Implementation – Phase 1 :: Indexing and Retrieval

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

#### Implementation – Phase 2 :: Displaying Results (15 points)
Implement a snippet generation technique and query term highlighting within results, in one of the baseline runs.

#### Implementation – Phase 3 :: Evaluation (20 points)

1. Produce one more (ninth) run that combines a query expansion technique with stopping
2. Implement and perform the following:
    1. MAP
    2. MRR
    3. P@K, K = 5 and 20
    4. Precision & Recall (provide full tables for all queries and all runs)

#### Extra Credit
Design and implement a query interface that is tolerant of spelling errors in the query terms. Given a query term 
that is not in the index, your program should provide a ranked list of up to 6 possible corrections for the user 
to choose from. Consider only terms within an edit distance of 1 or 2 from the potentially mis-spelled query term. 
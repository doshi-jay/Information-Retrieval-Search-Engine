# IRProject-Spring2019
## Additional Run

We have used Pseudo Relevance Feedback for query enrichment along with stopping to update the existing queries.
We then used BM25 to performed the additional run.

#### `inverted_indexer.py`
1. Please ensure that that the results generated in Phase1-Task1 for Lucene run are generated in the folder 
`src/phase1/task1/lucene_results`.
2. Make sure all the imports are installed that are used in the file.
 

#### `queryexpansion_stopping.py`
1. Please create an empty text file named `expanded_queries.txt` to store the expanded queries.
2. Please create an intermediate folder named `inverted_indexes` to store the top files for each query further used for
 Pseudo Relevance Feedback. 
3. Make sure all the imports are installed that are used in the file.
4. The text file will be populated with the 64 queries in t he format `<query_id <expnaded_query>`.
5. This file uses `inverted_indexer.py` . So, please follow the instructions given above.
 
 
#### `AdditionalRun.py`
1. Please create a folder named `Additional_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.

For running the additional run, do:
 - `python3 queryexpansion_stopping.py`
 - `python3 AdditionalRun.py`

## Evaluation

Setup requirements: 
- simply make sure you have python3 installed
- make sure you have the `evaluations/` folder in the same directory as the Evaluation.py file 

For running the code for evaluation, do: 
 - `python3 Evaluation.py`
 - input the full path of the folder that contains your results for the retrieval model you want to evaluate
 - input `'q'` for terminating the program once you are done.

We have referred the textbook “Information Retrieval in Practice” by W. Bruce Croft, Donald Metzler, and Trevor Strohman 
for the Mean Average Precision (MAP) expression, Mean Reciprocal Rank (MRR) expression, the P @ K expression and for the
procedure to calculate the precision and recall values. We have printed the precision and recall values in a table 
format for all queries at all ranks for all runs. 
 
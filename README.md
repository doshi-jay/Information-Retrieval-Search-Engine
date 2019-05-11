# IRProject-Spring2019
## INTRODUCTION: 

As a part of this project, we plan to build various information retrieval systems, varying in implementation by the techniques used for query enhancement and for preprocessing the corpus. We further plan to implement displaying results so that they describe the search results in a better manner. Additionally, we will evaluate these retrieval systems based on the results returned. 

### Prerequisites:
- Java - Apache Lucene runs of Java 7 or greater, Java 8 is verified to be compatible and may bring some performance improvements.
- Python - We have used [Python3](https://www.python.org/downloads/) for the project.  

### Contributors:
- Jay Doshi - 001850941
- Abhiruchi Karwa - 001821064
- Ketan Kale - 001821951

### Project structure:
- src/ : All the code for the project is in this directory.
- data/ : Contains the entire corpus along with the queries needed
- IRProject.pdf : Please find more details on our project in this document

---

### Phase - 1 `src/phase1/`
### Task - 1 `src/phase1/task1`

#### 1. BM25
##### Requirements
- `nltk (pip3 install nltk)`
- `collections.OrderedDict`
- `math`
- `os`
##### Compile & run
1. Please create a folder named `BM25_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using `python3 BM25.py`

#### 2. Query Likelihood Model (JM Smoothed)

##### Requirements
- `math`
##### Compile & run
1. Please create a folder named `JM_QLM_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using `python3 JMRetriever.py`


#### 3. Lucene
##### Setup
 - Install Apache Lucene - 4.7.2.
 - Add the following jar files to your java project’s list of referenced libraries:
 1. lucene-core-VERSION.jar
 2. lucene-queryparser-VERSION.jar
 3. lucene-analyzers-common-VERSION.jar.Where
##### Compile & run
- It is recommended to create two folders named `index` and `lucene_results` to be used.
- Create a java project with the provided java class `LuceneRun.java` in it.
- Compile and run the java code. (using javac and java commands) 
- Please follow the format of the folder path suggested, while giving inputs.
- The program takes the following inputs:
     1. Absolute path to the folder where the index files can be stored. (any temporary empty folder works)
     2. Absolute path to the folder containing all the files in the corpus. (`data\cleaned_corpus`) 
     3. Absolute path to the file containing all the queries in the format `<query_id> <query> `. (`data\queries.txt`)
     4. Absolute path to the folder where the top 100 files can be stored. (`lucene_results`)

#### 4. TF-IDF
##### Requirements
- `collections`
- `os`
- `math`
##### Compile & run
1. Please create a folder named `TF_IDF_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using `python3 tfidf.py`

### Task - 2 `src/phase1/task2`

#### Query Expansion
This folder contains implementations for the two query expansion techniques:
1. Query Expansion using Pseudo Relevance Feedback (QE-PRF)
2. Query Expansion using Thesaurus (QE-T)

##### Requirements for QE-PRF:
 - nltk (`pip3 install nltk`) 
 - make sure you have the `Query Expansion/` folder at the same level as this file
 
##### For running QE-PRF, do:
    `python3 queryexpansion_PRF.py`
    
##### Design Choices:
- For Query Expansion in QE-PRF we have used the dice's coefficient as the association metric to find the association of two terms.
       For a query, first, we create an inverted index from the top 100 relevant documents. Then from that index we generate the 
       document frequency table. Using the document frequency table we find the dice's coefficient for every query term with all the terms in the 
       document frequency table. Here, since every query term will have a different dice coefficient for a term in the table, we have chosen to take the average 
       of all those coefficients when associating the term with a query. we have used nltk's stopwords list to filter stopwords from my corpus. we also skip terms that
       are of length less than 4 as most probably they will be stop words. 
       
       Dice coefficient for two terms: A and B = Nab/(Na + Nb) 
    
       where, Nab = the documents in which both the terms A and B occur
              Na  = the documents in which A occurs
              Nb  = the documents in which B occurs
              
   Once we find the dice coefficients for all the terms, we sort them in decreasing order to get maximum association terms and choose 'N' terms out of them.
    - for the choice of data structures we have used sets in the document frequency table so that the look up operations are efficient.
    - Here we add N additional terms to the query while expanding it    
    
##### Requirements for QE-T:
 - nltk (`pip3 install nltk`) 
 - make sure you have the `Query Expansion/` folder at the same level as this file

 
##### For running QE-T, do:
    `python3 query_expansion_using_thesaurus.py`

##### References:
 - https://pythonprogramming.net/wordnet-nltk-tutorial/ 
 - http://wordnetweb.princeton.edu/perl/webwn  
 
##### Design choices:
- For Query expansion in QE-T the basic idea is expanding the query using the synonyms of the query words. We use nltk.wordnet for this
- One decision here is that we consider only top 3 unique lemmas for a query terms so that all query terms get equal chance of expansion

##### Requirements for runner.py
- nltk (`pip3 install nltk`)
- make sure you have the `BM_Results_after_qe_PRF/` folder to store the results 
- make sure you have the `BM_Results_after_qe_thesauri/` folder to store the results 


### Task - 3 `src/phase1/task3`

#### a) Stopping (using common_words.txt) with no stemming.

##### StoppedHelper.py
- This file helps create an inverted index while avoiding the stop-words provided for the corpus.
- This unigrams inverted index with stopping helps in refining the results.

##### 1. BM25 - `StoppedBM25.py`

##### Compile and Run
1. Please create a folder named `Stopped_BM25_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.

##### 2. Query Likelihood Model (JM Smoothed) - `StoppedJMRetriever.py`
1. Please create a folder named `Stopped_JM_QLM_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. For running the code for this task, do:
 - `python3 StoppedBM25.py`
 - `python3 StoppedJMRetriever.py`

#### b) Index the stemmed version of the corpus (cacm_stem.txt). Retrieve results for the queries in cacm_stem.query. 

##### StemmedHelper.py
- This file also parses the given `cacm_stem.txt` to get the separate text files in `stemmed_corpus`. 
- This file helps create an inverted index for the stemmed corpus provided.
- Run the helper using, `python3 StemmedHelper.py`
 

##### 1. BM25 - `StemBM25.py`
1. Please create a folder named `Stemmed_BM25_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using:
    For running the code for this task, do:
 - `python3 StemBM25.py`

##### 2. Lucene - `StemLuceneRun.java`
##### Setup
 - Install Apache Lucene - 4.7.2.
 - Add the following jar files to your java project’s list of referenced libraries:
     1. lucene-core-VERSION.jar
     2. lucene-queryparser-VERSION.jar
     3. lucene-analyzers-common-VERSION.jar.
     
##### Compile & run
- It is recommended to create two folders named `index` and `Stemmed_Lucene_results` to be used.
- Create a java project with the provided java class `StemLuceneRun.java` in it.
- Compile and run the java code. (using javac and java commands) 
- Please follow the format of the folder path suggested, while giving inputs.
- The program takes the following inputs:
     1. Absolute path to the folder where the index files can be stored. (any temporary empty folder works)
     2. Absolute path to the folder containing all the files in the corpus. (`data\stemmed_corpus`) 
     3. Absolute path to the file containing all the queries. (`data\cacm_stem.query.txt`)
     4. Absolute path to the folder where the top 100 files can be stored. (`Stemmed_Lucene_results`)
 
---

### Phase - 2 `src/phase2/`

#### Snippet Generation
This folder contains implementations for snippet generation:

##### Setup Requirements for snippet generation:
 - nltk (`pip3 install nltk`) 
 - beautiful soup (`pip3 install bs4`)
 - create `snippet_results/` folder in the same directory 

 
##### For running snippet_generation.py, do:
    `python3 snippet_generation.py`
    
##### Design Choices:

1. We have referred the textbook “Information Retrieval in Practice” by W. Bruce Croft, Donald Metzler, and Trevor Strohman 
    and chosen to adopt J.H.Luhn's approach for snippet generation with some modifications
2. We consider significant words to be the words present in query under consideration
3. We rank the sentences according to their significance factors and chose the best one and return it
4. For highlighting we have decided to embolden the query terms i.e putting the query term in `<b> </b>`

---

### Phase - 3 `src/phase3/`

#### Additional Run

We have used Pseudo Relevance Feedback for query enrichment along with stopping to update the existing queries.
We then used BM25 to performed the additional run.

##### `inverted_indexer.py`
1. Please ensure that that the results generated in Phase1-Task1 for Lucene run are generated in the folder 
`src/phase1/task1/lucene_results`.
2. Make sure all the imports are installed that are used in the file.
 

##### `queryexpansion_stopping.py`
1. Please create an empty text file named `expanded_queries.txt` to store the expanded queries.
2. Please create an intermediate folder named `inverted_indexes` to store the top files for each query further used for
 Pseudo Relevance Feedback. 
3. Make sure all the imports are installed that are used in the file.
4. The text file will be populated with the 64 queries in t he format `<query_id <expanded_query>`.
5. This file uses `inverted_indexer.py` . So, please follow the instructions given above.
 
 
##### `AdditionalRun.py`
1. Please create a folder named `Additional_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. For running the additional run, do:
 - `python3 queryexpansion_stopping.py`
 - `python3 AdditionalRun.py`

#### Evaluation

##### Setup requirements: 
- simply make sure you have python3 installed
- make sure you have the `evaluations/` folder in the same directory as the Evaluation.py file 

##### For running the code for evaluation, do: 
 - `python3 Evaluation.py`
 - input the full path of the folder that contains your results for the retrieval model you want to evaluate
 - input `'q'` for terminating the program once you are done.

We have referred the textbook “Information Retrieval in Practice” by W. Bruce Croft, Donald Metzler, and Trevor Strohman 
for the Mean Average Precision (MAP) expression, Mean Reciprocal Rank (MRR) expression, the P @ K expression and for the
procedure to calculate the precision and recall values. We have printed the precision and recall values in a table 
format for all queries at all ranks for all runs. 


---

### Extra Credit `src/extracredit/`

##### Compile and Run

- Run the python file `QueryCorrection.py` in the PyCharm IDE or a terminal.
- Input the query you want to correct.
- The input statement stops if you enter the string `'q'`

##### Design Choices 

- In this task, we use edit distance as a measure of closeness for two terms. Since, generally, the spelling mistakes have
only around 1 or 2 characters different, we consider terms with edit distance 1 or 2 for finding probable intended terms.
- For every term in the query input, which is not in the corpus (the index generated for this corpus), we find the terms in 
index that are edit distance 1 or 2 away from it (the "misspelled term") and add them to the suggestions list for that term.
Thus, we create suggested lists for all such "misspelled terms" and return at most top 6 suggestions for every term in
 the order in which they occur in the input query. 
- For the terms which are already in the index we don't return anything as we assume that the query will be correct. 

##### References
1. Search Engines by W. B. Croft, D. Metzler, T. Strohman
2. http://norvig.com/spell-correct.html
3. https://stackoverflow.com/questions/43410332/how-to-modify-peter-norvig-spell-checker-to-get-more-number-of-suggestions-per-w
4. https://github.com/pirate/spellchecker

---
 


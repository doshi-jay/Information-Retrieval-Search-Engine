## a) Stopping (using common_words.txt) with no stemming.

### StoppedHelper.py
- This file helps create an inverted index while avoiding the stop-words provided for the corpus.
- This unigrams inverted index with stopping helps in refining the results.

### 1. BM25 - `StoppedBM25.py`

#### Compile and Run
1. Please create a folder named `Stopped_BM25_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.

### 2. Query Likelihood Model (JM Smoothed) - `StoppedJMRetriever.py`
1. Please create a folder named `Stopped_JM_QLM_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.

For running the code for this task, do:
 - `python3 StoppedBM25.py`
 - `python3 StoppedJMRetriever.py`
---

## b) Index the stemmed version of the corpus (cacm_stem.txt). Retrieve results for the queries in cacm_stem.query. 

### StemmedHelper.py
- This file also parses the given `cacm_stem.txt` to get the separate text files in `stemmed_corpus`. 
- This file helps create an inverted index for the stemmed corpus provided.
- Run the helper using, `python3 StemmedHelper.py`
 

### 1. BM25 - `StemBM25.py`
1. Please create a folder named `Stemmed_BM25_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using:
    For running the code for this task, do:
 - `python3 StemBM25.py`

### 2. Lucene - `StemLuceneRun.java`
#### Setup
 - Install Apache Lucene - 4.7.2.
 - Add the following jar files to your java project’s list of referenced libraries:
     1. lucene-core-VERSION.jar
     2. lucene-queryparser-VERSION.jar
     3. lucene-analyzers-common-VERSION.jar.
     
#### Compile & run
- It is recommended to create two folders named `index` and `Stemmed_Lucene_results` to be used.
- Create a java project with the provided java class `StemLuceneRun.java` in it.
- Compile and run the java code. (using javac and java commands) 
- Please follow the format of the folder path suggested, while giving inputs.
- The program takes the following inputs:
     1. Absolute path to the folder where the index files can be stored. (any temporary empty folder works)
     2. Absolute path to the folder containing all the files in the corpus. (`data\stemmed_corpus`) 
     3. Absolute path to the file containing all the queries. (`data\cacm_stem.query.txt`)
     4. Absolute path to the folder where the top 100 files can be stored. (`Stemmed_Lucene_results`)
 

## Instructions for the baseline runs of the following

### 1. BM25
#### Requirements
- `nltk (pip3 install nltk)`
- `collections.OrderedDict`
- `math`
- `os`
#### Compile & run
1. Please create a folder named `BM25_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using `python3 BM25.py`
---

### 2. Query Likelihood Model (JM Smoothed)

#### Requirements
- `math`
#### Compile & run
1. Please create a folder named `JM_QLM_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using `python3 JMRetriever.py`

---

### 3. Lucene
#### Setup
 - Install Apache Lucene - 4.7.2.
 - Add the following jar files to your java project’s list of referenced libraries:
 1. lucene-core-VERSION.jar
 2. lucene-queryparser-VERSION.jar
 3. lucene-analyzers-common-VERSION.jar.Where
#### Compile & run
- It is recommended to create two folders named `index` and `lucene_results` to be used.
- Create a java project with the provided java class `LuceneRun.java` in it.
- Compile and run the java code. (using javac and java commands) 
- Please follow the format of the folder path suggested, while giving inputs.
- The program takes the following inputs:
     1. Absolute path to the folder where the index files can be stored. (any temporary empty folder works)
     2. Absolute path to the folder containing all the files in the corpus. (`data\cleaned_corpus`) 
     3. Absolute path to the file containing all the queries in the format `<query_id> <query> `. (`data\queries.txt`)
     4. Absolute path to the folder where the top 100 files can be stored. (`lucene_results`)
---

### 4. TF-IDF
#### Requirements
- `collections`
- `os`
- `math`
#### Compile & run
1. Please create a folder named `TF_IDF_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
4. Run this file using `python3 tfidf.py`
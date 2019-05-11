# IRProject-Spring2019

## Query Expansion
This folder contains implementations for the two query expansion techniques:
1. Query Expansion using Pseudo Relevance Feedback (QE-PRF)
2. Query Expansion using Thesaurus (QE-T) and,
3. runner.py - contains code for running the retrieval again with the expanded queries 

### Requirements for QE-PRF:
 - nltk (`pip3 install nltk`) 
 - make sure you have the `Query Expansion/` folder created at the same level as this file 
### For running QE-PRF, do:
    `python3 queryexpansion_PRF.py`
    
Design Choices:
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
    
### Requirements for QE-T:
 - nltk (`pip3 install nltk`)
 - make sure you have the `Query Expansion/` folder created at the same level as this file 

 
### For running QE-PRF, do:
    `python3 query_expansion_using_thesaurus.py`

### References:
 - https://pythonprogramming.net/wordnet-nltk-tutorial/ 
 - http://wordnetweb.princeton.edu/perl/webwn  
 
### Design choices:
- For Query expansion in QE-T the basic idea is expanding the query using the synonyms of the query words. We use nltk.wordnet for this
- One decision here is that we consider only top 3 unique lemmas for a query terms so that all query terms get equal chance of expansion

### Requirements for runner.py
- nltk (`pip3 install nltk`)
- make sure you have the `BM_Results_after_qe_PRF/` folder to store the results 
- make sure you have the `BM_Results_after_qe_thesauri/` folder to store the results 

 
# IRProject-Spring2019
## Snippet Generation
This folder contains implementations for snippet generation:

Setup Requirements for snippet generation:
 - nltk (`pip3 install nltk`) 
 - beautiful soup (`pip3 install bs4`)
 - create `snippet_results/` folder in this same directory 

 
For running snippet_generation.py, do:
    `python3 snippet_generation.py`
    
## Design Choices:

1. We have referred the textbook “Information Retrieval in Practice” by W. Bruce Croft, Donald Metzler, and Trevor Strohman 
    and chosen to adopt J.H.Luhn's approach for snippet generation with some modifications
2. We consider significant words to be the words present in query under consideration
3. We rank the sentences according to their significance factors and chose the best one and return it
4. For highlighting we have decided to embolden the query terms i.e putting the query term in `<b> </b>`

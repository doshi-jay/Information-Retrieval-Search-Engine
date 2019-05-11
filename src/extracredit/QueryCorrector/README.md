#### Compile and Run

- Run the python file `QueryCorrection.py` in the PyCharm IDE or a terminal.
- Input the query you want to correct.
- The input statement stops if you enter the string `'q'`

#### Design Choices 

- In this task, we use edit distance as a measure of closeness for two terms. Since, generally, the spelling mistakes have
only around 1 or 2 characters different, we consider terms with edit distance 1 or 2 for finding probable intended terms.
- For every term in the query input, which is not in the corpus (the index generated for this corpus), we find the terms in 
index that are edit distance 1 or 2 away from it (the "misspelled term") and add them to the suggestions list for that term.
Thus, we create suggested lists for all such "misspelled terms" and return at most top 6 suggestions for every term in
 the order in which they occur in the input query. 
- For the terms which are already in the index we don't return anything as we assume that the query will be correct. 

#### References
1. Search Engines by W. B. Croft, D. Metzler, T. Strohman
2. http://norvig.com/spell-correct.html
3. https://stackoverflow.com/questions/43410332/how-to-modify-peter-norvig-spell-checker-to-get-more-number-of-suggestions-per-w
4. https://github.com/pirate/spellchecker

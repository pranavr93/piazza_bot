'''
04/09/2017 Ke Yu

Requirement:
	nput_doc type is Post
	documents is list[] of Post objects
	n is the top 'n' similar documents

Effect:
	Given input_doc , return n most similar docs in <documents> 

Reference:
	http://stackoverflow.com/questions/12118720/python-tf-idf-cosine-to-find-document-similarity
'''

import numpy as np
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
	#credit to http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
	#credit to http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def clean_docs(documents):
	doc_clean = []
	for i in documents:
	    temp = re.sub("</?p[^>]*>", "", i)
	    temp = temp.lower()
	    tokens = temp.split(" ")
	    token_list = []
	    for w in tokens:
	        w = re.sub(r'[^a-zA-Z]+', '', w)
	        w = w.lower()
	        if w not in stopwords.words('english') and w != "":
	            token_list.append(w)
	    token_list = stem_tokens(token_list, stemmer)
	    doc_clean.append(token_list)

	documents_clean = []
	for i in doc_clean:
	    documents_clean.append(" ".join(i))
	return documents_clean 

#Input:
#	input_doc : a string
#	documents : a list of string
#	n : top n similar doc you want to get from documents
#Output:  
#	res : n most similar docs in a list
# 	res_score : n corresponding similarity socre.	
def find_top_N_similar_docs(input_doc, documents, n):
	#Preprocess each document in list and build a new list of docs
	#clean the input_doc and documents--> input_doc_clean, doc_clean
	documents.append(input_doc)
	doc_clean = clean_docs(documents)
	input_doc_clean = doc_clean[-1:]

	#Calculate TDIDF
	vec = TfidfVectorizer()
	tfidf = vec.fit_transform(doc_clean)
	input_vec = tfidf[-1:]

	#Calculate Similarity
	from sklearn.metrics.pairwise import linear_kernel
	cosine_similarities = linear_kernel(input_vec, tfidf).flatten()
	related_docs_indices = cosine_similarities.argsort()[::-1]
	if n != 0:
		top_n_idx = related_docs_indices[1:n+1]
		cosine_score = cosine_similarities[top_n_idx]
	res = []
	res_score = cosine_score.tolist()
	for i in range(len(top_n_idx)):
		idx = top_n_idx[i]
		res.append(documents[idx])
	return res, res_score




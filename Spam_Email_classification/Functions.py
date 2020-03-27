import scipy.io
import numpy as np
import re
import string
import nltk
from nltk.stem import PorterStemmer
import string
def getVocabList():
    with open("vocab.txt") as fid:
        vocalbList = {}
        for line in fid: # iterate over each line
            index, word = line.split() # split it by whitespace
            index = int(index) # convert index from string to int # convert bs from string to float
            vocalbList[index] = word
    return vocalbList

def readFile(filename):
    with open(filename,"r") as fid:
        if fid:
            file_contents = fid.read()
            print('File has been read')
        else:
            file_contents = ''
            print('Unable to open ' + filename)
    return file_contents

def processEmail(email_contents):
    vocabList = getVocabList()
    word_indices = [];
    email_contents = email_contents.lower() # Lower-casing
    email_contents = re.sub(r'[<>]', ' ',email_contents)# Stripping HTML
    email_contents = re.sub(r'[0-9]+', 'number',email_contents) # Normalizing Numbers 
    email_contents = re.sub(r'(http|https)://[^\s]*','httpaddr',email_contents)# Normalizing Email Addresses
    email_contents = re.sub(r'[^\s]+@[^\s]+', 'emailaddr', email_contents) # Normalizing URLs   
    email_contents = re.sub(r'[$]+', 'dollar',email_contents) # Normalizing Dollars
    email_contents = re.sub(r'[^\w\s]', '',email_contents) # remove all the punctuations,replaces not (^) word characters or spaces with the empty string
    email_contents = re.sub(r'[\r\n]', ' ',email_contents) # remove carriage return and line feed
    #print(email_contents)
    word_indices = []
    ps = PorterStemmer()

    if email_contents:
        final_str = re.split(' ', email_contents)
        final_str = list(filter(None, final_str)) # remove empty element in the list
    #print(final_str)
    for w in final_str:
        for idx in range(1,len(vocabList)):
            if ps.stem(w) == vocabList[idx]:
                word_indices.append(idx)
    return word_indices
    
def emailFeatures(word_indices):
    n = 1899
    x = np.zeros((n,1))
    for i in range(1,len(word_indices)):
        x[word_indices[i]] = 1
    return x
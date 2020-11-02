from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import csv
import numpy as np
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import language_v1
from pprint import pprint
from value_types import *
from run_function import run_functions

stop_words = set(stopwords.words('english'))
#remove from stopwords
neg_alpha1 = set(
    [chr(i) for i in range(ord('a'), ord('z'))] #bb
)

neg_alpha2 = set(
    [str(chr(i) + chr(i)) for i in range(ord('a'), ord('z'))] #aa
)

neg_extra = set([
    "to", "from", "into", "before", "after", "between", "below", 
    "above", "under", "over", "at", "of", "on", "in", "row", "col",
    "add", "value", "entry", "sort", "multiply", "sin", "cos", "bold",
    "entry", "cell", "value", "set", "background", "color", "filter", 
    "even", "prime", "odd", "max", "normalize", "by", "insert", "find"
])

# include in stopwords
pos_extra = set([
    "hey", "hi", "hello", "yo", "please", "could", "thanks", "make", "sure", "extra", "could", "can", "may"
])

def isInt(val):
    try:
        int(val)
        return True
    except:
        return False

ourset = neg_alpha1 | neg_alpha2 | neg_extra

stop_words = (stop_words - ourset) | pos_extra

lemmatizer = WordNetLemmatizer()

# Instantiates a client to connect to google cloud nlp model
client = language_v1.LanguageServiceClient()

SWAP_LIST = [
    "elephant", #cell
    "car", #row or col
    "ocean", #value
    "mine", #color
    "", # insert 
    "", # 
]

SIMPLE_SPACE = [
    # # ***** if you change the order of this list, make sure to update values of COMPLEX_SPACE dict
    # "add value 12 to entry 1 and entry 2",
    # "add value 14 to entry 1",
    # "add value 1 to cell 11",
    # "insert after entry",
    # "add entry 1 to entry2", <ENTRY_1> row 1, <ENTRY_2> row 2 entry
    # "insert before entry",

    
    "add " + SWAP_LIST[2] + " 1 to " + SWAP_LIST[1] + " 1 and " + SWAP_LIST[1] + " 2", #add value to entry 1 entry 2
    "add " + SWAP_LIST[2] + " 1 to " + SWAP_LIST[1] + " 1", #add value to entry
    "add " + SWAP_LIST[2] + " 1 to " + SWAP_LIST[0] + " 1", #add value to cell
    "add " + SWAP_LIST[1] + " 1 to " + SWAP_LIST[1] + " 2", #add entry to entry

    "insert " + SWAP_LIST[1] + " after " + SWAP_LIST[1] + " 1",
    "insert " + SWAP_LIST[1] + " before " + SWAP_LIST[1] + " 1",
    "insert " + SWAP_LIST[2] + " 1 into " + SWAP_LIST[0] + " 1",
    "insert average of " + SWAP_LIST[1] + " 1 into " + SWAP_LIST[0] + " 1",

    "bold " + SWAP_LIST[1] + " 1", #the text in 
    "bold " + SWAP_LIST[0] + " 1",

    "set background color of " + SWAP_LIST[0] + " 1 to " + SWAP_LIST[3] + "",
    "set background color from " + SWAP_LIST[0] + " 1 to " + SWAP_LIST[0] + " 2 to " + SWAP_LIST[3],
    "set background color of " + SWAP_LIST[1] + " 1 to " + SWAP_LIST[3] + "",

    "multiply " + SWAP_LIST[1] + " 1 by " + SWAP_LIST[2] + " 1",
    "multiply " + SWAP_LIST[0] + " 1 by " + SWAP_LIST[2] + " 1",

    "Find the sine of " + SWAP_LIST[1] + " 1",
    "Find the sine of " + SWAP_LIST[0] + " 1",
    "Find the sine of " + SWAP_LIST[0] + " 1 to " + SWAP_LIST[0] + " 2",
    "Find the cosine of " + SWAP_LIST[1] + " 1",
    "Find the cosine of " + SWAP_LIST[0] + " 1",
    "Find the cosine of " + SWAP_LIST[0] + " 1 to " + SWAP_LIST[0] + " 2",

    "Sort by " + SWAP_LIST[1] + " 1",

    "Filter " + SWAP_LIST[1] + " 1 by even numbers",
    "Filter " + SWAP_LIST[1] + " 1 by prime numbers",
    "Filter " + SWAP_LIST[1] + " 1 by odd numbers",
    "Normalize " + SWAP_LIST[1] + " 1",
]

SIMPLE_SPACE_CORRESPONDENTS = {
    0 : "ADD <NUM_1> <ENTRY_1>.ADD <NUM_1> <ENTRY_2>",
    1 : "ADD <NUM_1> <ENTRY_1>",
    2 : "ADD <NUM_1> <CELL_1>",
    3 : "ADD <ENTRY_1> <ENTRY_2>",
    4 : "INSERTAFT <ENTRY_1>",
    5 : "INSERTBEF <ENTRY_1>",
    6 : "SET <NUM_1> <CELL_1>",
    7 : "AVG <ENTRY_1>.SET <RES_1> <CELL_1>",
    8 : "BOLD <ENTRY_1>",
    9 : "BOLD <CELL_1>",
    10 : "SET_BG <COLOR_1> <CELL_1>",
    11 : "SET_BG <COLOR_1> <CELL_1> <CELL_2>",
    12 : "SET_BG <COLOR_1> <ENTRY_1>",
    13 : "MULTIPLY <NUM_1> <ENTRY_1> ",
    14 : "MULTIPLY <NUM_1> <CELL_1>",
    15 : "SIN <ENTRY_1>",
    16 : "SIN <CELL_1>",
    17 : "SIN <CELL_1> <CELL_2>",
    18 : "COS <ENTRY_1>",
    19 : "COS <CELL_1>",
    20 : "COS <CELL_1> <CELL_2>",
    21 : "SORT <ENTRY_1>",
    22 : "FILTER_EVEN <ENTRY_1>",
    23 : "FILTER_PRIME <ENTRY_1>",
    24 : "FILTER_ODD <ENTRY_1>",
    25 : "MAX_VAL <ENTRY_1>.NORMALIZE <RES_1> <ENTRY_1>",
}

print("sample space: ")
print(SIMPLE_SPACE)
COMPLEX_SPACE = {
    # complex in : expected simple out
    "Insert a row before row 2": 5,
    "Hey excelify can you please add 23 to cols a and j": 0,
    "Hello there excelify could you insert a row before row 4 please and thanks so much": 5,
    "Hey excelify can you please add 23 to rows 1 and 2": 0,
    "Hey excelify please insert a row after row 6": 4,
    "Add rows 3 and 4 together": 3,
    "Please insert a column before column D": 5,
    "Add 7 to row 2": 1,
    "Add 6 to F16": 2,

    "Bold cell A4 text please": 9,
    "Bold row 5 please": 8,
    "Bold the text in row 8 please": 8,
    "yo make sure to bold the column 5 and thanks": 9,

    "set the background color of row 3 to blue": 12,
    "highlight cell A5 green": 10, # wrong
    "do not forget to change the color of column Y to pink": 12,
    "make A1 to B4 red": 11, # wrong
    
    "multiply row 3 by 4 please ": 13,
    "multiply cell G68 by -29": 14,

    "find sine of col S": 15,
    "find cosine of I14": 19,

    "sort the table by col B": 21,

    "normalize col F": 25,
    "normalize column X": 25,
}

COLORS = [
    "red", "blue", "green", "purple", "pink", "orange", "yellow", "white", "black"
]

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

class MyPretrainedWord2Vec():
    pass

class MyPretrainedGlove():
    def __init__(self, num_dimentions):
        self.num_dimentions = num_dimentions
        self.loadVectors()

    def loadVectors(self):
        self.embeddings_dict = {}
        dict_file_name = "storage/embeddings/glove/embeddings_dict_" + \
            str(self.num_dimentions)+".pickle"

        if(os.path.isfile(dict_file_name)):
            # load existing dict
            with open(dict_file_name+".pickle", 'rb') as handle:
                self.embeddings_dict = pickle.load(handle)
        else:
            # Read vectors from txt file
            # with open(self.modelFileName+'.txt', 'r') as f:
            with open('storage/embeddings/glove/glove.6B.'+str(self.num_dimentions)+'d.txt', 'r') as f:
                for line in f:
                    values = line.split()
                    word = values[0]
                    vector = np.asarray(values[1:], "float32")
                    self.embeddings_dict[word] = vector

            # Save dict to pickle file
            with open(dict_file_name+'.pickle', 'wb') as handle:
                pickle.dump(self.embeddings_dict, handle,
                            protocol=pickle.HIGHEST_PROTOCOL)

    def fit(self, sents):
        pass

    def transform(self, sents):
        result = []
        for sent in sents:
            sent = word_tokenize(sent)
            arr = [w for w in sent]
            # print(key)
            total = np.zeros(
                self.num_dimentions, dtype="float32")
            for w in arr:
                if w in self.embeddings_dict:
                    # print("word was found in dict: ", w)
                    total = np.add(total, self.embeddings_dict[w])

            if len(arr) > 0:
                total = np.divide(total, len(arr))
            result.append(total)
        return np.array(result)

class MyTfidf():
    def __init__(self):
        self.model = TfidfVectorizer(sublinear_tf=True, analyzer='word',
                                     stop_words='english')  # vocabulary=vocabulary)

    def fit(self, sents):
        self.vectorizer.fit(sents)

    def transform(self, sents):
        return self.vectorizer.transform(sents)

class MyClassifier():
    def __init__(self, vectorizer, spreadsheet=None, debug=False):
        # self.model = model
        self.debug = debug
        self.simple_sent_clean = self.preprocess(SIMPLE_SPACE)
        self.actualOut = []
        self.spreadsheet = spreadsheet
        
        self.initVectorization(vectorizer)
        self.vectorizer.fit(self.simple_sent_clean)
        self.simple_sent_vects = self.getVectors(self.simple_sent_clean)
    
        if(debug):
            for complexSent in COMPLEX_SPACE.keys():
                self.classify(complexSent)

            self.calcAccuracy()

    def classify(self, complexSent):
        complexSent = complexSent.replace("*", "multiply")

        nums = {
            "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "zero": "0",
        }
        for k in nums.keys():
            complexSent = complexSent.replace(k, nums[k])

        self.vars = {}
        self.complex_sent_raw = complexSent
        self.complex_sent_clean = self.preprocess([complexSent], True)[0]
        self.complex_sent_vect = self.getVectors([self.complex_sent_clean])[0]
        self.calcCosineSim()
        
        if(not self.debug):
            self.runFunctions()

    def preprocess(self, sents, isComplexSpace=False):
        # re
        sents = [REPLACE_NO_SPACE.sub("", line.lower()) for line in sents]
        sents = [REPLACE_WITH_SPACE.sub(" ", line) for line in sents]

        # spell corrections
        # self.performCorrections(sents)

        # ******** run google cloud model, get entities, and swap values with replacement values

        # lemmatize and remove stop words

        for i in range(len(sents)):
            words = []
            for w in word_tokenize(sents[i].lower()):
                if(w not in stop_words):
                    words.append(lemmatizer.lemmatize(w))
                        
            sents[i] = ""
            for w in words:
                sents[i] = sents[i] + w + " "


        if isComplexSpace:
            sents = self.preprocessComplex(sents[0])

        weightShift = 5
        print(len(sents))
        for i in range(len(sents)):
            words = []
        
            for w in word_tokenize(sents[i].lower()):
                if(w == 'bold'):
                    for j in range(weightShift):
                        words.append(w)
                else:
                    words.append(w)
        
            sents[i] = ""
            for w in words:
                sents[i] = sents[i] + w + " "
       
        return sents
    
    def isRowOrCol(self, sent):
        entries = 0
        values = 0
        colors = 0
        cells = 0
        currType = ''
        arr = word_tokenize(sent)
        newSent = ""
        for i in range(len(arr)):
            w = arr[i]
            if w == 'row':
                if(i < len(arr) - 1 and isInt(arr[i + 1])):
                    currType = 'row'
                else:
                    newSent += SWAP_LIST[1] + " "
                continue;
            elif w == 'col' or w == 'column':
                if(i < len(arr) - 1 and len(arr[i + 1]) == 1):
                    currType = 'col'
                else:
                    newSent += SWAP_LIST[1] + " "
                continue
            if isInt(w):
                if currType == 'row':
                    print(w)
                    newVal = Entry(w.upper(), currType)
                    entries += 1
                    self.vars["<ENTRY_" + str(entries) + ">"] = newVal;
                    newSent += SWAP_LIST[1] + " " + str(entries) + " "
                else:
                    # value
                    newVal = Value(w)
                    values += 1
                    self.vars["<NUM_" + str(values) + ">"] = newVal;
                    newSent += SWAP_LIST[2] + " " + str(values) + " "
            # col a b c to row 2
            elif currType == 'col' and len(w) == 1:
                # col
                newVal = Entry(w.upper(), currType)
                entries += 1
                self.vars["<ENTRY_" + str(entries) + ">"] = newVal;
                newSent += SWAP_LIST[1] + " " + str(entries) + " "
            else:
                if(self.isCellValue(w)):
                    # cell value
                    newVal = Cell(w.upper())
                    cells += 1
                    self.vars["<CELL_" + str(cells) + ">"] = newVal;
                    newSent += SWAP_LIST[0] + " " + str(cells) + " "
                elif(w in COLORS):
                    newVal = Color(w)
                    colors += 1
                    self.vars["<COLOR_" + str(colors) + ">"] = newVal;
                    newSent += SWAP_LIST[3] + " " + str(colors) + " "
                else:
                    if(w not in neg_alpha1):
                        newSent += w + " "
                currType = ''
        return newSent
 
    # add 5 to row 1 2 3 and insert 4 to row 3
        
    def isCellValue(self, word):
        letter_flag = True
        if (word[0].isalpha()):
            for index in range(1, len(word), 1):
                if (word[index].isalpha() and (not letter_flag)):
                    return False
                if (word[index].isdigit()):
                    letter_flag = False
            return (not letter_flag)
        return False

    def preprocessComplex(self, text):
        newSent = self.isRowOrCol(text)
        print(text)
        print(newSent)
        pprint(self.vars)

        return [newSent.strip()]

    def initVectorization(self, vectName='count'):
        self.vectName = vectName
        if vectName == 'pretrained_glove_50':
            self.vectorizer = MyPretrainedGlove(50)
        elif vectName == 'pretrained_glove_100':
            self.vectorizer = MyPretrainedGlove(100)
        elif vectName == 'pretrained_glove_200':
            self.vectorizer = MyPretrainedGlove(200)
        elif vectName == 'pretrained_glove_300':
            self.vectorizer = MyPretrainedGlove(300)
        elif vectName == 'tfidf':
            self.vectorizer = TfidfVectorizer(sublinear_tf=True, analyzer='word',
                                              stop_words='english')  # vocabulary=vocabulary)
        elif vectName[:8] == 'word2vec':
            raise NotImplementedError
        else:
            print("Invalid vectorizer name | initVectorization")
            raise Exception
        
        # print("simple sent vects: ", len(self.simple_sent_vects))
        # print("complex sent vect: ", len(self.complex_sent_vect))

    def getVectors(self, sents):
        # print(sents)
        if self.vectName == 'count':
            return self.vectorizer.transform(sents).toarray()
        else:
            return self.vectorizer.transform(sents)

    def calcCosineSim(self):
        maxIdx = -1
        maxSim = -1
        for i in range(len(self.simple_sent_vects)):
            vec1 = np.array(self.simple_sent_vects[i]).reshape(1,-1)
            vec2 = np.array(self.complex_sent_vect).reshape(1,-1)
            # print("vec1size: ", vec1.ndim)
            # print("vec2size: ", vec2.ndim)
            simScore = cosine_similarity(vec1, vec2)

            if(simScore > maxSim):
                maxSim = simScore
                maxIdx = i
        
       
        self.actualOut.append(maxIdx)
        print("max idx is : ", maxIdx)
        print("Most similar sentence is (raw): ", SIMPLE_SPACE[maxIdx])
        # print("most sim simplespace sent (processed): ", self.simple_sent_clean[maxIdx])
        # print("Complex sent is (raw): ", self.complex_sent_raw)
        print("Complex sent (processed): ", self.complex_sent_clean)

    def runFunctions(self):
        print("debug print")
        pprint(SIMPLE_SPACE_CORRESPONDENTS)
        print(self.actualOut)
        print(SIMPLE_SPACE_CORRESPONDENTS[self.actualOut[-1]])
        run_functions(self.spreadsheet, SIMPLE_SPACE_CORRESPONDENTS[self.actualOut[-1]], self.vars)
        
        self.vars = {}

    def calcAccuracy(self):
        print("xpected out: ", list(COMPLEX_SPACE.values()))
        print("actual: ", self.actualOut)
        print("Testing accuracy: %s" % accuracy_score(list(COMPLEX_SPACE.values()), self.actualOut))

# def main():
#     vectorizers = ['pretrained_glove_50',]#'pretrained_glove_100', 'pretrained_glove_200', 'pretrained_glove_300', 'count', 'tfidf']
#     for vect in vectorizers:
#         print("currently doing ", vect)
#         MyClassifier(vectorizer=vect, debug=True)

# if __name__ == "__main__":
#     main()

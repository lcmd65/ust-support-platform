        
import re
import nltk 
import numpy 
import os
import gensim
import transformers
import torch
import json
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from fuzzywuzzy import fuzz
from db import connectMongoEmbedded
import openai

def readMongoEmbeddedDatabase(DB_model):
    data = DB_model.connectMongoEmbedded()
    database = []
    for item in data: 
            item_data = Dataset(\
                item["instruction"],
                item["input"],
                item["output"])
            database.append(item_data)
    return database

class Dataset():
    def __init__(self, instruction, input, output):
        self.instruction = instruction
        self.input = input
        self.output = output         
    
    def display(self):
        print(self.instruction,\
        self.input,\
        self.output)
        
class Conver():
    def __init__(self):
        self.bot_, self.user_, self.score = [], [], []
        self.length = 0
        self.output = [] # topscore list 
        self.model = self.sementicWord2Vec()
        self.llm_model = AutoModelForQuestionAnswering.from_pretrained("ancs21/xlm-roberta-large-vi-qa")
        self.tokenizer = AutoTokenizer.from_pretrained("ancs21/xlm-roberta-large-vi-qa", use_fast=False)
        self.pipeline = pipeline("question-answering", model=self.llm_model, tokenizer=self.tokenizer)
    
    ## fuzzy matching 
    def processingUserText(self, index):
        self.bot_.append(None)
        self.score.append(None)
        database_embedded = readMongoEmbeddedDatabase()
        Max_score = 0
        Max_score = fuzz.ratio(self.user_[index], database_embedded[0].instruction)/100
        for item in database_embedded:
            if fuzz.ratio(self.user_[index], item.instruction)/100 >= Max_score:
                self.bot_[index] = item.output
                Max_score = fuzz.ratio(self.user_[index], item.instruction)/100
        self.score[index] = Max_score
    
    def topScoreList(self, index):
        self.output.append([])
        self.bot_.append(None)
        self.score.append(None)
        database_embedded = readMongoEmbeddedDatabase()
        max_score = 0.8
        # fuzzy top score phrase
        for item in database_embedded:
            score_fuzz = fuzz.ratio(self.user_[index], item.instruction)/100
            if  score_fuzz >= 0.8:
                if score_fuzz > max_score:
                    self.bot_[index] = item.output
                    self.output[index].append(item)  
                    max_score = score_fuzz
            elif score_fuzz >= 0.3:
                string1_embedding = self.user_[index].lower().split()
                string2_embedding = item.instruction.lower().split()
                similar =  self.model.wmdistance(string1_embedding, string2_embedding)/max(len(self.user_[index]), len(item.instruction))
                if similar >= 0.3:
                    self.output[index].append(item)  
        self.score[index] = max_score  
                        
    def questionAnswering(self, question_, context_):
        answer = self.pipeline(question=question_, context=context_)
        return answer
        
    def processingTopScoreList(self, index):
        # processing Word2vec phrase
        max_score = self.score[index]
        for item in self.output[index]:
            answer_ = self.questionAnswering(self.user_[index], item.output)
            combine_score = answer_['score']*0.75 + fuzz.ratio(self.user_[index], item.output)*0.25/100
            if  combine_score >= max_score:
                self.bot_[index] = answer_['answer']
                max_score = combine_score
        self.score[index] = max_score
    
    def answerGenerate(self, index):
        if self.bot_[index] != None:
            return self.bot_[index]
        else:
            self.processingTopScoreList(index)
            return self.bot_[index]
            
    def sementicWord2Vec(self):
        model = 'app/data/vnex.model.bin'
        if os.path.isfile(model):
            from packaging import version
            if version.parse(gensim.__version__) >= version.parse("1.0.1"):
                from gensim.models import KeyedVectors
                word2vec_model = KeyedVectors.load_word2vec_format(model, binary=True)
                return word2vec_model
            else:
                from gensim.models import Word2Vec
                word2vec_model = Word2Vec.load_word2vec_format(model, binary=True)
                return word2vec_model
            
    def openAIAPIprocessing(self, index):
        messages = []
        # retrieve documentation intruction 
        for item, index_temp in zip(self.output[index], range(5)):
            messages.append({"role": "user", "content": str(item.instruction)})
            messages.append({"role": "system", "content": str(item.output)})
        messages.append({"role": "user", "content": self.user_[index]})
        session = openai.ChatCompletion.create(model="gpt-3.5-turbo",\
            messages = messages,\
            temperature=0.1,\
            max_tokens = 512)
        # return
        self.bot_[index] = session['choices'][0]['message']['content']

    def addConver(self, text):
        self.length +=1
        self.user_.append(text)
        self.topScoreList(self.length - 1)
        
    def getConver(self):
        if self.score[self.length-1] >= 0.9:
            return self.answerGenerate(self.length - 1)  
        else:
            self.openAIAPIprocessing(self.length -1)
            return self.bot_[self.length - 1]
    
    def getConverRule(self):
        if self.score[self.length-1] >= 0.9:
            return self.bot_[self.length - 1]
        else:
            self.openAIAPIprocessing(self.length -1)
            return self.bot_[self.length - 1]
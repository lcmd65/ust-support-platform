import os
import gensim
from transformers import (
    pipeline, 
    AutoModelForQuestionAnswering, 
    AutoTokenizer
)
from fuzzywuzzy import fuzz
import openai
from app import db

def readMongoEmbeddedDatabase():
    DB_model = db.DB()
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
        # list bot message, user message and score of embedded traning output
        self.bot_, self.user_, self.score = [], [], []
        self.length = 0
        self.output = [] # topscore list 
        
    def __dict__(self):
        return {
            "bot_": self.bot_,
            "user_": self.user_,
            "score": self.score,
            "length": self.length,
            "output": self.output
        }
        
    def initModelBase(self):
        self.model = self.sementicWord2Vec()
        self.llm_model = AutoModelForQuestionAnswering.from_pretrained("ancs21/xlm-roberta-large-vi-qa")
        self.tokenizer = AutoTokenizer.from_pretrained("ancs21/xlm-roberta-large-vi-qa", use_fast=False)
        self.pipeline = pipeline("question-answering", model=self.llm_model, tokenizer=self.tokenizer)
        
    def deleteModelBase(self):
        self.model = None
        self.llm_model = None
        self.tokenizer = None
        self.pipeeline = None
    
    ## fuzzy matching 2 text
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
    
    # Get the top score embedded, use to trainning fewshot
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
                text_message_from_user = self.user_[index].lower().split()
                text_embedded_from_system = item.instruction.lower().split()
                similar =  self.model.wmdistance(text_message_from_user, text_embedded_from_system)\
                    /max(len(self.user_[index]), len(item.instruction))
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
        model = 'app/data/vnex.model.bin' # vinbigdata pretraied word2vec2018 - wiki vietnamsese data- Nguyen Quoc Dat
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
        # few shot learning configuration
        for item, index_temp in zip(self.output[index], range(5)):
            messages.append({"role": "user", "content": str(item.instruction)})
            messages.append({"role": "system", "content": str(item.output)})
        messages.append({"role": "user", "content": self.user_[index]})
        session = openai.ChatCompletion.create(model="gpt-3.5-turbo",\
            messages = messages,\
            temperature=0.1)
        # return best choice in rank reward model
        self.bot_[index] = session['choices'][0]['message']['content']

    def addConver(self, text):
        # init sesstion processing in generator
        self.initModelBase()
        # processing
        self.length +=1
        self.user_.append(text)
        self.topScoreList(self.length - 1)
        # delete sesstion model processing generator
        
    def getConver(self):
        if self.score[self.length-1] >= 0.9:
            # one-shot learning 
            messages = []
            messages.append({"role": "user", "content": str(self.answerGenerate(self.length - 1))})
            messages.append({"role": "user", "content": self.user_[self.length-1]})
            session = openai.ChatCompletion.create(model="gpt-3.5-turbo",\
                messages = messages)
            self.bot_[self.length - 1] = session['choices'][0]['message']['content']
        else:
            # few-shot learning
            self.openAIAPIprocessing(self.length -1)
        self.deleteModelBase()
        return self.bot_[self.length - 1] 
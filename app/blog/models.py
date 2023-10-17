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
        self.output_length = [] # topscrore list volume, each index is define <=5
        
    def __dict__(self):
        return {
            "bot_": self.bot_,
            "user_": self.user_,
            "length": self.length,
        }
    def re_init(self):
        for index in range (self.length):
            self.output.append(None)
            self.output_length.append(None)
            self.score.append(None)
        
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
        
    # Get the top score embedded, use to trainning fewshot
    def topScoreList(self, index):
        self.output.append([])
        self.output_length.append(int(0))
        self.score.append([])
        database_embedded = readMongoEmbeddedDatabase()
        # fuzzy top score phrase
        for item in database_embedded:
            score_fuzz = fuzz.ratio(self.user_[index], item.instruction)/100
            if  score_fuzz >= 0.8:
                self.output[index].append(item)
                self.score[index].append(score_fuzz)
                self.output_length[index] +=1
            elif score_fuzz >= 0.5:
                text_message_from_user = self.user_[index].lower().split()
                text_embedded_from_system = item.instruction.lower().split()
                similar =  self.model.wmdistance(text_message_from_user, text_embedded_from_system)\
                    /max(len(self.user_[index]), len(item.instruction))
                if similar >= 0.5:
                    self.output[index].append(item)  
                    self.score[index].append(score_fuzz*similar)
                    self.output_length[index] += 1
                                            
    def questionAnswering(self, question_, context_):
        answer = self.pipeline(question = question_, context = context_)
        return answer
        
    def processingTopScoreList(self, index):
        # processing fewhot collect phrase
        output_new, output_length_new = [], int(0)
        while self.output_length[index] > 0 and output_length_new < 3:
                for index2 in range(self.output_length[index]-1):
                    if self.score[index][index2] == max(self.score[index]):
                        output_new.append(self.output[index][index2])
                        self.score[index].pop(index2)
                        self.output[index].pop(index2)
                        self.output_length[index] -= 1
                        output_length_new += 1
                        break
        self.output[index] = output_new
        self.output_length[index] = output_length_new
            
    def sementicWord2Vec(self):
        # vinbigdata pretraied word2vec2018 - wiki vietnamsese data- Nguyen Quoc Dat
        model = 'app/api/vnex.model.bin' 
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
        for item in self.output[index]:
            messages.append({"role": "user", "content": str(item.instruction)})
            messages.append({"role": "system", "content": str(item.output)})
        messages.append({"role": "user", "content": self.user_[index]})
        session = openai.ChatCompletion.create(model="gpt-3.5-turbo",\
            messages = messages)
        # return best choice in rank reward model
        self.bot_.append(session['choices'][0]['message']['content'])

    def addConver(self, text):
        # init sesstion processing in generator
        self.initModelBase()
        # processing
        self.length += 1
        self.user_.append(text)
        self.topScoreList(self.length - 1)
        self.processingTopScoreList(self.length - 1)
        # delete sesstion model processing generator
        
    def getConver(self):
        self.openAIAPIprocessing(self.length -1)
        # delete the model base after processing
        self.deleteModelBase()
        return self.bot_[self.length - 1]
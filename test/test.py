import selenium
from selenium import webdriver

class Test():
    def __init__(self):
        self.driver = None
        self.test = []
        
    def login_test(self, username, password):
        self.driver.find("div", id = "username")
        self.driver.send(username)
        self.driver.find("div", id = "pass")
        self.driver.send(password)
        
    def generate_question(self):
        pass
        
    def choosing_function(self, name_function):
        self.driver.find("button", _id = name_function).click()
        
    def generate_conversation(self, number_conver):
        list = [ None for x in range(number_conver)]
        for index in range(number_conver):
            list[index] = self.generate_question()
        return list
            
    def testing_conver(self):
        list_test = None 
        for item in list_test:
            self.driver.find("textra", _id = "entry-chat").send(item)
            self.driver.keyboard.find(id = 191).click()
    
    def create_test(self):
        pass
    
    def init_list_test(self):
        pass
    
    
        
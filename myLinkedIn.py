'''
Created on Jun 10, 2016

@author: seanbarow
'''
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse 
from urllib.parse import parse_qs
from mySiteObject import MySiteObject

class MyLinkedIn(MySiteObject):
    def __init__(self, keyfile):
        
        MySiteObject.__init__(self, keyfile)
        
        # Open a LinkedIn instance
        self.browser = webdriver.Chrome('/users/seanbarow/pySean/chromedriver')
        self.browser.get("https://linkedin.com/uas/login")
        # If something bad happens is the login, clean up (close the browser)
        try:
            emailElement = self.browser.find_element_by_id("session_key-login")
            emailElement.send_keys(self.username)
            passElement = self.browser.find_element_by_id("session_password-login")
            passElement.send_keys(self.password)
            passElement.submit()
        except Exception as E:
            print(E)
            self.closeBrowser()
        
        print('[+] Success!  Logged In!')
 
    def getID(self, url):
        """
        Parse a URL into size components including query string
        Returning a dict, return the first id that you dome to.  This is the LinkIn id
        """
        pUrl = urlparse(url)
        return parse_qs(pUrl.query)['id'][0]
        
    def ViewBot(self):
        visited = {}
        pList = []
        count = 0
        while True:
            # Sleep to make sure everything loads, add random to makue us look human
            time.sleep(random.uniform(3.5, 6.9))
            page = BeautifulSoup(self.browser.page_source, 'lxml')
            people = self.getLinks(page, 'profile/view?id=')
            if people:
                for person in people:
                    ID = self.getID(person)
                    if ID not in visited:
                        pList.append(person)
                        visited[ID] = 1
            if pList:  # if there are people to look at, then look at them
                person = pList.pop()
                self.browser.get(person)
                count += 1
            else: # otherwise find people via the jobs pages
                jobs = self.getLinks(page, '/jobs')
                if jobs:
                    job = random.choice(jobs)
                    root = 'http://www.linkedin.com'
                    roots = 'https://www.linkedin.com'
                    if root not in job or roots not in job:
                        job = roots + job
                    self.browser.get(job) 
                else: 
                    print("I'm losting exiting")
                    break 
            
            print("%s Visited! \n(%s / %s) Visited/Queue" % (self.browser.title, str(count), str(len(pList))))
                
                
        
if __name__ == '__main__':
    handler = MyLinkedIn('keyfile.txt')
    # Always close the browser even if something bad happens.
    try:
        handler.ViewBot()
    finally:
        handler.closeBrowser()
        
        
        
        
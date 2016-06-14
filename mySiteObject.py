'''
Created on Jun 13, 2016

@author: seanbarow
'''

class MySiteObject:
    
    # This is the general init which reads in the username and password from a keyfile
    def __init__(self, keyfile):
        with open(keyfile, 'r', encoding='utf-8') as f:
            keys = f.read().split()
            
        if len(keys) != 2:
            raise RuntimeError('Incorrect number of keys found in ' + keyfile)
        
        self.username, self.password = keys
    
    # This gets all the links from a page based on a seq
    # TODO: do we need an option not to have a sequence?    
    def getLinks(self, page, seq):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')
            if url:
                if seq in url:
                    links.append(url)
        return links
    
    # Close the browser, this seems to be common with all the classes
    def closeBrowser(self):
        self.browser.close()
        print('Goodbye!')
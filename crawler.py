# -*- coding:UTF-8 -*-
import urllib
import urllib2
import re
import collections,threading


class JokeGetter(object):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.queue = collections.deque()
        self.visited = set()
        start_index = '117860367'
        self.queue.append(start_index)
        self.visited.add(start_index)
        self.file_object = open('jokes.txt','w')
        self.file_object.write('1222222')
        self.mutex_q = threading.Lock()
        self.mutex_w = threading.Lock()
        self.condition = threading.Condition()
    
    def readPage(self,index):
        if not index:
            return 
        try:
            url = 'http://www.qiushibaike.com/article/'+index
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            #content = response.read()
            content = response.read().decode('utf-8')
            pattern = re.compile('<div class="content">((.|\n)*?)</div>',re.S)
            jokes = re.findall(pattern,content)
            url_pattern = re.compile('<a href="/article/(.*?)".*?>',re.S)
            urls = re.findall(url_pattern,content)
            chinese = u'笑话大全'
            
            type_pattern = re.compile(chinese,re.S)
            tp = re.findall(type_pattern,content)
            
            if not tp:
                jokes = None
                
            return urls,jokes
            '''for url in urls:
                if url not in self.visited:
                    self.queue.append(url)
                    self.visited.add(url)
            #print(content)
            print(index)
            if tp:
                for item in jokes:
                    tmp = item[0].encode('utf-8')
                    self.file_object.write(tmp+'\n')
                    print(tmp)'''
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
            return None,None
    def add_urls(self,urls):
        if not urls:
            return
        for url in urls:
            if url not in self.visited:
                self.queue.append(url)
                self.visited.add(url)
    def jokes_write(self,jokes):
        if not jokes:
            return
        for item in jokes:
            tmp = item[0].encode('utf-8')
            self.file_object.write(tmp+'\n')
            print(tmp)
    
        
    def thread_start(self):
        print('Reading.....')
        count = 0
        while count<100:
            print(count)
            self.condition.acquire()
            if not self.queue:
                print('wait')
                self.condition.wait()
            cur = self.queue.popleft()
            self.condition.release()
            print(cur)
            urls,jokes = self.readPage(cur)
            print('finish')
            self.condition.acquire()
            self.add_urls(urls)
            self.condition.notify()
            self.condition.release()
            
            self.mutex_w.acquire()
            self.jokes_write(jokes)
            self.mutex_w.release()
        
            count += 1
    def start(self):
        for i in xrange(10):
            t = ThreadClass(self.thread_start)
            t.start()
     
     
class ThreadClass(threading.Thread):
    def __init__(self,func):
        threading.Thread.__init__(self)
        self.func = func
        
    def run(self):
        '''
          run 方法用于要执行的功能
        '''
        apply(self.func)
          
      
        

JokeGetter = JokeGetter()
JokeGetter.start()
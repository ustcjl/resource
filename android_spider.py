import urllib2
import urllib
import re
import thread
import time
import os
import shutil
import random

class Spider_Model:

    def __init__(self):
        self.Url = "http://androidxref.com/2.3.6/xref/"
        self.save_Url = "http://androidxref.com/2.3.6/raw/"
        self.my_headers = [
                  'Mozilla/5.0 (Windows NT 6.1;WOW64;rv:27.0)Gecko/20100101 Firefox/27.0'
                  'Mozilla/5.0 (Windows;U;Windows NT 6.1;en-US;rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'
                  'Mozilla/5.0 (X11;Ubuntu;Linux i686;rv:10.0)Gecko/20100101 Firefox/10.0'
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
                ]

    def save_code(self, dir, file):
        if os.path.exists(dir+file):
          return
        save_file = dir+file
#        apk = open('apk.txt','a')
        print self.save_Url+save_file[2:]
        pid = os.fork()
        if pid == 0:
         req = urllib2.Request(self.save_Url+save_file[2:])

         random_header = random.choice(self.my_headers)

         req.add_header('User-Agent',random_header)
         req.add_header('Referer',self.Uri)

         url = urllib2.urlopen(req)
#        os.mknod(save_file)
         f = open(save_file, 'w+')
         while True:
          s = url.read(1024*32)
          if len(s) == 0:
            break
          f.write(s)
          exit(0)
         f.close()
        else:
         return

    def GetPage(self,dir):

        user_agent = random.choice(self.my_headers)
        if dir != './':
         myUrl = self.Url+dir
        else:
         myUrl = self.Url

        print dir
        req = urllib2.Request(myUrl)
        req.add_header('User-Agent',user_agent)
        req.add_header('Referer',self.Url)

        myResponse = urllib2.urlopen(req)

        myPage = myResponse.read()
        unicodePage = myPage.decode("utf-8")
#       print myPage

        pattern = re.compile(r'<tr><td><p\s+class="([^\"]+)"/></td><td><a\s+href="([^\"]+)/"><b>([^\"]+)</b></a>/</td><td>.*?</td><td>.*?</td></tr>|<tr><td><p\s+class="([^\"]+)"/></td><td><a\s+href="([^\"]+)">([^\"]+)</a></td><td>.*?</td><td>.*?</td></tr>',re.S)

#       pattern_p = re.compile(r'<tr><td><p\s+class="(.*?)"/></td><td><a\s+href="(.*?)">(.*?)</a>/</td><td>.*?</td><td>.*?</td></tr>',re.S)

        myItems = pattern.findall(unicodePage)

#       print myItems

        for item in myItems:
         if item[0] == '' and item[1] =='' and item[2] == '':
            if item[3] == 'p':
                self.save_code(dir, item[5])
                continue
            else:
                return
         if os.path.exists(dir+item[2]) == False:
            os.makedirs(dir+item[2])
#         if item[2] == 'bionic' or item[2] == 'bootable' or item[2] == 'build' or item[2] == 'cts' or item[2] == 'dalvik':
#            continue
         self.GetPage(dir+item[2]+'/')




    def Start(self):
        self.GetPage("./")

myModel = Spider_Model()
myModel.Start()

#!/usr/bin/python

#requires httrack

import urllib.request
import re
import os
import sys

def retrieveTop(quantity,retrieve):
    wfile = open("500.txt","w")
    page = "http://www.alexa.com/topsites/global;"
    pattern = r"<a href=\"/siteinfo/(.*?)\">(.*?)</a>"
    #command = "wget -q -l 1 -r -k -P webpages "
    command = 'cd webpages && mkdir <DIR> && cd <DIR> && wget -E -H -k -K -p <URL>'
    #command = "httrack <URL> -nr2N101 -O webpages/<DIR>"# -P proxy.unlu.edu.ar:8080"
    position = 1

    os.system('rm -rf webpages/ -R')
    os.system('mkdir webpages')

    for i in range(0, 1):#20):
        actualurl = page+str(i)
        content = urllib.request.urlopen(actualurl).read()
        match = re.findall(pattern, content.decode())
        for webpage in match:
            print(str(position)+' - '+webpage[1])
            wfile.write(webpage[1]+'\r\n')
            if retrieve:
                connection = urllib.request.urlopen('http://www.'+webpage[1])
                execution = command.replace('<URL>',connection.geturl()).replace('<DIR>',webpage[1])
                os.system(execution)
            position += 1
            if position > quantity:
                break

if __name__ == "__main__":
    try:
        quantity = int(sys.argv[1])
    except Exception as e:
        sys.exit('Usage: top500.py quantity(number) -r(retrieve sites in webpages/)')
    retrieve = 0
    try:
        if sys.argv[2] == '-r':
            retrieve = 1
    except:
        pass
    retrieveTop(quantity,retrieve)
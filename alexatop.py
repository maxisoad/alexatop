#!/usr/bin/python

#requires httrack

import urllib.request
import re
import os
import sys
import shutil
import argparse

def retrieveTop(quantity,retrieve):
    sitesPerPage = 25
    wfile = open("500.txt","w")
    page = "http://www.alexa.com/topsites/global;%i"
    pattern = r"<a href=\"/siteinfo/(.*?)\">(.*?)</a>"
    #command = "wget -q -l 1 -r -k -P webpages "
    command = 'cd webpages && mkdir <DIR> && cd <DIR> && wget -E -H -k -K -p <URL>'
    #command = "httrack <URL> -nr2N101 -O webpages/<DIR>"# -P proxy.unlu.edu.ar:8080"
    position = 1

    if retrieve:
        try:
            shutil.rmtree('webpages')
        except Exception as e:
            print(e)
        os.mkdir('webpages')
    
    #for i in range(0, 20):
    while quantity > position:
        i = int(position/sitesPerPage)
        actualurl = page % i
        content = urllib.request.urlopen(actualurl).read()
        match = re.findall(pattern, content.decode())
        for webpage in match:
            print(str(position)+' - %s' % webpage[1])
            wfile.write(webpage[1]+'\r\n')
            if retrieve:
                try:
                    connection = urllib.request.urlopen('http://www.'+webpage[1])
                    url = connection.geturl()
                except:
                    url = 'https://www.'+webpage[1]
                execution = command.replace('<URL>',url).replace('<DIR>',webpage[1])
                os.system(execution)
            position += 1
            if position > int(quantity):
                sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("quantity", help="Quantity",type=int)
    parser.add_argument("-r", "--retrieve", action="count", default=0)
    args = parser.parse_args()
    try:
        quantity = args.quantity
    except Exception as e:
        sys.exit('Usage: top500.py quantity(number) -r(retrieve sites in webpages/)')
    retrieve = False
    try:
        if args.retrieve:
            retrieve = True
    except:
        pass
    retrieveTop(quantity,retrieve)
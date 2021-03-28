import requests
import sys
import re
import argparse
parser = argparse.ArgumentParser()



urlregex=re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")


print("\n")
parser.add_argument("url",metavar="url",help="url")
parser.add_argument("-M", "--method",default="GET",choices=["GET","POST","PATCH","DELETE","PUT"],help="method")
parser.add_argument("-H","--headers",action="append",help="headers")
args = parser.parse_args()
#url validation
if(urlregex.match(args.url)==None):
    print("url is not valid\n")
    exit(0)
#---
#parse headers
headers={}
for i in args.headers:
    templist=i.split(",")
    for j in templist:
        headerlist=j.split(":")
        if(headerlist[0] in headers.keys()):
            print("Warning!input has duplicated value for header ("+headerlist[0]+"),Program will use the last one\n")
        headers[headerlist[0]]=headerlist[1]
print(headers)
        
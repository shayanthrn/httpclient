import requests
import sys
import re
import argparse
parser = argparse.ArgumentParser()



urlregex=re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
body=""

print("\n")
parser.add_argument("url",metavar="url",help="url")
parser.add_argument("-M", "--method",default="GET",choices=["GET","POST","PATCH","DELETE","PUT"],help="method")
parser.add_argument("-H","--headers",action="append",help="headers")
parser.add_argument("-Q","--queries",action="append",help="queries")
parser.add_argument("-D","--data",action="append",help="data")
parser.add_argument("--json",action="append",help="json")
parser.add_argument("--file",help="file")
args = parser.parse_args()
#url validation
if(urlregex.match(args.url)==None):
    print("url is not valid\n")
    exit(0)
#----
#parse headers
headers={}
if(args.headers!=None):
    for i in args.headers:
        templist=i.split(",")
        for j in templist:
            headerlist=j.split(":")
            if(headerlist[0].lower() in headers.keys()):
                print("Warning!input has duplicated value for header ("+headerlist[0]+"),Program will use the last one\n")
            headers[headerlist[0].lower()]=headerlist[1]
#----
#parse queries
queries={}
if(args.queries!=None):
    for i in args.queries:
        templist=i.split("&")
        for j in templist:
            qlist=j.split("=")
            if(qlist[0].lower() in queries.keys()):
                print("Warning!input has duplicated value for query ("+qlist[0]+"),Program will use the last one\n")
            queries[qlist[0].lower()]=qlist[1]
#----
#parse data
urlencoded_regex = re.compile("([A-Za-z0-9%./]+=[^\s]+)")
if(args.data!=None):
    for i in args.data:
        if(urlencoded_regex.match(i)==None):
            print("Warning!your data input is not in format of x-www-form-urlencoded ("+i+")\n")
        body+=i
        body+="&"
    body = body[:-1]
    if("content-type" not in headers.keys()):
        headers["content-type"]="application/x-www-form-urlencoded"
#----
#parse json
json_regex=re.compile(r"\{(.*\:.*)*\}")
if(args.json!=None):
    for i in args.json:
        if(json_regex.match(i)==None):
            print("Warning!your data input is not in format of JSON ("+i+")\n")
        body+=i
        body+=","
    body = body[:-1]
    if("content-type" not in headers.keys()):
        headers["content-type"]="application/json"
#----
#parse file
print(args.file)
import requests
import sys
import re
import argparse
parser = argparse.ArgumentParser()



urlregex=re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")



parser.add_argument("url",metavar="url",help="url")
parser.add_argument("-M", "--method", help="method")
args = parser.parse_args()
#url validation
if(urlregex.match(sys.argv[1])==None):
    print("url is not valid")
    exit(0)
#---
#method validation
if(args.method==None):
    args.method="GET"
if(args.method.upper() not in ["GET","POST","PATCH","DELETE","PUT"]):
    print("method is not valid")
    exit(0)
#---
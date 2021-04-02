import requests
import sys
import re
import argparse
from tqdm import tqdm
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
parser.add_argument("--timeout",help="timeout")
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
myfile=None
if(args.file!=None):
    try:
        myfile =open(args.file, "rb")
        body=myfile.read()
        if("content-type" not in headers.keys()):
            headers["content-type"]="application/octet-stream"
    except FileNotFoundError:
        print("file not found\n")
        exit(0)
#----
#parse timeout
timeout=100000
if(args.timeout!=None):
    timeout=float(args.timeout)
#----

try:
    if(args.method=="GET"):
        response=requests.get(args.url,headers=headers,params=queries,data=body,timeout=timeout,stream=True)
    elif args.method=="POST":
        response=requests.post(args.url,headers=headers,params=queries,data=body,timeout=timeout,stream=True)
    elif args.method=="PATCH":
        response=requests.patch(args.url,headers=headers,params=queries,data=body,timeout=timeout,stream=True)
    elif args.method=="PUT":
        response=requests.put(args.url,headers=headers,params=queries,data=body,timeout=timeout,stream=True)
    elif args.method=="DELETE":
        response=requests.delete(args.url,headers=headers,params=queries,data=body,timeout=timeout,stream=True)
    else:
        pass
    content_types=['application/pdf','application/octet-stream','image/jpeg','video/mp4','image/png','application/zip']
    print("version : HTTP/",response.raw.version)
    print("---------------------")
    print("status code : ",response.status_code)
    print("---------------------")
    print("method : ",args.method)
    print("---------------------")
    print("status massage : ",response.reason)
    print("---------------------")
    print("headers:\n")
    for header in response.headers:
        print(header,":",response.headers[header])
    print("---------------------")
    if(response.headers['content-type'] not in content_types):
        print("body: ")
        print(response.text)
    else:
        temp=response.url.split('/')
        filename=temp[-1]
        print(filename)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(filename, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")

except requests.exceptions.ConnectTimeout:
    print("Connection timeout!")
except requests.exceptions.ReadTimeout:
    print("Connection timeout!")
except requests.exceptions.ConnectionError:
    print("Too many requests!")
except:
    print("error occured")
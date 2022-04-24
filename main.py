import requests
import json
import sys
import base64
from os import path


token = sys.argv[1]
RepoName = sys.argv[2]
username = sys.argv[3]
branch = sys.argv[4]
filename = sys.argv[5]


def ChangeFile(FileName:str):
    if not path.exists(FileName):
        myFile = open(FileName, "w+")
        myFile.write("Day 0")
        myFile.close()
        return open(FileName,'r').readlines()[0]
    else:
        fileRead = open(FileName,'r').readlines()[0].split()
        number = int(fileRead[1]) + 1
        fileWrite = open(FileName, "w")
        fileWrite.write(fileRead[0] +" "+str(number))
        fileWrite.close()
        return open(FileName,'r').readlines()[0]

def CreateRepo(token:str, RepoName:str, username):
    url = "https://api.github.com/user/repos"
    headers =  {"Authorization" : "token {}".format(token)}
    data = {"name": RepoName}

    res = requests.post(url,data=json.dumps(data),headers=headers)
    file_content = str(ChangeFile(filename))
    
    data = {
        'message': 'Initial commit', 
        'content': base64.b64encode(file_content.encode('utf-8')).decode('utf-8'), 
    }
    response = requests.put(f"https://api.github.com/repos/{username}/{RepoName}/contents/{filename}", headers=headers, data=json.dumps(data))

def DeleteRepo(token:str, RepoName:str, username:str):
    headers = {
        "Authorization": "token {}".format(token)
    }
    url = "https://api.github.com/repos/{}/{}".format(username,RepoName)
    res = requests.delete(url,headers=headers)
    return res

def push_to_github(filename, RepoName, username, branch, token):
    url="https://api.github.com/repos/"+username+"/"+RepoName+"/contents/"+filename

    base64content=base64.b64encode(open(filename,"rb").read())

    data = requests.get(url+'?ref='+branch, headers = {"Authorization": "token "+token}).json()
    sha = data["sha"]

    if base64content.decode('utf-8')+"\n" != data['content']:
        message = json.dumps({"message":"update",
                            "branch": branch,
                            "content": base64content.decode("utf-8") ,
                            "sha": sha
                            })

        resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})

        print(resp)
    else:
        print("nothing to update")

def VerifRepo(RepoName:str):
    res = requests.get("https://api.github.com/users/lucas-science/repos").json()
    l = []
    for i in res:
        l.append(i['name'])
    if RepoName not in l:
        CreateRepo(token, RepoName, username)

VerifRepo(RepoName)
ChangeFile(filename)
push_to_github(filename,RepoName, username,branch, token)
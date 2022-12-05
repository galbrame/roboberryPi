#!/bin/python3

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A custom web server that runs on the Raspberry Pi. It serves the 
#
# Adapted from webserver.py in Assignment 1 chat app
#-----------------------------------------


import socket
import threading
import sys
import os
import json
from myHttp import * 


running = True
HOST = ""
PORT = 80
TEST_PORT = 4000
CODES = {200: "200 OK", 201: "201 Created", 204: "204 No Content", 400: "400 Bad Request", 
            401: "401 Unauthorized", 404: "404 Not Found", 500: "500 Internal Server Error"}
TYPES = {"txt": "text/plain", "html": "text/html", "json": "application/json", 
            "jpeg": "image/jpeg", "png": "image:png"}



#------------------------------------------
# readPath
#
# DESCRIPTION: Takes a path and tries to read from it. Throws a "404 not found"
#              error if the resource doesn't exist.
#
# PARAMETERS:
#       myPath: A file directory
#
# RETURNS:
#       body: Whatever was read from the path or an HTTP error
#-----------------------------------------
def readPath(myPath):
    body = ""
    searchPath = myPath
    #browser looking for index.html
    if myPath == "/":
        searchPath = "./index.html"

    elif len(myPath) > 1 and myPath[0] == "/":
        searchPath = "." + myPath

    elif myPath[0:2] != "./":
        searchPath = "./" + myPath
    
    if os.path.isfile(searchPath):
        try:
            fd = open(searchPath, "r")
            body = fd.read()
            fd.close()

        # resource found but some sort of error
        except Exception as e:
            raise ServerError

    # resource not found
    else:
        raise NotFound

    return body



#------------------------------------------
# parseAPI
#
# DESCRIPTION: Parses an API path call
#
# PARAMETERS:
#       path: an API call
#
# RETURNS:
#       parsed: a list of API path parts, minus the /api/ part
#-----------------------------------------
def parseAPI(path):
    parsed = path.split("/")
    #get rid of the /api/ part
    parsed.pop(0) 
    parsed.pop(0) 

    return parsed



#------------------------------------------
# doGET
#
# DESCRIPTION: Fulfills a response for a GET request.
#
# PARAMETERS:
#       path: A file directory
#       reqHeaders: A {list/dict?} of the http request headers
#
# RETURNS:
#       myResponse: An HttpResponse as a string
#-----------------------------------------
def doGET(path, reqHeaders):
    #default values
    respCode = CODES[204]
    contentType = TYPES["txt"]
    body = ""

    try:
        #API calls
        if path.find("api") > 0:
            apiPath = parseAPI(path)

        #regular file fetching
        else:
            body = readPath(path)
            if body.find("<html>"):
                contentType = TYPES["html"]
            else:
                pathParts = path.split(".")
                contentType = TYPES.get(pathParts[-1])


    except HttpException:
        print("httpErr in doGET")
        raise

    if body:
        respCode = CODES[200]

    #if cookie
    #do something with headers

    myResponse = HttpResponse(respCode, contentType, "", body)

    return myResponse.toString()



#------------------------------------------
# doPOST
#
# DESCRIPTION: POST API calls the robot control scripts
#
# PARAMETERS:
#       path: A file directory
#       reqHeaders: A {list/dict?} of the http request headers
#
# RETURNS:
#       myResponse: An HttpResponse as a string
#-----------------------------------------
def doPOST(path, reqHeaders, reqBody):
    pass



#------------------------------------------
# beginThread
#
# DESCRIPTION: Threads collect and parse the client request, then form the
#              response and return it to the client.
#
# PARAMETERS:
#       conn: A TCP connection to the client
#-----------------------------------------
def beginThread(conn):
    try:
        
        myResponse = str (BadRequest)   #default setting
        #print('Connected by', addr)
        data = conn.recv(1024)

        if data:
            asText = data.decode("utf-8")
            print("Received:\n" + asText)

            newReq = HttpRequest(asText)
            msgType, path, reqHeaders, reqBody = newReq.parse()

            if msgType == "GET":
                myResponse = doGET(path, reqHeaders)
            elif msgType == "POST":
                myResponse = doPOST(path, reqHeaders, json.loads(reqBody))

        # just in case something goes ka-boom
        if myResponse is None:
            myResponse = str (ServerError)
        
        print("Response:\n" + myResponse)
        conn.sendall(myResponse.encode())


    except socket.timeout as e:
        print("Thread timeout happened")

    except HttpException as httpErr:
        #print(httpErr)
        print("Response:\n" + str (httpErr))
        conn.sendall(str (httpErr).encode())

    except Exception as e:
        print("Unknown exception happened")
        print(e)

    finally:
        conn.close()




#---"MAIN"---------------------------------------------------
#--  BEGIN WEBSERVER
#------------------------------------------------------------

args = sys.argv

# alternatively, can run in test mode in conjuction with the test suite
if len(args) > 1:
    args.pop(0) # toss webserver.py
    if (args.pop(0) == "test"):
        PORT = TEST_PORT

print("RPi server running on", socket.gethostname(), PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen()

    while running:
        try:
            conn, addr = sock.accept()
            print("Connected by", addr)
            newThread = threading.Thread(target=beginThread, args=(conn,))
            newThread.start()

        except socket.timeout as e:
            print("Socket timeout!")
        
        except KeyboardInterrupt as e:
            print("\n***SERVER EXITING***\n")
            sock.close()
            running = False
        
        except Exception as e:
            print("An unknown exception occurred")
            print(e)

sys.exit(0)
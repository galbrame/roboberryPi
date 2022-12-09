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
PORT = 5000
TEST_PORT = 4000
CODES = {200: "200 OK", 201: "201 Created", 204: "204 No Content", 400: "400 Bad Request", 
            401: "401 Unauthorized", 404: "404 Not Found", 500: "500 Internal Server Error"}
TYPES = {"txt": "text/plain", "html": "text/html", "json": "application/json", 
            "jpeg": "image/jpeg", "png": "image/png", "css": "text/css",
            "js": "text/javascript"}



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
#       parsed: a string indicating the right API call
#-----------------------------------------
def parseAPI(path):
    # turns the path into a list of tokens
    parsed = path.split("/")

    # just need the last token
    return parsed[-1]




#------------------------------------------
# parseAPIBody
#
# DESCRIPTION: Extract the parameters from the POST body and turn them
#              into a dictionary.
#
# PARAMETERS:
#       body: the body of a POST API request
#
# RETURNS:
#       params: the API parameters, as a key: value pair dictionary
#-----------------------------------------
def parseAPIBody(body):
    params = {}

    if body:
        keyPairs = body.split("\n")

        for k in keyPairs:
            tempParam = k.split("=")
            params[tempParam[0]] = tempParam[1]

        if not ("direction" in params or "speed" in params):
            raise BadRequest
    
    else:
        raise BadRequest

    return params



#------------------------------------------
# doGET
#
# DESCRIPTION: Fulfills a response for a GET request.
#
# PARAMETERS:
#       path: A file directory
#       reqHeaders: A {list/dict?} of the http request headers  NEED THIS?
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
        body = readPath(path)

        # get the Content-Type from the file extension
        if path != "/":
            pathParts = path.split(".")
            contentType = TYPES[pathParts[-1]]

        # except index.html is often not called by name...
        elif body.find("<html>") > 0:
            contentType = TYPES["html"]
        

    except HttpException:
        print("httpErr in doGET")
        raise

    if body:
        respCode = CODES[200]

    #if cookie - check for who's asking or just compare to list of conn?
    #do something with headers

    myResponse = HttpResponse(respCode, contentType, "", body)

    return myResponse.toString()



#------------------------------------------
# doPOST
#
# DESCRIPTION: POST API calls the robot control scripts
#
# PARAMETERS:
#       path: The API call
#       reqHeaders: A {list/dict?} of the http request headers?????????????
#       reqBody: The body of the request, where the parameters are hidden
# RETURNS:
#       myResponse: An HttpResponse as a string
#-----------------------------------------
def doPOST(path, reqHeaders, reqBody):

    # if main user, then do POST
    # else unauth err (or something, maybe a browser popup like "wait your turn, please")

    # check for API calls specifically
    apiPath = parseAPI(path)

    # /api/stop will have empty request body
    if apiPath == "stop":
        os.system("./cgi-bin/stop.cgi")

    # /api/move and /api/speed will have parameters in the request body
    elif apiPath != "":
        try:
            theBody = json.loads(reqBody)
            params = parseAPIBody(theBody)

            if apiPath == "speed":
                os.system("./cgi-bin/changeSpeed.cgi") # " + params["speed"])

            else:
                os.system("./cgi-bin/" + params["direction"] + ".cgi") # + ".cgi " + params["speed"])
        
        except HttpException:
            print("httpErr in doPOST")
            raise

        except json.JSONDecodeError as jde:
            print("Problem unpacking json")
            print(jde)
            raise BadRequest

        except Exception as e:
            print("Something went wrong with launching the script")
            print(e)
            raise BadRequest

    else:
        raise BadRequest

    # if we've made it this far with no errors, then only "200 OK" possible
    myResponse = HttpResponse(CODES[200], TYPES["txt"], "", "")

    return myResponse.toString()



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
                myResponse = doPOST(path, reqHeaders, reqBody)

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
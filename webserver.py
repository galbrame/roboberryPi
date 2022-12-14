#!/bin/python3

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A multi-threaded, RESTful web server that runs on the Raspberry Pi.
#          Serves index.html to a web browser and deals with GET and POST
#          http requests. Multi-threaded allows us to handle multiple requests
#          at once. This isn't strictly necessary for the current implementation
#          but could help deal with multiple users in a future version.
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
HOST = "" # host will change depending on which local network roboberry is running on
PORT = 5000 # port number at boot time
TEST_PORT = 4000 # alternative port for testing purposes
# http response codes
CODES = {200: "200 OK", 201: "201 Created", 204: "204 No Content", 400: "400 Bad Request", 
            401: "401 Unauthorized", 404: "404 Not Found", 500: "500 Internal Server Error"}
# possible Content-Type response header options
TYPES = {"txt": "text/plain", "html": "text/html", "json": "application/json", 
            "jpeg": "image/jpeg", "png": "image/png", "css": "text/css",
            "js": "text/javascript"}
# Command line argument strings for cgi-bin/move.cgi
DIRECTIONS = {"forward": "1 0 1 0", "right": "1 0 0 1", "reverse": "0 1 0 1",
                "left": "0 1 1 0", "stop": "0 0 0 0"}
pwm_mode = False # Check if PWM has been properly activated yet



#------------------------------------------
# readPath
#
# DESCRIPTION: Takes a path and tries to read from it. Throws a "404 not found"
#              error if the resource doesn't exist or a "500 Server Error" if
#              something goes wrong trying to fetch the file.
#
# PARAMETERS:
#       myPath: (String) A file directory
#
# RETURNS:
#       body: (String) Whatever was read from the path or an HTTP error
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
#       path: (String) an API call
#
# RETURNS:
#       parsed: a String indicating the right API call
#-----------------------------------------
def parseAPI(path):
    # turns the path into a list of tokens
    parsed = path.split("/")

    # just need the last token
    return parsed[-1]




#------------------------------------------
# parseAPIBody
#
# DESCRIPTION: Extract the parameters from the POST body and turn them into a
#              dictionary. Throws a "400 Bad Request" http response for empty
#              Strings or if none of the expected keys are found.
#
# PARAMETERS:
#       body: (String) the body of a POST API request
#
# RETURNS:
#       params: (Dictionary) the API parameters, as a key: value pair dictionary
#-----------------------------------------
def parseAPIBody(body):
    params = {}

    if body:
        keyPairs = body.split("\n")

        for k in keyPairs:
            tempParam = k.split("=")
            params[tempParam[0]] = tempParam[1]

        if not ("direction" in params or "speed" in params or "light" in params):
            raise BadRequest
    
    else:
        raise BadRequest

    return params



#------------------------------------------
# doGET
#
# DESCRIPTION: Fulfills a response for a GET request (fetch a local resource).
#
# PARAMETERS:
#       path: (String) A file directory
# RETURNS:
#       myResponse: (String) A formatted HttpResponse
#-----------------------------------------
def doGET(path):
    global pwm_mode

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

            # Because of the issue with trying to change gpio mode to PMW
            # at boot time (see README.md), we do it here when the web page
            # is fetched to make sure that the speed functionality works as
            # expected
            if not pwm_mode:
                os.system("./cgi-bin/activatePWM.cgi")
                pwm_mode = True
        

    except HttpException:
        print("httpErr in doGET")
        raise

    if body:
        respCode = CODES[200]

    myResponse = HttpResponse(respCode, contentType, "", body)

    return myResponse.toString()



#------------------------------------------
# doPOST
#
# DESCRIPTION: POST API calls the robot control scripts. Some APIs have empty
#              bodies while others contain the control script arguments. Will
#              not raise an error if a body comes with an API that doesn't need
#              arguments (will just ignore) but APIs that require arguments are
#              expecting them as key:value pairs in JSON or else with raise a
#              "400 Bad Request" response.
#
# PARAMETERS:
#       path: (String) The API call
#       reqBody: (Empty String or JSON) The body of the request, where the
#                parameters are hidden. Non-empty reqquest bodies should be in
#                JSON format.
# RETURNS:
#       myResponse: (String) A formatted HttpResponse
#-----------------------------------------
def doPOST(path, reqBody):
    # default values, since /api/stop doesn't require a request body
    params = {}
    dir = "stop"
    speed = "0"
    light = "0"
    exitStatus = 0

    apiPath = parseAPI(path)

    # if the body is not empty, try to parse it
    if reqBody:
        try:
            theBody = json.loads(reqBody)
            params = parseAPIBody(theBody)

        except HttpException:
            print("httpErr in doPOST")
            raise

        except json.JSONDecodeError as jde:
            print("Problem unpacking json")
            print(jde)
            raise BadRequest

        except Exception as e:
            print("Something went wrong")
            print(e)
            raise BadRequest

    # do API call
    if apiPath != "":
        # /api/stop has an empty body
        if params.get("speed") is not None:
            speed = params["speed"]
        if params.get("direction") is not None:
            dir = params["direction"]
        if params.get("light") is not None:
            light = params["light"]
        
        try:
            # just change the speed
            if apiPath == "speed":
                exitStatus = os.system("./cgi-bin/changeSpeed.cgi " + speed)

            elif apiPath == "light":
                exitStatus = os.system("./cgi-bin/led.cgi " + light)

            # move in any direction or stop
            else:
                exitStatus = os.system("./cgi-bin/move.cgi " + DIRECTIONS[dir] + " " + speed)

            # error checking
            if exitStatus != 0:
                raise ServerError
        
        except Exception as e:
            print("Something went wrong with launching the script")
            print(e)
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
        data = conn.recv(1024)

        if data:
            asText = data.decode("utf-8")
            print("Received:\n" + asText)

            newReq = HttpRequest(asText)
            msgType, path, reqHeaders, reqBody = newReq.parse()

            if msgType == "GET":
                myResponse = doGET(path)
            elif msgType == "POST":
                myResponse = doPOST(path, reqBody)

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

    # turn led on to physically indicate server is running
    os.system("./cgi-bin/led.cgi 1")

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

#!/bin/python3

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: Testing suite built alongside webserver.py (and myHttp.py)
#          to ensure proper functionality. 
#
# TO RUN: In a terminal in the same directory as test_suite.py, enter:
#         `python -m unittest -v`
#
# NOTE: webserver.py must be running in test mode (port 4000) on the same
#       machine before launching the test suite: `./webserver.py test`
#-----------------------------------------

import unittest
import socket
import json
from myHttp import *


#------------------------------------------
# Test the classes in myHttp.py
#------------------------------------------
class httpClassTests(unittest.TestCase):

    _REQUEST = "{} {} HTTP/1.1\r\nContent-Length: {}\r\n\r\n{}"


    #------------------------------------------
    def test_request_parse(self):
        rType = "GET"
        rPath = "/path/resource"
        rBody = ""
        rLen = len(rBody)
        req = self._REQUEST.format(rType, rPath, rLen, rBody)
        
        print("\nTesting http request parsing")
        
        testRequest = HttpRequest(req)
        msgType, path, headers, body = testRequest.parse()

        self.assertEqual(msgType, rType)
        self.assertEqual(path, rPath)
        self.assertEqual(int (headers.get("Content-Length")), rLen)
        self.assertEqual(body, rBody)


    #------------------------------------------
    def test_create_reponse(self):
        status = "200 OK"
        contentType = "text/html"
        cookie = "myCookie=userName"
        body = "<html><body><p>This is a webpage</p></body></html>"

        print("\nTesting http response creation")

        testReponse = HttpResponse(status, contentType, cookie, body)
        testReponse = testReponse.toString()

        self.assertTrue(testReponse.find(status) > 0)
        self.assertTrue(testReponse.find(contentType) > 0)
        self.assertTrue(testReponse.find(cookie) > 0)
        self.assertTrue(testReponse.find(body) > 0)




#------------------------------------------
# Test the classes in webserver.py
#------------------------------------------
class webserverTests(unittest.TestCase):
    _HOST = '127.0.0.1' #local host
    _PORT = 4000 #different port than usual operation to avoid port conflicts
    _REQUEST = "{} {} HTTP/1.1\r\nCookie: {}\r\nContent-Length: {}\r\n\r\n{}"
    serConn = None


    #==== HOUSEKEEPING ========================
    #------------------------------------------
    def setUp(self):

        self.serConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serConn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serConn.connect((self._HOST, self._PORT))

        #prevents the tests from hanging if the webserver gets hung up
        self.serConn.settimeout(5)



    #------------------------------------------
    def tearDown(self):
        self.serConn.close()

    #==========================================


    # Helper function for checking the results of the tests. Parses 
    # webserver.py's http responses to verify status codes and body content.
    #------------------------------------------
    def parseResponse(self, response):
        respHeaders = {}
        
        # split body from header and pop header off
        respBody = response.split("\r\n\r\n" or "\n\r\n\r" or "\n\n")
        tempHeader = respBody.pop(0)
        
        #check if there even is a body before trying to pop it
        if respBody:
            respBody = respBody.pop(0) # want a string/JSON, not a list
        else:
            respBody = {}

        # split header into message status and headers
        tempHeader = tempHeader.split("\r\n" or "\n\r" or "\n")
        
        #get status code
        statusList = tempHeader.pop(0)
        print(statusList)
        statusList = statusList.split(" ")
        print(statusList)
        status = statusList[1]
        
        # turn headers into dictionary
        for pair in tempHeader:
            if pair != "": # ignore empty
                temp = pair.split(": ")
                respHeaders[temp[0]] = temp[1]
    
        return status, respHeaders, respBody



    # Verify actually checking for specific types of requests
    #------------------------------------------
    def test_bad_request(self):
        testReq = "This is not a proper HTTP request"
        print("\nTesting 400 Bad Request server response")

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(1024)
        theResp = testResp.decode("utf-8")

        status, respHeaders, respBody = self.parseResponse(theResp)

        self.assertEqual(status, "400")


    
    # This test requires an html file called index.html in the same directory
    # as test_suite.py. At a minimum, your index.html should contain the <html>
    # tag, as this is a verification check in webserver.py itself.
    #------------------------------------------
    def test_request_webpage(self):
        msgType = "GET"
        path = "/" #how index.html is often requested
        cookie = "username"
        msgLen = 0
        body = ""
        testCompare = ""

        print("\nTesting GET html")
        testReq = self._REQUEST.format(msgType, path, cookie, msgLen, body)

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(4096)
        theResp = testResp.decode("utf-8")

        status, respHeaders, respBody = self.parseResponse(theResp)

        try:
            fd = open("index.html", "r")
            testCompare = fd.read()
            fd.close()
        except FileNotFoundError as e:
            print("index.html must be located in same directory as testing suite to run this test")

        self.assertEqual(testCompare, respBody)
        self.assertEqual(respHeaders["Content-Type"], "text/html")



    # Checking for proper Content-Type header, since that's been an issue
    #------------------------------------------
    def test_request_css(self):
        msgType = "GET"
        path = "assets/roboStyles.css"
        cookie = "username"
        msgLen = 0
        body = ""
        testCompare = ""

        print("\nTesting GET css")
        testReq = self._REQUEST.format(msgType, path, cookie, msgLen, body)

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(4096)
        theResp = testResp.decode("utf-8")

        status, respHeaders, respBody = self.parseResponse(theResp)

        self.assertEqual(respHeaders["Content-Type"], "text/css")



    # This test requires a file called someText.txt in the same directory as
    # test_suite.py. The contents of the file don't matter, as they'll just 
    # be compared to the file itself (that is, there's no specifically 
    # expected contents)
    #------------------------------------------
    def test_request_file(self):
        msgType = "GET"
        path = "./someText.txt"
        cookie = "username"
        msgLen = 0
        body = ""
        testCompare = ""

        print("\nTesting GET a file")
        testReq = self._REQUEST.format(msgType, path, cookie, msgLen, body)

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(1024)
        theResp = testResp.decode("utf-8")

        status, respHeaders, respBody = self.parseResponse(theResp)

        try:
            fd = open(path, "r")
            testCompare = fd.read()
            fd.close()
        except FileNotFoundError as e:
            print("someText.txt must be located in same directory as testing suite to run this test")

        self.assertEqual(testCompare, respBody)



    # Self-explanitory
    #------------------------------------------
    def test_request_doesnt_exist(self):
        msgType = "GET"
        path = "foo.txt"
        cookie = "username"
        msgLen = 0
        body = ""
        testCompare = "404 Not Found"

        print("\nTesting 404 File Not Found webserver response")
        testReq = self._REQUEST.format(msgType, path, cookie, msgLen, body)

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(1024)
        theResp = testResp.decode("utf-8")

        self.assertTrue(theResp.find(testCompare) > 0)


    # Physical response tested manually, but verifying the correct response sent
    #------------------------------------------
    def test_request_move_car(self):
        msgType = "POST"
        path = "/api/move"
        cookie = "username"
        body = "direction=forward\nspeed=512"
        body = json.dumps(body)
        msgLen = len(body)

        print("\nTesting /api/move")
        testReq = self._REQUEST.format(msgType, path, cookie, msgLen, body)

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(1024)
        theResp = testResp.decode("utf-8")

        print(theResp)

        self.assertTrue(theResp.find("200 OK") > 0)


    # Physical response tested manually, but verifying the correct response sent
    #------------------------------------------
    def test_request_stop_car(self):
        msgType = "POST"
        path = "/api/stop"
        cookie = "username"
        body = ""
        msgLen = len(body)

        print("\nTesting /api/stop")
        testReq = self._REQUEST.format(msgType, path, cookie, msgLen, body)

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(1024)
        theResp = testResp.decode("utf-8")

        print(theResp)

        self.assertTrue(theResp.find("200 OK") > 0)


    # Physical response tested manually, but verifying the correct response sent
    #------------------------------------------
    def test_request_change_speed(self):
        msgType = "POST"
        path = "/api/speed"
        cookie = "username"
        body = "speed=512"
        body = json.dumps(body)
        msgLen = len(body)

        print("\nTesting /api/speed")
        testReq = self._REQUEST.format(msgType, path, cookie, msgLen, body)

        self.serConn.sendall(testReq.encode())
        testResp = self.serConn.recv(1024)
        theResp = testResp.decode("utf-8")

        print(theResp)

        self.assertTrue(theResp.find("200 OK") > 0)



#------------------------------------------
#
#------------------------------------------
if __name__ == '__main__':
    unittest.main()
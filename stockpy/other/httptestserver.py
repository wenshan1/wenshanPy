# httptestserver.py - the curl test http server

# Copyright (c) 2017 Wind River Systems, Inc.
#
# The right to copy, distribute, modify or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.

# modification history
# --------------------
# 31oct17,lan  added the dict to save the ip and url map.
# 27sep17,lan  added the url "/" handler.
# 05sep17,lan  written


import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

postdata = bytes(2)
lastestUrl = "/lastesturl"
ipurlDict = {}

class ServerHandler(BaseHTTPRequestHandler):

    def postTest1(self):
        global postdata
        contencLen = self.headers["Content-Length"]
        postdata = self.rfile.read (int(contencLen))
        print("data: %s", (postdata))
        strbody = "OK".encode('utf-8')
        self.setDefaultHeader()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def postZeroData(self):
        global postdata
        strbody = "zero length data".encode('utf-8')
        self.setDefaultHeader()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def postDataOnly(self):
        global postdata
        contencLen = self.headers["Content-Length"]
        postdata = self.rfile.read (int(contencLen))
        print("data: %s", (postdata))
        strbody = "OK".encode('utf-8')
        self.setDefaultHeader()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def deleteAFile (self):
        strbody = "OK".encode('utf-8')
        self.setDefaultHeader()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def do_HEAD(self):
        print('Head. client: %s:%d %s'% (self.client_address[0],
                                         self.client_address[1],
                                         self.path))

        if self.path == '/head':
            strbody = "OK".encode('utf-8')
            self.setDefaultHeader()
            self.send_response(200)
            self.send_header("Content-Length", str(len(strbody)))
            self.end_headers()
            # Send the html message
            self.wfile.write(strbody)

    def do_DELETE(self):
        global lastestUrl
        print('Delete. client: %s:%d %s'% (self.client_address[0],
                                           self.client_address[1],
                                           self.path))

        if self.path == '/delete':
            self.deleteAFile ()

        lastestUrl = self.path
        ipurlDict[self.client_address[0]] = lastestUrl
        return

    def do_POST(self):
        global  lastestUrl
        print('Post. client: %s:%d %s'% (self.client_address[0],
                                         self.client_address[1],
                                         self.path))
        if self.path == '/posttest1':
            self.postTest1 ()
        elif self.path == '/postzerodata':
            self.postZeroData ()
        elif self.path == '/postdataonly':
            self.postDataOnly ()
        lastestUrl = self.path
        ipurlDict[self.client_address[0]] = lastestUrl
        return

    def setDefaultHeader (self):
        self.protocol_version = 'HTTP/1.1'
        self.server_version = "curl http test server 1.0"
        return

    def getTest1 (self):
        strbody = "<html>Hello World</html>".encode('utf-8')
        self.setDefaultHeader ()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def getTest2 (self):
        self.setDefaultHeader ()
        self.send_response(200)
        self.send_header("Content-Length", 0)
        self.end_headers()
        return

    def getPostData (self):
        global postdata
        self.setDefaultHeader ()
        self.send_response(200)
        self.send_header("Content-Length", str(len(postdata)))
        self.end_headers()
        # Send the html message
        self.wfile.write(postdata)
        return

    def getLastestUrl (self):
        global  lastestUrl
        if self.client_address[0] in ipurlDict:
            strurl = ipurlDict[self.client_address[0]]
        else:
            strurl = lastestUrl;
        strbody = strurl.encode('utf-8')
        self.setDefaultHeader()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def getInfo (self):
        strbody = "getinfo".encode('utf-8')
        self.setDefaultHeader ()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def do_PUT(self):
        global lastestUrl
        print('Put. client:%s:%d %s'% (self.client_address[0],
                                        self.client_address[1],
                                        self.path))
        if self.path == '/put':
            strbody = "OK".encode('utf-8')
            self.setDefaultHeader()
            self.send_response(200)
            self.send_header("Content-Length", str(len(strbody)))
            self.end_headers()
            # Send the html message
            self.wfile.write(strbody)
        lastestUrl = self.path
        ipurlDict[self.client_address[0]] = lastestUrl
        return

    def getIndex (self):
        strbody = bytes('<html><head><title> Test Server </title></head><body><h2>This is a curl test server.</h2></body></html>',
                          "utf-8")
        self.setDefaultHeader ()
        self.send_response(200)
        self.send_header("Content-Length", str(len(strbody)))
        self.end_headers()
        # Send the html message
        self.wfile.write(strbody)
        return

    def do_GET(self):
        global lastestUrl

        print('Get. client:%s:%d %s'% (self.client_address[0],
                                        self.client_address[1],
                                        self.path))
        if self.path == '/test1':
            self.getTest1 ()
        elif self.path == '/test2':
            self.getTest2 ()
        elif self.path == '/getpostdata':
            self.getPostData()
        elif self.path == '/head':
            self.do_HEAD()
        elif self.path == '/lastesturl':
            self.getLastestUrl()
        elif self.path == '/getinfo':
            self.getInfo()
        elif self.path == '/incorrecturl':
            self.close_connection = True
        elif self.path == '/':
            self.getIndex ()
        else:
            self.send_error(404)
        lastestUrl = self.path
        ipurlDict[self.client_address[0]] = lastestUrl

        return

'''
a WebSocket server.
It reads a name from the client, sends a greeting, and closes the connection.
install the module to run the command:  pip3 install websockets
'''
'''
import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print("< {}".format(name))

    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))

def runWebSocketServer (port):
    start_server = websockets.serve(hello, '', port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def  my_fork():
    child_pid = os.fork()
    if child_pid == 0:
        print ("Child Process: PID# %s" % os.getpid())
        runWebSocketServer (8089)
    else:
        print ("Parent Process: PID# %s" % os.getpid())
        runCurlTestServer (8080)
'''

def runCurlTestServer (port):
    server = HTTPServer(('', port), ServerHandler)
    server.serve_forever()

if __name__ == '__main__':
    runCurlTestServer(8080)


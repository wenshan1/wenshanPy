# httpstestserver.py - the curl test https server

# Copyright (c) 2017 Wind River Systems, Inc.
#
# The right to copy, distribute, modify or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.

# modification history
# --------------------
# 05sep17,lan  written

from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
from httptestserver import ServerHandler
import socket


def runHttpsServer (port):
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain("cert.pem", "key.pem", password="123456789")
    server = HTTPServer(('', port), ServerHandler)

    server.socket = ctx.wrap_socket(server.socket,True, ServerHandler)

    server.serve_forever()

if __name__ == '__main__':
    runHttpsServer (8443)


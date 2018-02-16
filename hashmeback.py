#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import hashlib
import time
from os import curdir, sep
import random
import json


myhash = None
def worker():
    global myhash
    while True:
        global myhash
        myhash = hashlib.md5(str(int(time.time()))).hexdigest()
        print myhash
        time.sleep(5)
    return

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        global myhash
        seven_digits = {"0" : [" _ ","| |","|_|"],
                        "1" : ["   ","  |","  |"],
                        "2" : [" _ "," _|","|_ "],
                        "3" : [" _ "," _|"," _|"],
                        "4" : ["   ","|_|","  |"],
                        "5" : [" _ ","|_ "," _|"],
                        "6" : [" _ ","|_ ","|_|"],
                        "7" : [" _ ","  |","  |"],
                        "8" : [" _ ","|_|","|_|"],
                        "9" : [" _ ","|_|"," _|"],
                        "a" : [" _ ","|_|","| |"],
                        "b" : ["   ","|_ ","|_|"],
                        "c" : [" _ ","|  ","|_ "],
                        "d" : ["   "," _|","|_|"],
                        "e" : [" _ ","|_ ","|_ "],
                        "f" : [" _ ","|_ ","|  "]}
        finalhash = ""
        for i in range(0,3):
            for digit in myhash:
                finalhash += seven_digits[digit][i]
            finalhash += '\n'
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("Bienvenidos al CTF de programación! Me complace veros por aquí. \nEstáis listos para un pequeño reto?\n\nEs muy sencillo: para conseguir la password de este reto, solo tenéis que mandar este hash de abajo en una petición POST con la clave 'hash' y el valor del hash.\n\nEj:\thash=c8e4b610c3a3344204d18d38fefda0a8\n\nEl hash se regenera cada 5 segundos por lo que si no eres rápido no superarás el reto!\nBuena suerte! Have a nice code! ;)\n\nEl hash es:\n" + finalhash)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        post=post_data.split('=')
        print post
        self._set_response()
        global myhash
        if post[0]!='hash':
            self.wfile.write('Bad request, please follow the instructions O.o\'')
        else:
            if post[0]=='hash' and post[1]==myhash:
                self.wfile.write('password{HashMeBack!}')
            else:
                self.wfile.write("Too late :(")

class S2(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype + '; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

    def do_POST(self):
        def _send_error(self):
            self.send_response(404)
            self.end_headers()

        global hashes
        global hashes_rev
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        path = self.path.split('/')
        paja = ""
        paja_chars = ["_","\\","/","-"]
        del(path[0])
        if len(path) != 1:
            _send_error(self)
        if len(path[0]) != 65 and len(path[0]) != 0:
            _send_error(self)
        else:
            path = path[0]
            if path == '':
                next_cord = None
                path = "6bc193878f2dbdb1afc719cd75069c37bedd2f530346158f8e1a277572605f82"
            else:
                next_cord = path[64]
                path = path[:-1]
                print path  + " " + next_cord
            x_md5 = path[0:64:2]
            y_md5 = path[1:65:2]
            try:
                x = hashes[x_md5]
                y = hashes[y_md5]
            except KeyError:
                _send_error(self)
            if next_cord == 'S' and y < 1000:
                y = y + 1
            if next_cord == 'N' and y > 501:
                y = y - 1
            if next_cord == 'O' and x > 1:
                x = x - 1
            if next_cord == 'E' and x < 500:
                x = x + 1
            print str(x) + " " + str(y)
            hash1 = hashes_rev[str(x)]
            hash2 = hashes_rev[str(y)]
            mixed_hash = ''.join(i+j for i,j in zip(*(s+s[-1]*(max(len(hash1),len(hash2))-len(s)) for s in (hash1,hash2))))
            print mixed_hash
            for i in range(0,32):
                for j in range(0,84):
                    paja += paja_chars[random.randint(0, 3)]
                paja += '<br>'
            y = y - 500

            if x == 133 and y == 337:
                paja = paja[:1453] + '|' + paja[1454:]
            json_text = {"data": paja, 
                        "x":x, 
                        "y":y, 
                        "nextUP": mixed_hash + 'N',
                        "nextDOWN": mixed_hash + 'S',
                        "nextLEFT": mixed_hash + 'O',
                        "nextRIGHT": mixed_hash + 'E',
                        }
            self.send_response(200)
            self.send_header('Content-type','application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(json_text))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    t = threading.Thread(target=worker)
    t.start()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

def run2(server_class=HTTPServer, handler_class=S2, port=8081):
    global hashes
    hashes = json.load(open('123sum.json'))
    global hashes_rev
    hashes_rev = json.load(open('123sum_reverse.json'))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv
    t1 = threading.Thread(target=run)
    t2 = threading.Thread(target=run2)
    t1.start()
    t2.start()
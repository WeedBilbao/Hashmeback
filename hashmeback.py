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

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
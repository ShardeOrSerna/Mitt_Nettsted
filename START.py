import threading
from _python_files.testHTML import MyHandler
import socketserver
import webbrowser
import os

##########

MY_IP = "0.0.0.0"
PORT = 9002
print("Definging thread")
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        httpd = socketserver.TCPServer((MY_IP, PORT), MyHandler)
        while True:
            httpd.handle_request()

print("Creating thread")
server = MyThread()
print("Starting Server")
server.start()
print("Server Ready")

side = "http://localhost:" + str(PORT)
print("Opening site")
webbrowser.open(side)
import time
time.sleep(30)
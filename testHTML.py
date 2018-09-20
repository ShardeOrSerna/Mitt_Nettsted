MY_IP = "10.115.170.51"
PORT = 9002
HOST_NAME ="DESKTOP-HFOST1U"

from http.server import BaseHTTPRequestHandler
import socketserver
import re
#import enigma



class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.path = "_html_files/index.html"

        if self.path == "/favicon.ico":
            self.send_response(200)
            self.send_header("content-type", "image/vnd.microsoft.icon")
            self.end_headers()
            return
        else:

            if ".html" in self.path:            
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                with open ("./"+self.path, "rb") as f:
                    text = f.read()
                self.wfile.write(text)
                print("done html")
                return

            if ".css" in self.path:
                self.send_response(200)
                self.send_header("content-type", "text/css")
                self.end_headers()
                with open("./"+self.path, "rb") as f:
                    text = f.read()
                self.wfile.write(text)
                print("done css")
                return

            if ".png" in self.path:
                self.send_response(200)
                self.send_header("content-type", "image/png")
                self.end_headers()
                with open("./"+self.path, "rb") as f:
                    resp = f.read()
                self.wfile.write(resp)
                print("done png")
                return

            if ".pdf" in self.path:
                self.send_response(200)
                self.send_header("content-type", "application/pdf")
                self.end_headers()
                with open("./"+self.path, "rb") as f:
                    text = f.read()
                self.wfile.write(text)
                print("done pdf")
                return

'''
            if re.search("Py-(.*)", self.path):
                myTerm = re.search("Py-(.*)", self.path)
                command = myTerm.group(1)
                if re.search("eni(.*)", command):
                    print("yes")
                    newTerm = re.search("eni\((.*)\)", command)
                    values = newTerm.group(1).split(",")
                    print(values)
                    print(values[1])
                    values[1] = values[1].replace("%20", " ")
                    print(values)
                    if values[0] == "enc":
                        resp = enigma.Enigma().encrypt(*values[1:])
                    elif values[0] == "dec":
                        resp = enigma.Enigma().decrypt(*values[1:])

                    
                self.send_response(200)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes(resp, "UTF-8"))
                print("Done py")
                return
'''
                
        return


print("Serving local directory")
httpd = socketserver.TCPServer((MY_IP, PORT), MyHandler)

while True:
    httpd.handle_request()

    
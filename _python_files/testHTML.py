MY_IP = "0.0.0.0"
PORT = 9002
HOST_NAME ="DESKTOP-HFOST1U"

from http.server import BaseHTTPRequestHandler
import socketserver
import re
import os
from os import walk
import PyPDF2

if __name__ == "__main__":
    import enigma
else:
    import _python_files.enigma as enigma



class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/_html_files/_Spess/index.html"

        if self.path == "/favicon.ico":
            self.send_response(200)
            self.send_header("content-type", "image/vnd.microsoft.icon")
            self.end_headers()
            with open ("images/S-logo.jpg", "rb") as f:
                resp = f.read()
            self.wfile.write(resp)
            
        else:

            if ".html" in self.path:     
                       
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                with open("./_html_files/_Spess/nav.html", "rb") as f:
                    nav = f.read()
                self.wfile.write(nav)
                self.path = self.path[1:]
                with open ("./"+self.path, "rb") as f:
                    text = f.read()
                self.wfile.write(text)
                with open ("./js_files/maxWidth.js", "rb") as f:
                    script = f.read()
                self.wfile.write(script)
                print("done html")
                

            if ".css" in self.path:
                self.send_response(200)
                self.send_header("content-type", "text/css")
                self.end_headers()
                with open("./"+self.path, "rb") as f:
                    text = f.read()
                self.wfile.write(text)
                print("done css")
                

            if ".png" in self.path:
                self.send_response(200)
                self.send_header("content-type", "image/png")
                self.end_headers()
                with open("images/"+self.path, "rb") as f:
                    resp = f.read()
                self.wfile.write(resp)
                print("done png")
                

            if ".pdf" in self.path:
                self.send_response(200)
                self.send_header("content-type", "application/pdf")
                self.end_headers()
                with open("./"+self.path, "rb") as f:
                    text = f.read()
                self.wfile.write(text)
                print("done pdf")
                


            if re.search("Py-(.*)", self.path):
                myTerm = re.search("Py-(.*)", self.path)
                command = myTerm.group(1)
                command = command.replace("%20", " ")

                #Encrypt/Decrypt some text
                if re.search("eni(.*)", command):
                    print("yes")
                    newTerm = re.search("eni\((.*)\)", command)
                    values = newTerm.group(1).split(",")
                    if values[0] == "enc":
                        resp = enigma.Enigma().encrypt(*values[1:])
                    elif values[0] == "dec":
                        resp = enigma.Enigma().decrypt(*values[1:])

                #Search for page
                elif re.search("search(.*)", command):
                    print("Searching")
                    Search = re.search("search(.*)", command)
                    terms = Search.group(1).split(" ")
                    pages = []
                    directoryPath = []
                    for (dirpath, dirnames, filenames) in walk(os.getcwd()):
                        if "_html_files" in dirpath:
                            pages.append(filenames)
                            directoryPath.append(dirpath)
                    goodPages = {}
                    for term in terms:
                        for pageSection, dirpath in zip(pages, directoryPath):
                            if len(pageSection) > 0:
                                for page in pageSection:

                                    if not "pdf" in page:
                                        with open(dirpath+"\\"+page, "r") as f:
                                            text = f.read()
                                    else:
                                        file = open(dirpath+"\\"+page, "rb")
                                        fileReader = PyPDF2.PdfFileReader(file)
                                        text=""
                                        for i in range(fileReader.getNumPages()):
                                            text+=str(fileReader.getPage(i))
                                    
                                    if re.search(term, text, re.IGNORECASE):
                                        dar = re.search("(\\_html_files.*)", dirpath).group(1)
                                        goodPages[page]=(dar+"\\"+page)

                    goodPages = remove_dupes(goodPages)

                    with open("./_html_files/_Spess/nav.html") as f:
                        resp = f.read()
                    if len(goodPages) > 0:
                        resp+="<h2>Matches on '" + Search.group(1) + "'</h2>"
                        resp += "<ul>"
                        for page in goodPages:
                            resp += ("\n<li><a href={}>{}</li>".format(goodPages[page], page.remove(".html"))
                        resp += "\n</ul>"
                    else:
                        resp+="<h2>Sorry, no matches found for '" + Search.group(1) + "'</h2>"
                    



                    
                self.send_response(200)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes(resp, "UTF-8"))
                print("Done py")

        os.chdir(".")   

def remove_dupes(dictionary):
    result={}
    for key in dictionary:
        if dictionary[key] not in result.values():
            result[key] = dictionary[key]
    return result


if __name__ == "__main:":
    print("Serving local directory")
    httpd = socketserver.TCPServer((MY_IP, PORT), MyHandler)

    while True:
        httpd.handle_request()

    

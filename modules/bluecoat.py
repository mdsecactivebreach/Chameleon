
import urllib2
import requests
import sys
import re
from urlparse import urlparse
from bs4 import BeautifulSoup
import json
import threading
import SocketServer
import SimpleHTTPServer
import time


class NewHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'webroot/index.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

class ThreadedHTTPServer(object):
    handler = NewHandler
    def __init__(self, host, port):
        self.server = SocketServer.TCPServer((host, port), self.handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

class Bluecoat:
    def __init__(self, url, clonesite):
        self.url = url
        self.clonesite = clonesite
        self.server = ''

    def clone(self):
        print "[-] Cloning " + self.clonesite
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)' }
        webContent = requests.get(self.clonesite, headers=headers).content

        try:
            if webContent.lower().index("<base href=\""):
                pass
        except ValueError:
            parsed_uri = urlparse( self.clonesite)
            base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            content = re.sub(r"(<head.*?>)", "\g<0>\n<base href=\"" + base + "\">" , webContent, count=1, flags=re.IGNORECASE)
            webContent = content

        with open('webroot/index.html', 'w') as indexFile:
            indexFile.write(webContent)
            indexFile.close()

    def check_category(self):
        # Category checking lifted from CatMyFish
        # https://github.com/Mr-Un1k0d3r/CatMyFish/blob/master/CatMyFish.py
        print "[-] Checking category for " + self.url
        request = urllib2.Request("https://sitereview.bluecoat.com/rest/categorization")
        request.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)")
        request.add_header("Origin", "https://sitereview.bluecoat.com")
        request.add_header("Referer", "https://sitereview.bluecoat.com/sitereview.jsp")
        request.add_header("X-Requested-With", "XMLHttpRequest")
        response = urllib2.urlopen(request, "url=" + self.url)

        try:
            json_data = json.loads(response.read())
            if json_data.has_key("errorType"):
                if json_data["errorType"] == "captcha":
                    print "[-] BlueCoat blocked us :("
                    sys.exit(0)
            cat = BeautifulSoup(json_data["categorization"], "html.parser")
            cat = cat.find("a")
            cat = cat.text
            print "\033[1;32m[-] Your site is categorised as: " + cat + "\033[0;0m"
        except Exception as e:
			print "[-] An error occurred"

    def serve_content(self):
        print "[-] Serving content over HTTP server"
        self.server = ThreadedHTTPServer("0.0.0.0", 80)
	try:
        	self.server.start()
	except:
		pass
    def shutdown_server(self):
        print "[-] Shutting down HTTP server"
        self.server.stop()

    def run(self):
        self.clone()
        self.serve_content()
        time.sleep(10)
	self.check_category()
        self.shutdown_server()


if __name__ == "__main__":
    url = sys.argv[1]
    clonesite = sys.argv[2]
    b = Bluecoat(url, clonesite)
    b.clone()
    b.serve_content()
    time.sleep(10)
    b.check_category()
    b.shutdown_server()

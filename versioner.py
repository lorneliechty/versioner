import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def getCurrentVersion(path):
    if os.path.isdir(path):
        return '1.0.0.0\n'
    else:
        return None

class Responder(BaseHTTPRequestHandler):
    def do_GET(self):
        version = getCurrentVersion(os.curdir + self.path)
        if version:
            self._respond(version)
        else:
            self._respond('', status=404)

    def _respond(self, response, status=200):
         self.send_response(status)
         self.send_header("Content-type", "text/html")
         self.send_header("Content-length", len(response))
         self.end_headers()
         self.wfile.write(response)

server = HTTPServer(('', 8000), Responder)
server.serve_forever()

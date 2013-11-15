import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def getCurrentVersion(path):
    if os.path.isdir(path):
        with file(path + '/version') as f:
            return f.read()

    return None

def getNextVersion(path):
    cv = getCurrentVersion(path)
    cv_major, cv_minor, cv_patch, cv_build = cv.split('.')
    cv_build = int(cv_build) + 1
    nv = '.'.join([cv_major, cv_minor, cv_patch, str(cv_build)])

    with file(path + '/version', 'w') as f:
        f.write(nv)

    return nv

class Responder(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self._respond('', status=404)
            return

        version = getNextVersion(os.curdir + self.path)
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

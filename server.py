import sys, os, socket, json
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from detectnet import detect

HOST = socket.gethostname()

class Main:
    elma=0
    armut=0
    cilek=0
    muz=0
    uzum=0
    portakal=0
    tanimsiz=0
    toplam_elma=0
    toplam_armut=0
    toplam_cilek=0
    toplam_muz=0
    toplam_uzum=0
    toplam_portakal=0
    toplam_tanimsiz=0
    

class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('/home/samil/Desktop/Esra/Server/multithreaded-server/src/index.html', 'rb') as f:
                    html_content = f.read()

                self.wfile.write(html_content)
            elif self.path == '/value':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                data = {
                "elma": round(Main.elma/detect.frame),
                "armut": round(Main.armut/detect.frame),
                "cilek": round(Main.cilek/detect.frame),
                "muz": round(Main.muz/detect.frame),
                "uzum": round(Main.uzum/detect.frame),
                "portakal": round(Main.portakal/detect.frame),
                "tanımsız":round(Main.tanimsiz/detect.frame),
                "toplam_elma": Main.toplam_elma,
                "toplam_armut": Main.toplam_armut,
                "toplam_cilek": Main.toplam_cilek,
                "toplam_muz": Main.toplam_muz,
                "toplam_uzum": Main.toplam_uzum,
                "toplam_portakal": Main.toplam_portakal,
                "toplam_tanimsiz": Main.toplam_tanimsiz
                }
                self.wfile.write(json.dumps(data).encode('utf-8'))
            else:
                self.send_error(404, 'Not Found')

        except Exception as e:
            self.send_error(500, 'Internal Server Error: {}'.format(str(e)))

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 8080

if len(sys.argv) > 2:
    CWD = sys.argv[2]
    os.chdir(CWD)
else:
    CWD = os.getcwd()

def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

def start_server_in_thread():
    server_thread = threading.Thread(target=run)
    server_thread.start()
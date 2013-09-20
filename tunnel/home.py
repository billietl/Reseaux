import BaseHTTPServer

class HTTP_tunnel_handler(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(s):
      HTTP_tunnel_handler.do_something(s)
   def do_POST(s):
      HTTP_tunnel_handler.do_something(s)
   def do_HEAD(s):
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
   def do_something(s):
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
      s.wfile.write("<html><head><title>Hey!</title></head><body><h1>What are you doing here?</h1></body></html>")

def main():
   server_address = ('',8080)
   fresh_server = BaseHTTPServer.HTTPServer(server_address, HTTP_tunnel_handler)
   fresh_server.serve_forever()

if __name__ == "__main__":
    main()

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import sqlite3
import sys

class RequestHandler(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
        
  def do_HEAD(self):
    self._set_headers()

  def do_GET(self):
    db_path = "/var/opt/sensor_server/sensor_logger.db"

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(" SELECT * FROM SENSOR_LOG WHERE unix_time = (SELECT MAX(unix_time) FROM SENSOR_LOG); ")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
      sensor_data = list(row)

    parsed_path = urlparse(self.path)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(json.dumps({
      'timestamp': sensor_data[0],
      'temperature_c': sensor_data[1],
      'temperature_f': sensor_data[2],
      'humidity': sensor_data[3]
    }).encode())
    return

  def do_POST(self):
    content_len = int(self.headers.getheader('content-length'))
    post_body = self.rfile.read(content_len)
    data = json.loads(post_body)

    parsed_path = urlparse(self.path)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(json.dumps({
      'method': self.command,
      'path': self.path,
      'real_path': parsed_path.query,
      'query': parsed_path.query,
      'request_version': self.request_version,
      'protocol_version': self.protocol_version,
      'body': data
    }).encode())
    return

if __name__ == '__main__':
  if len(sys.argv) > 1 and int(sys.argv[1]) < 9999:
    server_port = int(sys.argv[1])
  else:
    server_port = 8008

  server = HTTPServer(('', server_port), RequestHandler)
  print('Starting server on port %i' % server_port)
  server.serve_forever()
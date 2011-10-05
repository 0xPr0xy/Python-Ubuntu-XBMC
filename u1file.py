#!/usr/bin/python

import sys

if len(sys.argv) <= 1:
  print "Need more arguments"
  sys.exit(1)

_login_success = False
def login():
  from gobject import MainLoop
  from dbus.mainloop.glib import DBusGMainLoop
  from ubuntuone.platform.credentials import CredentialsManagementTool

  global _login_success
  _login_success = False

  DBusGMainLoop(set_as_default=True)
  loop = MainLoop()

  def quit(result):
    global _login_success
    loop.quit()
    if result:
	    _login_success = True

  cd = CredentialsManagementTool()
  d = cd.login()
  d.addCallbacks(quit)
  loop.run()
  if not _login_success:
    sys.exit(1)

if sys.argv[1] == "login":
  login()

def logout():
  from gobject import MainLoop
  from dbus.mainloop.glib import DBusGMainLoop
  from ubuntuone.platform.credentials import CredentialsManagementTool

  DBusGMainLoop(set_as_default=True)
  loop = MainLoop()

  def quit(result):
    loop.quit()

  cd = CredentialsManagementTool()
  d = cd.clear_credentials()
  d.addCallbacks(quit)
  loop.run()

if sys.argv[1] == "logout":
  logout()

def create_volume(path):
  import ubuntuone.couch.auth as auth
  import urllib
  base = "https://one.ubuntu.com/api/file_storage/v1/volumes/~/"
  auth.request(base + urllib.quote(path), http_method="PUT")

if sys.argv[1] == "create-volume":
  login()
  create_volume(sys.argv[2])

def put(local, remote):
  import json
  import ubuntuone.couch.auth as auth
  import mimetypes
  import urllib

  # Create remote path (which contains volume path)
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  answer = auth.request(base + urllib.quote(remote),
                        http_method="PUT",
                        request_body='{"kind":"file"}')
  node = json.loads(answer[1])

  # Read info about local file
  data = bytearray(open(local, 'rb').read())
  size = len(data)
  content_type = mimetypes.guess_type(local)[0]
  content_type = content_type or 'application/octet-stream'
  headers = {"Content-Length": str(size),
             "Content-Type": content_type}

  # Upload content of local file to content_path from original response
  base = "https://files.one.ubuntu.com"
  url = base + urllib.quote(node.get('content_path'), safe="/~")
  auth.request(url, http_method="PUT",
               headers=headers, request_body=data)

if sys.argv[1] == "put":
  login()
  put(sys.argv[2], sys.argv[3])

def get(remote, local):
  import json
  import ubuntuone.couch.auth as auth
  import urllib

  # Request metadata
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  answer = auth.request(base + urllib.quote(remote))
  node = json.loads(answer[1])

  # Request content
  base = "https://files.one.ubuntu.com"
  url = base + urllib.quote(node.get('content_path'), safe="/~")
  answer = auth.request(url)
  f = open(local, 'wb')
  f.write(answer[1])

if sys.argv[1] == "get":
  login()
  get(sys.argv[2], sys.argv[3])

def get_children(path):
  import json
  import ubuntuone.couch.auth as auth
  import urllib

  # Request children metadata
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  url = base + urllib.quote(path) + "?include_children=true"
  answer = auth.request(url)

  # Create file list out of json data
  filelist = []
  node = json.loads(answer[1])
  if node.get('has_children') == True:
    for child in node.get('children'):
      child_path = urllib.unquote(child.get('path')).lstrip('/')
      filelist += [child_path]
  print filelist

if sys.argv[1] == "list":
  login()
  get_children(sys.argv[2])

def query(path):
  import json
  import ubuntuone.couch.auth as auth
  import urllib

  # Request metadata
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  url = base + urllib.quote(path)
  answer = auth.request(url)
  node = json.loads(answer[1])

  # Print interesting info
  print 'Size:', node.get('size')

if sys.argv[1] == "query":
  login()
  query(sys.argv[2])

def delete(path):
  import ubuntuone.couch.auth as auth
  import urllib
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  auth.request(base + urllib.quote(path), http_method="DELETE")

if sys.argv[1] == "delete":
  login()
  delete(sys.argv[2])

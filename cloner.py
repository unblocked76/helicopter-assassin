import os
import clonerex
from flask import Flask, request, Response, redirect

app = Flask(__name__, static_url_path='', static_folder='public_html')

@app.route('/')
def index():
  print("--system-index.html---")
  try:
    index_html= open("public_html/index.html").read()
  except:
    clonerex.getIndex()
    try:
      index_html= open("public_html/index.html").read()
    except:
      index_html= open("system/404.html").read()
  return index_html

@app.route('/sw.js')
def sw():
  return Response(open("system/sw.js", "rb").read(), mimetype='text/javascript')

@app.route('/download.zip')
def download():
  return redirect(os.getenv("REPL_SLUG")+ ".zip", 302)
    
@app.route('/'+ os.getenv("REPL_SLUG")+ '.zip')
def zipGame():
  os.system("rm *.zip")
  os.system("cp -r system/* public_html/")  
  os.system("zip -r "+ os.getenv("REPL_SLUG")+ ".zip public_html/*")
  return Response(open(os.getenv("REPL_SLUG")+ ".zip", "rb").read(), mimetype= "application/zip")

@app.errorhandler(404)
def page_not_found(e):
  if os.path.isdir("public_html" + request.path):
    return open("public_html" + request.path + "/index.html").read()
  if os.path.isfile("system" + request.path):
    fileExt= request.path.split(".").pop()
    mimetype= "text/html"
    if fileExt== "js":
      mimetype='text/javascript'
    if fileExt== "json":
      mimetype='application/json'
    if fileExt== "css":
      mimetype='text/css'      
    if fileExt== "png":
      mimetype='image/x-png'
    # print("path", request.path, "ext", fileExt, "mimetype", mimetype)
    return Response(open("system" + request.path, "rb").read(), mimetype= mimetype)
  if clonerex.fetchFile(request.path):
    redirectURL= "https://";
    redirectURL+= os.getenv("REPL_SLUG")
    redirectURL+= "."
    redirectURL+= os.getenv("REPL_OWNER")
    redirectURL+= ".repl.co"
    redirectURL+= request.path
    print("redirectURL", redirectURL)
    return redirect(redirectURL, code=302)
  return open("system/408.html").read(), 408
  
# Initalize
game_name= open("game_name.txt").read()
if game_name!= os.getenv("REPL_SLUG"):
  os.system("rm -rf public_html/*")
  os.system("rm *.zip")
  os.system("rm patch.txt")
  open("game_name.txt", "w").write(os.getenv("REPL_SLUG"))
  open("game_source.txt", "w").write("https://gamedistribution.com/games/"+ os.getenv("REPL_SLUG"))
  
app.run(host='0.0.0.0', port=81)

import cherrypy
import os.path
import sqlite3
import pyaudio
from datetime import datetime
import json
import hashlib
import requests
from jinja2 import Environment, FileSystemLoader


baseDir = os.path.dirname(os.path.abspath(__file__))

conf = {
    "/": { "tools.staticdir.root": baseDir},
    "/js": {"tools.staticdir.on" : True,
                "tools.staticdir.dir": "js"},
    "/css": {"tools.staticdir.on": True,
                "tools.staticdir.dir": "css"},
    "/html": {"tools.staticdir.on": True,
                   "tools.staticdir.dir": "html"},
    "/samples": {"tools.staticdir.on": True,
                   "tools.staticdir.dir": "samples"},
}

cherrypy.config.update({'server.socket_port': 10015,})

#https://camposha.info/cherrypy-pass-list-from-python-to-html-via-jinja2/

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
env=Environment(loader=FileSystemLoader(CUR_DIR), trim_blocks=True)

#sqlite = sqlite3.connect("database.db")
#db = sqlite.cursor()

def sqltodict(rows):
    #Transforma o resultado da query em uma lista de dicionários
    aux = []
    for row in rows:
        d = {}
        d["id"] = row[0]
        d["name"] = row[1]
        d["duration"] = row[2]
        d["votes"] = row[3]
        d["date"] = row[4]
        aux.append(d)
    return aux

#DATA E HORA
now = datetime.now()
nowformat = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", nowformat)

#SINTESE DO ID
h = hashlib.new('sha512_256')
h.update(b"Bruno")
print(h.hexdigest())

#def testaux():
 #   rowsaux = db.execute("SELECT * FROM songs;")
  #  return sqltodict(rowsaux)


class Root(object):
    
    @cherrypy.expose
    def index(self):
        with sqlite3.connect('database.db') as sql:
            db = sql.cursor()
            rows = db.execute("SELECT * FROM samples;")
            dictaux = rows.fetchall()
        html =  env.get_template("teste.html")
        return html.render(songs = sqltodict(dictaux))
        

    @cherrypy.expose
    def about(self):
	    return open("html/drum.html")

    @cherrypy.expose
    #Lista as músicas e samples
    def list(self,type):
        '''if type == "songs":
            result = db.execute("SELECT * FROM songs ORDER BY name ASC")
        elif type == "samples":
            result = db.execute("SELECT * FROM samples ORDER BY name ASC")
        
        return json.dumps(sqltodict(result.fetchall()))'''


    @cherrypy.expose
    def get(self,id):
        #result = db.execute("SELECT * FROM songs WHERE id = ?;", [id])
        #return sqltodict(result.fetchall())
        return None


    @cherrypy.expose
    def put(self):
        url = "http://127.0.0.1:10015/put"
        values = {} 
        r = requests.post(url, data = values)
        #Terminar depois
        return None


    @cherrypy.expose
    def vote(id, point):
        #result = db.execute("SELECT * FROM songs WHERE id = ?;", [id])
        #row = result.fetchall()
        #aux = sqltodict(result)
        #newvotes = aux[0]["votes"] + int(point)
        #db.execute("UPDATE songs SET votes = ? WHERE id = ?", [newvotes, id])
        #sqlite.commit()
        return None



    


cherrypy.quickstart(Root(),"/",config = conf)

#db.close()

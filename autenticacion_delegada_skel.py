# -*- coding: utf-8 -*-

#
# CABECERA AQUI
#
'''GIW
   Practica de autenticación delegada
   Grupo 13
   Adrián Martínez Jiménez
   Lucas Segarra Fernández
   Declaramos que esta soluci´on
   es fruto exclusivamente de nuestro trabajo personal. No hemos sido
   ayudados por ninguna otra persona ni hemos obtenido la soluci´on de
   fuentes externas, y tampoco hemos compartido nuestra soluci´on con
   nadie. Declaramos adem´as que no hemos realizado de manera deshonesta
   ninguna otra actividad que pueda mejorar nuestros resultados
   ni perjudicar los resultados de los dem´as.'''

from bottle import run, get, request, response
# Resto de importaciones

import urllib2, urllib
import hashlib
import os
import json
# Credenciales. 
# https://developers.google.com/identity/protocols/OpenIDConnect#appsetup
# Copiar los valores adecuados.
CLIENT_ID     = "64556356867-83l64d75qv4egbh0lh5go1nslatldu3p.apps.googleusercontent.com"
CLIENT_SECRET = "jZ6AMAO7TltKpSUZmXDWxgd6"
REDIRECT_URI  = "http://localhost:8080/token"


# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
# https://developers.google.com/identity/protocols/OpenIDConnect#authenticatingtheuser
DISCOVERY_DOC = "https://accounts.google.com/.well-known/openid-configuration"


# Token validation endpoint para decodificar JWT
# https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken
TOKEN_VALIDATION_ENDPOINT = "https://www.googleapis.com/oauth2/v4/token"

STATE =""
    

@get('/login_google')
def login_google():
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    response.set_cookie('state', state)
    p = "https://accounts.google.com/o/oauth2/v2/auth?client_id="+CLIENT_ID+"&response_type=code&scope=openid%20email&redirect_uri="+REDIRECT_URI+"&state="+state
    return "<a href="+ p +" ><button>Pulse aquí para autenticar con google </button></a>" 

@get('/token')
def token():
    if request.cookies.get('state') == request.params.get('state'):
        code = request.params.get('code')
        params = {"code":code,"client_id":CLIENT_ID,"client_secret":CLIENT_SECRET,"grant_type":"authorization_code","redirect_uri":REDIRECT_URI} 
        params = urllib.urlencode(params)
        m = urllib2.urlopen(TOKEN_VALIDATION_ENDPOINT, params)
        m = json.loads(m.read())
        p = urllib2.urlopen("https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+m['id_token'])
        p = json.loads(p.read())
        return "<b>Bienvenido "+p['email']+"</b>"
    else:
        return "<b>ERROR</b>"

if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)

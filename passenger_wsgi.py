import os
import sys
import main

sys.path.insert(0, os.path.dirname(__file__))
# application = main

def application(environ, start_response):
    main
    #start_response('200 OK', [('Content-Type', 'text/plain')])
    #message = 'It works!\n'
    #version = 'Python %s\n' % sys.version.split()[0]
    #response = '\n'.join([message, version])
    #return [response.encode()]
    
import os, os.path
import cherrypy

from controller import ReTrackerController

class ReTrackerRoutes(object):

    @cherrypy.expose
    def index(self):
        return ReTrackerController().index()

if __name__ == '__main__':

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.config.update("server.conf")
    cherrypy.quickstart(ReTrackerRoutes(), '/', conf)

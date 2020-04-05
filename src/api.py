import flask
from flask import request
from flask_restful import Resource, Api

from src.app import app
from src.database import Paste, service


class PasteApi(Resource):
    def get(self, token):
        return service.get(token)

    def post(self):
        dic = request.get_json(force=True)
        dic['ip'] = request.headers.get('X-Real-Ip', request.remote_addr)
        paste = Paste(dic)
        return {'token': service.add(paste)}


class PageApi(Resource):
    def get(self, num):
        return service.page(num)


class RawApi(Resource):
    def get(self, token):
        response = flask.make_response(service.get(token)['content'])
        response.headers['content-type'] = 'text/plain; charset=utf-8'
        return response

    def post(self):
        paste = Paste({
            'ip': request.headers.get('X-Real-Ip', request.remote_addr),
            'content': request.get_data().decode("utf-8")
        })
        token = service.add(paste)
        response = flask.make_response(token)
        response.headers['content-type'] = 'text/plain; charset=utf-8'
        return response


api = Api(app)
api.add_resource(PasteApi, '/paste/<string:token>', '/paste')
api.add_resource(PageApi, '/page/<int:num>')
api.add_resource(RawApi, '/raw/<string:token>', '/raw')

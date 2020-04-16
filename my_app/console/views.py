import json
from flask import Blueprint, abort, jsonify
from flask_restful import Resource, reqparse
from my_app.console.models import Console
from my_app import api, db

console = Blueprint('console',__name__)

parser = reqparse.RequestParser()
parser.add_argument('name',type=str)
parser.add_argument('year',type=int)
parser.add_argument('price',type=float)
parser.add_argument('quantity',type=int)
parser.add_argument('active',type=bool)

@console.route("/")
@console.route("/home")
def home():
    return "Catalogo de Consoles"

class ConsoleAPI(Resource):
    def get(self,id=None,page=1):
        if not id:
            consoles = Console.query.paginate(page,10).items
            res = []
            for con in consoles:
                res.append({
                    'id': con.id,
                    'name': con.name
                })
            return jsonify(res)
        else:
            consoles = [Console.query.get(id)]
            res = {}
            for con in consoles:
                res = {
                    'id': con.id,
                    'name': con.name,
                    'year': con.year,
                    'price': con.price,
                    'active': con.active,
                    'quantity': con.quantity
                }
            return jsonify(res)
        if not consoles:
            abort(404)

    def post(self):
        args = parser.parse_args()
        print("OIIII")
        print(args)
        name = args['name']
        year = args['year']
        price = args['price']
        quantity = args['quantity']
        active = args['active']

        con = Console(name,year,price,active,quantity)
        db.session.add(con)
        db.session.commit()
        res = { 'name' : con.name }
        return jsonify(res)

    def delete(self,id):
        con = Console.query.get(id)
        db.session.delete(con)
        db.session.commit()
        res = {'id':id}
        return jsonify(res)

    def put(self,id):
        con = Console.query.get(id)
        args = parser.parse_args()
        name = args['name']
        year = args['year']
        price = args['price']
        active = args['active']
        quantity = args['quantity']

        con.name = name
        con.year = year
        con.price = price
        db.session.commit()
        res = {'id':con.id}
        return jsonify(res)

api.add_resource(
    ConsoleAPI,
    '/api/console',
    '/api/console/<int:id>',
    '/api/console/<int:id>/<int:page>'
)
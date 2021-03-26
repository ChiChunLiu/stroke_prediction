import pickle
import pandas as pd
from flask_restful import Api, Resource
from flask import Flask, jsonify, request
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
api = Api(app)

predict_dict = {1: 'Yes', 0: 'No'}
with open("classifier.pkl","rb") as clf_pkl:
    clf = pickle.load(clf_pkl)

client = MongoClient("mongodb://localhost:27017/")
db = client['stroke_db']

users = db["Users"]

class Register(Resource):
    def post(self):

        try:
            posted_data = request.get_json()
            print(posted_data)
            username = posted_data["username"]
            password = posted_data["password"] 
            hashed_pwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        except:
            rect = {
                "status": 305,
                "msg": "you must input a password and a username"
            }
            return jsonify(ret)

        users.insert_one({
            "Username": username,
            "Password": hashed_pwd,
            "Stroke": 0,
        })
        
        ret = {
            "status": 200,
            "msg": "registration success."
        }

        return jsonify(ret)

def verify_pwd(username, password):
    hashed_pwd = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pwd) == hashed_pwd:
        return True
    return False


class Predict(Resource):
    def post(self):

        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        features = posted_data["features"]
        
        if not verify_pwd(username, password):
            ret = {
                "status":302
            }
            return jsonify(ret)

        features = pd.DataFrame([features])
        stroke = clf.predict(features)[0]
        
        users.update_one({
            "Username":username
        }, {
            "$set":{
                "Stroke": predict_dict[stroke]
            }
        })

        ret = {
            "status":200,
            "msg":"stroke saved successfully"
        }
        return jsonify(ret)

class Get(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]
        correct_pwd = verify_pwd(username, password)
        if not correct_pwd:
            ret = {
                "status":302
            }
            return jsonify(ret)

        stroke = users.find({
            "Username": username
        })[0]["Stroke"]
        ret = {
            "status":200,
            "stroke": str(stroke)
        }

        return jsonify(ret)


api.add_resource(Register, '/register')
api.add_resource(Predict, '/predict')
api.add_resource(Get, '/get')


@app.route('/')
def rootpage():
    return "Hello! You can evaluate a person's stroke risk here!"


if __name__=='__main__':
    

    app.run(host='0.0.0.0',port=8080, debug = True)
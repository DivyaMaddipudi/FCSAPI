from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'crud.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)



class User(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        username = db.Column(db.String(50),unique=True)
        email = db.Column(db.String(120),unique=True)

        def __init__ (self,username,email):
            self.username = username
            self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username','email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


#endpoints to get all the users  

@app.route("/user",methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


    #end point to create new user 

@app.route("/user",methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']

    new_user = User(username,email)

    db.session.add(new_user)
    db.session.commit()

    # return jsonify({"Status"= "Success","Username"= username,"Email ID"= email})
    return jsonify("success")

if __name__ == '__main__':
    app.run(debug= True)
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse,request, marshal,fields
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:9562@127.0.0.1:3306/users"

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(30), nullable=False)
    student_surname = db.Column(db.String(30), nullable=False)
    major = db.Column(db.String(30), nullable=False)
    course = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(1000), nullable=False)
    age = db.Column(db.Integer, nullable=False)

user_fields = {
    "id":fields.Integer,
    "name":fields.String(attribute="student_name"),
    "surname":fields.String(attribute="student_surname"),
    "major":fields.String,
    "course":fields.Integer,
    "age":fields.Integer

}





class UserResource(Resource,):
    def get(self, user_id):
        if user_id == "all":
            users = Users.query.all()
            users_list = [{
                "id": user.id,
                "student_name": user.student_name,
                "student_surname": user.student_surname,
                "major": user.major,
                "course":user.course,
                "reason": user.reason,
                "age": user.age
            } for user in users]
            return jsonify(users_list)
        elif int(user_id.isdigit()):
            user = Users.query.get(int(user_id))
            if user:
                user_data =  {
                    "id":user.id,
                    "name":user.student_name,
                    "surname":user.student_surname,
                    "major":user.major,
                    "course":user.course,
                    "reason":user.reason,
                    "age":user.age
                }
                return user_data
            else:
                return jsonify(message="User is not found..."), 404
        else:
            return jsonify(message="Invalid value..."), 400
    def put(self,user_id):
        change_user = Users.query.get(int(user_id))

        if change_user:
            # Parse and validate the data in the request body using reqparse
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('surname', type=str)
            parser.add_argument('major', type=str)
            parser.add_argument('course', type=int)
            parser.add_argument('reason', type=str)
            parser.add_argument('age', type=int)
            args = parser.parse_args()

            # Update user fields based on the provided data
            if args['name'] is not None:
                change_user.student_name = args['name']
            if args['surname'] is not None:
                change_user.student_surname = args['surname']
            if args['major'] is not None:
                change_user.major = args['major']
            if args['course'] is not None:
                change_user.course = args['course']
            if args['reason'] is not None:
                change_user.reason = args['reason']
            if args['age'] is not None:
                change_user.age = args['age']
        else:
            return jsonify(message="User is not found...")
    def post(self,user_id):
        post_user = Users.query.get(int(user_id))
        new_user_data = request.get_json()

        new_user = Users(
            student_name=new_user_data.get('name'),
            student_surname=new_user_data.get('surname'),
            major=new_user_data.get('major'),
            course=new_user_data.get('course'),
            reason=new_user_data.get('reason'),
            age=new_user_data.get('age')
        )

        db.session.add(new_user)
        db.session.commit()
        return marshal(new_user,user_fields)
    
    def delete(self,user_id):
        deleting_user = Users.query.get(int(user_id))
        if deleting_user:
            db.session.delete(deleting_user)
            db.session.commit()
            return jsonify(message="User succesfully deleted!")
        else:
            return jsonify(message="User not found...")


api.add_resource(UserResource, "/users/<string:user_id>")
api.add_resource(UserResource,"/users/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



# REST API
# users or students

"""
1. Create table users (SQLAlchemy) - orm using python code
2. CRUD - http methods (get, post, delete, put) methods: 
    2.1 ...../users - get all users (get)
    2.2 ...../users/{id} - get 1 users with id (get)
    2.3 ...../users - create users with payload (post)
    2.4 ...../users/{id} - update user with id (put)
    2.5 ...../users/{id} - delete users with id {delete}
3.  to test use Postman or browser plugins
"""
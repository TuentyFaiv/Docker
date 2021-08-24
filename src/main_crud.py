from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"]="" #Url of mongo
mongo = PyMongo(app)
CORS(app)

db = mongo.db.users
dbMessages = mongo.db.messages

@app.get("/")
def home():
	return "Hello fucking world!!"

@app.get("/users")
def get_users():
	users = []
	for doc in db.find():
		users.append({
			"_id": str(ObjectId(doc["_id"])),
			"name": doc["name"],
			"username": doc["username"]
		})

	return jsonify(users)

@app.get("/users/<id>")
def get_user(id):
	user = db.find_one({ "_id": ObjectId(id) })
	return jsonify({
		"_id": str(ObjectId(user["_id"])),
		"name": user["name"],
		"username": user["username"]
	})

@app.post("/users")
def create_user():
	id = db.insert({
		"name": request.json["name"],
		"username": request.json["username"]
	})

	return jsonify(str(ObjectId(id)))

@app.put("/users/<id>")
def update_user(id):
	db.update_one({ "_id": ObjectId(id) }, {"$set": {
		"name": request.json["name"],
		"username": request.json["username"]
	}})
	return jsonify({ "message": "User updated" })

@app.delete("/users/<id>")
def delete_user(id):
	db.delete_one({ "_id": ObjectId(id) })
	return jsonify({ "message": "User deleted" })

if __name__ == "__main__":
	app.run()

import mysql.connector
import json
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	return "Hello Fucking World!!"

@app.route('/widgets')
def get_widgets():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="inventory"
  )
  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM widgets")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  json_data=[
		{
			"name": "un nombre perron",
			"description": "una description perrona"
		},
		{
			"name": "un nombre perron 1",
			"description": "una description perrona 2"
		}
	]

  # for result in results:
  #   json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

@app.post("/widgets")
def create_widget():
	mydb = mysql.connector.connect(
		host="mysqldb",
		user="root",
		password="p@ssw0rd1",
		database="inventory"
	)
	cursor = mydb.cursor()

	name = request.json["name"]
	description = request.json["description"]

	print({ name, description })
	try:
		cursor.execute(f"INSERT INTO widgets set name ='${name}', description ='${description}'")
		cursor.close()
	except:
		return "Not inserted", 400

	return "Working", 200

@app.route('/initdb')
def db_init():
	try:
		mydb = mysql.connector.connect(
			host="mysqldb",
			user="root",
			password="p@ssw0rd1"
		)
		cursor = mydb.cursor()

		cursor.execute("DROP DATABASE IF EXISTS inventory")
		cursor.execute("CREATE DATABASE inventory")
		cursor.close()

		mydb = mysql.connector.connect(
			host="mysqldb",
			user="root",
			password="p@ssw0rd1",
			database="inventory"
		)
		cursor = mydb.cursor()

		cursor.execute("DROP TABLE IF EXISTS widgets")
		cursor.execute("CREATE TABLE widgets (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(255), description VARCHAR(255), PRIMARY KEY (id))")
		cursor.close()

	except:
		return "Not working"

	return "init database"

if __name__ == "__main__":
  app.run(debug=True,host ='0.0.0.0',port=5000)
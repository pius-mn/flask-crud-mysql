from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api

#Create an instance of Flask
app = Flask(__name__)

#Create an instance of MySQL
mysql = MySQL()

#Create an instance of Flask RESTful API
api = Api(app)

#Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'vacationDb'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

#Initialize the MySQL extension
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
#create tables if they do not exist
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS users (
        id int  AUTO_INCREMENT NOT NULL,
        username  VARCHAR(50) NOT NULL,R
        password  VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)  
    );'''
)
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS destinations (
        id int  AUTO_INCREMENT NOT NULL,
        country VARCHAR(50) NOT NULL,
        city VARCHAR(50) NOT NULL, 
        sightseeing VARCHAR(50),
        PRIMARY KEY (id)     
    );'''
)
cursor.execute('''
        CREATE TABLE IF NOT EXISTS trip (
        id int  AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        destinationid int NOT NULL,
        transportation VARCHAR(50) NOT NULL, 
        startdate DATE NOT NULL,
        enddate DATE NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (destinationid) REFERENCES destinations(id)
    );'''
)
cursor.close()
conn.close()

#Get All Users, or Create a new user
class UserList(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from users""")#execute select statements
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            # close database after operation
            cursor.close()
            conn.close()

    def post(self):# create new users
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _name = request.form['name']
            _age = request.form['age']
            _city = request.form['city']
            insert_user_cmd = """INSERT INTO users(username, password) 
                                VALUES(%s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_name, _age, _city))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)
            
#Get a user by id, update or delete user
class User(Resource):
    def get(self, user_id):# get user by id 
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('select * from users where id = %s',user_id)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def put(self, user_id):# update user
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _name = request.form['name']
            _age = request.form['age']
            update_user_cmd = """update users 
                                 set username=%s, password=%s
                                 where id=%s"""
            cursor.execute(update_user_cmd, (_name, _age, user_id))
            conn.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to update user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

    def delete(self, user_id):# delete user
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from users where id = %s',user_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

class destinationList(Resource):# get a list of all destinations
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from destinations""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self):#add a new destination
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _country = request.form['country']
            _city = request.form['city']
            _sightseeing=request.form['sightseeing']
            insert_user_cmd = """INSERT INTO destinations(country, city, sightseeing) 
                                VALUES(%s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_country,_city,_sightseeing))
            conn.commit()
            response = jsonify(message='destination added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add destination.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)            
#Get a destination by id, update or delete destination
class destination(Resource): # list a single destination
    def get(self, destination_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('select * from destinations where id = %s',destination_id)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def put(self, destination_id):# update destination
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _country = request.form['country']
            _city = request.form['city']
            _sightseeing=request.form['sightseeing']
            update_user_cmd = """update destinations 
                                 set country=%s, city=%s, sightseeing=%s
                                 where id=%s"""
            cursor.execute(update_user_cmd, (_country, _city,_sightseeing, destination_id))
            conn.commit()
            response = jsonify('destination updated successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to update destination .')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

    def delete(self, destination_id):# delete a destination
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from destinations where id = %s',destination_id)
            conn.commit()
            response = jsonify('destination deleted successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to delete destination.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)

class destinationList(Resource):# get all destinations and create new destinations
    def get(self):# list all destinations
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from destinations""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self):# add destination
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _country = request.form['country']
            _city = request.form['city']
            _sightseeing=request.form['sightseeing']
            insert_user_cmd = """INSERT INTO destinations(country, city, sightseeing) 
                                VALUES(%s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_country,_city,_sightseeing))
            conn.commit()
            response = jsonify(message='destination added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add destination.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)            
#Get a trip by id, update or delete trip
class tripList(Resource):# list all trips
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from trip""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self):
        # create a trip
        #WARNING foreign key constrain must be observed
        #destination id must exist in the destination table
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _destinationid = request.form['destinationid']
            _transportation = request.form['transportation']
            _startdate=request.form['startdate']
            _enddate=request.form['enddate']
            insert_user_cmd = """INSERT INTO trip(destinationid, transportation, startdate,enddate) 
                                VALUES(%s, %s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_destinationid,_transportation,_startdate,_enddate))
            conn.commit()
            response = jsonify(message='trip added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed add to trip.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response) 
class trip(Resource):# list a single trip
    def get(self, trip_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('select * from trip where id = %s',trip_id)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def put(self, trip_id):# update trip
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            			
            _destinationid = request.form['destinationid']
            _transportation = request.form['transportation']
            _startdate=request.form['startdate']
            _enddate=request.form['enddate']
            update_user_cmd = """update trip 
                                 set destinationid=%s, transportation=%s, startdate=%s,enddate=%s
                                 where id=%s"""
            cursor.execute(update_user_cmd, (_destinationid, _transportation,_startdate, _enddate,trip_id))
            conn.commit()
            response = jsonify('trip updated successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to update trip .')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

    def delete(self, trip_id):#delete trip
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from trip where id = %s',trip_id)
            conn.commit()
            response = jsonify('trip deleted successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to delete trip.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)  
#API resource routes
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/user/<int:user_id>', endpoint='user')
api.add_resource(destinationList, '/destinations', endpoint='destinations')
api.add_resource(destination, '/destination/<int:destination_id>', endpoint='destination')
api.add_resource(tripList, '/trips', endpoint='trips')
api.add_resource(trip, '/trip/<int:trip_id>', endpoint='trip')

if __name__ == "__main__":
    app.run(debug=True)
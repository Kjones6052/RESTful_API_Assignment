# Import as needed
import mysql.connector # for database connection
from mysql.connector import Error # for database errors
from flask import Flask, jsonify, request # for flask, marshmallow, request, and serializing/deserializing JSON
from flask_marshmallow import Marshmallow # for data validation
from marshmallow import fields, ValidationError # for use of fields and validation error

app = Flask(__name__) # Initializing flask
ma = Marshmallow(app) # Initializing marshmallow

# Class schema for Members
class MemberSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True) 
    age = fields.Integer(required=True)

    class Meta:
        fields = ("id", "name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Class schema for Workout Sessions
class WorkoutSchema(ma.Schema):
    session_id = fields.Integer(required=True)
    member_id = fields.Integer(required=True) 
    session_date = fields.Date(required=True)
    session_time = fields.Time(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ("session id", "member id", "session date", "session time", "activity")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

# Method to initiate database connection
def get_db_connection():
    # Database Connection Parameters:
    db_name = "e_commerce_db"
    user = "root"
    password = "password"
    host = "localhost"
    
    try: # Establishing the database connection
        conn = mysql.connector.connect(
	        database=db_name,
	        user=user,
	        password=password,
	        host=host
        )
        
        return conn # Return connection
    
    except Error as e: # Database Error handling
        print(f"Error: {e}")

# Route and method for home
@app.route("/")
def home():
    return "Welcome to the Fitness Center Management App"

# Route and method for adding a new member
@app.route("/members", methods=["POST"])
def new_member():
    try:
        member_data = member_schema.load(request.json) # Verifying data
    except ValidationError as e: # Validation Error Handling
        print(f"Error: {e}") # Display message to user
        return jsonify(e.messages), 400 # Converting error message with error type indicator
    
    try:
        conn = get_db_connection() # Establishing database connection
        if conn is None: # Verifying connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Converting error message with type indicator
        cursor = conn.cursor() # Activate cursor
        
        new_member = (member_data['id'], member_data['name'], member_data['age']) # Inserting data into variable for query
        
        query = "INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)" # Defining query to add new customer
        
        cursor.execute(query, new_member) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "New member added successfully"}), 201 # Display message to user with type indicator
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Converting error message with type indicator
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for retrieving a member
@app.route("/members/<int:id>", methods=["GET"])
def search_member(id):
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Converting error message with type indicatorl
        cursor = conn.cursor() # Activate cursor
        
        member_to_get = (id,) # Inserting data into variable for query
        
        cursor.execute("SELECT * FROM Members WHERE id = %s", member_to_get) # Execute query to get member
        member = cursor.fetchall() # Fetching data and inserting it into a variable
        if not member: # Verifying member exists
            return jsonify({"error": "Member not found"}), 404 # Converting error message with type indicator
        
        return member_schema.jsonify(member) # Convert data according to schema
    except Error as e:
        print(f"Error: {e}") # Display message to user
        return jsonify({"error": "Internal Server Error"}), 500 # Converting error message with type indicator
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for retrieving all members
@app.route("/members", methods=["GET"])
def view_members():
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verify vonnecction
            return jsonify({"error:": "Database connecction failed"}), 500 # Converting error message with type indicator
        cursor = conn.cursor(dictionary=True) # Activate cursor
        
        query = "SELECT * FROM Members" # Define query
        
        cursor.execute(query) # Execute query
        members = cursor.fetchall() # Insert data into variable
        
        return members_schema.jsonify(members) # Convert data according to schema
    except Error as e:
        print(f"Error: {e}") # Display message to user
        return jsonify({"error": "Internal Server Error"}), 500 # Converting error message with type indicator
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for updating a member
@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json) # Verifying data
    except ValidationError as e:
        print(f"Error: {e}") # Display error message to user
        return jsonify(e.messages), 400 # Converting error message with type indicator
    
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Displaying error message if database connection unsuccessful
        cursor = conn.cursor() # Activate cursor

        member_to_get = (id,) # Inserting data into variable for query
        
        cursor.execute("SELECT * FROM Members WHERE id = %s", member_to_get) # Execute query to get member
        member = cursor.fetchall() # Fetching data and inserting it into a variable
        if not member: # Verifying member exists
            return jsonify({"error": "Member not found"}), 404 # Display message to user
        
        updated_member = (member_data['id'], member_data['name'], member_data['age']) # Inserting update data into a variable for query

        query = "UPDATE Members SET id = %s, name = %s, age = %s WHERE id = %s" # Defining query

        cursor.execute(query, updated_member) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "Member updated successfully"}), 201 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for removing a member
@app.route("/members/<int:id>", methods=['DELETE'])
def remove_member(id):
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Displaying error message if database connection unsuccessful
        cursor = conn.cursor() # Activate cursor

        member_to_remove = (id,) # Inserting data into variable for query
        
        cursor.execute("SELECT * FROM Members WHERE id = %s", member_to_remove) # Execute query to get member
        member = cursor.fetchall() # Fetching data and inserting it into a variable
        if not member: # Verifying member exists
            return jsonify({"error": "Member not found"}), 404 # Display message to user
        
        query = "DELETE FROM Members WHERE id = %s" # Defining query

        cursor.execute(query, member_to_remove) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "Member removed successfully"}), 201 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for scheduling a new workout session
@app.route("/workoutsessions", methods=["POST"])
def schedule_workout():
    try:
        workout_data = member_schema.load(request.json) # Verifying data
    except ValidationError as e:
        print(f"Error: {e}") # Display message to user
        return jsonify(e.messages), 400 # Converting error message, 400 indicates error type
    
    try:
        conn = get_db_connection() # Establishing database connection
        if conn is None: # Verifying connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Display message to user
        cursor = conn.cursor() # Activate cursor 
        
        new_workout = (workout_data['session id'], workout_data['member id'], workout_data['session date'], workout_data['session time'], workout_data['activity']) # Inserting data into variable for query
        
        query = "INSERT INTO WorkoutSessions (session_id, member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s, %s)" # Defining query to add new customer
        
        cursor.execute(query, new_workout) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "New workout session was scheduled successfully"}), 201 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for updating a workout session
@app.route("/workoutsessions/<int:session_id>/<int:member_id>", methods=["PUT"])
def update_workout(session_id, member_id):
    try:
        workout_data = workout_schema.load(request.json) # Verifying data
    except ValidationError as e:
        print(f"Error: {e}") # Display error message to user
        return jsonify(e.messages), 400 # Converting error message with type indicator
    
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Displaying error message if database connection unsuccessful
        cursor = conn.cursor() # Activate cursor

        workout_to_get = (session_id, member_id) # Inserting data into variable for query
        
        cursor.execute("SELECT * FROM WorkoutSessions WHERE session_id = %s AND member_id = %s", workout_to_get) # Execute query to get member
        workout = cursor.fetchall() # Fetching data and inserting it into a variable
        if not workout: # Verifying member exists
            return jsonify({"error": "Workout Session Not Found"}), 404 # Display message to user
        
        updated_workout = (workout_data['session id'], workout_data['member id'], workout_data['session date'], workout_data['session time'], workout_data['activity']) # Inserting update data into a variable for query

        query = "UPDATE WorkoutSessions SET session_id = %s, member_id = %s, session_date = %s, session_time = %s, activity = %s WHERE session_id = %s AND member_id = %s" # Defining query

        cursor.execute(query, updated_workout) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "Workout session updated successfully"}), 201 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for searching for a workout session
@app.route("/workoutsessions/<int:session_id>/<int:member_id>", methods=["GET"])
def search_workout(session_id, member_id):
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Displaying error message if database connection unsuccessful
        cursor = conn.cursor() # Activate cursor

        workout_to_get = (session_id, member_id) # Inserting data into variable for query
        
        query = "SELECT * FROM WorkoutSessions WHERE session_id = %s AND member_id = %s" # Query to find workout session
        
        cursor.execute(query, workout_to_get) # Execute query to get workout session
        workout = cursor.fetchall() # Fetching data and inserting into a variable
        if not workout: # Verifying workout session exists
            return jsonify({"error": "Workout Session Not Found"}), 404 # Display message to user
        
        return workout_schema.jsonify(workout) # Convert data according to schema
    except Error as e:
        print(f"Error: {e}") # Display message to user
        return jsonify({"error": "Internal Server Error"}), 500 # Converting error message
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for viewing all workout sessions
@app.route("/workoutsessions", methods=["GET"])
def view_workouts():
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verify vonnecction
            return jsonify({"error:": "Database connecction failed"}), 500 # Converting error message
        cursor = conn.cursor(dictionary=True) # Activate cursor

        query = "SELECT * FROM WorkoutSessions" # Define query
        
        cursor.execute(query) # Execute query
        workouts = cursor.fetchall() # Insert data into variable
        
        return workouts_schema.jsonify(workouts) # Convert data according to schema
    except Error as e:
        print(f"Error: {e}") # Display message to user
        return jsonify({"error": "Internal Server Error"}), 500 # Converting error message
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Route and method for canceling a workout session
@app.route("/workoutsessions/<int:session_id>/<int:member_id>", methods=['DELETE'])
def cancel_workout(session_id, member_id):
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Displaying error message if database connection unsuccessful
        cursor = conn.cursor() # Activate cursor

        workout_to_remove = (session_id, member_id) # Inserting data into variable for query
        
        cursor.execute("SELECT * FROM WorkoutSessions WHERE session_id = %s AND member_id = %s", workout_to_remove) # Execute query to get member
        workout = cursor.fetchall() # Fetching data and inserting it into a variable
        if not workout: # Verifying workout session exists
            return jsonify({"error": "Workout Session Not Found"}), 404 # Display message to user
        
        query = "DELETE FROM WorkoutSessions WHERE session_id = %s AND member_id = %s" # Defining query

        cursor.execute(query, workout_to_remove) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "Workout session removed successfully"}), 201 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Placed here for ease of use if wanted or needed
if __name__ == "__main__":
    app.run(debug=True)
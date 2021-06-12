from flask import Flask, request, Response
import json
import traceback
import dbconnect
# entry point of flask server
app = Flask(__name__)


@app.get("/animals")
# gets all animals
def get_animals():
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    animals = None
    try:
        cursor.execute("SELECT name, id FROM animals")
        animals = cursor.fetchall()
    except:
        traceback.print_exc()
        print("Sorry, something went wrong!")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    if animals == None:
        return Response("Error fetching data", mimetype='text/plain', status=500)
    else:
        animals_json = json.dumps(animals, default=str)
        return Response(animals_json, mimetype='application/json', status=200)


@app.post("/animals")
def add_animal():
    # this saves the animal name that's input into postman in a variable
    animal_name = None
    try:
        animal_name = request.json['animalName']
    except:
        traceback.print_exc()
        return Response("Data input error", mimetype='text/plain', status=400)
    if(animal_name == None):
        return Response("Data input error", mimetype='text/plain', status=400)
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    animal_id = -1
    try:
        cursor.execute("INSERT INTO animals(name) VALUES(?)", [animal_name, ])
        conn.commit()
        animal_id = cursor.lastrowid
    except:
        traceback.print_exc()
        print("Sorry, something went wrong!")
    # do the thing and close conn/cursor immediately
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    if(animal_id == -1):
        return Response("Add new animal failed!", mimetype='text/plain', status=500)
    else:
        # returns success message in text data with status 201 = created
        return Response("Your animal has been added!", mimetype='application/json', status=201)


@app.patch("/animals")
def edit_animal():
    try:
        # saves the animal name and id that's input into postman in variables
        animal_id = int(request.json['animalId'])
        animal_name = request.json['animalName']
    except:
        traceback.print_exc()
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    try:
        cursor.execute(
            "UPDATE animals SET name = ? WHERE id = ?", [animal_name, animal_id])
        conn.commit()
    except:
        traceback.print_exc()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # I commented this stuff out because we didn't need input from the user??
    # put id here in case there's more than one asian elephant
    # animal_dictionary = {"animalName": animal_name,
    #                      "animalId": str(animal_id)
    #                      }
    # # converts the data into json
    # json.dumps(animal_dictionary, default=str)
    # returns success message in text data with status 200 = ok if success
    return Response("Your data has been updated!", mimetype='text/plain', status=200)


@app.delete("/animals")
def delete_animal():
    # takes in data from postman to use in SQL statement
    animal_id = int(request.json['animalId'])
    animal_name = request.json['animalName']
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute("DELETE FROM animals WHERE name = ? AND id = ?", [
                   animal_name, animal_id])
    conn.commit()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # animal_dictionary = {"animalName": animal_name,
    #                      "animalId": str(animal_id)
    #                      }
    # json.dumps(animal_dictionary, default=str)
    return Response("Your data has been deleted!", mimetype='text/plain', status=200)


# get_animals()
# add_animal()
# edit_animal()
# delete_animal()

# turns debut mode turned on so we can see the werkzeug interface if there are errors
app.run(debug=True)

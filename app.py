from flask import Flask, request, Response
import json
# import traceback
import dbconnect
# entry point of flask server
app = Flask(__name__)


@app.get("/animals")
# gets all animals
def get_animals():
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute("SELECT name, id FROM animals")
    animals = cursor.fetchall()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    animals_json = json.dumps(animals, default=str)
    return Response(animals_json, mimetype='application/json', status=200)
    # for animal in animals:
    #     print(f"Name: {animal[0]} \nID: {animal[1]} \n")


@app.post("/animals")
def add_animal():
    animal_name: None
    # this saves the animal name that's input into postman in a variable
    animal_name = request.json['animalName']
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute("INSERT INTO animals(name) VALUES(?)", [animal_name, ])
    conn.commit()
    # do the thing and close conn/cursor immediately
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # don't need id here because it's auto'd
    # I commented this stuff out because we didn't need input from the user??
    # json.dumps(animal_name, default=str)
    # returns success message in text data with status 201 = created
    return Response("Your animal has been added!", mimetype='application/json', status=201)


@app.patch("/animals")
def edit_animal():
    # saves the animal name and id that's input into postman in variables
    animal_id = int(request.json['animalId'])
    animal_name = request.json['animalName']
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute(
        "UPDATE animals SET name = ? WHERE id = ?", [animal_name, animal_id])
    conn.commit()
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

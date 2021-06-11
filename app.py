from flask import Flask, request, Response
import json
# import traceback
import dbconnect
app = Flask(__name__)


@app.get("/animals")
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
    animal_name = request.json['animalName']
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute("INSERT INTO animals(name) VALUES(?)", [animal_name, ])
    conn.commit()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    animal_json = json.dumps(animal_name, default=str)
    return Response(animal_json, mimetype='application/json', status=200)
    # print("New animal added!")


@app.patch("/animals")
def edit_animal():
    animal_id = int(request.json['animalId'])
    animal_name = request.json['animalName']
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute(
        "UPDATE animals SET name = ? WHERE id = ?", [animal_name, animal_id])
    conn.commit()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    animal_dictionary = {"animalName": "Asian Elephant",
                         "animalId": "18"
                         }
    json.dumps(animal_dictionary, default=str)
    return Response("Your data has been updated!", mimetype='text/plain', status=201)
    # print("Animal updated!")


@app.delete("/animals")
def delete_animal():
    # animal_id = int(request.json['animalId'])
    animal_name = request.json['animalName']
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute("DELETE FROM animals WHERE name = 'snake'")
    conn.commit()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    print("Animal deleted!")


# get_animals()
# add_animal()
# edit_animal()
# delete_animal()


app.run(debug=True)

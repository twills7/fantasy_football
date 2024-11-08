# app.py
from markupsafe import Markup
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect("data_management/player_base.db")
    conn.row_factory = sqlite3.Row  # This allows us to get rows as dictionaries
    return conn

# Route to retrieve data from the database
@app.route("/players", methods=["GET"])
def get_players():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    conn.close()
    return jsonify([dict(player) for player in players])  # Return data as JSON

# Route to add new data to the database
@app.route("/add_player", methods=["POST"])
def add_player():
    new_player = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, name, price_2021, price_2022, price_2023, price_2024, points_2024, team, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (new_player["id"], new_player["name"], new_player["price_2021"], new_player["price_2022"], new_player["price_2023"], new_player["price_2024"], new_player["points_2024"], new_player["team"], new_player["position"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Player added successfully!"}), 201

# Route to update data in the database
if __name__ == "__main__":
    app.run(debug=True)
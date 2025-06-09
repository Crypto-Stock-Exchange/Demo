import psycopg2
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from config import read_secret
    
liststocks_bp = Blueprint("liststocks", __name__)
CORS(liststocks_bp, origins=["http://localhost:8080"])

DB_NAME = read_secret("POSTGRES_DB")
DB_USER = read_secret("POSTGRES_USER")
DB_PASS = read_secret("POSTGRES_PASSWORD")
DB_HOST = "postgres"  # Docker service name
DB_PORT = "5432"

def makeconn():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

@liststocks_bp.route("/stocks", methods=["GET"])
def list_stocks():
    conn = makeconn()
    cursor = conn.cursor()

    # Kérdezze le a részvények nevét és árát
    cursor.execute("SELECT name, price, total_bet_amount, id FROM stocks")
    stocks = cursor.fetchall()

    # Válasz JSON formátumban
    stock_list = [{"name": stock[0], "price": stock[1], "total_bet_amount": stock[2], "id": stock[3]} for stock in stocks]

    cursor.close()
    conn.close()

    return jsonify(stock_list)

@liststocks_bp.route("/stocks/<int:stock_id>", methods=["GET"])
def get_stock_details(stock_id):
    conn = makeconn()
    cursor = conn.cursor()

    # Lekérdezés egy adott részvényre
    cursor.execute("SELECT id, name, price, week_52_range, volume, market_cap, avgintervalum, avgtime, avgvolume, total_bet_amount, link FROM stocks WHERE id = %s", (stock_id,))
    stock = cursor.fetchone()

    cursor.close()
    conn.close()

    if stock:
        stock_data = {
            "id": stock[0],
            "name": stock[1],
            "price": stock[2],
            "week_52_range": stock[3],
            "volume": stock[4],
            "market_cap": stock[5],
            "avgintervalum": stock[6],
            "avgtime": stock[7],
            "avgvolume": stock[8],
            "total_bet_amount": stock[9],
            "link": stock[10],
        }
        return jsonify(stock_data)
    else:
        return jsonify({"error": "Részvény nem található"}), 404
    
@liststocks_bp.route("/stocks/<int:stock_id>/<string:time>", methods=["GET"])
def get_price_history(stock_id, time):
    VALID_COLUMNS = {"pricehistory24h", "pricehistory5d", "pricehistory1m", "pricehistory6m", "pricehistory1y", "pricehistory5y", "pricehistoryall"}
    if time not in VALID_COLUMNS:
        return jsonify({"error": "SQL inection"}), 400
    conn = makeconn()
    cursor = conn.cursor()

    # Thanks Norbert :D
    cursor.execute(f"SELECT {time} FROM stocks WHERE id = %s", (stock_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return jsonify(result[0])
    else: 
        return jsonify({"error": "Részvény nem található"}), 404

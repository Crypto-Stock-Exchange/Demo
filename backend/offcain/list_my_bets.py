from flask import Blueprint, jsonify
from flask_cors import CORS
import psycopg2
from config import read_secret

list_my_bets_bp = Blueprint("list_my_bets", __name__)
CORS(list_my_bets_bp, origins=["http://localhost:8080"])

def get_db_connection():
    conn = psycopg2.connect(
        dbname=read_secret("POSTGRES_DB"),
        user=read_secret("POSTGRES_USER"),
        password=read_secret("POSTGRES_PASSWORD"),
        host="postgres",
        port="5432"
    )
    return conn

@list_my_bets_bp.route('/bets/<string:user_address>', methods=['GET'])
def get_bets(user_address):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 
                b.id, b.user_address, b.bet_id, b.symbol, b.lower, b.upper, b.amount, 
                b.deadline, b.datenow, b.ownerfee, b.winamount,
                s.id AS stockid
            FROM bets b
            LEFT JOIN stocks s ON b.symbol = s.link
            WHERE LOWER(b.user_address) = LOWER(%s)
            ORDER BY b.datenow DESC
        """, (user_address,))
        rows = cursor.fetchall()

        if not rows:
            return jsonify([])

        bets = []
        for row in rows:
            bets.append({
                'id': row[0],
                'user_address': row[1],
                'bet_id': row[2],
                'symbol': row[3],
                'lower': float(row[4]),
                'upper': float(row[5]),
                'amount': float(row[6]),
                'deadline': row[7],
                'datenow': row[8],
                'ownerfee': float(row[9]),
                'winamount': float(row[10]),
                'stockid': row[11]
            })
        return jsonify(bets)

    except Exception as e:
        print("Database error:", e)
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()

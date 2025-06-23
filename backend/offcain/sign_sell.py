import time
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import keccak
from eth_abi.packed import encode_packed
from config import read_secret
import psycopg2
from decimal import Decimal
from web3 import Web3

# Flask blueprint
URL = read_secret("URL")
sellbets_bp = Blueprint("sign_sell", __name__)
CORS(sellbets_bp, origins=[URL])

PRIVATE_KEY = read_secret("PRIVATE_KEY")
OWNER = read_secret("OWNER")
if not PRIVATE_KEY or not OWNER:
    raise Exception("Missing PRIVATE_KEY or OWNER in /run/secrets/")

account = Account.from_key(PRIVATE_KEY)

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

def divide_the_money_together(penalty_fee, now, symbol):
    try:
        conn = makeconn()
        cursor = conn.cursor()

        cursor.execute("SELECT price, avgintervalum, avgtime, avgvolume FROM stocks WHERE link = %s", (symbol,))
        result = cursor.fetchone()
        if not result:
            return Decimal(0)
        
        current_price, avg_interval, avg_time, avg_volume = map(float, result)

        cursor.execute(
            "SELECT id, lower, upper, amount, deadline, datenow, winamount FROM bets WHERE symbol = %s",
            (symbol,)
        )
        bets = cursor.fetchall()

        winners = []
        total_score = 0.0

        for bet in bets:
            id, lower, upper, amount_bet, deadline, datenow, winamount = bet
            
            if now > deadline:
                continue

            lower = float(lower)
            upper = float(upper)
            amount_bet = float(amount_bet)
            winamount = float(winamount)
            interval = upper - lower
            time_span = deadline - datenow

            if lower <= current_price <= upper:
                score = (
                    (avg_interval / interval) +
                    (time_span / avg_time) +
                    (amount_bet / avg_volume)
                )
                winners.append({
                    "id": id,
                    "score": score,
                    "winamount": winamount
                })
                total_score += score

        if total_score == 0.0:
            
            conn.rollback()
            return Decimal(0)
        else:
            for winner in winners:
                reward_share = winner["score"] / total_score
                reward = Decimal(str(reward_share)) * Decimal(str(penalty_fee))
                new_winamount = Decimal(str(winner["winamount"])) + reward
                cursor.execute(
                    "UPDATE bets SET winamount = %s WHERE id = %s",
                    (new_winamount, winner["id"])
                )
            conn.commit()
            return penalty_fee

    except Exception as e:
        print(f"Error in divide_the_money_together: {e}")
        return Decimal(0)

    finally:
        cursor.close()
        conn.close()

@sellbets_bp.route("/sell", methods=["POST"])
def sell_nft():
    try:
        data = request.json
        tokenId = int(data["tokenId"])
        signature = data["signature"]
        message = data["message"]


        conn = makeconn()
        cursor = conn.cursor()

        cursor.execute("SELECT amount, winamount, deadline, datenow, symbol, user_address FROM bets WHERE bet_id = %s", (tokenId,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"error": "Bet not found"}), 404

        amount = row[0]
        winamount = row[1]
        deadline = row[2]
        datenow = row[3]
        symbol = row[4]
        user_address = row[5]

        msg = encode_defunct(text=message)
        recovered = Web3().eth.account.recover_message(msg, signature=signature)

        if (user_address.lower() != recovered.lower()):
            return jsonify({"Hacker"}), 500
        
        price = amount + Decimal(winamount)
        now = Decimal(time.time())
        total_duration = abs(deadline - datenow)

        if now < deadline and total_duration > 0:
            penalty_fee = Decimal(0)
            time_elapsed = now - datenow
            ratio = time_elapsed / total_duration
            penalty_fee_percent = Decimal("0.5") * (1 - ratio)
            penalty_fee = price * penalty_fee_percent
            price -= divide_the_money_together(penalty_fee, now, symbol)

        price_wei = int(price * Decimal(10**18)) 

        ownerfee = price_wei // 100
        price_wei -= ownerfee

        buyer_bytes = bytes.fromhex(user_address[2:])
        owner_bytes = bytes.fromhex(OWNER[2:])

        message_backend = keccak(
            encode_packed(
                ['uint256', 'address', 'uint256', 'address', 'uint256'],
                [tokenId, buyer_bytes, price_wei, owner_bytes, ownerfee]
            )
        )

        eth_message = encode_defunct(message_backend)
        signed_message = Account.sign_message(eth_message, private_key=PRIVATE_KEY)
        delete_bet(tokenId)

        return jsonify({
            "signature": signed_message.signature.hex(),
            "owner": OWNER,
            "ownerfee": str(ownerfee),
            "price": str(price_wei) 
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def delete_bet(tokenId):
    try:
        conn = makeconn()
        cursor = conn.cursor()

        cursor.execute("SELECT lower, upper, amount, deadline, datenow, symbol FROM bets WHERE bet_id = %s", (tokenId,))
        bet = cursor.fetchone()
        if not bet:
            return jsonify({"error": "Bet not found"}), 404

        lower, upper, amount, deadline, datenow, symbol = bet
        interval = abs(float(upper) - float(lower))
        time_span = abs(float(deadline) - float(datenow))
        volume = float(amount)
        cursor.execute("""
        SELECT 1
        FROM bets
        WHERE symbol = %s
        """, (symbol,))
        prev_count = len(cursor.fetchall())


        cursor.execute("SELECT avgintervalum, avgtime, avgvolume, total_bet_amount FROM stocks WHERE link = %s", (symbol,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Stock not found"}), 404

        prev_avg_interval, prev_avg_time, prev_avg_volume, prev_total_volume = map(
            lambda x: float(x or 0), result
        )

        new_count = max(prev_count - 1, 1) 

        avg_interval = ((prev_avg_interval * prev_count) - interval) / new_count
        avg_time = ((prev_avg_time * prev_count) - time_span) / new_count
        avg_volume = ((prev_avg_volume * prev_count) - volume) / new_count
        total_volume = prev_total_volume - volume

        cursor.execute("""
            UPDATE stocks 
            SET avgintervalum = %s,
                avgtime = %s,
                avgvolume = %s,
                total_bet_amount = %s
            WHERE link = %s
        """, (avg_interval, avg_time, avg_volume, total_volume, symbol))

        cursor.execute("DELETE FROM bets WHERE bet_id = %s", (tokenId,))
        conn.commit()
        return jsonify({"success": True}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
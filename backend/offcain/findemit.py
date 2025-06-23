from flask import Blueprint, request, jsonify
from flask_cors import CORS
from web3 import Web3
import json
from web3._utils.events import get_event_data
import psycopg2.extras
import psycopg2
from config import read_secret
from decimal import Decimal


URL = read_secret("URL")
findemit_bp = Blueprint("findemit", __name__)
CORS(findemit_bp, origins=[URL])

SEPOLIA_RPC = read_secret("SEPOLIA_RPC_URL")
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))

# Szerződés címe
contract_address = "0x58201ECd3f23b6F8d6caf34d7bd11f00a46138d1"

# ABI részlet csak az eseményre
abi = json.loads("""[
    {
        "anonymous": false,
        "inputs": [
            { "indexed": true, "internalType": "address", "name": "user", "type": "address" },
            { "indexed": true, "internalType": "uint256", "name": "id", "type": "uint256" },
            { "indexed": false, "internalType": "string", "name": "symbol", "type": "string" },
            { "indexed": false, "internalType": "uint256", "name": "lower", "type": "uint256" },
            { "indexed": false, "internalType": "uint256", "name": "upper", "type": "uint256" },
            { "indexed": false, "internalType": "uint256", "name": "amount", "type": "uint256" },
            { "indexed": false, "internalType": "uint256", "name": "deadline", "type": "uint256" },
            { "indexed": false, "internalType": "uint256", "name": "datenow", "type": "uint256" },
            { "indexed": false, "internalType": "uint256", "name": "ownerfee", "type": "uint256" }
        ],
        "name": "BetCreated",
        "type": "event"
    }
]""")


def save_bet_to_db(last_event):
    conn = psycopg2.connect(
        dbname=read_secret("POSTGRES_DB"),
        user=read_secret("POSTGRES_USER"),
        password=read_secret("POSTGRES_PASSWORD"),
        host="postgres",
        port="5432"
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # 1. Feldolgozás
    user = last_event["args"]["user"]
    bet_id = last_event["args"]["id"]
    symbol = last_event["args"]["symbol"]

    # Feltehetően: lower/upper ➝ 2 tizedesjegyű, amount/fee ➝ 18 tizedesjegyű token
    lower = Decimal(last_event["args"]["lower"]) / Decimal("100")
    upper = Decimal(last_event["args"]["upper"]) / Decimal("100")
    amount = Decimal(last_event["args"]["amount"]) / Decimal("1e18")
    deadline = last_event["args"]["deadline"]
    datenow = last_event["args"]["datenow"]
    ownerfee = Decimal(last_event["args"]["ownerfee"]) / Decimal("1e18")

    duration_seconds = max(deadline - datenow, 1)  # hogy ne oszszunk nullával
    duration_minutes = Decimal(duration_seconds) / Decimal(60)
    lossfee = amount / duration_minutes

    # 2. Bet beszúrása
    insert_bet_query = """
        INSERT INTO bets (
            user_address, bet_id, symbol, lower, upper,
            amount, deadline, datenow, ownerfee, winamount, lossfee
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_bet_query, (
        user, bet_id, symbol, lower, upper,
        amount, deadline, datenow, ownerfee, 0, lossfee
    ))

    # 3. Lekérjük a meglévő beteket
    cursor.execute("""
        SELECT 1
        FROM bets
        WHERE symbol = %s
    """, (symbol,))
    new_count = len(cursor.fetchall())
    prev_count = new_count -1

    cursor.execute("""
        SELECT avgintervalum, avgtime, avgvolume, total_bet_amount
        FROM stocks
        WHERE link = %s
    """, (symbol,))
    result = cursor.fetchone()

    # Alapértékek ha nincs adat (ne forduljon hiba)
    prev_avg_interval = Decimal(result["avgintervalum"] or 0)
    prev_avg_time = Decimal(result["avgtime"] or 0)
    prev_avg_volume = Decimal(result["avgvolume"] or 0)
    prev_total_volume = Decimal(result["total_bet_amount"] or 0)

    # 4. Új adatok az új bet alapján
    new_interval = abs(upper - lower)
    new_time = abs(Decimal(datenow) - Decimal(deadline))
    new_volume = amount


    # Új átlagok számítása
    avg_interval = ((prev_avg_interval * prev_count) + new_interval) / new_count
    avg_time = ((prev_avg_time * prev_count) + new_time) / new_count
    avg_volume = ((prev_avg_volume * prev_count) + new_volume) / new_count
    total_volume = prev_total_volume + new_volume

    # 5. Frissítés stocks táblába
    cursor.execute("""
        UPDATE stocks
        SET avgintervalum = %s,
            avgtime = %s,
            avgvolume = %s,
            total_bet_amount = %s
        WHERE link = %s
    """, (avg_interval, avg_time, avg_volume, total_volume, symbol))

    # 6. Mentés és bezárás
    conn.commit()
    cursor.close()
    conn.close()



event_abi = abi[0]
@findemit_bp.route('/emit', methods=['POST'])
def get_user_last_betcreated():
    data = request.json
    user_address = data.get("user_address")
    if not user_address:
        return jsonify({"error": "user_address is required"}), 400

    user_address = Web3.to_checksum_address(user_address)

    from_block = 0
    to_block = w3.eth.block_number

    user_topic = "0x" + "0" * 24 + user_address.lower().replace("0x", "")

    # Event signature topic
    event_signature_text = "BetCreated(address,uint256,string,uint256,uint256,uint256,uint256,uint256,uint256)"
    event_signature_hash = "0x" + Web3.keccak(text=event_signature_text).hex()

    filter_params = {
        "fromBlock": from_block,
        "toBlock": to_block,
        "address": contract_address,
         "topics": [
             event_signature_hash,
             user_topic
         ]
    }

    logs = w3.eth.get_logs(filter_params)

    events = []
    for log in logs:
        ev = get_event_data(w3.codec, event_abi, log)
        events.append(ev)

    if not events:
        return jsonify({"message": "No events found for user"}), 404

    # Az utolsó esemény a lista végén van (időrendben)
    last_event = events[-1]

    save_bet_to_db(last_event)

    return jsonify("Works"), 200
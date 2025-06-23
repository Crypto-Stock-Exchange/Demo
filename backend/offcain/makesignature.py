from flask import Blueprint, request, jsonify
from flask_cors import CORS
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import keccak
from eth_abi.packed import encode_packed
from config import read_secret

# Flask blueprint
URL = read_secret("URL")
makesignature_bp = Blueprint("makesignature", __name__)
CORS(makesignature_bp, origins=[URL])

PRIVATE_KEY = read_secret("PRIVATE_KEY")
OWNER = read_secret("OWNER")
if not PRIVATE_KEY or not OWNER:
    raise Exception("Missing PRIVATE_KEY_HEX or OWNER in /run/secrets/")


account = Account.from_key(PRIVATE_KEY)

@makesignature_bp.route('/sign', methods=['POST'])
def sign_data():

    data = request.json

    required_keys = ["sender", "amountInWei", "deadline"]
    if not all(k in data for k in required_keys):
        return jsonify({"error": "Missing required fields"}), 400

    sender = data["sender"]
    amountInWei = int(data["amountInWei"])
    deadline = int(data["deadline"])

    ownerfee = amountInWei // 100  # 1%

    senderstring = str(sender)
    senderstring = senderstring.lower()
    OWNERstring = str(OWNER)
    OWNERstring = OWNERstring.lower()
    sender_bytes = bytes.fromhex(senderstring[2:])   # levágja "0x"-et
    owner_bytes = bytes.fromhex(OWNERstring[2:])

    try:


        message = keccak(
            encode_packed(
                ['address', 'address', 'uint256', 'uint256'],
                [sender_bytes, owner_bytes, ownerfee, deadline]
            )
        )

        eth_message = encode_defunct(message)


        signed_message = Account.sign_message(eth_message, private_key=PRIVATE_KEY)

        return jsonify({
            "signature": signed_message.signature.hex(),
            "owner": OWNER,
            "ownerfee": str(ownerfee),
            "signer": account.address
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

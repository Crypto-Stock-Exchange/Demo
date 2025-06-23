from flask import Flask
from flask_cors import CORS
from liststocks import liststocks_bp
from offcain.makesignature import makesignature_bp
from offcain.findemit import findemit_bp
from offcain.list_my_bets import list_my_bets_bp
from offcain.sign_sell import sellbets_bp
from config import read_secret
#from filldata import populate_data


app = Flask(__name__)
URL = read_secret("URL")
CORS(app, origins=[URL, URL])
app.register_blueprint(liststocks_bp, url_prefix="/api")
app.register_blueprint(makesignature_bp, url_prefix="/api")
app.register_blueprint(findemit_bp, url_prefix="/api") 
app.register_blueprint(list_my_bets_bp, url_prefix="/api")
app.register_blueprint(sellbets_bp, url_prefix="/api")
@app.route("/")
def hello():
    # tickers = ["AAPL",  # Apple
    #             "NVDA",  # Nvidia
    #             "MSFT",  # Microsoft
    #             "GOOGL", # Alphabet (Google)
    #             "AMZN",  # Amazon
    #             "AMD",   # Advanced Micro Devices
    #             "TSLA",  # Tesla
    #             "INTC",  # Intel
    #             "CRM",   # Salesforce
    #             "ORCL",  # Oracle
    #             ]
    # for ticker in tickers:  
    #     populate_data(ticker)
    return "Data has been populated!"

if __name__ == "__main__":
    #populate_data()  # meghívja a függvényt, hogy adatokat töltse be
    app.run(host="0.0.0.0", port=5000)

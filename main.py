import sqlite3
from flask import Flask, jsonify, request
from cryptocurrency import *



def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        #conn.execute('''DROP TABLE addressLists''')
        conn.execute('''
            CREATE TABLE addressLists (
                id INTEGER PRIMARY KEY,
                coin TEXT NOT NULL,
                address TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("AddressLists table created successfully")
    except:
        print("AddressLists table creation failed - Maybe table")
    finally:
        conn.close()

def insert_coin(coin):
    coin = coin['coin']
    address = ""
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        if coin == "BTC" or coin == "btc":
            insert_fields = """INSERT INTO addressLists(coin, address) VALUES(?, ?)"""
            conn.execute(insert_fields, (coin.upper(), getBTC()))
            conn.commit()
            address = getBTC()
        elif coin == "ETH" or coin == "eth":
            insert_fields = """INSERT INTO addressLists(coin, address) VALUES(?, ?)"""
            conn.execute(insert_fields, (coin.upper(), getETH()))
            conn.commit()
            address = getETH()
        else:
            print("Enter the correct coin e.g: BTC, ETH")
    except:
        conn().rollback()

    finally:
        conn.close()

    return ("Address is Generated coin: {}, address: {},".format(coin.upper(),address))

def get_coins():
    coins = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM addressLists")
        rows = cur.fetchall()
        # # convert row objects to dictionary
        for i in rows:
            coin = {}
            coin["id"] = i["id"]
            coin["coin"] = i["coin"]
            coin["address"] = i["address"]
            coins.append(coin)
    except:
        coins = []
    return coins

def get_coin_by_id(coin_id):
    coin = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM addressLists WHERE id = ?", (coin_id,))
        row = cur.fetchone()
        # convert row objects to dictionary
        coin["id"] = row["id"]
        coin["coin"] = row["coin"]
        coin["address"] = row["address"]
    except:
        coin = {}
    return coin



#create table
create_db_table()


app = Flask(__name__)

@app.route('/GenerateAddress',  methods = ['POST'])
def getGenerateAddress():
    coin = request.get_json()
    return jsonify(insert_coin(coin))


@app.route("/ListAddress", methods = ['GET'])
def getListAddress():
    return jsonify(get_coins())

@app.route("/RetrieveAddress/<int:coin_id>", methods = ['GET'])
def RetrieveAddress(coin_id):
    return jsonify(get_coin_by_id(coin_id))

if __name__ == "__main__":
    app.run(debug=True)
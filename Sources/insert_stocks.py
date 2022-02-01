import sqlite3, config
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('/Users/Gokay9U/Desktop/Stock-Bot/app.db')
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
               SELECT symbol, name FROM stock
               """)

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows]

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.URL)
assets = api.list_assets() 

#crontab can be useable for linux to schedule the DB update
for asset in assets:
    try: 
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES(?,?,?)", (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e) 
   
connection.commit() 
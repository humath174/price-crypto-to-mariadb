import requests
import mysql.connector
import time

# Liste des cryptos à suivre (IDs CoinGecko)
crypto_ids = ["bitcoin", "solana", "uniswap", "polkadot", "dogecoin", "cardano", "avalanche"]

# Fonction pour récupérer les prix de plusieurs cryptos
def get_crypto_prices(crypto_ids):
    ids = ','.join(crypto_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    print("API Response:", data)  # Affiche la réponse pour le débogage
    return data

# Connexion à la base de données MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="10.0.0.12",
        port=3306,
        user="grafana",
        password="grafana",
        database="grafana"
    )

# Insérer les prix dans la base de données
def store_crypto_prices_in_mysql(prices):
    db = connect_to_db()
    cursor = db.cursor()
    for crypto_id, data in prices.items():
        # Vérifie si le prix USD est disponible pour cette cryptomonnaie
        if 'usd' in data:
            price = data['usd']
            cursor.execute("""
                INSERT INTO crypto_prices (crypto, price, timestamp) 
                VALUES (%s, %s, UTC_TIMESTAMP())
            """, (crypto_id, price))
            print(f"Stored {crypto_id} price: {price} USD")
        else:
            print(f"No USD price data available for {crypto_id}")
    db.commit()
    cursor.close()
    db.close()

# Boucle pour récupérer et enregistrer les données toutes les X minutes
while True:
    prices = get_crypto_prices(crypto_ids)
    store_crypto_prices_in_mysql(prices)
    time.sleep(15)  # 5 minutes

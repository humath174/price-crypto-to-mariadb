	# Utiliser une image Python de base
FROM python:3.9-slim

# Installer les dépendances
RUN pip install requests mysql-connector-python

# Copier le script dans le conteneur
COPY crypto_collector.py /app/crypto_collector.py

# Définir le répertoire de travail
WORKDIR /app

# Lancer le script
CMD ["python", "crypto_collector.py"]

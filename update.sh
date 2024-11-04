#!/bin/bash

echo "[+] pulling frontend image from dockerhub"
docker pull peetahdarius/jenkins-test-frontend:$1 || { echo "Failed to pull frontend image"; exit 1; }

echo "[+] pulling backend image from dockerhub"
docker pull peetahdarius/jenkins-test-backend:$1 || { echo "Failed to pull backend image"; exit 1; }

echo "[+] running docker-compose down"
docker-compose down || { echo "Failed to bring down docker-compose"; exit 1; }

echo "[+] cleaning docker builder cache"
docker builder prune --force || { echo "Failed to prune docker builder cache"; exit 1; }

echo "[+] starting the new containers with the updated images"
docker-compose up -d || { echo "Failed to start docker-compose"; exit 1; }

echo "[+] cleaning up unused resources"
docker system prune -f || { echo "Failed to prune docker system"; exit 1; }


update_database(){
    # Load environment variables from .env file
    set -a
    source .env || { echo "Failed to load .env file"; exit 1; }
    set +a

    # Ensure required environment variables are set
    if [[ -z "$DATABASE_PASSWORD" || -z "$DATABASE_NAME" || -z "$DATABASE_USER" || -z "$DATABASE_HOST" || -z "$DATABASE_PORT" ]]; then
        echo "One or more required database environment variables are missing."
        exit 1
    fi

    # SQL command to update the table
    SQL="UPDATE api_version SET frontend_version = $1 WHERE custom_id = 1;"
    SQL1="UPDATE api_version SET backend_version = $1 WHERE custom_id = 1;"

    # Use the environment variables to connect and run SQL
    echo "[+] updating database"
    PGPASSWORD="$DATABASE_PASSWORD" psql -d "$DATABASE_NAME" -U "$DATABASE_USER" -h "$DATABASE_HOST" -p "$DATABASE_PORT" -c "$SQL" || { echo "Database update failed"; exit 1; }
    PGPASSWORD="$DATABASE_PASSWORD" psql -d "$DATABASE_NAME" -U "$DATABASE_USER" -h "$DATABASE_HOST" -p "$DATABASE_PORT" -c "$SQL1" || { echo "Database update failed"; exit 1; }
}

update_database

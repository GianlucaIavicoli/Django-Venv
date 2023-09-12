#!/bin/bash


setup_mysql() {
    echo "Starting MySQL docker...."
    
    containerId=$(docker run -d --name $CONTAINER_NAME -p $MYSQL_HOST:$MYSQL_PORT:3306 -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD mysql:latest)
    
    sleep 10
    echo "MySQL docker started with id: $containerId"
    
    # Check if the MySQL container is running
    if docker ps | grep "$CONTAINER_NAME" &>/dev/null; then
        
        QUERIES=("CREATE DATABASE $CONTAINER_NAME;"
            "CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';"
            "GRANT ALL PRIVILEGES ON $CONTAINER_NAME.* TO '$MYSQL_USER'@'localhost';"
        "FLUSH PRIVILEGES;")
        
        for query in "${QUERIES[@]}";
        do
            docker exec -it $CONTAINER_NAME mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "$query"
        done
        
        echo "MySQL user -> '$MYSQL_USER' created succesfully."
        echo "MySQL database -> '$CONTAINER_NAME' created succesfully."
        
    else
        exit "MySQL container is not running."
    fi
}


setup_postgresql() {
    echo "Starting PostgreSQL Docker container...."
    
    containerId=$(docker run -d --name $CONTAINER_NAME -p $POSTGRESQL_HOST:$POSTGRESQL_PORT:5432 -e POSTGRES_PASSWORD=$POSTGRESQL_PASSWORD postgres:latest)
    
    sleep 10
    echo "PostgreSQL Docker container started with id: $containerId"
    
    # Check if the PostgreSQL container is running
    if docker ps | grep "$CONTAINER_NAME" &>/dev/null; then
        
        QUERIES=("CREATE DATABASE $CONTAINER_NAME;"
            "CREATE USER $POSTGRESQL_USER WITH ENCRYPTED PASSWORD '$POSTGRESQL_PASSWORD';"
            "ALTER ROLE $POSTGRESQL_USER SET client_encoding TO 'utf8';"
            "ALTER ROLE $POSTGRESQL_USER SET default_transaction_isolation TO 'read committed';"
            "ALTER ROLE $POSTGRESQL_USER SET timezone TO 'UTC';"
            "GRANT CREATE, TEMP, CONNECT ON DATABASE $CONTAINER_NAME TO $POSTGRESQL_USER;"
        )
        
        
        for query in "${QUERIES[@]}"; do
            docker exec -it $CONTAINER_NAME psql -U postgres -c "$query"
        done
        
        # Grant for public
        docker exec -it $CONTAINER_NAME psql -U postgres $CONTAINER_NAME -c "GRANT ALL ON SCHEMA public TO $POSTGRESQL_USER;"
        
        echo "PostgreSQL user -> '$POSTGRESQL_USER' created successfully."
        echo "PostgreSQL database -> '$CONTAINER_NAME' created successfully."
        
    else
        echo "PostgreSQL container is not running."
        exit 1
    fi
}


setup_cassandra() {
    exit 1
}

setup_scylla() {
    exit 1
}


check_docker() {
    if command -v docker &>/dev/null; then
        if [ "$DATABASE_TYPE" == 'mysql' ]; then
            setup_mysql
            
            elif [ "$DATABASE_TYPE" == 'postgre' ]; then
            setup_postgresql
            
            elif [ "$DATABASE_TYPE" == 'cassandra' ]; then
            setup_cassandra
            
            elif [ "$DATABASE_TYPE" == 'scylla' ]; then
            setup_scylla
        fi
    else
        echo "Docker is not installed."
        exit 1
    fi
}


check_docker


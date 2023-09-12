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


setup_postgres() {
    exit 1
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
            
            elif [ "$DATABASE_TYPE" == 'postgres' ]; then
            setup_postgres
            
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


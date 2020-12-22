import config
import os

database = ""
webserver = ""

if config.database == 0:
    database = """
            image: postgres
            restart: always
            volumes:
                - ./database_mount:/var/lib/postgresql/data
            environment:
                POSTGRES_PASSWORD: """ + config.database_password
elif config.database == 1:
    database = """
            image: mysql
            volumes:
                - ./database_mount:/var/lib/mysql
            command: --default-authentication-plugin=mysql_native_password --innodb_use_native_aio=0
            environment:
                MYSQL_ROOT_PASSWORD: """ + config.database_password
elif config.database == 2:
    database = """
            image: mongo
            restart: always
            volumes:
                - ./database_mount:/data/db
            environment:
                MONGO_INITDB_ROOT_USERNAME: root
                MONGO_INITDB_ROOT_PASSWORD: """ + config.database_password
else: 
    exit

if config.webserver == 0:
    webserver = """
            image: node
            volumes: 
                - ./webserver_mount:/usr/app/
            ports: 
                - "8888:3000" """
elif config.webserver == 1:
    webserver = """
            image: php:apache
            volumes: 
                - ./webserver_mount:/var/www/html
            ports:
                - "8888:80" """
elif config.webserver == 2:
    webserver = """
            image: python 
            volumes:
                - ./webserver_mount:/
            ports:
                - "8888:80" """
else: 
    exit

file_docker_compose = """version: '3.6'
services: 
    db: 
        """ + database+ """
    webserver:
        """ + webserver+ """
    adminer:
            image: adminer
            ports: 
                - 8080:8080
"""
f = open("docker-compose.yml", "w")
f.write(file_docker_compose)
f.close()

os.system("docker-compose up")
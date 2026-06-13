## load in the testdata git submodule
`git submodule update`

## startup the db container
`docker compose up -d`

## init the database with the testdata

`docker exec -it mysql-test-db bash`

`cd /userdata && mysql --password=db --commands < employees.sql`

This will than load in the testdata needed

## Connect

* host: localhost
* port: 3306
* user: root
* password: db
* database: employees
* driver: mysql

Connection-String: ``
# Challenge: ETL (C#, MySQL)

This program was built with the purpose of extracting the data from .txt files using the C# programming language and inserting them into a MySQL database, ensuring data cleansing.

### ETL - C#

This ETL process get all the .txt files inside de folder ```C:/arquivosProva/``` , do the necessary transformations and insert them into a MySQL Database for future analysis.

### Database - MySQL

The SQL script to create the database and also the table for the data to be insert can be checked on the ```create_database_and_table.sql``` file.

### Analysis - Python

Two scripts were created in order to be able to analyse some information about the data.

The first one, ```charts_unique_users.py```, create two charts where the number of daily and monthly unique users can be checked.

The second one, ```charts_retention.py```, create two charts where the one day period retention and three days period retention can be checked.
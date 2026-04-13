from flask import Flask
import mysql.connector


mysql.connect = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shweta@123",
    database="product_management"
)


mysql_cursor = mysql.connect.cursor()   
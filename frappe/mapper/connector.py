import psycopg2
import sys
 
def connector_postgres():
	conn_string = "host='172.18.0.2' dbname='Product' user='odoo' password='odoo'"
	# connection = psycopg2.connect(database="Product", user="odoo", password="odoo", host="localhost", port=5432)
 
	print "Connecting to database\n	->%s" % (conn_string)
 
	conn = psycopg2.connect(conn_string)
 
	cursor = conn.cursor()
	print "Connected!\n"
 
# if __name__ == "__main__":
# 	main()

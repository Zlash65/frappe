import psycopg2
import sys
# import inspect

# @frappe.whitelist()
def main():
	conn_string = "host='172.18.0.2' dbname='Product' user='odoo' password='odoo'"
	# connection = psycopg2.connect(database="Product", user="odoo", password="odoo", host="localhost", port=5432)
	print "Connecting to database\n	->%s" % (conn_string)
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	# print "Connected!\n"

	l = []
	k = []
	cursor.execute("SELECT commercial_company_name FROM res_partner WHERE supplier=True AND is_company=True")
	column_names = [row[0] for row in cursor.description]
	print column_names
	records = cursor.fetchall()

	print len(records)
	company_name = []
	for x in records:
		company_name.append(x)
	print company_name
	# print company_name
	# print inspect.getfile(inspect.currentframe())

	# for x in company_name:
	# 	print x
	# 	print '-' * 20
 
if __name__ == "__main__":
	main()

import MySQLdb

def main():
	db = MySQLdb.connect(host="localhost", user="root", passwd="root")
	cur = db.cursor()

	# cur.execute("SELECT * FROM tabProgram")
	cur.execute('SHOW databases')
	databases = cur.fetchall()
	# print databases
	for row in databases:
		# print row[0]
		db = MySQLdb.connect(host="localhost", user="root", passwd="root", db=row[0])
		cur = db.cursor()
		cur.execute('SHOW tables')
		print cur.fetchall()
		print '-' * 50

if __name__ == "__main__":
	main()
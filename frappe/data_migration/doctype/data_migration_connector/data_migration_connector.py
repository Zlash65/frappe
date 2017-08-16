# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import psycopg2

class DataMigrationConnector(Document):
	def connect(self):
		self.connection = PostGresConnection(self.as_dict())

	def get_objects(self, object_type, condition=None, selection="*"):
		return self.connection.get_objects(object_type, condition, selection)

	def get_join_objects(self, object_type, join_type, primary_key):
		return self.connection.get_join_objects(object_type, join_type, primary_key)

class PostGresConnection(object):
	def __init__(self, properties):
		self.__dict__.update(properties)
		self._connector = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(self.hostname,
				self.database_name, self.username, self.password))
		self.cursor = self._connector.cursor()

	def get_objects(self, object_type, condition, selection):
		if not condition:
			condition = ''
		else:
			condition = ' WHERE ' + condition
		self.cursor.execute('SELECT {0} FROM {1}{2}'.format(selection, object_type, condition))
		raw_data = self.cursor.fetchall()
		data = []
		for r in raw_data:
			row_dict = frappe._dict({})
			for i in range(len(r)):
				row_dict[self.cursor.description[i][0]] = r[i]
			data.append(row_dict)

		return data

	def get_join_objects(self, object_type, join_type, primary_key):
		condition = str(object_type) + ".id=" + str(join_type[0]) + ".id AND " + str(object_type) + ".id=" + str(primary_key)
		obj_type = str(object_type) + ", " + str(join_type[0])
		selection = str(join_type[0]) + "." + str(join_type[2])

		return self.get_objects(obj_type, condition, selection)
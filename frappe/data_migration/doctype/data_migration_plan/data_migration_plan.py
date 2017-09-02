# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
from frappe import _

class DataMigrationPlan(Document):
	def migrate(self):
		self.source_connector = frappe.get_doc('Data Migration Connector', self.source_connector)
		self.source_connector.connect()

		for x in self.apps:
			# Can be used to bundle together mappings
			app = frappe.get_doc('Data Migration App', x.app)

			for d in app.mappings:
				# iterating through each mappings
				self.mapping = frappe.get_doc('Data Migration Mapping', d.mapping)
				data = self.source_connector.get_objects(self.mapping.source_objectname, self.mapping.condition, "*")
				self.make_custom_fields(self.mapping.target_doctype) # Creating a custom field for primary key

				# pre process
				if self.mapping.pre_process:
					exec self.mapping.pre_process in locals()

				for i, self.source in enumerate(data):
					# Fetchnig the appropriate doctype
					target = self.fetch_doctype()
					target.set('migration_key', self.source.get('id')) # Setting migration key

					self.store_mapped_data(target) # fetching data and storing it appropriately

					frappe.publish_progress(float(i)*100/len(data),
						title = _('Migrating {0}').format(target.doctype), doctype=self.doctype, docname=self.name)


				frappe.publish_progress(100,
					title = _('Migrating {0}').format(target.doctype), doctype=self.doctype, docname=self.name)

	def store_mapped_data(self, target):
		""" mapping source field to target field """
		# Iterating through each field to map
		for field in self.mapping.mapping_details:
			source_field = field.source_fieldname

			# If source field contains a dot linkage, then its a foreign key relation
			if '.' in  source_field:
				arr = source_field.split('.')
				join_data = self.source_connector.get_join_objects(self.mapping.source_objectname, field, self.source.get('id'))

				if len(join_data) > 1:
					join_data = join_data[0:1] # ManyToOne mapping, taking the first value only

				target.set(field.target_fieldname, join_data[0][arr[1]])
			else:
				# Else its a simple column to column mapping
				target.set(field.target_fieldname, frappe.as_unicode(self.source.get(source_field)))

		# post process
		if self.mapping.post_process:
			exec self.mapping.post_process in locals()

		try:
			target.save()
		except frappe.DuplicateEntryError:
			target.save()


	def make_custom_fields(self, dt):
		""" Adding custom field for primary key """
		field = frappe.db.get_value("Custom Field", {"dt": dt, "fieldname": 'migration_key'})
		if not field:
			create_custom_field(dt, {
				'label': 'Migration Key',
				'fieldname': 'migration_key',
				'fieldtype': 'Data',
				'hidden': 1,
				'read_only': 1,
				'unique': 1,
			})

	def fetch_doctype(self):
		""" Returns correct doctype type - new or existing """
		flag = frappe.db.get_value(self.mapping.target_doctype, {'migration_key': self.source.get('id')})

		if flag:
			# If it is, then fetch that docktype
			return frappe.get_doc(self.mapping.target_doctype, flag)
		else:
			# If not, then check if a data by that name already exist or not
			primary_name = self.mapping.mapping_details[0].target_fieldname
			primary_value = self.source.get(self.mapping.mapping_details[0].source_fieldname)

			flag_2 = frappe.db.get_value(self.mapping.target_doctype, {primary_name: primary_value})

			if flag_2:
				# If same name is found, fetch that doctype
				return frappe.get_doc(self.mapping.target_doctype, flag_2)
			else :
				#  Else create a new doctype for current data object
				return frappe.new_doc(self.mapping.target_doctype)

	def clean_data(self, doctype, condition):
		frappe.db.sql("""delete from `tab{0}`{1}""".format(doctype, condition)) # Incase default frappe data needs to be deleted

@frappe.whitelist()
def migrate(plan):
	plan = frappe.get_doc('Data Migration Plan', plan)
	plan.migrate()

	frappe.clear_messages()
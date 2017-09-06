# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class DataMigrationPlan(Document):
	def migrate(self):
		source_connector = frappe.get_doc('Data Migration Connector', self.source_connector)
		source_connector.connect()
		for d in self.mappings:
			mapping = frappe.get_doc('Data Migration Mapping', d.mapping)
			data = source_connector.get_objects(mapping.source_objectname, mapping.condition)
			for i, source in enumerate(data):
				target = frappe.new_doc(mapping.target_doctype)
				for field in mapping.mapping_details:
					target.set(field.target_fieldname, source.get(field.source_fieldname))

				# post process
				if mapping.post_process:
					exec mapping.post_process in locals()

				try:
					target.insert()
				except frappe.DuplicateEntryError:
					target.save()

				frappe.publish_progress(float(i)*100/len(data),
					title = _('Migrating {0}').format(target.doctype), doctype=self.doctype, docname=self.name)


			# frappe.publish_progress(100,
			# 	title = _('Migrating {0}').format(target.doctype), doctype=self.doctype, docname=self.name)



@frappe.whitelist()
def migrate(plan):
# 	frappe.enqueue(_migrate, plan=plan)

# def _migrate(plan):
	plan = frappe.get_doc('Data Migration Plan', plan)
	plan.migrate()

	frappe.clear_messages()
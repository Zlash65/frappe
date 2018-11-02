frappe.ui.form.ControlCodeEditor = frappe.ui.form.ControlText.extend({
	make_input: function() {
		this._super();
		console.log(this);
		$(this.input_area).find("textarea")
			.allowTabs()
			.addClass('control-code');
	}
});

// import QRCode from 'qrcode-svg';
// const QRCode = require('qrcode-svg');
var QRCode = require('qrcode-svg');

frappe.ui.form.ControlQrCode = frappe.ui.form.ControlData.extend({
	make_wrapper() {
		this._super();

		let $input_wrapper = this.$wrapper.find('.control-input-wrapper');
		this.qr_code_area = $(`<div class="qr-code-wrapper border"></div>`);

		this.qr_code_area.appendTo($input_wrapper);
	},

	parse(value) {
		// Parse raw value
		return value ? this.get_qr_code_html(value) : "";
	},

	// set_formatted_input(value) {
	// 	let svg = value;


	// },

	get_qr_code_html(value) {
		console.log($(this.qr_code_area).find('.qr-code-wrapper'));
		let svg = $('body').find('.qr-code-wrapper')[0];
		let temp = new QRCode(value);
		console.log(temp.svg());
		$(svg).append(temp.svg());
	}
});

$(function() {
	console.log('start');
	var dt_picker_date = {'useCurrent': true, 'format': 'YYYY-MM-DD','pickTime': false}; //{ language: 'ru', autoclose: true, format: "yyyy-mm-dd", minView: "month" };
	$("#id_sumsql_date_start").datetimepicker(dt_picker_date);
	$("#id_sumsql_date_end").datetimepicker(dt_picker_date);
	console.log('end');
});

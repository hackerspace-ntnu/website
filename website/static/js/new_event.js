$('#timepicker_start').val("00:00");
$('#timepicker_end').val("00:00");
$('#datepicker').val($('#id_date').val());
var input = $('.clockpicker-with-callbacks').clockpicker({
align: 'left',
    afterDone: function() {
        //console.log("after done");
        $('#id_time_start').val($('#timepicker_start').val());
        $('#id_time_end').val($('#timepicker_end').val());
    }
});
$('#datepicker').datepicker({
    autoClose: "true",
    dateFormat: "dd/mm/yyyy",
    onSelect: function onSelect(fd, date) {
        $('#id_date').val($('#datepicker').val());
    }
})

function edit() {
    document.getElementById("edit").style.display="inline";
    document.getElementById("content").style.display="none";
    document.getElementById("cancelBtn").style.display="inline";
    document.getElementById("editBtn").style.display="none";
}
function cancel() {
    location.reload();
}
function adminPage() {
    var url = window.location.href;
    var id = url.substr(url.length-3, url.length-2);
    window.location.replace("/admin/news/event"+id+"change/");
}
function del() {
    var url = window.location.href;
    var id = url.substr(url.length-3, url.length-2);
    window.location.replace("/admin/news/event"+id+"delete/");
}
function createnew() {
    window.location.replace("/admin/news/event/add/");
}

$('#timepicker_start').val($('#id_time_start').val());
$('#timepicker_end').val($('#id_time_end').val());
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

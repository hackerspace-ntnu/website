$('#timepicker_start').val($('#id_time_start').val());
$('#timepicker_end').val($('#id_time_end').val());
$('#datepicker').val($('#id_date').val());
$('#thumbnailPicker').attr("src", $('#id_thumbnail').val());

var input = $('.clockpicker-with-callbacks').clockpicker({
  align: 'left',
      afterDone: function() {
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

$("#thumbnailPicker").click(function() {
    thumbWindow = window.open('/ckeditor_uploader/browse_thumbnail', 'Select Thumbnail', 'width=920,height=640,scrollbars=yes');
});

function getThumnail(thumb) {
    $("#id_thumbnail").val(thumb);
    $("#thumbnailPicker").attr("src", thumb);
}

$("#id_thumbnail").change(function() {
  $("#thumbnailPicker").attr("src", $("#id_thumbnail").val());
});

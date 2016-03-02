$('#thumbnailPicker').attr("src", $('#id_thumbnail').val());

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

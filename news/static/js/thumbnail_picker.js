$('#thumbnail_picker').attr("src", $('#id_thumbnail').val());

$("#thumbnail_picker").click(function() {
    thumbWindow = window.open('/ckeditor_uploader/browse_thumbnail', 'Select Thumbnail', 'width=920,height=640,scrollbars=yes');
});

function getThumnail(thumb) {
    $("#id_thumbnail").val(thumb);
    $("#thumbnail_picker").attr("src", thumb);
    $("label[for='id_thumbnail']").addClass("active");
}

$("#id_thumbnail").change(function() {
  $("#thumbnail_picker").attr("src", $("#id_thumbnail").val());
});

$(".thumbnailPicker").click(function() {
    thumbWindow = window.open('/files/images');
});

function selectThumnail(src, id) {
  thumbWindow.close();
  $("input[name^=thumbnail]").val(id);
  $(".thumbnailPicker").find("div").css("background-image", "url("+src+")");
}

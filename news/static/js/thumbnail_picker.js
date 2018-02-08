$(".thumbnailPicker").click(function() {
    thumbWindow = window.open('/files/images');
});

function selectThumnail(src, id) {
  thumbWindow.close();
  $("input[name^=thumbnail]").val(id);
	console.log("try to set bgimg");
  $(".thumb-preview").css("background-image", "url("+src+")");
}

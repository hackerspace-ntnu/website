$(document).ready(function() {
  pos = "top";
});

$(window).scroll(function() {
  var scrollTop = $(window).scrollTop();
  if (pos == "top" && scrollTop > 20) {
    pos = "page";
    $("#homeico").addClass("floatDown");
    $("#homeico").removeClass("floatUp");
  } else if (pos == "page" && scrollTop <= 20) {
    pos = "top";
    $("#homeico").addClass("floatUp");
    $("#homeico").removeClass("floatDown");
  }
});

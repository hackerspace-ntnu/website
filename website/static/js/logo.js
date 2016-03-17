$(function() {
  pos = "top";
});

$(window).scroll(function() {
  var scrollTop = $(window).scrollTop();
  if (pos == "top" && scrollTop > 20) {
    pos = "page";
    $("#logo").addClass("floatDown");
    $("#logo").removeClass("floatUp");
  } else if (pos == "page" && scrollTop <= 20) {
    pos = "top";
    $("#logo").addClass("floatUp");
    $("#logo").removeClass("floatDown");
  }
});

function logoClick() {
  if (pos == "top") {
    window.location.href = "/";
  } else {
    var $anchor = $(this);
    $('html, body').stop().animate({
        scrollTop: $("#header").offset().top
    }, 1000, 'easeInOutExpo');
    event.preventDefault();
  }
}

function logoClick_mobile() {
  window.location.href = "/";
}

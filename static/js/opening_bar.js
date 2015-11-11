$(function() {
  $("#header").click(function() {
    if($("body").hasClass("open")) {
        $("body").removeClass("open closed").addClass("closed");
    } else {
        $("body").removeClass("open closed").addClass("open");
    } 
      });
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollToTop').fadeIn('slow');
        } else {
            $('.scrollToTop').fadeOut();
        }
    });
    
    $('.scrollToTop').click(function(){
        $('html, body').animate({scrollTop : 0}, 1200, 'easeInOutExpo');
        return false;
    });
  });
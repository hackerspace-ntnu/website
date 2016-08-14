$("#application-form").submit(function(event){
  event.preventDefault();
  ajax_post($(this), "", "/");

});
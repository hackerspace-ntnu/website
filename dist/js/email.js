/* Email subscription */
var subscribe = function() {
  $.ajax({
    type: "POST",
    url: "https://lists.ansatt.ntnu.no/idi.ntnu.no",
    data: {
      "list": "hackernews",
      "action": "subrequest",
      "email": $("#email").val(),
    },
    complete: getPassword,
  })
}

var getPassword = function(data) {
  $("#emailwrap").hide();
  $("#passwrap").show();
}

var sendPass = function() {
  $.ajax({
    type: "POST",
    url: "https://lists.ansatt.ntnu.no/idi.ntnu.no",
    data: {
      "passwd": $("#password").val(),
      "email": $("#email").val(),
      "list": "hackernews",
      "action": "subrequest",
      "previous_list": "hackernews",
      "previous_action": "subrequest",
      "action_subscribe": "Subscribe",
    },
    complete: thanks,
  })
}

var thanks = function() {
  $("#passwrap").hide()
  $("#email-header").hide()
  $("#thanks").show()
}

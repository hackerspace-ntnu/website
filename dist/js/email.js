/* Email subscription */
var subscribe = function () {
    $.ajax({
        type: "POST",
        url: "https://lists.ansatt.ntnu.no/idi.ntnu.no",
        data: {
            "list": "hackernews",
            "action": "subrequest",
            "email": $("#email").val()
        },
        complete: getValidationKey
    });
};

var getValidationKey = function (data) {
    $("#emailwrap").hide();
    $("#validationwrap").show();
};

var sendKey = function () {
    $.ajax({
        type: "POST",
        url: "https://lists.ansatt.ntnu.no/idi.ntnu.no",
        data: {
            "passwd": $("#validation").val(),
            "email": $("#email").val(),
            "list": "hackernews",
            "action": "subrequest",
            "previous_list": "hackernews",
            "previous_action": "subrequest",
            "action_subscribe": "Subscribe"
        },
        complete: thanks
    });
};

var thanks = function () {
    $("#validationwrap").hide();
    $("#email-header").hide();
    $("#thanks").show();
};

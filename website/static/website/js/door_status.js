$(function() {
    setTimeout(function(){get_data()}, 30000);
});

function get_data() {
    $.ajax({
        "type": "GET",
        "url": "/door/get_status/",
        "success": function(data) {
            change_status(data);
        },
    });
    setTimeout(function(){get_data()}, 30000);
}

function change_status(status) {
    if (status == 'True') {
        $("#doorstatus").css("background-color","var(--hs-green)");
        $("#doorstatus p").html("Hackerspace er åpent");
    } else if (status == 'False') {
        $("#doorstatus").css("background-color","var(--hs-red)");
        $("#doorstatus p").html("Hackerspace er stengt");
    }
}

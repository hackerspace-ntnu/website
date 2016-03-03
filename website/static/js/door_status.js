$(document).ready(function() {
    setTimeout(function(){get_data()}, 1000);
    function get_data() {
        $.ajax({
            "type": "POST",
            "url": "/door/get_status/",
            "success": function(data) {
              change_status(data);
            },
        });
        setTimeout(function(){get_data()}, 1000);
    }
});

function change_status(status) {
    if (status == 'True') {
        $("#status").css("background-image","url(/static/img/Logo_green.png)");
    } else if (status == 'False') {
        $("#status").css("background-image","url(/static/img/Logo_white.png)");
    }
}

$(document).ready(function() {
    setTimeout(function(){get_data()}, 30000);
});

function get_data() {
    $.ajax({
        "type": "POST",
        "url": "/door/get_status/",
        "success": function(data) {
          change_status(data);
        },
    });
    setTimeout(function(){get_data()}, 30000);

}

function change_status(status) {
    console.log(status);
    if (status == 'True') {
        $("#statusImg").attr("src","/static/img/Logo_green.png");
    } else if (status == 'False') {
        $("#statusImg").attr("src","/static/img/Logo_white.png");
    }
}

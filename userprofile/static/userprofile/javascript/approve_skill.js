$(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    $(".approve-btn").click(function () {
        skillID = parseInt($(this).data('skillid'));
        apiURL = $(this).data('apiurl');
        button = $(this)
        payload = JSON.stringify(
            {
                skill_id: skillID
            }
        )
        $.ajax({
            url: apiURL,
            method: 'POST',
            data: payload,
            dataType: 'json',
            contentType: 'application/json; charset=UTF-8',
            success: function (data) {
                button.addClass('disabled')
                button.text('Godkjent')
                button.parentsUntil("li").filter("div").prev().find(".approve-checkmark").hide()
            },
            complete: function (xhr, status) {

            }
        }
        )

    });
});
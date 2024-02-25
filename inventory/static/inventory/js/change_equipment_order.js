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

    $(".order-up").click(function () {
        equipmentId = parseInt($(this).data('id'));
        apiURL = $(this).data('apiurl');
        console.log(equipmentId, apiURL);
        $.ajax({
            url: apiURL,
            method: 'PATCH',
            dataType: 'json',
            contentType: 'application/json; charset=UTF-8',
            success: function (data) {

            },
            complete: function (xhr, status) {

            }
        }
        )

    });
    $(".order-down").click(function () {
        equipmentId = parseInt($(this).data('id'));
        apiURL = $(this).data('apiurl');
        console.log(equipmentId, apiURL);
        $.ajax({
            url: apiURL,
            method: 'PATCH',
            dataType: 'json',
            contentType: 'application/json; charset=UTF-8',
            success: function (data) {

            },
            complete: function (xhr, status) {

            }
        }
        )

    });
});
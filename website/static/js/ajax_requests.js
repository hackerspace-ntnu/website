
// Global function for post requests with ajax
function ajax_post($form, url, redirectUrl) {

    // Remove all error messages before submitting
    $(".errorlist").each(function () {
        $(this).remove();
    });

    // Remove all the red lines before submitting
    $(".invalid").each(function () {
        $(this).removeClass('invalid');
    });

    // Serialize data and do ajax request
    var serializedData = $form.serialize();
    $.ajax({
        url: url,
        type: "post",
        data: serializedData,

        success: function (data, textStatus, jqXHR) {
            Materialize.toast(data, 5000);
            if (redirectUrl != undefined) {
                setTimeout(function () {
                    window.location.replace(redirectUrl);
                }, 2000);
            }
        },
        // If statusCode is 400, the request is bad, then it will show all the error messages received
        statusCode: {
            400: function (jqXHR, textStatus, errorThrown) {
                var response = JSON.parse(JSON.parse(jqXHR['responseText']));
                for (var key in response) {
                    if (response.hasOwnProperty(key)) {
                        var $inputField = $form.find("#" + key);
                        $inputField.append('<ul class="errorlist"><li>' + response[key] + '</li></ul>');
                        $inputField.find('input').addClass("invalid");
                        $inputField.find('textarea').addClass("invalid");
                    }
                }
            }
        },
        // If errors exists, show them in the console
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("The following error occured: " + textStatus, errorThrown);
        }
    });
}

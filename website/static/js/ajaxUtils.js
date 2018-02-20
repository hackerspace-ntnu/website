// Fra django docs om ajax: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajaxSetup() {
    // Metode for å gjøre det mulig å bruke POST, PUT og DELETE med ajax.
    // Kall denne metoden med en gang, hent csrftoken fra {% csrftoken %}

    var csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

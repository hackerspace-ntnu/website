$(() => {
    $.ajaxSetup({
        beforeSend(xhr) {
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const rawCookies = document.cookie.split(';');
                    for (const rawCookie of rawCookies) {
                        const cookie = jQuery.trim(rawCookie);
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
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

    const approveBtn = $(".approve-btn")
    approveBtn.click(() =>
        $.ajax({
            url: approveBtn.data('apiurl'),
            method: 'POST',
            data: JSON.stringify(
                {
                    skill_id: parseInt(approveBtn.data('skillid'))
                }
            ),
            dataType: 'json',
            contentType: 'application/json; charset=UTF-8',
            success() {
                approveBtn.addClass('disabled')
                approveBtn.text('Godkjent')
                approveBtn.parentsUntil("li").filter("div").prev().find(".approve-checkmark").hide()
            }
        })
    );
});

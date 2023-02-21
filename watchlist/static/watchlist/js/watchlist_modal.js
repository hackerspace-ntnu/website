const weekdays = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag'];
let modal_shift_id = 0;
let modal_day = 0;
let modal_time = '';
let modal_watchers = [];
let modal_register = true;
let modal_register_url = '';
let has_perms = '';
let close_button = '<a href="#!" class="modal-close btn hs-red">Lukk</a>';

function updateModalInformation() {
    $('#registration-modal-day').text(weekdays[modal_day]);
    // Tiden til vakten inneholder i utgangspunktet en newline. Dette er vanligvis en syntaksfeil fordi vi ikke kan escape den
    // Så vi setter inn tiden med <br> for newlines i templaten, så fjerner vi den her for å få tidsrammen på en linje
    modal_time = modal_time.replace('<br>', '');
    $('#registration-modal-time').text(modal_time);

    const watchlist_div = $('#registration-modal-watchlist');
    // Tøm div-en
    watchlist_div.empty();

    // Tøm diven for knappelering
    const footer_div = $('#registration-modal-footer');
    footer_div.empty();

    // legg til knapp for på-/avregistrering
    let change_registration_button = $('<a class="btn"></a>');
    change_registration_button.attr('href', modal_register_url);
    if (modal_register === true) {
        change_registration_button.addClass('hs-green');
        change_registration_button.text('Registrer');
    }
    else {
        change_registration_button.addClass('hs-red');
        change_registration_button.text('Avregistrer');
    }

    if (has_perms === "False") {
        watchlist_div.append($('<p>DU MÅ LOGGE INN FOR Å REGISTRERE VAKT!</p>'));
        footer_div.append($(close_button));
    } else {
        if (modal_watchers.length > 0) {
            watchlist_div.append($('<h5>Vakthavende</h5>'));
            // Legg til navnet på alle vakthavende
            const watchlist_names = $('<p></p>');
            for (let i = 0; i < modal_watchers.length; i++) {
                watchlist_names.append($('<span>' + modal_watchers[i] + '</span><br>'));
            }
            watchlist_div.append(watchlist_names);
        }
        else {
            watchlist_div.append($('<p>Ingen på vakt!</p>'));
        }

        footer_div.append(change_registration_button);
        // og sleng med en avbryt-knapp
        footer_div.append(' ');
        footer_div.append($(close_button));
    }
}

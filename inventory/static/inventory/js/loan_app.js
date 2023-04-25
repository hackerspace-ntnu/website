document.addEventListener("DOMContentLoaded", function() {
    const datepickers = document.querySelectorAll('.datepicker');

    internationalization = {
        months:	[
            'Januar',
            'Februar',
            'Mars',
            'April',
            'Mai',
            'Juni',
            'Juli',
            'August',
            'September',
            'Oktober',
            'November',
            'Desember'
        ],
        weekdays: [
            'Søndag',
            'Mandag',
            'Tirsdag',
            'Onsdag',
            'Torsdag',
            'Fredag',
            'Lørdag'
        ],
        weekdaysShort: [
            'Søn',
            'Man',
            'Tir',
            'Ons',
            'Tor',
            'Fre',
            'Lør'
        ],
        weekdaysAbbrev: ['S','M','T','O','T','F','L']
    }

    for (dp of datepickers) {
        options = {
            format: 'dd.mm.yyyy',
            firstDay: 1,
            i18n: internationalization,
            minDate: new Date()
        }
        const maxDateStr = dp.getAttribute('data-max-date')
        if (maxDateStr) {
            options.maxDate = new Date(maxDateStr)
        }
        M.Datepicker.init(dp, options);
    }


    // Vis og gjem deler som relateres til påmeldinger
    var reg_box = document.getElementsByClassName('reg-box')[0];
    var reg_check = document.getElementsByName('registration')[0]
    var ext_reg = document.getElementsByClassName('ext-reg')[0];

    if(reg_check.checked) {
        reg_box.classList.remove('hide');
        ext_reg.classList.add('hide');
    }
    else {
        reg_box.classList.add('hide');
        ext_reg.classList.remove('hide');
    }

    reg_check.onchange = function() {
        if(this.checked) {
            reg_box.classList.remove('hide');
            ext_reg.classList.add('hide');
        }
        else {
            reg_box.classList.add('hide');
            ext_reg.classList.remove('hide');
            document.getElementById('id_external_registration').value = '';
        }
    };

});

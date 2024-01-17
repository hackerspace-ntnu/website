document.addEventListener("DOMContentLoaded", function() {
    var datepickers = document.querySelectorAll('.datepicker');

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
    options = {
        format: 'yyyy-mm-dd',
        firstDay: 1,
        i18n: internationalization
    }
    M.Datepicker.init(datepickers, options);


    var elems = document.querySelectorAll('.timepicker');
    options = {
        twelveHour: false,
        format: 'HH:mm',
    };
    M.Timepicker.init(elems, options);
});

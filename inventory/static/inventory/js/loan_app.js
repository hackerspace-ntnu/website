document.addEventListener("DOMContentLoaded", () => {
    const options = {
        format: 'dd.mm.yyyy',
        firstDay: 1,
        i18n: {
            months: [
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
            weekdaysAbbrev: ['S', 'M', 'T', 'O', 'T', 'F', 'L']
        },
        minDate: new Date()
    }
    const datePickers = document.querySelectorAll('.datepicker');
    for (const dp of datePickers) {
        const maxDateStr = dp.getAttribute('data-max-date')
        M.Datepicker.init(dp, {
            ...options,
            ...(maxDateStr && {maxDate: new Date(maxDateStr)})
        });
    }
});

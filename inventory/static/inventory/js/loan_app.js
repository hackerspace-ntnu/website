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

    const loanFromDate = document.getElementById('id_loan_from');
    options = {
        format: 'dd.mm.yyyy',
        firstDay: 1,
        i18n: internationalization,
        minDate: new Date(loanFromDate.value)
    }

    for (dp of datepickers) {
        if (dp.id === 'id_loan_to') {
            if (maxLoanDays) {
                const maxDate = new Date()
                maxDate.setDate(new Date(loanFromDate.value).getDate() + maxLoanDays)
                options.maxDate = maxDate
            }
        }
        M.Datepicker.init(dp, options);
    }


    loanFromDate.addEventListener('change', () => {
        updateLoanToDatepicker(options, maxLoanDays)
    });

});

function parseFormattedDate(dateString) {
    const dateParts = dateString.split('.');
    return new Date(dateParts[2], dateParts[1]-1, dateParts[0]);
}

function updateLoanToDatepicker(datepickerOptions, maxLoanDays) {
    const loanFromDateEl = document.getElementById('id_loan_from');
    const loanToDate = document.getElementById('id_loan_to');

    const loanFromDate = parseFormattedDate(loanFromDateEl.value)

    datepickerOptions.minDate = loanFromDate

    if (maxLoanDays) {
        const maxDate = new Date(loanFromDate)
        maxDate.setDate(loanFromDate.getDate() + maxLoanDays)
        datepickerOptions.maxDate = maxDate
    }

    M.Datepicker.init(loanToDate, datepickerOptions);
}

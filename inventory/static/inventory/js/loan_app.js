document.addEventListener("DOMContentLoaded", function() {
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

    const loanFromDateEl = document.getElementById('id_loan_from');
    const loanToDateEl = document.getElementById('id_loan_to');

    options = {
        format: 'dd.mm.yyyy',
        firstDay: 1,
        i18n: internationalization
    }

    initDatepickers(loanToDateEl, loanFromDateEl, maxLoanDays, loanFromMaxDate, options)
    loanFromDateEl.addEventListener('change', () => {
        updateLoanToDatepicker(loanToDateEl, loanFromDateEl, options, maxLoanDays)
    });

});

function parseFormattedDate(dateString) {
    const dateParts = dateString.split('.');
    return new Date(dateParts[2], dateParts[1]-1, dateParts[0]);
}

function initDatepickers(loanToEl, loanFromEl, maxLoanDays, loanFromMaxDate, dpOptions) {
    const toDateOptions = dpOptions
    const fromDateOptions = {
            ...toDateOptions,
    }

    fromDateOptions.minDate = parseFormattedDate(loanFromEl.value);
    if (loanFromMaxDate) {
        fromDateOptions.maxDate = new Date(loanFromMaxDate);
    }

    M.Datepicker.init(loanFromEl, fromDateOptions);
    M.Datepicker.init(loanToEl, toDateOptions);

    updateLoanToDatepicker(loanToEl, loanFromEl, toDateOptions, maxLoanDays)
}

function updateLoanToDatepicker(loanToEl, loanFromEl, datepickerOptions, maxLoanDays) {
    const loanFromDate = parseFormattedDate(loanFromEl.value)

    datepickerOptions.minDate = loanFromDate

    if (maxLoanDays) {
        const maxDate = new Date(loanFromDate)
        maxDate.setDate(loanFromDate.getDate() + maxLoanDays)
        datepickerOptions.maxDate = maxDate
    }

    M.Datepicker.init(loanToEl, datepickerOptions);
}

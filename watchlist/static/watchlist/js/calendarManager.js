document.addEventListener('DOMContentLoaded', function() {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'nb',
        plugins: ['moment', 'interaction', 'timeGrid'],
        defaultView: "timeGridWeek",
        selectLongPressDelay: 350,
        nowIndicator: true,
        selectable: true,
        selectMirror: true,
        selectAllow: function(info) {
            return moment().diff(info.start) <= 0
        },
        height:"auto",
        allDaySlot: false,
        slotDuration: '02:00:00',
        snapDuration: '00:10:00',
        slotLabelInterval: '02:00:00',
        slotLabelFormat: {
            hour: 'numeric',
            minute: '2-digit',
            omitZeroMinute: false,
        },
        selectOverlap: false,
        minTime: "10:15:00",
        maxTime: "18:15:00",
        weekends: true,

       
    });

    calendar.render();
});
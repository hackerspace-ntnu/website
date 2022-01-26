function selectAll() {
    selectAllWithSelector('.userCheckbox:not(.waiting)');
}

function selectAllAttendees() {
    selectAllWithSelector('.userCheckbox.attendee');
}

function selectAllWithSelector(selector) {
    const checkedBoxes = document.querySelectorAll(selector + ':checked');
    const uncheckedBoxes = document.querySelectorAll(selector + ':not(:checked)');

    if (uncheckedBoxes.length !== 0) {
        for (const checkbox of uncheckedBoxes) {
            checkbox.click();
        }
    } else {
        for (const checkbox of checkedBoxes) {
            checkbox.click();
        }
    }
}

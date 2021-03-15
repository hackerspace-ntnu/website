from .models import ShiftSlot, weekday_loc

def get_shift_weekview_rows():
    '''Returns a list of timeslot row headers to populate a weekview table with'''
    slots = ShiftSlot.objects.all()
    if not slots:
        return None

    rows = []
    for slot in slots:
        row_header = (slot.start, slot.end)
        if row_header not in rows:
            rows.append(row_header)

    # Sort by start time
    rows.sort(key=lambda r: r[0])
    # Reformat into strings
    rows = ["{} -\n{}".format(row[0].strftime("%H:%M"), row[1].strftime("%H:%M")) for row in rows]
    
    return rows

def get_shift_weekview_columns():
    '''Returns a list of weekday name column headers to populate a weekview table with'''
    slots = ShiftSlot.objects.all()
    if not slots:
        return None

    cols = []
    for slot in slots:
        col_header = slot.get_weekday_name()
        if col_header not in cols:
            cols.append(col_header)
    
    return cols

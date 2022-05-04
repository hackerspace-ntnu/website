from .models import ShiftSlot


def get_shift_weekview_rows():
    """Returns a dictionary of shifts for each timeslot, for each weekday"""
    slots = ShiftSlot.objects.all().order_by("start")
    if not slots:
        return None

    # Could be troublesome wrt. sorting of dictionary keys.
    # Doesn't *seem* to be an issue right now but it *technically* already is!
    rows = {}
    for slot in slots:
        row_header = "{} -\n{}".format(
            slot.start.strftime("%H:%M"), slot.end.strftime("%H:%M")
        )
        if row_header not in rows:
            rows[row_header] = []
        rows[row_header].append(slot)

    # Sort each list in the dict by weekday
    for time in rows.keys():
        rows[time].sort(key=lambda s: s.weekday)

    return rows


def get_shift_weekview_columns():
    """Returns a list of weekday name column headers to populate a weekview table with"""
    slots = ShiftSlot.objects.all().order_by("weekday")
    if not slots:
        return None

    cols = []
    for slot in slots:
        col_header = slot.get_weekday_name()
        if col_header not in cols:
            cols.append(col_header)

    return cols

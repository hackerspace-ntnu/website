import datetime
from datetime import date, timedelta

from reservations.models import Reservation


def get_queue_reservations_for_week(queue, week_delta=0, interval=30, start_time=10, end_time=18):
    """
    :param queue: Queue object
    :param week_delta: weeks from now. 0=current week, 1=next week, ...
    :param interval: interval (in minutes) to display reservation in
    :param start_time: when the reservations start
    :param end_time: when the reservations stop
    :return: dict with start_time, end_time,
            dict(weekday: user who made the reservation for every interval during that day),
            list of intervals during a day,
    """
    # get the date of this week's monday
    week_start_date = date.today() - timedelta(days=date.today().weekday())

    # move forward/back in time to appropriate monday based on week_delta
    base_date = week_start_date + timedelta(weeks=week_delta)

    queue_reservations = Reservation.objects.filter(parent_queue=queue)

    reservation_day_time = {}
    for i in range(7):  # for every weekday
        day = base_date + timedelta(days=i)

        # ascending list of reservations made that day
        reservations_today = sorted(queue_reservations.filter(date=day), key=lambda e: e.start_time)

        reservations = []
        reservation_intervals = []
        t = datetime.datetime(100, 1, 1, start_time, 0, 0)
        while t.time() < datetime.time(end_time):
            for r in reservations_today:
                if r.start_time <= t.time() <= r.end_time:
                    reservations.append(r.user)
                    break
            else:
                reservations.append(None)

            reservation_intervals.append(t.time())
            t += datetime.timedelta(minutes=interval)

        # map day's weekday name to reservations for day
        reservation_day_time[day.strftime("%A")] = reservations

    return_dict = {
        'start_time': start_time,
        'interval': interval,
        'reservation_day_dict': reservation_day_time,
        'reservation_intervals': reservation_intervals,
    }
    return return_dict




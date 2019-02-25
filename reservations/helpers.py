import datetime
from datetime import date, timedelta, time

from django.db.models import Q

from reservations.models import Reservation


def get_queue_reservations_for_week(queue, paginate=0, reservation_min_length=30, queue_start_time=10, queue_end_time=18):
    """
    :param queue: Queue object
    :param paginate: weeks from now. 0=current week, 1=next week, ...
    :param reservation_min_length: interval (in minutes) to display reservation in
    :param queue_start_time: when the reservations start
    :param queue_end_time: when the reservations stop
    :return: a list of dictionaries with key_val=reservation interval start. value is a list of length 7,
    containing either a reservation object or an empty QS (no reservation)
    """
    if 60 % reservation_min_length != 0:
        raise ValueError("reservation_min_length must divide 60")

    # get the date of this week's monday
    week_start_date = date.today() - timedelta(days=date.today().weekday())

    # move forward/back in time to appropriate monday based on week_delta
    base_date = week_start_date + timedelta(weeks=paginate)

    queue_reservations = Reservation.objects.filter(parent_queue=queue)
    intervals = []

    """
    Iterate through every interval available for reservation and either get user who made reservation for that 
    interval/day-combo or an empty QS 
    """
    for hour in range(queue_start_time, queue_end_time):
        for minutes in range(0, 60, reservation_min_length):
            interval = time(hour=hour, minute=minutes)
            if minutes + reservation_min_length == 60:
                interval_end = time(hour=hour+1)
            else:
                interval_end = time(hour=hour, minute=minutes + reservation_min_length)
            # for every day in week, check
            reservations_for_interval = [
                queue_reservations.filter(
                    Q(date=base_date + timedelta(days=i))
                    & Q(start_time__lt=interval)  # less than
                    & Q(end_time__gte=interval_end)  # greater than or equal
                )
                for i in range(7)
            ]
            intervals.append(
                {
                    'start': interval,
                    'stop': interval_end,
                    'reservations': reservations_for_interval,
                }
            )
    return intervals

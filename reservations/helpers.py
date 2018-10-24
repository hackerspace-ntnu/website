from datetime import date, timedelta

from reservations.models import Reservation


def get_queue_reservations_for_week(queue, week_delta=0):
    """
    :param queue: Parent queue of the reservations
    :param week_delta: distance in weeks from today you want to view the Q's reservations. -1 moved you back in time
    :return: dictionary: {'weekday_name': [(reservation_start_time, reservation_end_time)...]}
    """

    # get the date of this week's monday
    week_start_date = date.today() - timedelta(days=date.today().weekday())

    # move forward/back in time to appropriate monday based on week_delta
    base_date = week_start_date + timedelta(weeks=week_delta)

    queue_reservations = Reservation.objects.filter(parent_queue=queue)
    reservation_dict = {}
    for i in range(7):
        day = base_date + timedelta(days=i)
        reservations_today = queue_reservations.filter(date=day)

        # map day's weekday name to reservations for day
        reservation_dict[day.strftime("%A")] = [
            [(r.start_time, r.end_time) for r in reservations_today]
        ]

    return reservation_dict




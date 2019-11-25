from datetime import date, timedelta, time, datetime
from pytz import timezone, utc
import re

TODAY = "today"
TOMORROW = "tomorrow"
YESTERDAY = "yesterday"

RELATIVE_DATES = [YESTERDAY, TODAY, TOMORROW]
DAYS_OF_WEEK = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']
# monday = 0 index

DAY = "day"
WEEK = "week"
MONTH = "month"
YEAR = "year"
HOUR = "hour"
MINUTE = "minute"

OFFSET_UNITS_TO_DAYS = {DAY: 1,
                        WEEK: 7,
                        MONTH: 30,
                        YEAR: 365}
# to do: handle months and leap years

DURATION_UNITS = {HOUR: "hours",
                  MINUTE: "minutes",
                  DAY: "days"}


def fix_fake_response_times(fake_json_response):
    return [fix_event(event) for event in fake_json_response]

def fix_event(event):
    day = parse_day(event.get("day_specifier"))
    offset = parse_offset(event.get('offset_specifier'))
    time = event.get('time')
    event_datetime = datetime.combine(day + offset, time)
    duration = parse_duration(event.get('duration_specifier'))
    tz = event.get("timezone")
    event['start'] = eb_timestamp(event_datetime, tz=tz)
    event['end'] = eb_timestamp(event_datetime, tz=tz, duration=duration)
    return event

def eb_timestamp(event_datetime,
                 tz="UTC",
                 duration=None):
    local_tz = timezone(tz)
    local_stamp = local_tz.localize(event_datetime).isoformat()
    utc_stamp = utc.localize(event_datetime).isoformat()
    return {
        "timezone": tz,
        "local": local_stamp,
        "utc": utc_stamp
    }

def parse_duration(duration_specifier):
    """Determine the desired duration
    something like "1 hour" or "90 minute"
    """
    regex = re.compile("(\d*) (\w*)")
    match = regex.match(duration_specifier)
    if not match:
        return timedelta(hours=1)  #fuckit
    qty, unit = match.groups()
    if unit not in DURATION_UNITS:
        return timedelta(hours=1)  #again, fuckit
    return timedelta(**{DURATION_UNITS[unit]: int(qty)})

def parse_day(day_specifier):
    """Determine the desired base day, as a datetime.date
    Possible specifiers: "today", "tomorrow", "yesterday", days of week (lowercase)
    If day_of_week is specified, assume that we mean upcoming
    (this may change, depending on what people prefer)
    """
    if day_specifier in RELATIVE_DATES:
        return _handle_relative_date(day_specifier)
    if day_specifier in DAYS_OF_WEEK:
        return _handle_day_of_week(day_specifier)
    else:
        return date.today()

def _handle_relative_date(day_specifier):
    offset =  RELATIVE_DATES.index(day_specifier) - 1
    return date.today() + timedelta(offset)

def _handle_day_of_week(day_specifier):
    # we want the upcoming instance of day_specifier
    # ie, if today is Tuesday, "monday" means next Monday,
    # not yesterday
    
    today = date.today()
    weekday = DAYS_OF_WEEK.index(day_specifier)
    offset = (weekday - today.weekday()) % 7
    return today + timedelta(days=offset)
    
def parse_offset(offset_specifier):
    """Determine the desired offset, in days.
    Negative offsets indicate past events.
    Offset format: "[+-][int] [day|week|month|year]", eg "+2 week"
    To do: allow plurals
    """
    
    if not offset_specifier:
        # no offset specified, assume no offset intended
        return timedelta(days=0)
    pat = re.compile("([+-])(\d+) (\w+)")
    m = pat.match(offset_specifier)
    if not m:
        # match failed, assume no offset TODO: error handling
        return timedelta(0)
    sign, quantity, unit = m.groups()
    return _compute_offset(sign, int(quantity), unit)

def _compute_offset(sign, qty, unit):
    polarity = 1 if sign == "+" else -1
    offset_units = OFFSET_UNITS_TO_DAYS.get(unit, 0)
    # if bad unit, default to zero TO DO error handling
    return timedelta(days=polarity * qty * offset_units)



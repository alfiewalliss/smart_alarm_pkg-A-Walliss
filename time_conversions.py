"""a module containing all of the time opperations used within the program"""
import time
def minutes_to_seconds( minutes: str ) -> int:
    """Converts minutes to seconds
    minutes -- the minutes to be converted to seconds"""
    return int(minutes)*60
def hours_to_minutes( hours: str ) -> int:
    """Converts hours to minutes
    hours -- the hours to be converted to minutes"""
    return int(hours)*60
def hhmm_to_seconds( hhmm: str ) -> int:
    """converts hhmm to seconds
    hhmm -- the time in the format hh:mm to be converted to seconds"""
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])
def hhmmss_to_seconds( hhmmss: str ) -> int:
    """converts hhmmss to seconds
    hhmmss -- The time in hh:mm:ss to be converted into seconds"""
    if len(hhmmss.split(':')) != 3:
        print('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
        minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])
def current_time_hhmm() -> str:
    """returns the current time"""
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)

from googleapiclient.discovery import build

import pytz


def create_calendar_event(service, start_time, end_time, active_app):
    tz = pytz.timezone('America/Phoenix')  # Set to the appropriate timezone
    start_time = tz.localize(start_time)
    end_time = tz.localize(end_time)

    event = {
        'summary': f'Used {active_app}',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Phoenix',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Phoenix',
        },
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created for {active_app}:', created_event['htmlLink'])
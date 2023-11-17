from googleapiclient.discovery import build
import tkinter as tk
import threading
import time
import datetime
from APIUse import authenticate
from Auth import create_calendar_event
import psutil

# List of software applications to track
tracked_apps = ['Code.exe', 'idea64.exe', 'RobloxStudioBeta.exe']

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Software Activity Tracker")

        self.running = False
        self.tracking_thread = None

        self.start_button = tk.Button(self.root, text="Start Tracking", command=self.start_tracking)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Tracking", command=self.stop_tracking)
        self.stop_button.pack()

        self.tracked_app_label = tk.Label(self.root, text="")
        self.tracked_app_label.pack()

    def start_tracking(self):
        self.running = True
        self.tracking_thread = threading.Thread(target=self.track_apps)
        self.tracking_thread.start()

    def stop_tracking(self):
        self.running = False
        if self.tracking_thread:
            self.tracking_thread.join()

    def track_apps(self):
        credentials = authenticate()
        service = build('calendar', 'v3', credentials=credentials)

        active_app = None
        event_start_time = None

        while self.running:
            current_app = self.get_active_tracked_app()

            if current_app != active_app:
                if active_app is not None and event_start_time is not None:
                    event_end_time = datetime.datetime.now()
                    if active_app in tracked_apps:
                        self.create_calendar_event(service, event_start_time, event_end_time, active_app)

                active_app = current_app
                event_start_time = datetime.datetime.now()

            if active_app:
                self.tracked_app_label.config(text=f"Tracking: {active_app}")
            else:
                self.tracked_app_label.config(text="")

            time.sleep(1)  # Adjust the sleep interval as needed

    def get_active_tracked_app(self):
        active_app = None
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] in tracked_apps:
                active_app = proc.info['name']
                break
        return active_app

    def create_calendar_event(self, service, start_time, end_time, active_app):
        event = {
            'summary': f'Used {active_app}',
            'start': {
                'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Your_Timezone',
            },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Your_Timezone',
            },
        }
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created for {active_app}:', created_event['htmlLink'])


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

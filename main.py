from data_manager import *
from notification_manager import *

data_manager = DataManager()
data_manager.get_spreadsheet_data()
data_manager.get_flight_data()
notification_manager = NotificationManager()
notification_manager.create_email_body(data_manager.flight_data)
notification_manager.send_emails()

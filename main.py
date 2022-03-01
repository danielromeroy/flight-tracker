from flight_data import FlightData
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.criteria_data
flight_data = FlightData(sheet_data)
data_manager.criteria_data = flight_data.criteria_data
data_manager.update_sheet()
flight_search = FlightSearch(data_manager.criteria_data)
flight_search.fetch_flights()
notification_manager = NotificationManager(flight_search)
notification_manager.send_mail()

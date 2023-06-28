import requests
import datetime
from data_and_keys import *

NUMBER_OF_FLIGHTS_LISTED_PER_DESTINATION = 1
todays_date_formatted = datetime.date.today().strftime("%d/%m/%Y")
sixmonths_date_formatted = (datetime.datetime.now() + datetime.timedelta(6 * 30)).strftime("%d/%m/%Y")


def format_date_and_time(x):
	x = x.split("T")
	date = x[0].split("-")
	date = date[-1] + "." + date[-2] + "." + date[-3] + "."
	time = x[1].split(":")
	time = time[0] + ":" + time[1]
	return {"fdate": date, "ftime": time}


class DataManager:
	def __init__(self):
		self.spreadsheet_data = None
		self.flight_data = []
		self.tequila_request_parameters = None
		self.tequila_response_data = None

	def get_spreadsheet_data(self):
		response = requests.get(url=SHEETY_API, auth=SHEETY_BASIC_AUTH)
		if response.status_code == 200:
			self.spreadsheet_data = response.json()
			print("Sheety data fetched successfully.")
		else:
			print("Error communicating with Sheety.")

	def get_flight_data(self):
		for i in range(len(self.spreadsheet_data["sheet1"])):
			self.tequila_request_parameters = {
				"fly_from": self.spreadsheet_data["sheet1"][0]["departureCode"],
				"fly_to": self.spreadsheet_data["sheet1"][i]["destinationCode"],
				"flight_type": "round",
				"adult_hold_bag": self.spreadsheet_data["sheet1"][0]["givenBaggagePieces"],
				"adult_hand_bag": self.spreadsheet_data["sheet1"][0]["handBaggagePieces"],
				"nights_in_dst_from": self.spreadsheet_data["sheet1"][i]["minimumNightsStay"],
				"nights_in_dst_to": self.spreadsheet_data["sheet1"][i]["maximumNightsStay"],
				"limit": NUMBER_OF_FLIGHTS_LISTED_PER_DESTINATION,
				"date_from": todays_date_formatted,
				"date_to": sixmonths_date_formatted
			}
			response = requests.get(url=TEQUILA_API_ENDPOINT, headers=TEQUILA_HEADERS,
									params=self.tequila_request_parameters)
			if response.status_code == 200:
				try:
					self.tequila_response_data = response.json()
					self.flight_data.append({
						"cityFrom": self.tequila_response_data["data"][0]["cityFrom"],
						"countryFromCode": self.tequila_response_data["data"][0]["countryFrom"]["code"],
						"cityTo": self.tequila_response_data["data"][0]["cityTo"],
						"countryToCode": self.tequila_response_data["data"][0]["countryTo"]["code"],
						"price": self.tequila_response_data["data"][0]["price"],
						"currency": self.tequila_response_data["currency"],
						"departureDate":
							format_date_and_time(self.tequila_response_data["data"][0]["local_departure"])["fdate"],
						"departureLocalTime":
							format_date_and_time(self.tequila_response_data["data"][0]["local_departure"])["ftime"],
						"arrivalDate": format_date_and_time(self.tequila_response_data["data"][0]["local_arrival"])[
							"fdate"],
						"arrivalLocalTime":
							format_date_and_time(self.tequila_response_data["data"][0]["local_arrival"])["ftime"],
						"nightsInDestination": self.tequila_response_data["data"][0]["nightsInDest"],
						"deepLink": self.tequila_response_data["data"][0]["deep_link"]
					})
				except IndexError:
					pass
			else:
				print("Error communicating with Tequila.")
		print("Tequila data fetched successfully.")

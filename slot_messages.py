from models.flight import Flight
from parser.b2b_parser import B2BParser

class SlotMessages:
    def __init__(self, b2b_relative_path, aftn_relative_path):
        self.b2b_relative_path = b2b_relative_path
        self.aftn_relative_path = aftn_relative_path
        self.flights = {}
        self.b2b_parser = B2BParser(b2b_relative_path)

    def parse_slot_messages(self):
        self.b2b_parser.parse_slot_messages(self.flights)

    def print_flights(self):
        for ifplid, flight in self.flights.items():
            print(ifplid)
            print("######")
            print(flight.print_all_slot_messages())
            print()
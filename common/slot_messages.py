from typing import Dict

from common.models import Flight
from common.parser.b2b_parser import B2BParser
from common.parser.aftn_parser import AFTNParser

class SlotMessages:
    def __init__(self, b2b_relative_path: str, aftn_relative_path: str):
        self.flights: Dict[str, Flight]|Dict = {}
        self.b2b_parser = B2BParser(b2b_relative_path)
        self.aftn_parser = AFTNParser(aftn_relative_path)

    def parse_slot_messages(self) -> None:
        """
        Parse slot messages from all sources
        """
        #self.b2b_parser.parse_slot_messages(self.flights)
        self.aftn_parser.parse_slot_messages(self.flights)

    def print_flights(self) -> None:
        for ifplid, flight in self.flights.items():
            print(ifplid)
            print("######")
            print(flight.print_all_slot_messages())
            print()

    def get_flights(self) -> Dict[str, Flight]:
        return self.flights
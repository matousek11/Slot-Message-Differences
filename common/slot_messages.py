from typing import Dict, List

from common.models import Flight
from common.parser.b2b_parser import B2BParser
from common.parser.aftn_parser import AFTNParser

class SlotMessages:
    def __init__(self, b2b_relative_paths: List[str], aftn_relative_paths: List[str]):
        self.flights: Dict[str, Flight]|Dict = {}
        self.b2b_parser = B2BParser(b2b_relative_paths)
        self.aftn_parser = AFTNParser(aftn_relative_paths)

    def parse_slot_messages(self) -> None:
        """
        Parse slot messages from all sources
        """
        self.aftn_parser.parse_slot_messages(self.flights)
        self.b2b_parser.parse_slot_messages(self.flights)

    def print_flights(self) -> None:
        for ifplid, flight in self.flights.items():
            print(ifplid)
            print("######")
            print(flight.print_all_slot_messages())
            print()

    def get_flights(self) -> Dict[str, Flight]:
        return self.flights
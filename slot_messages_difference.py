from datetime import datetime
from models.slot_message import SlotMessage
from models.flight import Flight

class SlotMessagesDifference:
    def __init__(self, b2b_relative_path):
        self.b2b_relative_path = b2b_relative_path
        self.flights = {}


    def parse_slot_messages(self):
        with open(self.b2b_relative_path, 'r') as file:
            for line in file:
                if line.isspace() or '###' in line:
                    continue
                parsed_slot_message_data = self.parse_b2b_slot_message(line)
                self.save_slot_message_to_flight(parsed_slot_message_data[0], parsed_slot_message_data[1])

    def parse_b2b_slot_message(self, b2b_slot_message):
        b2b_slot_message = b2b_slot_message.replace("#", "")
        b2b_slot_message = b2b_slot_message.strip()
        b2b_slot_message = b2b_slot_message.split(" : ")
        slot_created_timestamp = datetime.strptime(b2b_slot_message[0], '%Y-%m-%d %H:%M:%S %f').timestamp()
        slot = SlotMessage(slot_created_timestamp, b2b_slot_message[2])
        return [b2b_slot_message[1], slot]

    def save_slot_message_to_flight(self, ifplid, slot_message):
        if self.flights.get(ifplid) != None:
            self.flights.get(ifplid).add_b2b_slot(slot_message)
        else:
            self.flights[ifplid] = Flight([slot_message], [])


    def print_flights(self):
        for ifplid, flight in self.flights.items():
            print(ifplid)
            print("######")
            print(flight.print_all_slot_messages())
            print()
from typing import Dict

from models import Flight, SlotMessage


class Parser:
    def parse_slot_messages(self, flights: Dict[str, Flight]|Dict) -> None:
        raise NotImplementedError('Child classes have to implement this method!')

    def save_slot_message_to_flight(self, ifplid: str, slot_message: SlotMessage, flights: Dict[str, Flight]|Dict) -> None:
        """
        Checks if flight with IFPLID exists and adds SlotMessage to the flight or create new flight and adds SlotMessage to the flight

        :param ifplid: identifier of each flight
        :param slot_message: SlotMessage object
        :param flights: currently known flights
        """
        classname = self.__class__.__name__
        aftn_classname = 'AFTNParser'
        if flights.get(ifplid) is not None:
            flight = flights.get(ifplid)
            flight.add_aftn_slot(slot_message) if classname is aftn_classname else flight.add_b2b_slot(slot_message)
        else:
            flights[ifplid] = Flight([], [slot_message]) if classname is aftn_classname else Flight([slot_message], [])
        
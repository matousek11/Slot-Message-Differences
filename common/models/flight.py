from typing import List

from common.models import SlotMessage


class Flight:
    def __init__(self, flight_id, b2b_slots, aftn_slots):
        self.flight_id = flight_id
        self.b2b_slots = b2b_slots
        self.aftn_slots = aftn_slots

    def add_b2b_slot(self, b2b_slot: SlotMessage) -> None:
        self.b2b_slots.append(b2b_slot)
        self.b2b_slots = [slot for slot in self.b2b_slots if slot is not None]

    def add_aftn_slot(self, aftn_slot: SlotMessage) -> None:
        self.aftn_slots.append(aftn_slot)
        self.aftn_slots = [slot for slot in self.aftn_slots if slot is not None]


    def print_all_slot_messages(self) -> None:
        """
        Print all slots of flight divided by source of slot messages
        """
        print("B2B slots:")
        for b2b_slot in self.b2b_slots:
            print(b2b_slot.to_string())

        print()
        print("AFTN slots:")
        for aftn_slot in self.aftn_slots:
            print(aftn_slot.to_string())

    def get_slot_messages(self) -> [List[SlotMessage]|None, List[SlotMessage]|None]:
        """

        :return: array where on index 0 are B2B slots and on index 1 are AFTN slots
        """
        return [self.b2b_slots, self.aftn_slots]

    def get_b2b_messages(self) -> List[SlotMessage]|None:
        return self.b2b_slots

    def get_aftn_messages(self) -> List[SlotMessage] | None:
        print(self.aftn_slots)
        return self.aftn_slots
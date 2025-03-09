from typing import List

from common.models import SlotMessage


class Flight:
    def __init__(self, flight_id, b2b_slots, aftn_slots):
        self.flight_id = flight_id
        self.b2b_slots = b2b_slots
        self.aftn_slots = aftn_slots
        self.detection_failure = False
        self.slots_are_identical = False
        self.average_detection_time_diff = None

    def add_b2b_slot(self, b2b_slot: SlotMessage) -> None:
        self.b2b_slots.append(b2b_slot)
        self.b2b_slots = [slot for slot in self.b2b_slots if slot is not None]
        self.b2b_slots.sort(key=lambda slot: slot.slot_sent_timestamp)

    def add_aftn_slot(self, aftn_slot: SlotMessage) -> None:
        self.aftn_slots.append(aftn_slot)
        self.aftn_slots = [slot for slot in self.aftn_slots if slot is not None]
        self.aftn_slots.sort(key=lambda slot: slot.slot_sent_timestamp)

    def detect_failure(self, b2b_relative_file_paths: List[str], aftn_relative_file_paths: List[str]) -> None:
        if len(self.b2b_slots) > 0 and len(self.aftn_slots) > 0:
            return
        if len(self.b2b_slots) == 0:
            for file_path in b2b_relative_file_paths:
                if self.find_flight_id(file_path, self.flight_id) is True:
                    self.detection_failure = True
                    return
        if len(self.aftn_slots) == 0:
            for file_path in aftn_relative_file_paths:
                if self.find_flight_id(file_path, self.flight_id) is True:
                    self.detection_failure = True
                    break

    def find_flight_id(self, relative_file_path: str, ifplid: str) -> bool:
        with open(relative_file_path, 'r') as file:
            for line in file:
                if ifplid in line:
                    print("detected", ifplid, line)
                    return True
        return False

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

    def get_aftn_messages(self) -> List[SlotMessage]|None:
        print(self.aftn_slots)
        return self.aftn_slots

    # todo: should be done in more automatic way after all files have been parsed in order to not forget to call it
    def have_identical_slots(self) -> bool:
        aftn_messages = self.get_aftn_messages()
        b2b_messages = self.get_b2b_messages()

        if len(aftn_messages) != len(b2b_messages):
            self.slots_are_identical = False
            return False

        # check if each slot message have it's pair from second system
        checked_messages = []
        for aftn_key, aftn_message in aftn_messages:
            # skip slots which are not detected from B2B system
            if aftn_message.message_type == 'ACK':
                continue
            for b2b_key, b2b_message in b2b_messages:
                if aftn_message.message_type == b2b_message.message_type and b2b_key not in checked_messages:
                    checked_messages.append(b2b_key)
                    b2b_message.set_detection_diff(b2b_message.slot_sent_timestamp - aftn_message.slot_sent_timestamp)
                    break

        # not all messages have same type and therefore it's pair from second system
        if len(checked_messages) != len(aftn_messages):
            self.slots_are_identical = False
            return False

        total_detection_diff_for_flight = 0
        self.slots_are_identical = True
        for b2b_message in b2b_messages:
            if b2b_message.get_detection_diff() is not None:
                total_detection_diff_for_flight += b2b_message.get_detection_diff()
        self.average_detection_time_diff = total_detection_diff_for_flight / len(b2b_messages)

        return True


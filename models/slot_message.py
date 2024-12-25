# 2024-08-17 09:00:03 729 : AA62191784 : SAM : ctot = 2024-08-17 11:13

class SlotMessage:
    def __init__(self, slot_created_timestamp, message_type):
        self.slot_created_timestamp = slot_created_timestamp
        self.message_type = message_type

    def to_string(self):
        return "message type: " + self.message_type + ", timestamp: " + str(self.slot_created_timestamp)
    
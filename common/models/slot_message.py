from datetime import datetime, timezone

class SlotMessage:
    def __init__(self, slot_sent_timestamp: float, message_type: str):
        self.slot_sent_timestamp = slot_sent_timestamp
        self.message_type = message_type
        self.detection_time_diff_compared_to_aftn = None

    def __iter__(self):
        return iter((self.__hash__(), self))

    def __hash__(self):
        return hash((self.slot_sent_timestamp, self.message_type))  # Hash tuple of attributes

    def get_detection_diff(self) -> float|None:
        return self.detection_time_diff_compared_to_aftn

    def set_detection_diff(self, detection_diff: float) -> None:
        self.detection_time_diff_compared_to_aftn = detection_diff

    def to_string(self) -> str:
        # Convert timestamp to datetime in UTC
        dt = datetime.fromtimestamp(self.slot_sent_timestamp, tz=timezone.utc)

        # Format with milliseconds and UTC
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + ' UTC'
        string_value = ("type: " + self.message_type + ", sent at: " + formatted_time)
        if self.detection_time_diff_compared_to_aftn is not None:
            string_value += ", detection diff: " + str(round(self.detection_time_diff_compared_to_aftn, 2)) + "s"

        return string_value
from common.models import Flight


def get_flights_statistics(flights: dict[str, Flight]) -> object:
    number_of_flights = len(flights)
    if number_of_flights == 0:
        return {}

    average_detection_time_diff_compared_to_aftn = None
    number_of_parsing_failures = 0
    number_of_flights_with_identical_slots = 0
    for key, flight in flights.items():
        # todo: detect_failure could be optimized, it takes a lot of resources as it goes through all files for each slot message
        # flight.detect_failure(b2b_relative_paths, aftn_relative_paths)
        if flight.have_identical_slots():
            if average_detection_time_diff_compared_to_aftn is None:
                average_detection_time_diff_compared_to_aftn = 0
            number_of_flights_with_identical_slots += 1
            average_detection_time_diff_compared_to_aftn += flight.average_detection_time_diff

        if flight.detection_failure:
            number_of_parsing_failures += 1

    if average_detection_time_diff_compared_to_aftn is not None:
        average_detection_time_diff_compared_to_aftn =average_detection_time_diff_compared_to_aftn / number_of_flights

    b2b_messages_number = 0
    aftn_messages_number = 0
    for key, flight in flights.items():
        aftn_messages_number += len(flight.get_aftn_messages())
        b2b_messages_number += len(flight.get_b2b_messages())

    b2b_messages_number /= number_of_flights
    aftn_messages_number /= number_of_flights

    return {
        'number_of_flights': number_of_flights,
        'number_of_parsing_failures': number_of_parsing_failures,
        'number_of_flights_with_identical_slots': number_of_flights_with_identical_slots,
        'number_of_flights_with_identical_slots_relative': number_of_flights_with_identical_slots / number_of_flights * 100,
        'average_detection_time_diff': average_detection_time_diff_compared_to_aftn,
        'duplicate_slot_detection_number': get_number_duplicate_slot_detection(flights),
        'not_detected_slots_number': get_number_not_detected_slots(flights),
        'average_num_of_messages': {
            'b2b_messages_number': b2b_messages_number,
            'aftn_messages_number': aftn_messages_number,
        },
    }

def get_number_duplicate_slot_detection(flights: dict[str, Flight]) -> int:
    number = 0
    for key, flight in flights.items():
        aftn = flight.get_aftn_messages()
        aftn = [item for item in aftn if item.message_type != 'ACK']
        b2b = flight.get_b2b_messages()

        if len(b2b) > len(aftn):
            number += 1
    return number

def get_number_not_detected_slots(flights: dict[str, Flight]) -> int:
    number = 0
    for key, flight in flights.items():
        aftn = flight.get_aftn_messages()
        aftn = [item for item in aftn if item.message_type != 'ACK']
        b2b = flight.get_b2b_messages()

        if len(b2b) < len(aftn):
            number += 1
    return number

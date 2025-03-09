from common.models import Flight


def get_flights_statistics(flights: dict[str, Flight]) -> object:
    number_of_flights = len(flights)

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
        'average_detection_time_diff': average_detection_time_diff_compared_to_aftn / number_of_flights,
        'average_num_of_messages': {
            'b2b_messages_number': b2b_messages_number,
            'aftn_messages_number': aftn_messages_number,
        },
    }


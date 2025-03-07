from django.shortcuts import render

from common.slot_messages import SlotMessages
def home(request):
    b2b_relative_paths = ['b2b-1']
    aftn_relative_paths = ['aftn-1']
    slot_messages_difference = SlotMessages(b2b_relative_paths, aftn_relative_paths)
    slot_messages_difference.parse_slot_messages()
    flights = slot_messages_difference.get_flights()

    number_of_detection_failures = 0
    filtered_flights = []
    for key, flight in flights.items():
        flight.detect_failure(b2b_relative_paths, aftn_relative_paths)
        if flight.detection_failure:
            number_of_detection_failures += 1

        if len(flight.get_b2b_messages()) > 0 and len(flight.get_aftn_messages()) > 0:
            filtered_flights.append([key, flight])

    total_number = len(flights)
    number_of_flights_with_b2b_and_aftn_messages = len(filtered_flights)

    b2b_messages_number = 0
    aftn_messages_number = 0
    for key, flight in flights.items():
        aftn_messages_number += len(flight.get_aftn_messages())
        b2b_messages_number += len(flight.get_b2b_messages())


    b2b_messages_number /= total_number
    aftn_messages_number /= total_number
    #slot_messages_difference.print_flights()
    return render(request, 'home.html', {
        'flights': flights,
        'total_number': total_number,
        'number': number_of_flights_with_b2b_and_aftn_messages,
        'number_of_detection_failures': number_of_detection_failures,
        'average_num_of_messages': {
            'b2b_messages_number': b2b_messages_number,
            'aftn_messages_number': aftn_messages_number,
        },
    })
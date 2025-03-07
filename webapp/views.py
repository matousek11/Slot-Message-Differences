from django.shortcuts import render

from common.slot_messages import SlotMessages
def home(request):
    b2b_relative_paths = ['b2b-1']
    aftn_relative_paths = ['aftn-1']
    slot_messages_difference = SlotMessages(b2b_relative_paths, aftn_relative_paths)
    slot_messages_difference.parse_slot_messages()
    flights = slot_messages_difference.get_flights()
    slot_messages_difference.print_flights()
    return render(request, 'home.html', {'flights': flights})

    number_of_detection_failures = 0
    for key, flight in flights.items():
        flight.detect_failure(b2b_relative_paths, aftn_relative_paths)


    #slot_messages_difference.print_flights()
    })
import json
import os

from django.shortcuts import render

from common.services.statistics import get_flights_statistics
from common.slot_messages import SlotMessages
def home(request):
    b2b_relative_paths = ['b2b']
    aftn_relative_paths = ['aftn']

    json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'legends_data.json')
    with open(json_file_path, 'r') as legends_file:
        legends = json.load(legends_file)

    slot_messages_difference = SlotMessages(b2b_relative_paths, aftn_relative_paths)
    slot_messages_difference.parse_slot_messages()
    flights = slot_messages_difference.get_flights()

    statistics = get_flights_statistics(flights)

    return render(request, 'home.html', {
        'legends': legends,
        'flights': flights,
        'statistics': statistics
    })
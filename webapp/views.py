from django.http import HttpResponse
from django.shortcuts import render

from common.slot_messages import SlotMessages


def home(request):
    slot_messages_difference = SlotMessages('../SLOT Message/B2B/slots_17_msgs.txt', 'aftn')
    slot_messages_difference.parse_slot_messages()
    flights = slot_messages_difference.get_flights()
    slot_messages_difference.print_flights()
    return render(request, 'home.html', {'flights': flights})
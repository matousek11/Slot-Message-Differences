from slot_messages_difference import SlotMessagesDifference


slot_messages_difference = SlotMessagesDifference('../SLOT Message/B2B/slots_17_msgs.txt');
slot_messages_difference.parse_slot_messages()
slot_messages_difference.print_flights()

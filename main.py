from slot_messages import SlotMessages

slot_messages_difference = SlotMessages('../SLOT Message/B2B/slots_17_msgs.txt', '../SLOT Message/AFTN/a_aftnmsgs_17');
slot_messages_difference.parse_slot_messages()
slot_messages_difference.print_flights()

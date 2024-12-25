class Flight:
    def __init__(self, b2b_slots, aftn_slots):
        self.b2b_slots = b2b_slots
        self.aftn_slots = aftn_slots

    def add_b2b_slot(self, b2b_slot):
        self.b2b_slots.append(b2b_slot)

    def add_aftn_slot(self, aftn_slot):
        self.aftn_slots.append(aftn_slot)


    def print_all_slot_messages(self):
        print("B2B slots:")
        for b2b_slot in self.b2b_slots:
            print(b2b_slot.to_string())

        print()
        print("AFTN slots:")
        for aftn_slot in self.aftn_slots:
            print(aftn_slot.to_string())



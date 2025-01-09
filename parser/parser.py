class Parser:
    def __init__(self, relative_filepath):
        raise NotImplementedError('Child classes have to implement this method!')

    def parse_slot_messages(self, flights):
        raise NotImplementedError('Child classes have to implement this method!')
        
from datetime import datetime
from typing import List, TextIO, Dict

from .parser import Parser
from common.models.flight import Flight
from common.models.slot_message import SlotMessage

#At: 2024-08-17 00:00:05.008       INFO       Process: afp(15598036/26542530)       In: src/aftn_comm_mod.c/acm_recvGetOldestMsgFromDb()/1727       Subject: #ACM(OTHER)
#AFP process calls ``aftndb'' and receive following AFTN message:
#SEN001 170000
#FF LKPREPWC
#170000 EUCHZMFP
#-TITLE ACK -MSGTYP IARR -FILTIM 162359 -ORIGINDT 2408170000
#-BEGIN ADDR 
#       -FAC LKPREPWC
#-END ADDR 
#-IFPLID AA62237582
#-MSGTXT (ARR-TVS6EH-LGKO2115-LKPR0000)


#At: 2024-08-17 00:00:11.009       INFO       Process: afp(15598036/26542530)    In: src/aftn_comm_mod.c/acm_recvGetOldestMsgFromDb()/1727       Subject: #ACM(OTHER)
#AFP process calls ``aftndb'' and receive following AFTN message:
#SEN002 170000
#FF LKAAZFZX LKKVZTZX
#170000 LKPRZPZX
#(FPL-OKGUU02-VG
#-ULAC/L-Y/C
#-LKBE0615
#-N0065VFR DCT LKHV DCT LKPS DCT BEKTO DCT
#-LKCB0123 LKKV
#-DOF/240817 OPR/PISTEK LKBE PER/A RMK/PIC HYBNER TEL +420608756293
#)

# wanted ipflid, message type, timestamp

class AFTNParser(Parser):
    def __init__(self, relative_filepaths: List[str]):
        self.aftn_relative_paths = relative_filepaths

    def parse_slot_messages(self, flights: Dict[str, Flight]|Dict) -> None:
        """
        Parse AFTN messages file into separate AFTN slot message
        """
        for aftn_relative_path in self.aftn_relative_paths:
            with open(aftn_relative_path, 'r') as file:
                all_lines = file.readlines()
                last_line_index = len(all_lines) - 1
                last_line = all_lines[last_line_index]
                file.seek(0)  # reset pointer to start
                while True:
                    message = self.parse_aftn_slot_message(file, last_line)
                    if message is None:
                        break
                    result = self.get_slot_message(message)
                    if result is not None:
                        self.save_slot_message_to_flight(result[0], result[1], flights)

    def parse_aftn_slot_message(self, file: TextIO, last_line: str) -> List[str]|None:
        """
        Separate AFTN slot messages from AFTN slot messages file

        :param file: AFTN slot messages file
        :param last_line: last line of AFTN slot messages file
        :return: Lines of AFTN slot message or None if nothing found
        """
        number_of_empty_lines = 0
        message = []
        for line_number, line in enumerate(file):
            if line.isspace():
                number_of_empty_lines += 1
            if number_of_empty_lines > 1 or line == last_line:
                return message
            elif line.isspace():
                continue

            message.append(line)
            number_of_empty_lines = 0

    def get_slot_message(self, message: List[str]) -> List[str|SlotMessage]|None:
        """
        Take lines of AFTN slot message and parse it into IFPLID and SlotMessage object.

        :param message: lines with slot message in AFTN format
        :return: IFPLID and SlotMessage
        """
        result = [None, None, None]
        for line in message:
            if '-IFPLID' in line:
                result[0] = line.split(' ')[1]
            if 'Subject: ' in line:
                start_index = line.find('Subject: ') + len('Subject: ')
                result[1] = line[start_index:start_index + 3]
            if 'At: ' in line:
                start_index = line.find('At: ') + len('At: ')
                time = line[start_index:start_index + 23]
                result[2] = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f').timestamp()

        if result[0] is not None and result[1] is not None and result[2] is not None:
            return [result[0], SlotMessage(result[2], result[1])]
        return None
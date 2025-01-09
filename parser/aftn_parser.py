from datetime import datetime
from .parser import Parser
from models.flight import Flight
from models.slot_message import SlotMessage

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
    def __init__(self, relative_filepath):
        self.aftn_relative_path = relative_filepath

    def parse_slot_messages(self, flights):
        with open(self.aftn_relative_path, 'r') as file:
            message = self.get_one_message(file)
            if message:
                print(self.get_slot_message(message))
                
                
    def get_one_message(self, file):
        numberOfEmptyLines = 0
        message = []
        for line in file:
            if line.isspace():
                numberOfEmptyLines = numberOfEmptyLines + 1
                continue;
            elif numberOfEmptyLines > 1:
                return message

            print(message)
            message.append(line)
            numberOfEmptyLines = 0

    def get_slot_message(self, message):
        result = [None, None, None]
        for line in message:
            if '-IFPLID' in line:
                result[0] = line.split(' ')[1]
            if 'Subject: ' in line:
                startIndex = line.find('Subject: ') + len('Subject: ') - 3
                result[1] = line[startIndex:startIndex + 3]
            if 'At: ' in line:
                startIndex = line.find('At: ') + len('Subject: ')  - 3
                time = line[startIndex:startIndex + 21]
                result[2] = datetime.strptime(time, '%y-%m-%d %H:%M:%S.%f').timestamp()

        if result[0] and result[1] and result[2]:
            return [result[0], SlotMessage(result[2], result[1])]
        return None

                
                
        
                


            
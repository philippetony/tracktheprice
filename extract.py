import re
import os
from pathlib import Path
from model import Ticket, ArticlePrice
import datetime

target_path=Path('data')
single_line_systeme_u_pattern = ' *([A-Z0-9 ./()&%-]+) +([0-9,]+) € +[0-9]+ *$'
multi_line_systeme_u_pattern = ' *(\d+) +x +([0-9,]+) € +([0-9,]+) € +[0-9]+ *$'

def extract_systeme_u(target):
    res = []
    for item in os.listdir(target):
        if item.endswith('.txt'):
            parsed_ticket = Ticket()
            with open(target/item, 'r') as ticket:
                lines = ticket.readlines()
                for line_number, line in enumerate(lines):
                    if match := re.match(single_line_systeme_u_pattern, line):
                        fusion_groups = [x.strip() for x in match.groups()]
                        parsed_ticket.prices.append(ArticlePrice(fusion_groups[0], float(fusion_groups[1].replace(',','.'))))
                    elif match := re.match(multi_line_systeme_u_pattern, line):
                        fusion_groups=[lines[line_number-1].strip(), match.groups()[1]]
                        parsed_ticket.prices.append(ArticlePrice(fusion_groups[0], float(fusion_groups[1].replace(',','.'))))
                    elif (date_match := re.search("(\d{2}\/\d{2}\/\d{2})", line)) and (re.search("Date", lines[line_number-1])):
                        parsed_ticket.date = datetime.datetime.strptime(date_match.group(0), "%d/%m/%y").date()
            res.append(parsed_ticket)
    return res
                        

if __name__ == '__main__':
    tickets = extract_systeme_u(target_path)
    print(tickets)
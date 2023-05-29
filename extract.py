import re
import os
from pathlib import Path
from model import Ticket, ArticlePrice
import datetime

temp_path = Path('temp')
single_line_systeme_u_pattern = ' *([A-Z0-9 .,/()&%-]+) +([0-9,]+) € +[0-9]+ *$'
multi_line_systeme_u_pattern = ' *(\d+) +x +([0-9,]+) € +([0-9,]+) € +[0-9]+ *$'

single_line_lidl_pattern = ' *([\w\d ./()&%-]+) +([0-9,]+) [xX]+ ([0-9]+) ([0-9,]+) [AB] *$'


def extract_systeme_u(target):
    res = []
    for item in os.listdir(target):
        if item.endswith('.u.txt'):
            parsed_ticket = Ticket()
            parsed_ticket.store_name = "U"
            with open(target/item, 'r') as ticket:
                lines = ticket.readlines()
                parsed_ticket.store_city = " ".join([x.strip() for x in lines[:4]])
                current_category = None
                for line_number, line in enumerate(lines):
                    if match := re.match(">>>> (.*)", line.strip()):
                        current_category = match.group(1)
                    if match := re.match(single_line_systeme_u_pattern, line):
                        fusion_groups = [x.strip() for x in match.groups()]
                        parsed_ticket.prices.append(ArticlePrice.of(
                            fusion_groups[0], float(fusion_groups[1].replace(',', '.')), current_category))
                    elif match := re.match(multi_line_systeme_u_pattern, line):
                        fusion_groups = [lines[line_number-1].strip(), match.groups()[1]]
                        parsed_ticket.prices.append(ArticlePrice.of(
                            fusion_groups[0], float(fusion_groups[1].replace(',', '.')), current_category))
                    elif (date_match := re.search("(\d{2}\/\d{2}\/\d{2})", line)) and (re.search("Date", lines[line_number-1])):
                        parsed_ticket.date = datetime.datetime.strptime(date_match.group(0), "%d/%m/%y").date()
            res.append(parsed_ticket)
    return res


def extract_lidl(target):
    res = []
    for item in os.listdir(target):
        if item.endswith('.lidl.txt'):
            parsed_ticket = Ticket()
            parsed_ticket.store_name = "Lidl"
            with open(target/item, 'r') as ticket:
                lines = ticket.readlines()
                for line_number, line in enumerate(lines):
                    if match := re.match(single_line_lidl_pattern, line):
                        fusion_groups = [x.strip() for x in match.groups()]
                        parsed_ticket.prices.append(ArticlePrice.of(fusion_groups[0], float(
                            fusion_groups[1].replace(',', '.'))))
                    if (match := re.match(" *Rem ([\w\d ./()&%-]+) *(-[0-9,]+)", line)) and len(parsed_ticket.prices) > 0:
                        parsed_ticket.prices[-1].price += float(match.group(2).replace(',', '.'))
                    elif (date_match := re.search("(\d{2}.\d{2}.\d{2}) \d{2}:\d{2}:\d{2}", line)):
                        parsed_ticket.date = datetime.datetime.strptime(date_match.group(1), "%d.%m.%y").date()
                    if parsed_ticket.store_city is None and (match := re.search("\d{5}\w+", line)):
                        parsed_ticket.store_city = match.group(0)
            res.append(parsed_ticket)
    return res


if __name__ == '__main__':
    tickets = []
    tickets += extract_systeme_u(temp_path/"u")
    # tickets += extract_lidl(temp_path/"lidl")
    print(tickets)

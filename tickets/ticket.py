# coding:utf-8

"""
Usage:
    ticket [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    ticket 北京　上海　2017-10-10
    ticket -dg 成都　南京　2017-10-10
"""
from prettytable import PrettyTable
from docopt import docopt
import re
import requests
from colorama import Fore

with open('station_name.txt', 'r', encoding='utf-8') as f:
    content = f.read()
result = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', content)
stations = dict(result)


def cli():
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicket' \
          'DTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    r = requests.get(url, verify=False)
    available_trains = r.json()['data']
    TraninsCollection(available_trains, options).pretty_print()


class TraninsCollection(object):
    headers = "车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座".split()

    def __init__(self, available_trains, options):
        self.available_tranins = available_trains
        self.options = options

    def _color_print(self, item, color):
        return color + item + Fore.RESET

    def parser_time(self, time):
        time_list = time.split(':')
        result = list(map(str, map(int, time_list)))
        return result[0] + '时' + result[1] + '分'

    @property
    def trains(self):
        for item in self.available_tranins['result']:
            item = item.split("|")
            item = list(map(lambda x: x.replace('', '--') if x == '' else x, item))
            train_no = item[3]
            if not self.options or item[3].lower()[0] in self.options:
                start_station = self.available_tranins['map'].get(item[6])
                end_station = self.available_tranins['map'].get(item[7])
                departure = item[8]
                arrival = item[9]
                duration = self.parser_time(item[10])
                yideng = item[-4]
                erdeng = item[-5]
                ruanwo = item[23]
                yingwo = item[-7]
                yingzuo = item[-6]
                wuzuo = item[26]
                row = [train_no,
                       '\n'.join(['始　'+self._color_print(start_station, Fore.YELLOW),
                                  '终　'+self._color_print(end_station, Fore.GREEN)]),
                       '\n'.join([self._color_print(departure, Fore.YELLOW),
                                  self._color_print(arrival, Fore.GREEN)]),
                       duration, yideng, erdeng, ruanwo, yingwo, yingzuo, wuzuo]
                yield row

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.headers)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


if __name__ == '__main__':
    cli()

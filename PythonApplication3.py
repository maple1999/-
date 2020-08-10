import requests
from lxml import etree
import time
import csv
import re
header = ['时间', '场内待运车辆数', '前半小时进场车辆数', '前半小时离场车辆数']
with open('./taxi_info_xzjc.csv', encoding='UTF-8', mode='w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(header)
f.close()
 
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
 
def save_data(data):
    with open('./taxi_info_xzjc.csv', encoding='UTF-8', mode='a+') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(data)
    f.close()
def get_info(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        selector = etree.HTML(res.text)
        at_time = selector.xpath('//*[@id="Label_Msg"]/text()[3]')[0][7:].rstrip('）').lstrip()
        car_num_in_room = selector.xpath('//*[@id="Label_Msg"]/text()[5]')[0]
        car_num_in_room_num = re.search(r"\d+", car_num_in_room).group()
        before_half_hour_in_car = selector.xpath('//*[@id="Label_Msg"]/text()[7]')[0]
        before_half_hour_in_car_num = re.search(r"\d+", before_half_hour_in_car).group()
        before_half_hour_out_car = selector.xpath('//*[@id="Label_Msg"]/text()[9]')[0]
        before_half_hour_out_car_num = re.search(r"\d+", before_half_hour_out_car).group()
        tup = (at_time, car_num_in_room_num, before_half_hour_in_car_num, before_half_hour_out_car_num)
        save_data(tup)
 
 
if __name__ == '__main__':
    url = "http://www.whalebj.com/xzjc/default.aspx?tdsourcetag=s_pctim_aiomsg"
    while 1:
        get_info(url)
        time.sleep(10)
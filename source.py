#!/usr/bin/env python
# coding=utf-8


import requests
from bs4 import BeautifulSoup as BS
import json
import time
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')


while(True):
    try:
        r = requests.get('https://3g.dxy.cn/newh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0')
        soup = BS(r.content, 'html.parser')
        _cn_data = soup.find('script',id='getStatisticsService').get_text()
        _s = _cn_data.index('{', _cn_data.index('{')+1)
        _e = _cn_data.index('catch')-1
        _china = json.loads(_cn_data[_s:_e])
        _timestamp = _china['modifyTime']
        _cc,_sc,_dc,_cuc = _china['confirmedCount'],_china['suspectedCount'],_china['deadCount'],_china['curedCount']
        print _timestamp,_cc,_sc,_dc,_cuc
        if open('data_new/湖北省.csv').readlines()[-1].split(',')[0]==str(_timestamp):
        #if False:
            print('data not flush')
        else:
            #row = 'timestamp,confirmedCount,suspectedCount,curedCount,deadCount'
            #os.system('echo '+row+' >> data_new/中国.csv')
            row = ','.join([str(_timestamp),str(_cc),str(_sc),str(_cuc),str(_dc)])
            os.system('echo '+row+' >> data_new/中国.csv')
            _data = soup.find('script',id='getAreaStat').get_text()
            _data =  _data[_data.find('['):_data.rfind(']')+1]
            _provinces = json.loads(_data)
            for _province in _provinces:
                print _timestamp,_province['provinceName'],_province['provinceShortName'],_province['confirmedCount'],_province['suspectedCount'],_province['curedCount'],_province['deadCount'],len(_province['cities'])
                _fn = _province['provinceName']+'.csv'
                #row = 'timestamp,provinceName,cityName,confirmedCount,suspectedCount,curedCount,deadCount,locationId'
                #os.system('echo '+row+' >> data_new/'+_fn)
                for _city in _province['cities']:
            	    row = ','.join([str(_timestamp),_province['provinceName'],_city['cityName'],str(_city['confirmedCount']),str(_city['suspectedCount']),str(_city['curedCount']),str(_city['deadCount']),str(_city['locationId'])])
            	    os.system('echo '+row+' >> data_new/'+_fn)
    except Exception as e:
        print(e)

    time.sleep(60*10) # 10分钟flush一次

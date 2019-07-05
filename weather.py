import os
import requests
import urllib3
import json
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

current_dir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(current_dir, '.tmp')

def weather(location):
    base_url = "https://free-api.heweather.net/s6/weather/now"
    params = {
        'location': location,
        'key': 'aff0d0ec0ee4457ca4ba704e060a1e58'
    }
    last_update_time = 0.0
    if os.path.exists(data_file):
        with open(data_file, 'rb+') as f:
            content = f.read()
            if content:
                data_json = json.loads(content, encoding='utf-8')
                last_update_time = data_json['last_update_time']                
        if last_update_time + 30.0 * 60.0 <= time.mktime(time.localtime()):
            try:
                result_json = requests.get(url=base_url, params=params, verify=False).json()[
                    'HeWeather6'][0]
                with open(data_file, 'wb+') as f:
                    f.write(json.dumps({'last_update_time': time.mktime(time.localtime()), 'result': result_json}).encode('utf-8'))
                    f.flush()
            except Exception as e:
                os.remove(data_file)
                result_json = None
        else:
            result_json = data_json['result']
    else:
        try:
            result_json = requests.get(url=base_url, params=params, verify=False).json()[
                'HeWeather6'][0]
            with open(data_file, 'wb+') as f:
                f.write(json.dumps({'last_update_time': time.mktime(time.localtime()), 'result': result_json}).encode('utf-8'))
                f.flush()
        except Exception as e:
            os.remove(data_file)
            result_json = None
    return result_json


def parse(result):
    current_time = time.localtime()
    current_hour = int(time.strftime('%H', current_time))
    if result:
        basic = result['basic']
        location = basic['location']
        update = result['update']['loc']
        status = result['now']
        cond_code = status['cond_code']
        cond_text = status['cond_txt']
        tmp = status['tmp']
        wind_sc = status['wind_sc']
        wind_dir = status['wind_dir']
        if (current_hour < 7 or current_hour > 19) and os.path.exists(os.path.join(current_dir, str(cond_code) + 'n.png')):
            cond_pic = os.path.join(current_dir, str(cond_code) + 'n.png')
        else:
            cond_pic = os.path.join(current_dir, str(cond_code) + '.png')
        print('${image ' + cond_pic + ' -p 35,435 -s 50x50 -f 86400}${offset 100}${color FF7878}' + location + '区 ' + cond_text)
        print('${offset 100}${color grey}${font WenQuanYi Micro Hei:bold:size=10}' + str(tmp) + '°C ' + wind_dir + '' + wind_sc + '级')
        print('${offset 30}更新时间：' + update)
    else:
        print('${offset 70}${color grey}${font WenQuanYi Micro Hei:bold:size=10}当前服务不可用')


if __name__ == "__main__":
    parse(weather('370602'))

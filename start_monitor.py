"""
For demo pi controlled by slack

__author__="Alex Xiao"
__date__="2019-10-10"
__version__="0.1"
"""
from common import *
from selenium import webdriver
from datetime import datetime, timedelta
import time
import traceback
import logging

class Monitor:
    def __init__(self, input_file_name=dataset_file):
        self.input_file_name = input_file_name
        self.running = None
        self.output_file = None
        # self.driver = webdriver.Chrome()
        desired_capabilities = {}
        desired_capabilities['chromeOptions'] = {
            "args": ["--disable-extensions"],
            "extensions": []
        }
        self.driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        self.timeformat = '%Y-%m-%d %H:%M:%S'
        self.interval = 10
        self.driver.fullscreen_window()
        os.system('xset dpms force off') 
            
    
    def form_time(self, time_part, now, delta=None):
        standard = '00:00:00'
        t = datetime.strptime(now.strftime(self.timeformat)[:11] + time_part + standard[len(time_part):], self.timeformat)
        if delta:
            t += delta
        return t
    
    def build_file(self, info, template_file = 'templates/template.html'):
        filename = base_dir + 'display.html'        
        with open('/opt/demo_flight/' +template_file, "r") as t:
            temp = t.readlines()

            def fill(text, src, val):
                return [x.replace(src, val) for x in text]

            temp = fill(temp, '#DEST#', info['Destination'])
            temp = fill(temp, '#FLIGHT#', info['Flight'])
            temp = fill(temp, '#TIME#', info['time'].strftime(self.timeformat))
            temp = fill(temp, '#C_TEXT_SIZE#', info.get('COUNT_TEXT_SIZE', '60'))
            temp = fill(temp, '#S_TEXT_SIZE#', info.get('DESC_TEXT_SIZE', '60'))
            temp = fill(temp, '#H1_SIZE#', info.get('HEAD_TEXT_SIZE', '100'))
            with open(filename, 'w') as w:
                w.writelines(temp)
        return 'file:///' + filename

    def run(self):
        dataset = read_source(self.input_file_name, flight_schema)
        params = {x['Name'].upper(): x['Val'] for x in read_source(param_file, param_schema).to_dict(orient='records')}
        start_delta = -60 * int(params.get('AHEAD', '40'))
        end_delta = 60 * int(params.get('AFTER', '5'))
        self.interval = int(params.get('REFRESH_INTERVAL', '10'))
        now = datetime.now()
        dataset['time'] = dataset['Cutoff'].apply(lambda x:self.form_time(x, now))
        dataset['time_start'] = dataset['Cutoff'].apply(lambda x:self.form_time(x, now, timedelta(seconds=start_delta)))
        dataset['time_end'] = dataset['Cutoff'].apply(lambda x:self.form_time(x, now, timedelta(seconds=end_delta)))
        a_list = dataset[(dataset['time_start'] <= now)&(dataset['time_end'] > now )].sort_values(['time_start'])
        # if len(a_list) > 1:
        #    # multi records overlaps
        #    a_list = a_list[a_list['time'] >= now]
        #    print('Filter overlaps')
        print(now, a_list)
        logging.debug(str(a_list))
        if len(a_list) > 0: # and self.running is None:
            # get the 1st
            current = a_list.iloc[0].to_dict()
            new_flg = False
            if self.running is None:
                new_flg = True
            else:
                # need to deal with overlaps
                pass
            
            if new_flg:            
                print(now, current)
                self.driver.get(self.build_file({**current, **params}))
                self.driver.refresh()
                self.running = current          
                os.system('xset dpms force on') # trun screen on
                logging.info('Turn Screen On')
        else:
            if self.running is not None:
                # if self.driver:
                #     self.driver.close()
                # self.driver = None
                self.driver.get(self.build_file(self.running, template_file='templates/template_blank.html'))
                self.driver.refresh()
                self.running = None
                print(now, 'Turning off display')
                logging.info('Turn Screen Off')
                os.system('xset dpms force off') # blank screen
        
if __name__== '__main__':
    m = Monitor(dataset_file)
    # poll forever
    print('Start polling forever!')
    while True:
        try:
            m.run()
        except:
            traceback.print_exc()
        time.sleep(m.interval)
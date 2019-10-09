"""
For demo pi controlled by slack

__author__="Alex Xiao"
__date__="2019-10-10"
__version__="0.1"
"""

import slack
import time
import os
import pandas
import sys
import traceback
from common import *

def save(dataset, name=dataset_file):
    dataset.to_csv(name, index=False)

def del_flight(dataset, flight):
    return dataset[dataset['Flight'] !=  flight.upper()]

def process(cmd):
    rtn = 'Unable to process'
    dataset = read_source(dataset_file, flight_schema)
    dataset['Flight'] = dataset['Flight'].apply(lambda x:x.upper())
    if ' ' in cmd:
        cmd_key, cmd_val = cmd.split(' ', maxsplit=1)
    else:
        cmd_key, cmd_val = cmd, None
    cmd_key = cmd_key.lower()
    if cmd_key == 'list':
        if len(dataset) < 1:
            rtn = 'Please set flight list <FLGHT_NAME> <DESTINATION> <CUTOFF_TIME> <CLEAR_TIME>'
        else:
            rtn = dataset.to_string(index=False)
    elif cmd_key == 'set':
        fname, dest, cutt, ct = cmd_val.split()
        if fname.upper() in dataset['Flight'].to_list():
            # remove existing
            dataset = del_flight(dataset, fname)
        # add a new
        dataset = dataset.append([{"Flight": fname.upper(), "Destination": dest.upper(),
                                   "Cutoff": cutt, "Cleardown": ct}, ])
        save(dataset)
        rtn = f'Set {fname} to: {dest}, {cutt}, {ct}'
    elif cmd_key == 'del':
        fname = cmd_val
        if fname.upper() in dataset['Flight'].to_list():
            # existing
            dataset = del_flight(dataset, fname)
            rtn = f'Deleted fight {fname}'
            save(dataset)
        else:
            # raise error
            rtn = f'Unknown flight {fname}, cannot remove'
    elif cmd_key == 'param':
        name, val = cmd_val.split(maxsplit=1)
        params = read_source(param_file, param_schema)
        params = params[params['Name'] != name.upper()]
        params = params.append([{'Name': name.upper(), "Val": val}])
        save(params, param_file)
        rtn = params.to_string(index=False)
    elif cmd_key == 'del_param':
        params = read_source(param_file, param_schema)
        params = params[params['Name'] != cmd_val.upper()]
        save(params, param_file)
        rtn = f'Removed parameter: {cmd_val}'
    elif cmd_key == 'hot_fix_code':
        os.system('/opt/demo_flight/apply_hot_fix.sh')
        rtn = 'Applied Hot Fix Code'
    return rtn

    
@slack.RTMClient.run_on(event='hello')
def hello(**payload):
    print("Bot is up running")
    web_client = payload['web_client']
    web_client.chat_postMessage(
                channel=channel,
                text='I am online! Ready to display flight info')
    
@slack.RTMClient.run_on(event='message')
def listen(**payload):
    data = None
    try:
        data = payload['data']
        channel_id = data['channel']
        if channel_id == channel_id and data.get('subtype','user') != 'bot_message':
            cmd = data['text']
            user = data['user']
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data['ts'])))
            print(f'Received {cmd} from {user} @ {ts}') 
            web_client = payload['web_client']
            try:
                processed = process(cmd)
            except:
                processed = 'Uanble to process'
            web_client.chat_postMessage(
                channel=channel_id,
                text=processed)
    except:
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print('Failed @' + t)
        print(data)
        traceback.print_exc()

if __name__== '__main__':
    rtm_client = slack.RTMClient(token=slack_token, auto_reconnect=True)
    rtm_client.start()
    

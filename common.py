"""
For demo pi controlled by slack

__author__="Alex Xiao"
__date__="2019-10-10"
__version__="0.1"
"""

import pandas
import os

slack_token = os.environ['SLACK_TOKEN']
channel= os.environ['SLACK_CHANNEL']
base_dir = os.environ['DEMO_BASE']
dataset_file = base_dir + 'flight.list'
param_file = base_dir + 'parameters.list'
template_dir = base_dir + 'templates/'
flight_schema =[{"Flight":"Test", "Destination":"Test",
                  "Cutoff": "00:00:00", "Cleardown": "00:00:00"
                     },]
param_schema = [{'Name':"Name", "Val": "Val"}, ]

def read_source(file_name, default_schema):
    try:
        dataset = pandas.read_csv(file_name)
    except:
        dataset = pandas.DataFrame(default_schema).head(0)
    return dataset

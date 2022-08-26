import blessed
import json
import ldclient
from ldclient.config import Config
import os
from prettytable import PrettyTable as pt
import sys
import time
import unicodedata
from utils.create_user import random_ld_user
from dotenv import load_dotenv

'''
Create a terminal and clear it
'''
term = blessed.Terminal()
print(term.clear)

'''
Set sdk_key and feature_flag_key to your LaunchDarkly keys, then initialize the LD client
'''
load_dotenv()
sdk_key = os.environ.get('SDK_KEY')
feature_flag_key = os.environ.get('FLAG_KEY')
ldclient.set_config(Config(sdk_key))

'''
Define symbols for the table
'''
true_icon = unicodedata.lookup('WHITE HEAVY CHECK MARK')
false_icon = unicodedata.lookup('CROSS MARK')

'''
Create fake targets for this exercise
'''
def create_targets():
    num_targets = 15
    users_array = {'users':[]}
    for i in range(num_targets):
        # f = open('data/targets.json', 'w')
        user = random_ld_user()
        users_array['users'].append(user)
        with open('data/targets.json', 'w') as f:
            json.dump(users_array, f)

'''
Adds targets to the table
'''
def add_targets_to_table(data):
    target_table = pt()
    # print(term.clear)
    target_table.field_names = ['key', 'firstName', 'lastName', 'version', 'plan', 'lang', '?']
    for i in data['users']:
        feature = ldclient.get().variation("toms-beautiful-feature", i, False)
        if feature:
            feature = true_icon
        else:
            feature = false_icon
        target_table.add_row([i['key'][0:5] + '...', i['firstName'], i['lastName'], i['custom']['version'], i['custom']['plan'], i['custom']['lang'], str(feature)])
    return target_table


'''
Clears the terminal, then renders the table
'''
def render_table(table):
    # with term.location(0, term.height - 1):
    with term.hidden_cursor():
        print(term.home + term.clear, end='')
        print(table)


'''
Persistent loop that keeps rerendering the table multiple times per second
'''
if __name__ == '__main__':
    create_targets()
    data = json.load(open("data/targets.json"))
    while True:
        table = add_targets_to_table(data)
        render_table(table)
        time.sleep(.01)

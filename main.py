import blessed
from dotenv import load_dotenv
import json
import ldclient
from ldclient.config import Config
import os
import time
import unicodedata
from utils.create_context import *

'''
Get environment variables
'''
load_dotenv()

'''
Create a terminal and clear it
'''
term = blessed.Terminal()
print(term.clear, end='')


'''
Set sdk_key and feature_flag_key to your LaunchDarkly keys, then initialize the LD client. These keys are pulled from your Replit environment variables, AKA secrets.
'''
sdk_key = os.environ.get('SDK_KEY')
feature_flag_key_1 = os.environ.get('FLAG_KEY_1')
feature_flag_key_2 = os.environ.get('FLAG_KEY_2')
feature_flag_key_3 = os.environ.get('FLAG_KEY_3')
ldclient.set_config(Config(sdk_key,send_events=False))


'''
Define symbols for the table
'''
none_icon = unicodedata.lookup('WHITE LARGE SQUARE')
flag_key_1_icon = unicodedata.lookup('BLACK LARGE SQUARE')
flag_key_2_icon = unicodedata.lookup('LARGE BLUE SQUARE')
flag_key_3_icon = unicodedata.lookup('LARGE YELLOW SQUARE')
conflict_icon = unicodedata.lookup('CROSS MARK')


'''
Create fake targets for this exercise
'''
def create_contexts():
    num_contexts = 2000
    contexts_array = []
    for i in range(num_contexts):
        context = create_multi_context()
        contexts_array.append(context)
    return contexts_array


'''
Add targets to the table
'''
def add_targets_to_table(data):
    context_table = []

    for i in data:
        feature_1 = ldclient.get().variation(feature_flag_key_1, i, False)
        feature_2 = ldclient.get().variation(feature_flag_key_2, i, False)
        feature_3 = ldclient.get().variation(feature_flag_key_3, i, False)

        values_array = [feature_1, feature_2, feature_3]
        true_count = values_array.count(True)
        
        if true_count > 1:
            icon = conflict_icon
        elif feature_1:
            icon = flag_key_1_icon
        elif feature_2:
            icon = flag_key_2_icon
        elif feature_3:
            icon = flag_key_3_icon
        else:
            icon = none_icon

        context_table.append(icon)
        
    return context_table


'''
Clears the terminal, then renders the table
'''
def render_table(table):
    with term.hidden_cursor():
        print(term.home + term.clear, end='')
        print(term.clear, end='')
        # print(table)
        for i in table:
            print(i, end = '')

'''
Defines what the listener should do when a flag change occurs
'''
def flag_change_listener(flag_change):
    table = add_targets_to_table(data)
    render_table(table)


if __name__ == '__main__':
    data = create_contexts()
    flag_change_listener(data)
    listener = ldclient.get().flag_tracker.add_listener(flag_change_listener)
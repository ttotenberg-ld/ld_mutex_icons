import blessed
import json
import ldclient
from ldclient.config import Config
import os
from prettytable import PrettyTable as pt
import time
import unicodedata
from utils.create_user import random_ld_user


'''
Create a terminal and clear it
'''
term = blessed.Terminal()
print(term.clear)


'''
Set sdk_key and feature_flag_key to your LaunchDarkly keys, then initialize the LD client
'''
sdk_key = os.environ['SDK_KEY']
feature_flag_key = os.environ['FLAG_KEY']
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
    num_targets = 40
    users_array = {'users': []}
    for i in range(num_targets):
        user = random_ld_user()
        users_array['users'].append(user)
        with open('data/targets.json', 'w') as f:
            json.dump(users_array, f)


'''
Adds targets to the table
'''
def add_targets_to_table(data):
    target_table = pt()
    target_table.field_names = [
        'key', 'name', 'version', 'plan', 'region', 'Targeted?'
    ]
    for i in data['users']:
        feature = ldclient.get().variation(feature_flag_key, i, False)
        if feature:
            feature = true_icon
        else:
            feature = false_icon
        target_table.add_row([
            i['key'][0:8] + '...', i['name'], i['custom']['version'], i['custom']['plan'], i['custom']['region'], str(feature)
        ])
    return target_table


'''
Clears the terminal, then renders the table
'''
def render_table(table):
    with term.hidden_cursor():
        print(term.home + term.clear, end='')
        print(table)


'''
OK, word of warning: Everything below is pretty hacky. :)
Ideally, I wanted to subscribe to flag changes and render the table only when there was an update. However, once I was mostly done creating this, I realized the Python SDK doesn't have that functionality yet! (as of fall 2022)

https://docs.launchdarkly.com/sdk/features/flag-changes

So instead, I'm saving an array of trues/falses for each target user, updating that array multiple times per second based on the latest targeting data from LaunchDarkly, and re-rendering the table if that has been updated.

Don't judge me! It's hacky but it works!
'''
if __name__ == '__main__':
    # Uncomment the line below and rerun the script if you want to generate new targets
    # create_targets()
    data = json.load(open("data/targets.json"))
    target_array = [False]
    new_target_array = []
    while True:
        new_target_array = []
        for i in data['users']:
            feature = ldclient.get().variation(feature_flag_key, i, False)
            new_target_array.append(feature)
        if target_array != new_target_array:
            table = add_targets_to_table(data)
            render_table(table)
            target_array = new_target_array
            new_target_array = []
        time.sleep(.1)
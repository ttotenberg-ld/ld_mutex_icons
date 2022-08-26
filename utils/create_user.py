import names
import random
import uuid


'''
Construct and return a random user
'''
def random_ld_user():
    key = str(uuid.uuid4())
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    plan = random.choice(['platinum', 'silver', 'gold', 'diamond'])
    version = random.choice(['1.0.2', '1.0.4,', '1.0.7', '1.1.0', '1.1.5'])
    lang = random.choice(['EN', 'CN', 'SP', 'IN', 'GR'])

    user = {
        "key": key,
        "firstName": first_name,
        "lastName": last_name,
        "custom": {
          "plan": plan,
          "version": version,
          "lang": lang
        }
    }
    return user
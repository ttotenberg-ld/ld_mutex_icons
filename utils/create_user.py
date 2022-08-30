import names
import random
import uuid


'''
Construct and return a random user
'''
def random_ld_user():
    key = str(uuid.uuid4())
    name = f'{names.get_first_name()} {names.get_last_name()}'
    plan = random.choice(['platinum', 'silver', 'gold', 'diamond'])
    version = random.choice(['1.0.2', '1.0.4', '1.0.7', '1.1.0', '1.1.5'])
    region = random.choice(['NA', 'CN', 'EU', 'IN', 'SA'])

    user = {
        "key": key,
        "name": name,
        "custom": {
          "plan": plan,
          "version": version,
          "region": region
        }
    }
    return user
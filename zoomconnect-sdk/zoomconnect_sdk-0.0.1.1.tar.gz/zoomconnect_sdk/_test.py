import os
from client import Client

c = Client(api_token=os.getenv('token'), account_email=os.getenv('email'))
try:
    # message = c.create_contact("Lambo","Steyn","0828548929","Mnr")
    # contact = c.update_contact("5eeb23edc0fa4d7d7d19ba1f","Lambrie","Steyn","0828548929",None)
    # contact = c.get_contacts_all()
    # groups = c.get_groups_all()
    add = c.add_contact_to_group("5eeb23edc0fa4d7d7d19ba1f","5eeb25d3c0fa4d7d7d19bb69")

except Exception as e:
    print(e)
else:
    # print(f"{contact}")
    # print(f"{groups}")
    print(f"{add}")
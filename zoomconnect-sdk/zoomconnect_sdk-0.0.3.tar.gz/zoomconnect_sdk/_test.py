import os
from client import Client

c = Client(api_token=os.getenv('token'), account_email=os.getenv('email'))
try:
    # result = c.create_contact("Lambo","Steyn","0828548929","Mnr")
    # result = c.update_contact("5eeb23edc0fa4d7d7d19ba1f","Lambrie","Steyn","0828548929",None)
    # result = c.get_contacts_all()
    # result = c.get_groups_all()
    # result = c.add_contact_to_group("5eeb23edc0fa4d7d7d19ba1f","5eeb25d3c0fa4d7d7d19bb69")
    # result = c.get_contact("5eeb23edc0fa4d7d7d19ba1f")
    result = c.delete_contact("5eeb23edc0fa4d7d7d19ba1f")


except Exception as e:
    print(e)
else:
    print(f"{result}")
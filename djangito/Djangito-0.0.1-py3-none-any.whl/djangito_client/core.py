# "core.py" contains pure functions i.e., no side effects
def extract_foreign_key_data(user_data):
    foreign_key_list = []
    for x in user_data:
        if type(user_data[x]) == dict:
            foreign_key_list.append(x)

    string_data = {x: user_data[x] for x in
                   set(user_data) - set(foreign_key_list)}
    foreign_key_data = {x: user_data[x] for x in foreign_key_list}
    string_data['server_id'] = string_data['id']
    del string_data['id']
    for x in foreign_key_data:
        foreign_key_data[x]['server_id'] = foreign_key_data[x]['id']
        del foreign_key_data[x]['id']
    return string_data, foreign_key_data

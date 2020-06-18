def get_url(text):
    if text == None:
        return None
    urls = re.findall(r'http[s]?://[a-zA-Z0-9\_\-]+\.[:.a-zA-Z0-9/\_\-]+', text)
    return urls

def get_user(user_list,msg):
    chat_id_temp = re.findall('@[a-zA-Z0-9\_\.\-]+', msg)
    for user in chat_id_temp:
        user_list.append(user)
def get_domain(text):
    domain_groups = re.search(
                r"(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?", text)
    return domain_groups
def get_facebook(user_list,msg):
    if "facebook.com/groups/" in msg:
        chat_id_temp = re.findall('facebook.com/groups/[a-zA-Z0-9\_\.\-]+', msg)
        for user in chat_id_temp:
            user_list.append(user)
    else:
        chat_id_temp = re.findall('facebook.com/[a-zA-Z0-9\_\.\-]+', msg)
        for user in chat_id_temp:
            user_list.append(user)
def get_twitter(user_list,msg):
    chat_id_temp = re.findall('twitter.com/[a-zA-Z0-9\_\.\-]+', msg)
    for user in chat_id_temp:
        user_list.append(user)
def get_tg(user_list,msg):
    if "t.me/joinchat/"  in msg:
        chat_id_temp = re.findall('t\.me/joinchat/[a-zA-Z0-9]+', msg)
        for user in chat_id_temp:
            user_list.append(user)
    else:
        chat_id_temp = re.findall('t\.me/[a-zA-Z0-9\_\.\-]+', msg)
        for user in chat_id_temp:
            user_list.append(user)
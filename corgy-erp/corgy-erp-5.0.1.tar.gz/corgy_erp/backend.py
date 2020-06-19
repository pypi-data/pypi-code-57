from django.contrib import messages, get_messages

def post_message(request):
    messages.add_message(request, messages.INFO, 'Hello world.')
    return True

def get_messages(request):

    storage = get_messages(request)
    for message in storage:
        do_something_with_the_message(message)
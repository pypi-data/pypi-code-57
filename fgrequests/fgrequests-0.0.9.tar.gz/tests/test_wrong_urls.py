import fgrequests

arr = ['https://wrongdomain.com']

response = fgrequests.build(arr)
assert type(response) == list

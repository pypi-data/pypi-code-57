"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random temperature value.

"""
import random
import time
import zdm

device_id = 'device_id'
password = 'password'


def pub_random():
    # this function is called periodically to publish to ZDM random int value labeled with tags values
    print('------ publish random ------')
    tags = ['tag1', 'tag2', 'tag3']

    for t in tags:
        value = random.randint(0, 20)
        payload = {
            'value': value
        }
        # publish payload to ZDM
        device.publish_data(t, payload)
        print('published on tag:', t, ':', payload)

    print('pub_random done')


def pub_temp_pressure():
    # this function publish another payload with two random int values
    print('---- publish temp_pressure ----')
    tag = 'tag4'
    temp = random.randint(19, 23)
    pressure = random.randint(50, 60)
    payload = {'temp': temp, 'pressure': pressure}
    device.publish_data(tag, payload)
    print('published on tag: ', tag, ':', payload)


device = zdm.ZDMClient(device_id=device_id)
device.set_password(password)
device.connect()

while True:
    time.sleep(2)
    pub_random()
    pub_temp_pressure()

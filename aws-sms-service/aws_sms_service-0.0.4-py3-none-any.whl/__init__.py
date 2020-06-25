import re

import boto3

import os


class SMS:
    """ A class to send SMS over AWS SNS service """
    client = boto3.client('sns',region_name=os.environ['region_name'])

    SENDER_ID_MIN_LENGTH = 1  # [char]
    SENDER_ID_MAX_LENGTH = 11  # [char]

    MESSAGE_MIN_LENGTH = 1  # [char]
    MESSAGE_MAX_LENGTH = 140  # [char]

    TOPIC_NAME_MIN_LENGTH = 1  # [char]
    TOPIC_NAME_MAX_LENGTH = 256  # [char]

    PHONE_NUMBER_E_164 = '^\+?[1-9]\d{1,14}$'

    def __init__(self, sender_id: str, message: str, phone_number: list, topic_name=None):

        self.sender_id = None
        self.message = None
        self.phone_number = None
        self.topic_name = None

        self.set_sender_id(sender_id)
        self.set_message(message)
        self.set_phone_number(phone_number)
        self.set_topic_name(topic_name)

    def set_sender_id(self, sender_id):
        if type(sender_id) is not str:
            raise Exception('sender_id should be a string')

        id_len = len(sender_id)
        if id_len < SMS.SENDER_ID_MIN_LENGTH or id_len > SMS.SENDER_ID_MAX_LENGTH:
            raise Exception('sender_id should have length in the range' \
                            f'[{SMS.SENDER_ID_MIN_LENGTH}, {SMS.SENDER_ID_MAX_LENGTH}]'
                            f' but the current sender_id length is {id_len}')

        if not re.search('[a-zA-Z]', sender_id):
            raise Exception('sender_id should have at least one letter')

        self.sender_id = sender_id
        SMS.client.set_sms_attributes(attributes={'DefaultSenderID': self.sender_id})

    def set_message(self, message):
        if type(message) is not str:
            raise Exception('message should be a string')

        message_len = len(message)
        if message_len < SMS.MESSAGE_MIN_LENGTH or message_len > SMS.MESSAGE_MAX_LENGTH:
            raise Exception('message should have length in the range' \
                            f'[{SMS.MESSAGE_MIN_LENGTH}, {SMS.MESSAGE_MAX_LENGTH}]' \
                            f' but the current message length is {message_len}')

        self.message = message

    def set_phone_number(self, phone_number):
        for number in phone_number:
            if type(number) is not str:
                raise Exception('All phone numbers must be of string type')

            if not re.match(SMS.PHONE_NUMBER_E_164, number):
                raise Exception(f'All phone numbers must match E.164 standard (Error in {number})')

        self.phone_number = phone_number

    def set_topic_name(self, topic_name):

        if len(self.phone_number) > 1:
            # Topic name is used only for broadcasting purposes

            if type(topic_name) is not str:
                raise Exception('topic_name should be a string')

            name_len = len(topic_name)
            if name_len < SMS.TOPIC_NAME_MIN_LENGTH or name_len > SMS.TOPIC_NAME_MAX_LENGTH:
                raise Exception('topic_name should have length in the range' \
                                f'[{SMS.TOPIC_NAME_MIN_LENGTH}, {SMS.TOPIC_NAME_MAX_LENGTH}]' \
                                f' but the current topic_name length is {name_len}')

            if ' ' in topic_name:
                raise Exception('topic_name cannot have any spaces')

            self.topic_name = topic_name

        else:
            self.topic_name = None

    def send(self):
        if len(self.phone_number) == 1:
            self.send_single_sms()

        elif len(self.phone_number) > 1:
            self.send_multiple_sms()

        else:
            raise Exception('phone_number list should have at least one phone number')

    def send_single_sms(self):
        """ Sending an SMS to one recipient only """
        if len(self.phone_number) > 1:
            raise Exception('This method can be called only when phone number list has one phone number only')

        SMS.client.publish(PhoneNumber=self.phone_number[0], Message=self.message)

    def send_multiple_sms(self):
        """ Sending an SMS to multiple recipients """

        # Create a topic
        topic = SMS.client.create_topic(Name=self.topic_name)
        topic_arn = topic['TopicArn']  # get its Amazon Resource Name

        # Add receivers
        for number in self.phone_number:
            SMS.client.subscribe(
                TopicArn=topic_arn,
                Protocol='sms',
                Endpoint=number  # <-- number who'll receive an SMS message.
            )

        # Broadcasting the message
        SMS.client.publish(Message=self.message, TopicArn=topic_arn)

        # Delete the topic
        SMS.client.delete_topic(TopicArn=topic_arn)

from aws_sms_service import SMS

# To send an SMS to one recipient only
sms1 = SMS('Sender', 'Hello From QuakingAspen', ['+90000000000'])
sms1.send()

# To send an SMS to multiple recipients
sms2 = SMS('Sender', 'Hello From QuakingAspen', ['+90111111222', '+90111111111'], topic_name = 'your_topic_name')
sms2.send()
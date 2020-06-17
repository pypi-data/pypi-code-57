
class ActivityExtractor:
	""" The main purpose of this class is to extract the activity name"""

	@staticmethod
	def extract_activity_name(activity_object):
		basic_activities = ['tweet_delete_events', 'direct_message_mark_read_events', 'direct_message_indicate_typing_events']

		type_based_activities = ['follow_events','mute_events','block_events']

		key_based_activities = ['direct_message_events', 'favorite_events']

		for k in activity_object.keys():
			if 'event' in k:
				activity_key = k
				break

		if activity_key in basic_activities:
			activity = activity_key

		elif activity_key in type_based_activities:
			activity = ActivityExtractor.extract_type_based_activity_name(activity_object, activity_key)

		elif activity_key in key_based_activities:
			activity = ActivityExtractor.extract_key_based_activity_name(activity_object, activity_key)

		elif activity_key == 'tweet_create_events':
			activity = ActivityExtractor.extract_tweet_create_activity_name(activity_object, activity_key)

		return activity

	@staticmethod
	def extract_type_based_activity_name(activity_object, activity_key):
		# Get activity type
		activity_type = activity_object[activity_key][0]['type']

		# Test if the event done by user or to user
		if activity_type == 'follow':
			follow_to = activity_object['follow_events'][0]['target']['id']
			user_id = activity_object['for_user_id']
			res = ActivityExtractor.by_or_to(user_id, follow_to, 'to_if_equal')
			activity = f'follow_{res}_user_events'

		# If event is unfollow, mute, unmute, block, or unblock
		else:
			activity = f'{activity_type}_by_user_events'

		return activity

	@staticmethod
	def extract_key_based_activity_name(activity_object, activity_key):
		if activity_key == 'direct_message_events':
			message_by = activity_object["direct_message_events"][0]['message_create']['sender_id']
			user_id = activity_object['for_user_id']
			res = ActivityExtractor.by_or_to(message_by, user_id, 'by_if_equal')
			activity = f'message_{res}_user_events'

		elif activity_key == 'favorite_events':
			favorite_by = activity_object['favorite_events'][0]['user']['id_str']
			user_id = activity_object['for_user_id']
			res = ActivityExtractor.by_or_to(favorite_by, user_id, 'by_if_equal')
			activity = f'favorite_{res}_user_events'

		return activity

	@staticmethod
	def extract_tweet_create_activity_name(activity_object, activity_key):
		# Tweet create events maybe tweet (by user), re-tweet(to user,by user) , reply(to user,by user),mention (to user)
		if activity_object['tweet_create_events'][0]['in_reply_to_status_id'] is None:
			# Recognize the activity is it re-tweet or tweet by user ?
			# If false it is tweet event
			if "retweeted_status" in activity_object['tweet_create_events'][0].keys():
				retweeted_by = activity_object['tweet_create_events'][0]['user']['id_str']
				user_id = activity_object['for_user_id']

				res = ActivityExtractor.by_or_to(retweeted_by, user_id, 'by_if_equal')
				activity = f'retweet_{res}_user_events'

			else:
				activity = activity_key

		else:

			if activity_object['tweet_create_events'][0]['in_reply_to_user_id_str'] == activity_object['for_user_id']:
				activity = 'reply_to_user_events'

			else:
				if activity_object['tweet_create_events'][0]['user']['id_str'] == activity_object['for_user_id']:
					activity = 'reply_by_user_events'
				else:
					activity = 'mention_to_user_events'

		return activity

	@staticmethod
	def by_or_to(id1, id2, mode):
		if mode == 'by_if_equal':
			if id1 == id2:
				return 'by'

			else:
				return 'to'

		elif mode == 'to_if_equal':
			if id1 == id2:
				return 'to'

			else:
				return 'by'


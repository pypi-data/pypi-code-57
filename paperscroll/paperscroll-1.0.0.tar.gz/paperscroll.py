import requests
import base64
import time

class PaperScroll:
	def __init__(self, access_token: str, merchant_id: int):
		if not access_token:
			raise NotImplementedError("Отсутсвует {access_token}")
		if not merchant_id:
			raise NotImplementedError("Отсутсвует {merchant_id}")
		self.access_token = access_token
		self.merchant_id = merchant_id
		
		self.token = base64.b64encode('{}:{}'.format(self.merchant_id, self.access_token).encode()).decode()
		self.api_url = 'https://paper-scroll.ru/api/{}'
		
	def request(self, method: str, params: dict) -> dict:
		result = requests.post(self.api_url.format(method), json=params, headers={ "Authorization":"Basic {}".format(self.token)}).json()
		
		if 'error' in result:
			return result
		
		return result['response']
		
	def merchant_get(self, merchant_ids: list = [] ) -> dict:
		return self.request("merchants.get",{
				'merchant_ids': merchant_ids
		})
	def merchant_edit(self, NewObject: dict) -> dict:
		l = self.request("merchants.edit", NewObject)
		return l
	def user_get(self, user_ids: list) -> dict:
		result = self.request("users.get", {
			'user_ids':user_ids
	})
		return result
	
	def balance_send(self, to, type, type_id, amount ):
		return self.request("transfers.create", {
				"peer_id": int(to),
				"object_type":type,
				"object_type_id":type_id,
				"amount":amount
		})
	
	def balance_get(self, user_ids: list) -> dict:
		return self.request("users.getBalances", {
				'user_ids': user_ids
		})
	
	def transfer_get(self, ids: list) -> dict:
		return self.request("transfers.get", {
				"transfer_ids":ids
		})
		
	def transfer_history(self, offset: int = 0, limit: int = 50 ) -> dict:
		return self.request("transfers.getHistory", {
			"offset":offset,
			"limit":limit
		})
		#https://paper-scroll.ru/api/transfers.getHistory
	
	def items_dis(self) -> dict:
		return self.request("storage.getDisinfectants", {})
	
	def items_storage(self) -> dict:
		result = self.request("storage.getItems", {})
		return result
		
	def getLink(self, amount, payload, edit=True):
		if edit == True:
			return "https://vk.com/app7420483#m" + str(self.merchant_id) + "_" + str(int(amount)) + "_" + str(payload) + "_0"
		else:
			return "https://vk.com/app7420483#m" + str(self.merchant_id) + "_" + str(int(amount)) + "_" + str(payload) + "_1"
		
		
	def run_longpoll(self, interval=0.05):
		longpoll_transaction = self.transfer_history()
		while True:
			time.sleep(interval)
			one_transaction = self.transfer_history()[0]
			try:
				if longpoll_transaction[0] != one_transaction:
					new_transaction = one_transaction
					if new_transaction['type'] == 'transfer':
						if new_transaction['object_type'] == 'balance':
							longpoll_transaction = one_transaction
							return new_transaction
						
			except IndexError:
				pass
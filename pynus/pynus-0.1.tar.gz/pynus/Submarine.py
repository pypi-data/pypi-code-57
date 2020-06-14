class Submarine:
	'''
	------------------------
	Test Doc

	'''

	def __init__(self,price,budget):
		self.captain = 'NuS'
		self.sub_name = 'U69'
		self.price = price # Million
		self.kilo = 0
		self.budget = budget
		self.total = 0

	def Missile(self):
		''' eiei '''

		print('I am a Launcher')

	def Cal_Commission(self):
		percent = self.price * 0.1
		print('NuS is gonna take roughly {} million baht'.format(percent))

	def Goto(self,point,distance):
		print("Let's go to {} distance around {} km".format(point,distance))
		self.kilo += distance
		self.Fuel()

	def Fuel(self):
		diesel = 20
		Cal_cost = diesel * self.kilo
		print("Current fuel cost is {:,d} bath".format(Cal_cost))
		self.total += Cal_cost

	@property # creating a variable to take this value	
	def Budget_Remaining(self):
		remaining = self.budget - self.total
		print("The remaining budget is {:,.2f}".format(remaining))
		return remaining

class ElectricSubmarine(Submarine):

	def __init__(self,price=15000,budget=50000):
		self.sub_name = 'Algerie'
		self.Battery_distance = 10000
		super().__init__(price,budget)

	def Battery(self):
		Allbattery = 100
		calculate = (self.Battery_distance - self.kilo) * 100 / self.Battery_distance
		print("All Battery remaining is {} %".format(calculate))

	def Electric(self):
		kwatt = 5
		Cal_cost = kwatt * self.kilo
		print("Current power cost is {:,d} bath".format(Cal_cost))
		self.total += Cal_cost


if __name__ == '__main__': # จะรันคำสั่งด้านล่างในไฟล์นี้เท่านั้น สำหรับเทส... 

	I401 = ElectricSubmarine(40000,2000000)

	print(I401.budget)
	I401.Goto('japan',4000)
	print(I401.Budget_Remaining)
	I401.Battery()

'''
Red_Blood_Fleet = Submarine(500)
print(Red_Blood_Fleet.captain)
print(Red_Blood_Fleet.sub_name)
print(Red_Blood_Fleet.price)

Red_Blood_Fleet.Cal_Commission()
Red_Blood_Fleet.Goto('china',1000)
Red_Blood_Fleet.Goto('japan',2000)
Red_Blood_Fleet.Fuel()

current = Red_Blood_Fleet.Budget_Remaining
print(current*10)

Juo = Submarine(70000)
Juo.captain = 'Nagato'
print(Juo.captain)
'''
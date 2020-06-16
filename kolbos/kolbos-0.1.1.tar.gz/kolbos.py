import os
from colorama import Fore
from vbml import Patcher

print(Fore.GREEN+"\nHello," + Fore.RED + " user!" + Fore.GREEN + " KolbOS 0.1.1\n\n " + Fore.BLUE + "         Commands Helper"+Fore.RED+" >" + Fore.YELLOW + " help\n" + Fore.BLUE + "          Creator"+Fore.RED+" > "+ Fore.YELLOW +"LooPeKa\n" + Fore.BLUE + "          FeedBack" + Fore.RED + " >\n             " + Fore.BLUE +" VK"+Fore.RED+" > "+Fore.YELLOW + "https://vk.com/loopeka\n        "+Fore.BLUE +"      Gmail"+Fore.RED+" > "+Fore.YELLOW + " loudmaks10@gmail.com\n\n"+Fore.GREEN +"Good luck! [ 🍀 ]\n\n")

from vbml import PatchedValidators

class Validators( PatchedValidators ):
	def int( self, text: str, *args ):
		valid = text.isdigit()
		if valid:
			return int( text )
			
			
patcher = Patcher( validators = Validators )


def main():
	while True:
		try:
			move = input( Fore.YELLOW + "$" + Fore.WHITE + " " )
			if move.lower() == "help" :
				yes = 1
				print( Fore.GREEN + 'Commands' + Fore.BLUE + ' > \n         ' + Fore.CYAN + ' print \"<text>\" - print text\n          c - clear of console\n          exit() - exit\n          ls - list of file in directory\n          python - python shell\n		  pip install <package> - install python package \n		  pip list - list python packages\n		  python <file> - start .py file' )
				
			elif move.lower() == "exit()":
				break
				
			elif move.lower() == "c" :
				s = os.system('clear')
				
			elif move.lower().startswith( "print" ):
				pattern = patcher.pattern( 'print "<text>"' )
				res = patcher.check( move, pattern )
				print( res['text'] )
				
			elif move.lower() == "python":
				os.system("python3")
				
			elif move.startswith( "pip install" ):
				pattern = patcher.pattern( "pip install <package>" )
				res = patcher.check( move, pattern )
				os.system( "pip install " + str( res['package'] ) )
				
			elif move.lower() == 'pip list':
				os.system('pip list')
				
			elif move.lower() == 'ls':
				os.system( 'ls' )
				
			elif move.startswith( "python " ):
				if move.lower() == 'python kolbos.py':
					print('.__.')
					
				elif move.lower() == 'python kolbos':
					print('.__.')
					
				elif move.lower() != 'python kolbos.py':
					if move[len(move)-3:len(move)+1] == '.py':
						print( Fore.RED + "\nPRESS CTRL + C TO STOP" + Fore.WHITE )
						pattern = patcher.pattern( 'python <file>' )
						res = patcher.check( move, pattern )
						os.system('python3 ' + str( res['file'] ) )
						
					else:
						print( Fore.RED + "\nPRESS CTRL + C TO STOP" + Fore.WHITE )
						move += '.py'
						pattern = patcher.pattern( "python <file>" )
						res = patcher.check( move, pattern )
						os.system("python3 " + str( res['file'] ))
						
			elif move.startswith( "cd " ):
				os.system( move )
				
			
					
			else:
				print( Fore.RED + "Command not found > " + str( move ) + "\nWrite \"help\"" )
				
		except Exception as exc:
			print( Fore.RED + str( exc ) )

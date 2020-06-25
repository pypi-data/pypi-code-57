from filecmp import dircmp
import os
import argparse
import easygui
import pandas as pd


def main():
	
	df = pd.DataFrame(columns=['Identical File', 'Path in Group A','Path in Group B'])
	
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--no_gui", action="store_true", required=False,
					help="input from the terminal (default easygui)")
	ap.add_argument("-t", "--terminal_output", action="store_true", required=False,
					help="output in the terminal (default excel)")
	args = vars(ap.parse_args())
	
	no_gui = args['no_gui']
	t_output = args['terminal_output']
	
	if no_gui == False:
		group_A = easygui.diropenbox()
		print(group_A)
		group_B = easygui.diropenbox()
		print(group_B)
	
	else:
		group_A = input('Give the path of the first foldergroup: ')
		print(group_A)
		group_B = input('Give the path of the second foldergroup: ')
		print(group_B)
	
	
	for roota, dirsa, filesa in os.walk(group_A):
		for rootb, dirsb, filesb in os.walk(group_B):
			dc = dircmp(roota, rootb)
			if dc.same_files == []:
				pass
			else:
	
				if t_output == True:
					print('###################################')
					print('Same File found in : '+roota+' and '+rootb)
					print(dc.same_files)
				else:
					for f in dc.same_files:
						temp_df = pd.DataFrame([[f, roota, rootb]], columns=['Identical File', 'Path in Group A','Path in Group B'])
						df = df.append(temp_df, ignore_index=True)
	
	
	save_path = easygui.filesavebox(default="identical_files_from_")
	df.to_excel(save_path+'.xlsx')
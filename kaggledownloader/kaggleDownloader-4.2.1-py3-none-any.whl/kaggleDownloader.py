# -*- coding: utf-8 -*-
def get_dataset(kaggle_dataset_api = None):
  """
  download the dataset and unzip the zip files

  Checks: 
  1. upload the kaggle json file obtained from your kaggle account
  
  Simply call the 'get_dataset' function or call by passing the kaggle dataset api link as an argument in string format in the get_dataset() function

  """
  import os
  if not kaggle_dataset_api:
    kaggle_dataset_api = input('Enter the Kaggle API dataset download link: ')

  jsonFile = False
  for file in os.listdir():
    if file == "kaggle.json":
        jsonFile = True
        break
  if jsonFile == False:
    print("Please add the kaggle.json file to the current working directory which is to be obtained from your kaggle account")
    return
  os.system("mkdir -p ~/.kaggle")
  os.system("cp kaggle.json ~/.kaggle/")
  os.system("chmod 600 ~/.kaggle/kaggle.json")
  os.system("ls ~/.kaggle")

  os.system("ls -l ~/.kaggle")
  os.system("cat ~/.kaggle/kaggle.json")

  os.system("pip install --upgrade --force-reinstall --no-deps kaggle")
  #os.system("pip install -q kaggle-cli")
  print('Downloading the dataset....\n')
  os.system(kaggle_dataset_api)

  print('Download completed..\nUnzipping the zip files\n')
  import zipfile
  zipfiles = [file for file in os.listdir() if file.endswith('.zip')]
  for file in zipfiles:
    zipref = zipfile.ZipFile(file)
    zipref.extractall()
    zipref.close()

  print('Zip Files unzipped')
  print('\n', 'Directory contains the following files : ', os.listdir())
  print()
  res = input('Remove zip files ? (yes/no) :')
  if res == 'yes' or res == 'Y' or res == 'y' or res == 'Yes' or res == 'YES' :
    for file in zipfiles:
      os.remove(file)
  print('\n', 'Directory contains the following files : ', os.listdir())
 

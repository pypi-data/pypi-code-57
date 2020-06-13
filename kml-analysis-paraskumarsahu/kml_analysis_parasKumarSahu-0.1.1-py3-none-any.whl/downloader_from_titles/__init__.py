from multiprocessing import Pool, cpu_count
import wikipediaapi
import time
from itertools import islice
from datetime import datetime

def download_wiki(title):
    try:
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(title.split("/")[1])

        if page_py.exists() and len(str(page_py.text.encode("utf-8"))) > 10:
            file = open(title+".txt","w")
            file.write(str(page_py.text.encode("utf-8")))
            file.close()
            print(title, "downloaded")
        else:
            print("Error in downloading ->", title)    

    except Exception as e:
        print(e)


def run(file_name):
	file = open(file_name+".txt")
	titles = file.read().replace(".xml", "").replace("?", "").split("\n")
	
	for i in range(len(titles)):
		titles[i] = file_name+"/"+titles[i]
	file.close()

	#print(len(titles))
	titles_iter = iter(titles)

	n = int(len(titles) / 10)

	if len(titles) % 10 != 0:
		n += 1

	sub_titles_list = [list(islice(titles_iter, 10)) for i in range(n)]

	print("There are {} CPUs on this machine ".format(cpu_count()))

	startTime = datetime.now()

	for sub_titles in sub_titles_list: 
	    pool = Pool(cpu_count())
	    results = pool.map(download_wiki, sub_titles)
	    pool.close()
	    pool.join()
	    time.sleep(1)

	print("Download Time", datetime.now() - startTime)
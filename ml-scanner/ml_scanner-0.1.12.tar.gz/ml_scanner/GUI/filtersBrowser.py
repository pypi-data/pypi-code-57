from ..getDataML import getDataML
import pickle
import PySimpleGUI as sg

#f = open('available_filters','rb')
#aF = pickle.load(f)
#print(aF[0]['name'])

url = getDataML.mlURL()
url.find = 'ford fiesta kinetic 2011'
url.CATEGORY_ID = 'MLA90998'

URL = url.getURL()

req = getDataML.get_by_key(URL)


total = req['paging']['total']
filts = req["filters"]


filters = [[filt['name'],filt['id']] for filt in filts]
#filters_id = [ for filt in filts]

Afilts = req["available_filters"]
available_filters = [[filt['name'], filt['id']] for filt in Afilts]
#available_filters_id = [ filt['id'] for filt in Afilts]

filtersList = ['/'.join((fil,fil_id)) for fil,fil_id in filters]
AfiltersList = ['/'.join((fil,fil_id)) for fil,fil_id in available_filters]


sg.theme('Dark Brown')
layout = [[sg.Text('ML Filters Browser')],
        [sg.Text('ID: '), sg.Text(size=(15,1),key='-ID-')],
        [sg.Text('Current Filters '), sg.Text(size=(20,1),key='-NAME-'),
        sg.Text('Available Filters '), sg.Text(size=(20,1),key='-NAME2-')],
        [sg.Listbox(values=filtersList, size=(40, 20), key='-FILT-', enable_events=True),
        sg.Listbox(values=AfiltersList, size=(40, 20), key='-A_FILT-', enable_events=True)],
        [sg.Button('Exit'),sg.Button('Restart')]]

window = sg.Window('Filter Browser', layout)

while True:  # Event Loop
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event in (None, 'Restart'):
        #catDict = getCategories()
        #catList = [cat['name'] for cat in catDict]
        #catListID = [cat['id'] for cat in catDict]
        #window['-LIST-'].update(catList)
        event = False
#    if event:    
 #       try:
            #CATEGORY_NAME = values['-LIST-'][0]
            #idx = catList.index(CATEGORY_NAME)
            #CATEGORY_ID = catListID[idx]

            #try:
            #    catDict = getCategories(catListID[idx], key = 'child')
            #except Exception as e:
            #    print(e)
            
            #catList = [cat['name'] for cat in catDict]
            #catListID = [cat['id'] for cat in catDict]
            
            #window['-LIST-'].update(catList)
            #window['-ID-'].update(CATEGORY_ID)
            #window['-NAME-'].update(CATEGORY_NAME)
            #print(CATEGORY_ID)
        #except:
        #    print('No hay mas subcategorias')

window.close()
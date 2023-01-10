import PySimpleGUI as sg 

tags = []

def tag_news(news_text):
    print("news text:", news_text)
    tags = ["fraud", "zort"]
    return tags

def tags_to_string():
    str = ""
    for tag in tags:
        str += tag + " "
    return str

sg.theme('Dark Amber')  # Let's set our own color theme

# STEP 1 define the layout
layout = [ 
            [sg.Text('Please select the machine learning model you want to generate the tags with')],
            [sg.Radio('Model1', "MLModelRadio", default=True, size=(10,1), k='-M1-'), sg.Radio('Model2', "MLModelRadio", default=True, size=(10,1), k='-M2-'),
             sg.Radio('Model3', "MLModelRadio", default=True, size=(10,1), k='-M3-'), sg.Radio('All Models', "MLModelRadio", default=True, size=(10,1), k='-M4-')],
            [sg.Multiline(size=(60,20), expand_x=True, expand_y=True, k='news_text')],
            [sg.Multiline(size=(20,5), expand_x=True, expand_y=True, k='tag_results_gui')],
            [sg.Button('Run'), sg.Button('Exit')]
         ]

#STEP 2 - create the window
window = sg.Window('Cyber Security News Tagger', layout)

# STEP3 - the event loop
while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    
    if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
        print('============ Event = ', event, ' ==============')
        print('-------- Values Dictionary (key=value) --------')
        for key in values:
            print(key, ' = ',values[key])
    if event == 'Run':
        tags = tag_news(values['news_text'])
        window['tag_results_gui'].update(value=tags_to_string())
    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
      break
    
window.close()

from threading import Thread
from configparser import *
from utils import *
from guis import *
import PySimpleGUI as sg
import configparser
import webbrowser
import os
#^--- imports

if os.name!='nt':#check if system not linux, macos
    rprint('Wine Launcher does not support your system as it works on .bat files which linux does not understand\nYou also can use wine (linux windows api) but launcher maybe work bad')
    quit()

rprint(getlogo())#print launcher logo


config = configparser.ConfigParser()#Config
if not os.path.isfile('.\\settings.ini'):#check if config exist
    rprint('Created config')
    with open('settings.ini', 'w') as newconfig:
        newconfig.write('[settings]\nram = 1\nnickname = WineLauncher\nselected_cheat = NoRender')#Save default config
        newconfig.close()
    config.read('settings.ini')
else:
    rprint('Loaded config')
    config.read('settings.ini')

sg.LOOK_AND_FEEL_TABLE['WineTheme'] = {'BACKGROUND': '#2f2f2f',#Custom theme, thx to quuenton
'TEXT': 'white',
'INPUT': '#616161',
'TEXT_INPUT': 'white',
'SCROLL': '#616161',
'BUTTON': ('white', '#616161'),
'PROGRESS': ('#D1826B', '#CC8019'),
'BORDER': 0, 'SLIDER_DEPTH': 0,
''
'PROGRESS_DEPTH': 0}

sg.ChangeLookAndFeel('WineTheme', True)#Apply theme

def check_core():
    if not os.path.isdir('./minecraft'):#check if folder "minecraft" exist
        sg.Popup('Нажмите ок для начала скачивания и ждите.')
        rprint(colors.RED+'Downloading Core...\n'+colors.ENDC)
        download_libs()#download libs and etc.
    elif not os.path.isdir('./assets'):
        download_libs(True)#download libs and etc.
check_core()#check if files exist

#static vars for gui
version = '1.6'
header = f'Wine Launcher {version}'#Header to use in changetexts(), utils.py
changelog = ['[+] Оптимизировал чуть код','[+] Убрал надпись Recode']#Changelog
credits = ['PLNT - owner, создатель гуи','quuenton - второй создатель']#credits

cheats = [#cheats
'NoRender',
'Fluger',
'Rockstar',
'Expensive',
'Wexside',
'Celestial',
'Osium',
'EntityWare',
'MincedRecode',
'ShitRecode',
'DestroySquad',
'Zamorozka',
'Rise']

run_cheats = {}#Cheats dict, don't touch it

for i in cheats:
    run_cheats[i] = str_to_class(i)

cheats = [cheat for cheat in list(run_cheats.keys())]#get keys from dict and convert to list
rams = [i for i in range(1,9)]#ram
#dynamic vars for gui
config_cheat = str(config.get('settings','selected_cheat'))

def SaveCfg(value):
    temp = value['ram']
    ram_save = str(temp)
    config['settings'] = {'ram': ram_save,'nickname': str(value['USERNAME']),'selected_cheat': str(value['selected_cheat'])}
    config.write(open('./settings.ini','w',encoding='utf-8'))

def MainWindow():#Main Window
    layout = [#Layout aka gui
[

sg.Image('./assets/wine-icon.png',key='logo',enable_events=True),
sg.Text('',font='"Bahnschrift SemiBold SemiConden" 18',key='header'),
sg.Push()],

[sg.HorizontalSeparator()],
[

sg.Text('List of cracks:',font='Bahnschrift 13'),

sg.InputCombo(
    cheats,
    key='selected_cheat',
    font='Bahnschrift 13',readonly=True,
    default_value=config_cheat,
    enable_events=True,),

sg.Text('Ram (GB): ',font='Bahnschrift 12'),

sg.InputCombo(
    rams,
    default_value=str(config.get('settings', 'ram')),
    key='ram',
    enable_events=True,
    readonly=True,
    font='Bahnschrift 13',
    text_color='white'),

sg.Image(filename='./assets/settings.png',key='settings_icon',enable_events=True),sg.Push(),sg.Text('\n'.join(changelog),font='Bahnschrift 10')],

[sg.Text('',key='cheat_name',font='Bahnschrift 13')],
[sg.Text('',key='cheat_type',font='Bahnschrift 13')],
[sg.VPush()],
[

sg.Text('\n\nGlory to Ukraine',font='Bahnschrift 13'),
sg.Push(),
sg.Text('\n'.join(credits), font='Bahnschrift 12')],

[sg.HorizontalSeparator()],

[#last row

sg.Push(),
sg.Text('Name: ',font='Bahnschrift 15'),
sg.InputText(str(config.get('settings','nickname')),font='Bahnschrift 16',key='USERNAME'),
sg.Button('Start',font='Bahnschrift 17',key='start_cheat')]

]

    window = sg.Window('Wine Launcher',layout,size=(800,430),finalize=True, icon='./assets/wine-icon.ico',background_color='#2f2f2f',use_default_focus=False).Finalize()
    #^-- launcher window

    changetexts('ChangeText',header,'header',window)#animate header
    
    while True:
        event,value = window.read()
        
        if event == sg.WIN_CLOSED:#if pressed close button
            break
        
        elif event in ['ram','usetray']:#save cfg on event
            SaveCfg(value)
        
        elif event == 'settings_icon':
            window.hide()
            SettingsMenu()
            window.un_hide()
        
        elif event == 'logo':#on press logo
            webbrowser.open('https://discord.gg/Ag6XCDfzXz')#open our discord server in browser
        
        elif event == 'selected_cheat':#print cheat information
            SaveCfg(value)
            name = str(value['selected_cheat'])
            cheat_type = 'Тип: '+Cheat.gettype(run_cheats[value['selected_cheat']])
            changetexts('ChangeInfoText',name,'cheat_name',window)
            changetexts('ChangeTypeText',cheat_type,'cheat_type',window)

        elif event == 'start_cheat':#start button
            if value['selected_cheat']=='':#if cheat not selected
                sg.Popup('Выберите чит')
            class Start(Thread):#run cheat as thread
                def run(self):
                    new_memory = value['ram'] * 1024#get ram
                    new_memory_str = str(new_memory)#convert ram, idk why cheat not run if don't do this
                    Cheat.run(run_cheats[value['selected_cheat']],value['USERNAME'],new_memory_str[0:4])#run cheat
            startcheat = Start()
            startcheat.start()#run cheat
    window.close()#close window

if __name__ == "__main__":
    MainWindow()#Run launcher


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
    with open('settings.ini', 'w') as newconfig:#open empty config
        newconfig.write('[settings]\nram = 1\nnickname = WineLauncher\nselected_cheat = NoRender')#Save default config
        newconfig.close()#close config file
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
header = f'Wine Launcher (Beta {version})'#Header to use in changetexts(), utils.py
changelog = [
'[-] Убрал надпись Recode',
'[/] Переместил чендж лог в настройки ',
'[/] Переместил кнопку настроек',
'[+] Добавил надпись BETA',
'[+] Добавил кнопку Sounds',
'[+] Добавил эффект hover кнопкам',
'[+] Добавил пасхалку',
'[+] Починил кнопку prefetch',
'[+] Добавит чит BoberWare (паста NH)']#Changelog
credits = ['PLNT - owner, создатель гуи','quuenton - второй создатель','aMinato - заливщик файлов','Markusha - создатель сайта']#credits

cheats = [#cheats
'NoRender',
'Osium',
'Fluger',
'Rockstar',
'Expensive',
'Wexside',
'Celestial',
'EntityWare',
'MincedRecode',
'ShitRecode',
'DestroySquad',
'Zamorozka',
'BoberWare',
'ExtremeHack']

run_cheats = {}#Cheats dict, don't touch it

for i in cheats:
    run_cheats[i] = str_to_class(i)

cheats = [cheat for cheat in list(run_cheats.keys())]#get keys from dict and convert to list
rams = [i for i in range(1,9)]#ram
#dynamic vars for gui
config_cheat = str(config.get('settings','selected_cheat'))

def SaveCfg(value):#save cfg function
    temp = value['ram']
    ram_save = str(temp)
    config['settings'] = {'ram': ram_save,'nickname': str(value['USERNAME']),'selected_cheat': str(value['selected_cheat'])}
    config.write(open('./settings.ini','w',encoding='utf-8'))

def MainWindow():#Main Window
    layout = [#Layout aka gui
[

sg.Image('./assets/wine-icon.png',key='logo',enable_events=True),#logo
sg.Text('',font='"Bahnschrift SemiBold SemiConden" 18',key='header'),#header
sg.Push(),
sg.Image(filename='./assets/settings.png',key='settings_icon',enable_events=True)],

[sg.HorizontalSeparator()],
[
sg.Text('List of cracks:',font=gfont(13)),
sg.InputCombo(cheats,key='selected_cheat',font=gfont(13),readonly=True,default_value=config_cheat,enable_events=True)],
[
sg.Text('Ram (GB): ',font=gfont(12)),
sg.InputCombo(rams,default_value=str(config.get('settings', 'ram')),key='ram',enable_events=True,readonly=True,font=gfont(13))],

[sg.Text('',key='cheat_name',font=gfont(13))],
[sg.Text('',key='cheat_type',font=gfont(13))],

[sg.VPush()],


[#Down
sg.Text('\n\nGlory to Ukraine!',font=gfont(13)),
sg.Push(),
sg.Text('\n'.join(credits), font=gfont(12))],

[sg.HorizontalSeparator()],

[#last row

sg.Push(),
sg.Text('Name: ',font=gfont(15)),
sg.InputText(str(config.get('settings','nickname')),font=gfont(16),key='USERNAME'),
sg.Button('Start',font=gfont(17),key='start_cheat')]#Start cheat button

]

    window = sg.Window('Wine Launcher',layout,size=(800,430),finalize=True, icon='./assets/wine-icon.ico',background_color='#2f2f2f',use_default_focus=False)
    #^-- launcher window

    generate_hover(layout,window,sg)#bind all sg.Button elements in layout

    changetexts('ChangeText',header,'header',window)#animate header
    
    while True:#tkinter loop?
        event,value = window.read()#get events, value, example if you pressed button
        
        if event == sg.WIN_CLOSED:#if pressed close button
            break#stop tkinter loop

        check_hover(event,window)#if buttons hovered

        if event in ['ram','start_cheat']:#save cfg on event
            SaveCfg(value)#save config
        
        if event == 'settings_icon':#Settings window
            window.hide()#hide main window
            SettingsMenu(cheats,run_cheats,changelog)#show settings window
            window.un_hide()#show main window
        
        if event == 'logo':#on press logo
            webbrowser.open(discord_server)#open our discord server in browser
        
        if event == 'selected_cheat':#print cheat information
            SaveCfg(value)#save cheat
            name = str(value['selected_cheat'])#get name
            cheat_type = 'Тип: '+Cheat.gettype(run_cheats[value['selected_cheat']])#get type, free,crack
            changetexts('ChangeInfoText',name,'cheat_name',window)#make text animation
            changetexts('ChangeTypeText',cheat_type,'cheat_type',window)#make text animation 2x

        if event == 'start_cheat':#start button
            if value['selected_cheat']=='':#if cheat not selected
                sg.Popup('Выберите чит')#send popup
            else:
                class Start(Thread):#run cheat as thread
                    def run(self):#run function
                        new_memory = value['ram'] * 1024#get ram
                        new_memory_str = str(new_memory)#convert ram, idk why cheat not run if don't do this
                        Cheat.run(run_cheats[value['selected_cheat']],value['USERNAME'],new_memory_str[0:4])#run cheat
                startcheat = Start()#make startcheat class
                startcheat.start()#run cheat
    window.close()#close window

if __name__ == "__main__":
    MainWindow()#Run launcher
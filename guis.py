import os,shutil
import PySimpleGUI as sg
import webbrowser
import configparser
from utils import *

config = configparser.ConfigParser()
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
#static
rams = [i for i in range(1,9)]
#dynamic
def SettingsMenu():
    config.read('settings.ini')
    layout = [
    [sg.Image('./assets/wine-icon.png'),sg.Text('',font='"Bahnschrift SemiBold SemiConden" 24',key='header'),sg.Push(),sg.Button('Github',font='Bahnschrift 13',size=(10,2),key='github')],
    [sg.HorizontalSeparator()],
    [sg.Text(f'''Конфиг:
Оперативная память: {str(config.get("settings","ram"))}гб
Ник: {str(config.get("settings","nickname"))}
Выбранный чит: {str(config.get("settings","selected_cheat"))}
''',font='Bahnschrift 13')],
    [sg.VPush()],
    [sg.HorizontalSeparator()],
    [
    sg.Button('Назад',font='Bahnschrift 13',size=(23,2),key='back'),
    sg.Button('Сбросить лаунчер',font='Bahnschrift 13',size=(23,2),key='factory_reset'),
    sg.Button('Дискорд сервер',font='Bahnschrift 13',size=(23,2),key='discord'),
    ],
    [
    sg.Button('Чистка папки recent',font='Bahnschrift 13',size=(23,2),key='delete_recent'),
    sg.Button('Удалить prefetch',font='Bahnschrift 13',size=(23,2),key='delete_prefetch'),
    sg.Button('Чистка папки temp',font='Bahnschrift 13',size=(23,2),key='delete_temp'),
    ]
    ]
    window = sg.Window('Settings',icon='./assets/wine-icon.ico',layout=layout,size=(800,430),finalize=True,use_default_focus=False)
    changetexts('ChangeHeaderText','Settings','header',window)
    while True:
        event,values = window.read()
        if event==sg.WIN_CLOSED or event=='back':
            break
        elif event=='select_jar_file':
            window['selected_jar_path'].update(str(values['select_jar_file']))
        elif event=='select_json_file':
            window['selected_json_path'].update(str(values['select_json_file']))
        elif event=='delete_recent':
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                sg.Popup(deletefiles(f'{os.getenv("APPDATA")}\\Microsoft\\Windows\\Recent'),icon='./assets/wine-icon.ico',title='Wine Launcher')#delete all in folder recent
                sg.Popup('Папка recent очищена (на проверке скажите что вы отключили сбор данных)',icon='./assets/wine-icon.ico',title='Wine Launcher')
            else:pass
        elif event=='delete_prefetch':
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                sg.Popup(deletefiles(f'C:\Windows\Prefetch'),icon='./assets/wine-icon.ico',title='Wine Launcher')#delete prefetch folder
                sg.Popup('Папка prefetch очищена (на проверке скажите что вы отключили сбор данных)',icon='./assets/wine-icon.ico',title='Wine Launcher')
            else:pass
        elif event=='factory_reset':#reset all launcher delete minecraft folder
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                shutil.rmtree('minecraft')#delete
                sg.Popup('Лаунчер сброшен нажмите ок и перезапустите его',icon='./assets/wine-icon.ico',title='Wine Launcher')
                exit()
            else:pass
        elif event=='delete_temp':#delete temp folder - %appdata%/Temp
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                sg.Popup(deletefiles(os.getenv('temp')),icon='./assets/wine-icon.ico',title='Wine Launcher')
            else:pass
        elif event=='discord':
            webbrowser.open('https://discord.gg/Dc7jWat2KP')
        elif event=='github':
            webbrowser.open('https://github.com/quuenton/Wine-Launcher')
    window.close()

#SettingsMenu()
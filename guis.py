from utils import *
from links import *
import os,shutil
import PySimpleGUI as sg
import webbrowser
import configparser
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
#---------
def SettingsMenu(cheats_list,cheats_dict,changelog,position):
    config.read('settings.ini')
    layout = [
    [sg.Image('./assets/wine-icon.png',key='easter_egg',enable_events=True),
    sg.Text('',font='"Bahnschrift SemiBold SemiConden" 24',key='header'),
    sg.Push(),
    sg.Button('Github',font=gfont(13),size=(10,2),key='github'),
    sg.Button('Sounds',font=gfont(13),size=(10,2),key='sounds')],
    [sg.HorizontalSeparator()],
    [
sg.Text(f'''Конфиг:
Оперативная память: {str(config.get("settings","ram"))}гб
Ник: {str(config.get("settings","nickname"))}
Выбранный чит: {str(config.get("settings","selected_cheat"))}
''',font=gfont(13)),sg.Push(),sg.Text('\n'.join(changelog),font=gfont(10))],
    [sg.VPush()],
    [sg.Text('Всего читов: '+str(len(cheats_list)),font=gfont(13)),sg.Push(),sg.Text('\nДлина чендж лога: '+str(len(changelog)),font=gfont(13))],
    [sg.HorizontalSeparator()],
    [
    sg.Button('Назад',font=gfont(13),size=(23,2),key='back'),
    sg.Button('Сбросить лаунчер',font=gfont(13),size=(23,2),key='factory_reset'),
    sg.Button('Дискорд сервер',font=gfont(13),size=(23,2),key='discord'),
    ],
    [
    sg.Button('Чистка папки recent',font=gfont(13),size=(23,2),key='delete_recent'),
    sg.Button('Удалить prefetch',font=gfont(13),size=(23,2),key='delete_prefetch'),
    sg.Button('Чистка папки temp',font=gfont(13),size=(23,2),key='delete_temp'),
    ]
    ]
    window = sg.Window('Settings',icon='./assets/wine-icon.ico',location=position,layout=layout,size=(800,430),finalize=True,use_default_focus=False,modal=True)

    generate_hover(layout,window,sg)
    changetexts('ChangeHeaderText','Settings','header',window)

    while True:
        event,value = window.read()
        if event==sg.WIN_CLOSED or event=='back':
            break

        check_hover(event,window)

        window_pos = window.CurrentLocation()

        if event=='delete_recent':
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                wine_popup(deletefiles(f'{os.getenv("APPDATA")}\\Microsoft\\Windows\\Recent'))#delete all in folder recent
                wine_popup('Папка recent очищена (на проверке скажите что вы отключили сбор данных)')
        
        elif event=='delete_prefetch':
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                prefetches=os.listdir('C:\WINDOWS\Prefetch')
                count=0
                for pf in prefetches:
                    os.remove('C:\WINDOWS\Prefetch'+pf)
                    count+=1
                wine_popup('Удалено: '+str(count),sg)#delete prefetch folder
                wine_popup('Папка prefetch очищена (на проверке скажите что вы отключили сбор данных)',sg)
        
        elif event=='factory_reset':#reset all launcher delete wine minecraft folder
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                shutil.rmtree('minecraft')#delete
                wine_popup('Лаунчер сброшен нажмите ок и перезапустите его',sg)
                exit()
            else:pass
        
        elif event=='delete_temp':#delete temp folder - %appdata%/Temp
            if sg.PopupOKCancel('Вы уверены?',icon='./assets/wine-icon.ico',title='Wine Launcher')=='OK':
                wine_popup(deletefiles(os.getenv('temp')),sg)
            else:pass
        
        elif event=='discord':
            webbrowser.open(discord_server)#link to discord server
        
        elif event=='github':
            webbrowser.open(repository)#link to github repository
        
        elif event=='easter_egg':
            changetexts('ChangeHeaderText','Never Gonna Give You Up','header',window)
            webbrowser.open(rickroll)
        
        elif event=='sounds':
            sounds_dict = {True:'Yes',False:'No'}#convert bool to str
            sounds = []
            for cheat in list(cheats_dict.items()):
                sounds.append(cheat[0]+' Sounds: '+sounds_dict[cheat[1].getsounds()])
            sg.Popup('\n'.join(sounds),icon='./assets/wine-icon.ico',title='Wine Launcher')

    window.close()
    return window_pos

#SettingsMenu(['1','2'],{'1'},'1')
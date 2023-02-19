from time import sleep as wait
from download import download
from random import choice
from links import *
from glob import *
import os,sys,shutil
import re

libraries_path = sys.path[0]+'\\minecraft\\libraries'
natives_path = sys.path[0]+'\\minecraft\\natives'

class colors:#colors for logo
    RED = '\033[91m'#Red color
    ENDC = '\033[0m'#Stop red color

def rprint(text):
    return print(colors.RED+text+colors.ENDC)

def download_libs(onlyassets=False):
    if not onlyassets:    
        d = download(url='https://cdn.discordapp.com/attachments/1022495936628392164/1023650548819439667/bruh.zip',#core aka minecraft folder
            path='.\\minecraft\\', progressbar=True, replace=True, kind='zip')
        if os.path.isdir('./assets') == False or os.path.isfile('./minecraft/OpenAL64.dll'):
            assets = download(
                url='https://cdn.discordapp.com/attachments/1025789472916389928/1038070679028908032/assets.zip',#assets to work, images etc.
                path='.\\', progressbar=True, replace=True, kind='zip'
            )
            os.remove('./minecraft/natives/OpenAL64.dll')#remove old openal
            shutil.copy('./minecraft/OpenAL64.dll','./minecraft/natives/OpenAL64.dll')#copy new opeanal to natives
            os.mkdir('./minecraft/--assetsDir')
            if not os.path.isdir('./minecraft/--assetsDir/assets'):#fix sounds
                d = download(
                    url='https://cdn.discordapp.com/attachments/1025789472916389928/1025790255808385034/objects.zip',
                    path='.\\minecraft\\--assetsDir\\assets\\', progressbar=True, replace=True, kind='zip'
                )
                shutil.move('./minecraft/assets/indexes','./minecraft/--assetsDir/assets')#fix sounds
    elif onlyassets:
        assets = download(
                    url='https://cdn.discordapp.com/attachments/1025789472916389928/1038070679028908032/assets.zip',#assets to work, images etc.
                    path='.\\', progressbar=True, replace=True, kind='zip'
        )

jar_symbols = "'()[]!@#$%^&*`~;\\"
def check_jar(jar):
    for jar_char in jar:
        if jar_char in jar_symbols:
            return True
    

def text_animation(text):#return a list with step by step animation
    symbols = ['*','@','#','$','%','^','&']#symbols to insert to step
    temp = text
    temp+=temp[:1]#fix bug
    shif = []
    for i in range(1,len(temp)+1):#idk what this doing
        shif.append(choice(symbols))
    steps = []
    phrase = []
    for i in range(1,int(len(temp))+1):
        phrase.append(temp[i-1:i])
    x = 0
    for i in phrase:#idk how this work without errors
        shif.pop(x)
        str = ''.join(shif)
        steps.append(str)
        shif.insert(x,i)
        str = ''.join(shif)
        x+=1
    return steps

def generate_hover(layout,window,sg):#Make buttons hover effect
    for i in layout:
        for x in i:
            if isinstance(x,sg.Button):#bind events to every button
                window[str(x.key)].bind('<Enter>', '&+MOUSE OVER+')
                window[str(x.key)].bind('<Leave>', '&+MOUSE AWAY+')
                window[str(x.key)].bind('<Button-1>', '&+LEFT CLICK+')
                window[str(x.key)].bind('<Button-1>', '&+LEFT CLICK+')
                button = window[str(x.key)]
                button.Widget.configure(cursor='hand2')#change cursor when hover

            if isinstance(x,sg.Image):
                image = window[str(x.key)]
                image.Widget.configure(cursor='hand2')

            if isinstance(x,sg.Combo):
                inputcombo = window[str(x.key)]
                inputcombo.Widget.configure(cursor='hand2')

def check_hover(event,window):#check if button hovered
    if '+MOUSE OVER+' in event:window[str(event).split('&')[0]].update(button_color='#717171')#button hover effect
    
    elif '+MOUSE AWAY+' in event:window[str(event).split('&')[0]].update(button_color='#616161')#button hover effect
    
    elif '+LEFT CLICK+' in event:window[event.split('&')[0]].update(button_color='#919191')#button click effect
        

def fix_bat(newname,newram,onlyname):#fix bat files, change nickname,ram: please don't touch this function
    bats=[os.path.join(r,f) for r,d,fs in os.walk('minecraft') for f in fs if f.endswith('.bat')]#idk how this work, copy paste from stack overflow :)
    names = ['WineLauncher','quuenton','Purpl3_YT']#please don't touch this
    for bat in bats:
        x = open(bat,mode='r')
        s = str(x.read())
        if onlyname==False and s.find('cd ..')==-1:
            print('Fixed bat file: '+bat)
            s = s.replace('.\\','')
            s = re.sub('title dont close this','title dont close this\ncd minecraft',str(s))
            s = re.sub('pause','cd ..\npause',str(s))
            s = re.sub('-Xmx2048M',f'-Xmx{newram}M',str(s))
            for i in names:
                s = re.sub(f'--username {i}',f'--username {newname}',str(s))
        elif onlyname==True:
            s = re.sub(s[s.find('-Xmx'):s.find('M')+1],f'-Xmx{newram}M',str(s))#find where ram and replace it
            s = re.sub(str(s)[s.find('--username')+len('--username')+1:s.find('--width')],f'{newname} ',str(s))#find where nick and replace it
        w=open(bat,mode='w')
        w.write(s)
        w.close()

def deletefiles(folder):
    total = len(os.listdir(folder))
    deleted = 0
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                deleted+=1
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Ошибка удалить: %s. Причина: %s' % (file_path, e))
    return f'Удалено файлов: {deleted} из {total}'

def getlogo():#return launcher logo
    logo = '''
 __        _____ _   _ _____   _        _   _   _ _   _  ____ _   _ _____ ____  
 \ \      / /_ _| \ | | ____| | |      / \ | | | | \ | |/ ___| | | | ____|  _ \ 
  \ \ /\ / / | ||  \| |  _|   | |     / _ \| | | |  \| | |   | |_| |  _| | |_) |
   \ V  V /  | || |\  | |___  | |___ / ___ \ |_| | |\  | |___|  _  | |___|  _ <
    \_/\_/  |___|_| \_|_____| |_____/_/   \_\___/|_| \_|\____|_| |_|_____|_| \_\ 
'''
    return logo

def gfont(size: int):
    return 'Bahnschrift '+str(size)

def wine_popup(msg,sg):
    return sg.Popup(msg,icon='./assets/wine-icon.ico',title='Wine Launcher')

def changetexts(name,text,key,window):#do text animation
    #idk how its work
    exec(f'''
from threading import Thread
from utils import text_animation
from time import sleep as delay
class {name}(Thread):
    def run(self):
        for i in text_animation('{text}'):window['{key}'].update(i);delay(0.05)
anim_{name+'var'} = {name}();anim_{name+'var'}.setDaemon(True);anim_{name+'var'}.start()''',{'window':window})#idk how it work

def str_to_class(classname):#return class
    return getattr(sys.modules[__name__], classname)

class Cheat:
    def __init__(self,name: str,dwnlink: list,jar: str,bat: str,type: str,sounds: bool,crack_by: str):
        self.name = name
        self.dwnlink = dwnlink
        self.jar = jar
        self.bat = bat
        self.type = type
        self.sounds = sounds
        self.crack_by = crack_by
        rprint('Add new cheat: '+name)
    def getname(self):#get cheat name
        return self.name

    def gettype(self):#get cheat type
        return self.type

    def getsounds(self):#get cheat sounds
        return self.sounds

    def getcrack_by(self):#get crack_by
        return self.crack_by

    def cheat_info(self):
        return f'Run minecraft cheat: {self.name}, type: {self.type}, sounds: {str(self.sounds)}'

    def run(self,nickname,ram):
        prefix = '.\\minecraft\\'
        if not os.path.isfile(prefix+self.jar) or not os.path.isfile(prefix+self.bat):#Check if cheat exist
            for i in self.dwnlink:#download all files
                if i!=None:
                    dwnfiles = download(#Download
                        url=i,
                        path='.\\minecraft\\', progressbar=True, replace=True, kind='zip'
                    )
            fix_bat(nickname,ram,False)#fix bat file
            rprint(self.cheat_info())#log to console
            os.system(prefix+self.bat)#run
        else:
            fix_bat(nickname,ram,True)#fix bat file
            rprint(self.cheat_info())#log to console
            os.system(prefix+self.bat)#run

class CustomCheat:
    def __init__(self,jar) -> None:
        self.jar = jar

    def getname(self):
        return str(self.jar[int(str(self.jar).find('\\'))+1:]).capitalize()

    def run(self):
        rprint(f'Run custom cheat: {self.jar}')#log to console
        os.chdir('.\\minecraft')
        os.system('\\minecraft\\'+f'jre8\\bin\\javaw.exe -noverify -Xmx1024M -Djava.library.path="{natives_path}"; -cp "{libraries_path}"\*;"'+sys.path[0]+'\\'+f'{self.jar}" net.minecraft.client.main.Main --username Purpl3_YT --width 854 --height 480 --version CustomCheat --gameDir  --assetsDir assets --assetIndex 1.12 --uuid N/A --accessToken 0 --userType mojang')
        os.chdir('.\\')
           
#---------------
#Cheats

NoRender = Cheat('NoRender',NoRender_download,'Norendercrack.jar','Norender.bat','crack',True,'HCU')

Osium = Cheat('Osium',Osium_download,'OsiumClient.jar','OsiumClient.bat','crack',True,'WhiteWhess')

Fluger = Cheat('Fluger',Fluger_download,'fluger.jar','fluger.bat','crack',True,'kshk')

Rockstar = Cheat('Rockstar',Rockstar_download,'Rockstar.jar','Rockstar.bat','crack',True,'HCU')

Expensive = Cheat('Expensive',Expensive_download,'Expensive.jar','Expensive.bat','crack',True,'HCU')

Wexside = Cheat('Wexside',Wexside_download,'Wexside.jar','Wexside.bat','crack',True,'HCU')

Celestial = Cheat('Celestial',Celestial_download,'Celestial.jar','Celestial.bat','crack',True,'HCU')

EntityWare = Cheat('EntityWare',EntityWare_download,'EntityWare.jar','EntityWare.bat','crack',True,'nn')

MincedRecode = Cheat('MincedRecode',MincedRecode_download,'MincedPon.jar','MincedPon.bat','free',True,None)

ShitRecode = Cheat('ShitRecode',ShitRecode_download,'ShitBeta.jar','ShitBeta.bat','free',True,None)

DestroySquad = Cheat('DestroySquad',DestroySquad_download,'descsquad.jar','descsquad.bat','free',True,None)

Zamorozka = Cheat('Zamorozka',Zamorozka_download,'Zamorozka0.5.jar','Zamorozka0.5.bat','crack',True,'WintWare')

BoberWare = Cheat('BoberWare',BoberWare_download,'BoberWareFree.jar','BoberWareFree.bat','free',True,None)

ExtremeHack = Cheat('ExtremeHack',Extremehack_download,'ExtremeHackB17.jar','ExtremeHackB17.bat','free',True,None)

#---------------
#ExampleCheat = Cheat(
# 'MyCheat2023',     | Name
#  MyCheat_download, | Var to download, check links.py
# 'MyCheat.jar',     | Path to jar
# 'MyCheat.bat',     | Path to bat
# 'free',            | License ['free','crack']
# True)              | Sounds [True,False]

def debug(cheat: Cheat,nick,ram):
    cheat.run(nick,ram)

#debug(NoRender,'Purpl3_YT',4096)
from download import download
from random import choice
from glob import *
from links import *
import os,sys,shutil
import re


class colors:#colors for logo
    RED = '\033[91m'#Red color
    ENDC = '\033[0m'#Stop red color

def rprint(text):
    return print(colors.RED+text+colors.ENDC)

def download_libs(onlyassets=False):
    if not onlyassets:
        if os.path.isdir('./minecraft/') == False:
            d = download(url='https://cdn.discordapp.com/attachments/1022495936628392164/1023650548819439667/bruh.zip',#core aka minecraft folder
                path='.\\minecraft\\', progressbar=True, replace=True, kind='zip')
            if os.path.isdir('./assets') == False or os.path.isfile('./minecraft/OpenAL64.dll'):
                assets = download(
                    url='https://cdn.discordapp.com/attachments/1025789472916389928/1038070679028908032/assets.zip',#assets to work, images etc.
                    path='.\\', progressbar=True, replace=True, kind='zip'
                )
                os.remove('./minecraft/natives/OpenAL64.dll')#remove old openal
                shutil.move('./minecraft/OpenAL64.dll','./minecraft/natives/OpenAL64.dll')#move new opeanal to natives
                os.mkdir('./minecraft/--assetsDir')
                if not os.path.isdir('./minecraft/--assetsDir/assets'):#fix sounds
                    d = download(
                        url='https://cdn.discordapp.com/attachments/1025789472916389928/1025790255808385034/objects.zip',
                        path='.\\minecraft\\--assetsDir\\assets\\', progressbar=True, replace=True, kind='zip'
                    )
                    shutil.move('./minecraft/assets/indexes','./minecraft/--assetsDir/assets')#fix sounds
        else:pass
    elif onlyassets:
        assets = download(
                    url='https://cdn.discordapp.com/attachments/1025789472916389928/1038070679028908032/assets.zip',#assets to work, images etc.
                    path='.\\', progressbar=True, replace=True, kind='zip'
        )

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

def changetexts(name,text,key,window):#do text animation
    #idk how its work
    exec(f'''
from threading import Thread
from utils import text_animation
from time import sleep as delay
class {name}(Thread):
    def run(self):
        for i in text_animation('{text}'):window['{key}'].update(i);delay(0.05)
anim_{name+'var'} = {name}();anim_{name+'var'}.setDaemon(True);anim_{name+'var'}.start()''',{'window':window})

def str_to_class(classname):#return class
    return getattr(sys.modules[__name__], classname)

class Cheat:
    def __init__(self,name: str,dwnlink: list,jar: str,bat: str,type: str,sounds: bool):
        self.name = name
        self.dwnlink = dwnlink
        self.jar = jar
        self.bat = bat
        self.type = type
        self.sounds = sounds
    def getname(self):#get cheat name
        return self.name

    def gettype(self):#get cheat type
        return self.type

    def getsounds(self):#get cheat sounds
        return self.sounds
    
    def run(self,nickname,ram):
        if not os.path.isfile(self.jar) or not os.path.isfile(self.bat):#Check if cheat exist
            for i in self.dwnlink:#download all files
                if i!=None:
                    dwnfiles = download(#Download
                        url=i,
                        path='.\\minecraft\\', progressbar=True, replace=True, kind='zip'
                    )
            fix_bat(nickname,ram,False)#fix bat file
            rprint(f'Run minecraft cheat: {self.name}, type: {self.type}')#log to console
            os.system(self.bat)#run
        else:
            fix_bat(nickname,ram,True)#fix bat file
            rprint(f'Run minecraft cheat: {self.name}, type: {self.type}')#log to console
            os.system(self.bat)#run
#---------------
#Cheats

NoRender = Cheat('NoRender',NoRender_download,'.\\minecraft\\Norendercrack.jar','.\\minecraft\\Norender.bat','crack',True)
#Norender.run('Purpl3_YT',4096,True)
Fluger = Cheat('Fluger',Fluger_download,'.\\minecraft\\fluger.jar','.\\minecraft\\fluger.bat','crack',True)
#Fluger.run('Purpl3',4096,False)
Rockstar = Cheat('Rockstar',Rockstar_download,'.\\minecraft\\Rockstar.jar','.\\minecraft\\Rockstar.bat','crack',True)
#Rockstar.run('Purpl3_YT',4096,False)        
Expensive = Cheat('Expensive',Expensive_download,'.\\minecraft\\Expensive.jar','.\\minecraft\\Expensive.bat','crack',True)
#Expensive.run('Purpl3_YT',4096,True)
Wexside = Cheat('Wexside',Wexside_download,'.\\minecraft\\Wexside.jar','.\\minecraft\\Wexside.bat','crack',True)
#Wexside.run('Purpl3_YT',4096,True)
Celestial = Cheat('Celestial',Celestial_download,'.\\minecraft\\Celestial.jar','.\\minecraft\\Celestial.bat','crack',True)
#Celestial.run('Purpl3_YT',4096)
NeverHook = Cheat('NeverHook',NeverHook_download,'.\\minecraft\\"NeverHook.jar"','.\\minecraft\\"NeverHook.bat"','crack',True)
#NeverHook.run('Purpl3_YT',4096)
Osium = Cheat('Osium',Osium_download,'.\\minecraft\\OsiumClient.jar','.\\minecraft\\OsiumClient.bat','crack',True)
#Osium.run('Purpl3_YT',4096)
EntityWare = Cheat('EntityWare',EntityWare_download,'.\\minecraft\\EntityWare.jar','.\\minecraft\\EntityWare.bat','crack',True)
#EntityWare.run('Purpl3_YT',4096)
MincedRecode = Cheat('MincedRecode',MincedRecode_download,'.\\minecraft\\MincedPonchik.jar','.\\minecraft\\MincedPonchik.bat','free',True)
#Minced.run('Purpl3_YT',4096)
ShitRecode = Cheat('ShitRecode',ShitRecode_download,'.\\minecraft\\ShitBeta.jar','.\\minecraft\\ShitBeta.bat','free',True)
#ShitRecode.run('Purpl3_YT',4096)
DestroySquad = Cheat('DestroySquad',DestroySquad_download,'.\\minecraft\\descsquad.jar','.\\minecraft\\descsquad.bat','free',True)
#DestroySquad.run('Purpl3_YT',4096)
Zamorozka = Cheat('Zamorozka',Zamorozka_download,'.\\minecraft\\Zamorozka0.5.jar','.\\minecraft\\Zamorozka0.5.bat','crack',True)
#Zamorozka.run('Purpl3_YT',4096)
#---------------
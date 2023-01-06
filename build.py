from gui import version
import os,sys,glob,shutil
import time
out_folder = './out'
name = 'WineLauncher_Beta_'+version
main_script = './gui.py'

os.chdir(sys.path[0])

os.system('cls')

def build():
    os.system(sys.path[0]+'\\venv\\Scripts\\activate.bat')
    os.system(f'pyinstaller --noconfirm --onefile --console --clean --distpath "{out_folder}" --icon "./assets/wine-icon.ico" --name "{name}"  "{main_script}"')


def clear_cache():#delete unused files
    all_specs = glob.glob('./*.spec')
    folders = ['./build','__pycache__']
    for spec in all_specs:
        os.remove(spec)
    for tree in folders:
        try:
            shutil.rmtree(tree)
        except FileNotFoundError:
            pass

if '__main__' == __name__:
    build()#build
 
    time.sleep(2)
    
    clear_cache()#clear cache etc
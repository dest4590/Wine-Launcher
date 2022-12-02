from gui import version
import os,sys,glob

out_folder = './out'
name = 'WineLauncher_Beta_'+version
main_script = './gui.py'

def build():
    os.system(sys.path[0]+'\\venv\\Scripts\\activate.bat')
    os.system(f'pyinstaller --noconfirm --onefile --console --clean --distpath "{out_folder}" --icon "./assets/wine-icon.ico" --name "{name}"  "{main_script}"')

def clear_cache():#delete unused files
    all_specs = glob.glob('./*.spec')
    for spec in all_specs:
        os.remove(spec)
    os.remove('./build')

if '__main__' == __name__:
    build()#build
    clear_cache()#clear cache etc
from gui import version
import os,sys

out_folder = './out'
name = 'WineLauncher_TEST_'+version
main_script = './gui.py'

def build():
    os.system(sys.path[0]+'\\venv\\Scripts\\activate.bat')
    os.system(f'pyinstaller --noconfirm --onefile --console --clean --distpath "{out_folder}" --icon "./assets/wine-icon.ico" --name "{name}"  "{main_script}"')

if '__main__' == __name__:
    build()
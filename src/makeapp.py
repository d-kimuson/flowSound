import os
import shutil


bef_path = "C:/Users/kaito/Projects/flowSound/src/dist"
aft_path = "C:/Users/kaito/Projects/flowSound/src/app"


def makeapp():
    shutil.rmtree(f"{os.getcwd()}/dist/profiles")
    shutil.rmtree(f"{os.getcwd()}/build")
    os.remove(f"{os.getcwd()}/dist/connect.exe")
    os.system("py -3.6 -m PyInstaller connect.spec")
    shutil.make_archive(aft_path, 'zip', root_dir=bef_path)


if __name__ == "__main__":
    makeapp()

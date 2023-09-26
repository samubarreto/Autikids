#python autikidsSetup.py build
import sys
from cx_Freeze import setup, Executable

build_exe_options = {"build_exe": "Autikids EXE", "packages": ["os", "pygame", "win32com.client", "win32"], "includes": ["tkinter", "sqlite3"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Autikids",
    version = 1.0,
    description = None,
    options = {"build_exe": build_exe_options},
    executables = [Executable("Autikids.py", base=base, icon="icon.ico")]
)
import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame"],
    "excludes": ["tkinter", "unittest"],
    "include_files": [] 
}

base = None
if sys.platform == "win32":
    base = "gui"

setup(
    name="EscapeDoLorkus",
    version="2.0",
    description="Jogo 2D - Desvie dos Livros do Professor Lorkus",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="EscapeDoLorkus.exe"
        )
    ]
)

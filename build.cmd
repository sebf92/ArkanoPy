pyinstaller --onefile main.py
cd dist
del arkanopy.exe
rename main.exe arkanopy.exe
cd ..
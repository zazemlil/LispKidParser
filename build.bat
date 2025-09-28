rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del LispKidParser.spec 2>nul

.\.venv\Scripts\pyinstaller.exe --onefile --noupx --clean --name=LispKidParser --icon=.\icon.ico parser.py
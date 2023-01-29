import os

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

searchTerm = ''
scanfolderpath = ''
chosenfilepath = ''
chosenfilename = ''
xPosition = 0
yPosition = 0
windowWidth = 500
windowHieght = 1100
sidebarIsVisibile = False

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
HTML_EXTENSIONS = ['.htm', '.html']

TEXT = ""
DATA = None
FILETOANALYZE = None

ALREADY_CONVERTED_FILES = []

PDFJS = f"file://{os.path.abspath(os.path.join('static', 'pdfjs', 'web', 'viewer.html'))}"
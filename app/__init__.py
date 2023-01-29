import datetime
import re
import time
from dotenv import load_dotenv
from matplotlib import pyplot as plt

from app.model import getText, getExcel, loadExcel
load_dotenv()

import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as qtc

from app.editor import TextEdit as Editor
from app.methods import splitext

import os, sys, json

from app.contants import *

from PyQt6.QtWebEngineWidgets import QWebEngineView
import xlwt


def cancelEdit(mainWindow):
    global TEXT
    TEXT = ""
    navigateTo(mainWindow, 'mainWindow')

def navigateTo(window, windowname):
    newWindow = globals()[windowname](window)
    window.setCentralWidget(newWindow)

def searchDocs(window, term):
    global searchTerm
    searchTerm = term
    navigateTo(window, "storageWindow")

def createPrerequisites(mainwindow, currentwindow, title):
    # set window position
    mainwindow.title = title
    mainwindow.setWindowTitle(mainwindow.title)
    # set window background color
    # window.setStyleSheet("background-color: #CBDFE0;")
    currentwindow.containerLayout = qtw.QHBoxLayout()
    currentwindow.setLayout(currentwindow.containerLayout)
    # create a mainLayout that will contain other layouts
    currentwindow.mainLayout = qtw.QVBoxLayout()
    currentwindow.containerLayout.addLayout(currentwindow.mainLayout)
    # create navigation bar
    createNavigationBar(mainwindow, currentwindow)

def createNavigationBar(mainwindow, currentwindow):
    # create a navigation bar that sits at the top
    navigationBar = qtw.QHBoxLayout()
    # add a menu icon by the left side of the navigation bar
    homeIcon = qtw.QPushButton()
    homeIcon.setIcon(gui.QIcon(os.path.join('static', 'home.png')))
    homeIcon.setIconSize(qtc.QSize(30, 30))
    homeIcon.setStyleSheet("background-color: #CBDFE0;")
    homeIcon.setFixedSize(qtc.QSize(30, 30))
    navigationBar.addWidget(homeIcon)
    # when menu icon is clicked, toggle sidebar
    homeIcon.clicked.connect(lambda: navigateTo(mainwindow, 'mainWindow'))
    # add a title by the center of the navigation bar
    titleLabel = qtw.QLabel(mainwindow.title)
    # make title bigger, bold and centered
    titleLabel.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
    titleLabel.setFixedSize(qtc.QSize(windowWidth, 30))
    navigationBar.addWidget(titleLabel)
    # add a search bar by the right side of the navigation bar
    currentwindow.searchBar = qtw.QLineEdit()
    # set search bar text to searchTerm
    currentwindow.searchBar.setText(searchTerm)
    # add placeholder text
    currentwindow.searchBar.setPlaceholderText('Search stored documents')
    currentwindow.searchBar.setFixedSize(qtc.QSize(300, 30))
    navigationBar.addWidget(currentwindow.searchBar)
    # when enter key is pressed, search for the entered term
    currentwindow.searchBar.returnPressed.connect(lambda: searchDocs(mainwindow, currentwindow.searchBar.text()))
    # add a settings icon by the right side of the navigation bar
    settingsIcon = qtw.QPushButton()
    settingsIcon.setIcon(gui.QIcon(os.path.join('static', 'settings.png')))
    settingsIcon.setIconSize(qtc.QSize(30, 30))
    settingsIcon.setStyleSheet("background-color: #CBDFE0;")
    settingsIcon.setFixedSize(qtc.QSize(30, 30))
    navigationBar.addWidget(settingsIcon)
    # add analysis button to the right side of the navigation bar
    analysisIcon = qtw.QPushButton()
    analysisIcon.setIcon(gui.QIcon(os.path.join('static', 'analysis.png')))
    analysisIcon.setIconSize(qtc.QSize(30, 30))
    analysisIcon.setStyleSheet("background-color: #CBDFE0;")
    analysisIcon.setFixedSize(qtc.QSize(30, 30))
    navigationBar.addWidget(analysisIcon)
    # when settings is clicked, navigate to settings page
    settingsIcon.clicked.connect(lambda: navigateTo(mainwindow, 'settingsWindow'))
    settingsIcon.setToolTip('Change settings')
    # when analysis is clicked, navigate to analysis page
    analysisIcon.clicked.connect(lambda: navigateTo(mainwindow, 'analysisWindow'))
    # when analysisIcon is hovered over, show a tooltip
    analysisIcon.setToolTip('Analyze documents')
    # add the navigation bar to the layout
    currentwindow.mainLayout.addLayout(navigationBar)

def changeSettings(mainwindow, currentwindow, settingsName):
    if settingsName == 'Mode':
        setMode(mainwindow)
    elif settingsName == 'Scan Folder':
        setScanfolder(mainwindow)
    elif settingsName == 'Storage Folder':
        setStoragefolder(mainwindow)
    # reload the current window
    navigateTo(mainwindow, currentwindow.__class__.__name__)

def chooseFile(window):
    global chosenfilename, chosenfilepath
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    # open image files only
    file = str(qtw.QFileDialog.getOpenFileName(window, 'Open file', settings.get('scanfolder'), 'Image files (*.png *.jpg *.jpeg *.gif *.bmp)'))
    if file.strip() != "('', '')":
        # get the filename from the path
        filename = os.path.basename(file)
        filename = filename.split("'")[0]
        # set the filename to the button
        window.fileButton.setText(filename)
        # set the filename to chosenfilename
        chosenfilename = filename
        # get the filepath from the file
        filepath = os.path.dirname(file)
        # set the filepath to chosenfilepath
        chosenfilepath = os.path.join(filepath[2:], filename)

def chooseDirectory(window):
    path = str(qtw.QFileDialog.getExistingDirectory(window, 'Open directory', './'))
    return path

def setScanfolder(window):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    scanfolder = chooseDirectory(window)
    if scanfolder:
        settings['scanfolder'] = scanfolder
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

def setStoragefolder(window):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    storagefolder = chooseDirectory(window)
    if storagefolder:
        settings['storagefolder'] = storagefolder
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

def changeMode(window, mode):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    settings['mode'] = mode
    with open('settings.json', 'w') as f:
        json.dump(settings, f)
    # reload the settings window
    navigateTo(window, 'settingsWindow')

def setMode(window):
    # create a popup window with a dark or light mode option
    window.modePopup = qtw.QWidget()
    window.modePopup.setWindowTitle('Choose mode')
    window.modePopup.setFixedSize(qtc.QSize(300, 200))
    window.modePopup.setWindowFlags(qtc.Qt.WindowType.WindowStaysOnTopHint)
    window.modePopup.setAttribute(qtc.Qt.WidgetAttribute.WA_DeleteOnClose)
    window.modePopup.setAttribute(qtc.Qt.WidgetAttribute.WA_TranslucentBackground)
    window.modePopup.setAttribute(qtc.Qt.WidgetAttribute.WA_NoSystemBackground)
    window.modePopup.setWindowModality(qtc.Qt.WindowModality.ApplicationModal)
    # create a layout for the popup window
    modePopupLayout = qtw.QVBoxLayout()
    window.modePopup.setLayout(modePopupLayout)
    # create a label for the popup window
    modeLabel = qtw.QLabel('Choose mode')
    modeLabel.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
    modePopupLayout.addWidget(modeLabel)
    # create a dark mode button
    darkModeButton = qtw.QPushButton('Dark mode')
    darkModeButton.setFixedSize(qtc.QSize(250, 50))
    darkModeButton.clicked.connect(lambda: changeMode(window, 'dark'))
    modePopupLayout.addWidget(darkModeButton)
    # create a light mode button
    lightModeButton = qtw.QPushButton('Light mode')
    lightModeButton.setFixedSize(qtc.QSize(250, 50))
    lightModeButton.clicked.connect(lambda: changeMode(window, 'light'))
    modePopupLayout.addWidget(lightModeButton)
    # show the popup window
    window.modePopup.show()


def checkSettings(window):
    global ALREADY_CONVERTED_FILES
    # create settings.json if it doesn't exist
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as f:
            f.write('{"mode": "light"}')
    # load settings.json
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    # check if scanfolder has value
    if not settings.get('scanfolder'):
        # create a dialog to ask the user to choose a directory
        dialog = qtw.QMessageBox()
        dialog.setIcon(qtw.QMessageBox.Icon.Information)
        dialog.setText('Please choose a directory to scan')
        dialog.setWindowTitle('No scanfolder')
        dialog.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        dialog.exec()
        setScanfolder(window)
    if not settings.get('storagefolder'):
        # create a dialog to ask the user to choose a directory
        dialog = qtw.QMessageBox()
        dialog.setIcon(qtw.QMessageBox.Icon.Information)
        dialog.setText('Please choose a storage directory')
        dialog.setWindowTitle('No storagefolder')
        dialog.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        dialog.exec()
        setStoragefolder(window)
    # set content of scanfolder to alreadyconvertedfiles
    ALREADY_CONVERTED_FILES = os.listdir(settings.get('scanfolder'))

def previewImage(window, folder, filename):
    # create a preview window
    window.previewWindow = qtw.QWidget()
    window.previewWindow.setWindowTitle('Preview')
    # make the window size to a mimimum of 500x500 and maximum of A4 paper
    window.previewWindow.setMinimumSize(qtc.QSize(500, 500))
    window.previewWindow.setMaximumSize(qtc.QSize(1000, 500))
    window.previewWindow.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
    window.previewWindow.setAttribute(qtc.Qt.WA_DeleteOnClose)
    window.previewWindow.setAttribute(qtc.Qt.WA_TranslucentBackground)
    window.previewWindow.setAttribute(qtc.Qt.WA_NoSystemBackground)
    window.previewWindow.setWindowModality(qtc.Qt.ApplicationModal)
    # create a layout for the preview window
    previewWindowLayout = qtw.QVBoxLayout()
    window.previewWindow.setLayout(previewWindowLayout)
    # create a label for the preview window
    previewLabel = qtw.QLabel(filename)
    previewLabel.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
    previewWindowLayout.addWidget(previewLabel)
    # create a label for the preview window
    previewImage = qtw.QLabel()
    filename = os.path.join(folder, filename)
    previewImage.setPixmap(gui.QPixmap(filename))
    # make image fit the window
    previewImage.setScaledContents(True)
    previewWindowLayout.addWidget(previewImage)
    # show the preview window
    window.previewWindow.show()

class mainWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, os.environ.get('APP_NAME'))
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.mainLayout.addLayout(self.mainContent)
        # create an image widget that displays and a gif image from the static folder
        self.imageWidget = qtw.QLabel()
        self.imageWidget.setPixmap(gui.QPixmap(os.path.join('static', 'scanner.png')))
        self.imageWidget.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.mainContent.addWidget(self.imageWidget)
        # self.mainContent.addWidget(self.body)
        self.converterLayout = qtw.QHBoxLayout()
        self.mainContent.addLayout(self.converterLayout)
        # create a button for choosing file and add it to the left side of the mainContent layout
        self.fileButton = qtw.QPushButton('Choose file')
        self.fileButton.setFixedSize(qtc.QSize(200, 30))
        # set button color to #509BA6
        self.fileButton.setStyleSheet("background-color: #509BA6;")
        self.converterLayout.addWidget(self.fileButton)
        # set default chosen file type
        self.chosenfiletype = 'text'
        # create a combo box for choosing file types and add it to the right side of the mainContent layout
        self.fileTypeComboBox = qtw.QComboBox()
        self.fileTypeComboBox.setFixedSize(qtc.QSize(200, 30))
        self.fileTypeComboBox.addItem('Choose File Type')
        self.fileTypeComboBox.addItem('text')
        self.fileTypeComboBox.addItem('table')
        # set combo box color to #509BA6
        self.fileTypeComboBox.setStyleSheet("background-color: #509BA6;")
        # when the user chooses a file type, set the chosen file type to the chosen file type
        self.fileTypeComboBox.currentTextChanged.connect(lambda: self.setChosenFileType(self.fileTypeComboBox.currentText()))
        self.converterLayout.addWidget(self.fileTypeComboBox)
        self.fileTypeButton = qtw.QPushButton('Convert')
        self.fileTypeButton.setFixedSize(qtc.QSize(200, 30))
        # set button color to #509BA6
        self.fileTypeButton.setStyleSheet("background-color: #509BA6;")
        self.converterLayout.addWidget(self.fileTypeButton)
        # when fileButton is clicked call chooseFile
        self.fileButton.clicked.connect(lambda: chooseFile(self))
        # when the fileTypeButton is clicked hide this window and show editWindow
        self.fileTypeButton.clicked.connect(lambda: startEditing(window, self.chosenfiletype))

    def setChosenFileType(self, chosenfiletype):
        global FILETOANALYZE
        FILETOANALYZE = None
        self.chosenfiletype = chosenfiletype if chosenfiletype != 'Choose File Type' else 'text'
        self.fileTypeComboBox.setCurrentText(self.chosenfiletype)



def startEditing(window, filetype):
    # check if chosenfilepath exists
    if chosenfilepath:
        if filetype == 'text':
            navigateTo(window, 'editWindow')
        elif filetype == 'table':
            navigateTo(window, 'excelWindow')
    else:
        # create a dialog to ask the user to choose a file
        dialog = qtw.QMessageBox()
        dialog.setIcon(qtw.QMessageBox.Icon.Information)
        dialog.setText('Please choose a file')
        dialog.setWindowTitle('No file')
        dialog.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        dialog.exec()

class excelWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, os.environ.get('APP_NAME'))
        # convert the given image file to text
        self.converter = Converter(chosenfilepath, 'table')
        self.converter.start()
        self.converter.finished.connect(lambda: self.setupUi(window))
        # create a widget that shows a loading gif using qmovie
        self.loader = gui.QMovie(os.path.join('static', 'loading.gif'))
        self.loadingWidget = qtw.QLabel()
        self.loadingWidget.setMovie(self.loader)
        self.loadingWidget.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.loadingWidget)
        self.loader.start()
    
    def setupUi(self, window):
        self.filename = None
        # remove the loading widget
        self.mainLayout.removeWidget(self.loadingWidget)
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.mainLayout.addLayout(self.mainContent)
        self.table = qtw.QTableWidget()
        # set table background color to #F5F5F5
        # self.table.setStyleSheet("background-color: #F5F5F5;")
        # self.table.setStyleSheet("color: #000000;")
        self.mainContent.addWidget(self.table)
        # create a layout for the buttons
        self.buttonLayout = qtw.QHBoxLayout()
        self.mainContent.addLayout(self.buttonLayout)
        # add save button
        self.saveButton = qtw.QPushButton('Save')
        self.saveButton.setFixedSize(qtc.QSize(200, 30))
        # set button color to #509BA6
        self.saveButton.setStyleSheet("background-color: #509BA6;")
        self.buttonLayout.addWidget(self.saveButton)
        # when the save button is clicked, save the file
        self.saveButton.clicked.connect(lambda: self.savefile(self.filename))
        # add analysis button
        self.analysisButton = qtw.QPushButton('Analyze')
        self.analysisButton.setFixedSize(qtc.QSize(200, 30))
        self.analysisButton.setStyleSheet("background-color: #509BA6;")
        self.buttonLayout.addWidget(self.analysisButton)
        self.analysisButton.hide()
        # when the analysis button is clicked, show analysisWindow
        self.analysisButton.clicked.connect(lambda: navigateTo(window, 'analysisWindow'))
        # add cancel button
        self.cancelButton = qtw.QPushButton('Cancel')
        self.cancelButton.setFixedSize(qtc.QSize(200, 30))
        # set button color to #509BA6
        self.cancelButton.setStyleSheet("background-color: #509BA6;")
        self.buttonLayout.addWidget(self.cancelButton)
        # when the cancel button is clicked, hide this window and show mainWindow
        self.cancelButton.clicked.connect(lambda: navigateTo(window, 'mainWindow'))
        if DATA.size == 0:
            return
        DATA.fillna('', inplace=True)
        self.table.setRowCount(DATA.shape[0])
        self.table.setColumnCount(DATA.shape[1])
        columns = [ str(i) for i in DATA.columns ]
        self.table.setHorizontalHeaderLabels(columns)
        # returns pandas array object
        for row in DATA.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = qtw.QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, tableItem)
        self.table.setColumnWidth(2, 300)

        # when the table is right clicked, show a context menu
        self.table.setContextMenuPolicy(qtc.Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.showContextMenu)

    
    def showContextMenu(self, pos):
        # create menu for the selected area on table
        menu = qtw.QMenu()
        # create a delete row action
        deleteRowAction = menu.addAction('Delete Row')
        # when delete row action is clicked, delete the selected row
        deleteRowAction.triggered.connect(lambda: self.deleteRow(self.table.currentRow()))
        # create a delete column action
        deleteColumnAction = menu.addAction('Delete Column')
        # when delete column action is clicked, delete the selected column
        deleteColumnAction.triggered.connect(lambda: self.deleteColumn(self.table.currentColumn()))
        # # create a delete selection action
        # deleteSelectionAction = menu.addAction('Delete Selection')
        # # when delete selection action is clicked, delete the selected area
        # deleteSelectionAction.triggered.connect(lambda: self.deleteSelection(self.table.selectedRanges()))
        # # show the menu at the position of the click
        menu.exec(self.table.mapToGlobal(pos))
    
    def deleteRow(self, row):
        # delete the selected row
        self.table.removeRow(row)
    
    def deleteColumn(self, column):
        # delete the selected column
        self.table.removeColumn(column)
    
    def deleteSelection(self, selection):
        # delete only the rows and columns selected
        for range in selection:
            self.table.removeRow(range.topRow())
            self.table.removeColumn(range.leftColumn())

    def savefile(self, filename=None):
        global FILETOANALYZE
        if not filename:
            filename,_ = qtw.QFileDialog.getSaveFileName(self, 'Save File', '', "Excel Files (*.xlsx *.xls *.csv)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.table.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, qtc.Qt.Orientation.Horizontal)
            sheet.write(0, c+1, text, style=style)

        for r in range(model.rowCount()):
            text = model.headerData(r, qtc.Qt.Orientation.Vertical)
            sheet.write(r+1, 0, text, style=style)

        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r+1, c+1, text)
        if filename:
            wbk.save(filename)
            FILETOANALYZE = filename
            self.filename = filename
            self.analysisButton.show()


class analysisWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, 'Document Analysis')
        self.filename = None
        self.setupUi(window)
    
    def setupUi(self, window):
        global FILETOANALYZE
        # if self.filename is None create a popup to choose file from the file system
        self.filename = FILETOANALYZE
        if self.filename is None:
            # get storagefolder from settings.json
            with open(os.path.join('settings.json'), 'r') as f:
                settings = json.load(f)
                storagefolder = settings['storagefolder']
                self.filename, _ = qtw.QFileDialog.getOpenFileName(self, 'Open File', storagefolder, "Excel Files (*.xlsx *.xls *.csv)")
        if not self.filename:
            # go back to main window if no file is selected
            cancelEdit(window)
        # load the excel file into pandas dataframe
        DATA = loadExcel(self.filename)
        # create a horizontal layout for the analysis area and the maincontent
        self.field = qtw.QHBoxLayout()
        # create a vertical layout for the analysis area
        self.analysisLayout = qtw.QVBoxLayout()
        # add a filter area
        self.filterArea = qtw.QVBoxLayout()
        self.analysisLayout.addLayout(self.filterArea)
        # add a label for the filter area
        self.filterLabel = qtw.QLabel('Filter')
        self.filterArea.addWidget(self.filterLabel)
        # center and bold the label
        self.filterLabel.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.filterLabel.setStyleSheet("font-weight: bold;")
        # add retirementArea to the analysisLayout
        self.ritermentAnalysisArea = qtw.QVBoxLayout()
        self.analysisLayout.addLayout(self.ritermentAnalysisArea)
        # add a label to the ritermentAnalysisArea
        self.rlabel = qtw.QLabel('Retirement Analysis')
        # center and bold the label
        self.rlabel.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.rlabel.setStyleSheet("font-weight: bold;")
        self.ritermentAnalysisArea.addWidget(self.rlabel)
        # add the distributionAnalysis area to the analysis area
        self.distributionAnalysisArea = qtw.QVBoxLayout()
        self.analysisLayout.addLayout(self.distributionAnalysisArea)
        # add a label to the distributionAnalysisArea
        self.dlabel = qtw.QLabel('Distribution Analysis')
        # center and bold the label
        self.dlabel.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.dlabel.setStyleSheet("font-weight: bold;")
        self.distributionAnalysisArea.addWidget(self.dlabel)
        # add the analysis area to the horizontal layout
        self.field.addLayout(self.analysisLayout, 20)
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.field.addLayout(self.mainContent, 80)
        self.mainLayout.addLayout(self.field)

        # initialize a hidden progress bar
        self.progressBar = qtw.QProgressBar()
        self.progressBar.setGeometry(30, 40, 200, 25)
        self.progressBar.hide()
        self.mainContent.addWidget(self.progressBar)
        
        self.table = qtw.QTableWidget()
        self.mainContent.addWidget(self.table)
        # add select field that shows a list of all the columns in the excel file
        self.filterColumns = qtw.QComboBox()
        self.retirementColumns = qtw.QComboBox()
        self.distributionColumns = qtw.QComboBox()
        self.selectedColumn = '0'
        # when the select field is changed, set the selected column
        self.filterColumns.currentIndexChanged.connect(lambda: self.setSelectedColumn(self.filterColumns.currentText()))
        self.retirementColumns.currentIndexChanged.connect(lambda: self.setSelectedColumn(self.retirementColumns.currentText()))
        self.distributionColumns.currentIndexChanged.connect(lambda: self.setSelectedColumn(self.distributionColumns.currentText()))
        # create a layout for the buttons
        self.buttonLayout = qtw.QHBoxLayout()
        self.mainContent.addLayout(self.buttonLayout)
        # add save button
        self.saveButton = qtw.QPushButton('Save')
        # set button color to #509BA6
        self.saveButton.setStyleSheet("background-color: #509BA6;")
        self.buttonLayout.addWidget(self.saveButton)
        # when the save button is clicked, save the file
        self.saveButton.clicked.connect(lambda: self.savefile(self.filename))
        # add save as button
        self.saveAsButton = qtw.QPushButton('Save As')
        # set button color to #509BA6
        self.saveAsButton.setStyleSheet("background-color: #509BA6;")
        self.buttonLayout.addWidget(self.saveAsButton)
        # when the save button is clicked, save the file
        self.saveAsButton.clicked.connect(lambda: self.savefileas())
        # add undo button
        # add undo button
        self.undoButton = qtw.QPushButton('Reload')
        self.undoButton.setStyleSheet("background-color: #509BA6;")
        self.buttonLayout.addWidget(self.undoButton)
        # when the undo button is clicked, undo the retirement analysis
        self.undoButton.clicked.connect(self.createTable)
        # add cancel button
        self.cancelButton = qtw.QPushButton('Cancel')
        # set button color to #509BA6
        self.cancelButton.setStyleSheet("background-color: #509BA6;")
        self.buttonLayout.addWidget(self.cancelButton)
        # when the cancel button is clicked, hide this window and show mainWindow
        self.cancelButton.clicked.connect(lambda: navigateTo(window, 'mainWindow'))
        if DATA.size == 0:
            return
            
        # SET ANALYSIS AREA
        self.setupFilterArea()
        self.setupRetirementArea()
        self.setupDistributionArea()
        
        self.createTable()

    
    def setupFilterArea(self):
        # add filter column
        self.filterArea.addWidget(self.filterColumns)
        # add a combo box for selecting criteria
        self.filterCriteria = qtw.QComboBox()
        self.filterCriteria.addItems(['contains', 'does not contain', 'is equal to', 'is not equal to', 'is greater than', 'is less than'])
        self.filterArea.addWidget(self.filterCriteria)
        # add filter word
        self.filterword = qtw.QLineEdit()
        self.filterword.setPlaceholderText('Filter word')
        self.filterArea.addWidget(self.filterword)
        # add filter button
        self.filterButton = qtw.QPushButton('Apply Filter')
        self.filterButton.setFixedSize(qtc.QSize(200, 30))
        # set button color to #509BA6
        self.filterButton.setStyleSheet("background-color: #509BA6;")
        self.filterArea.addWidget(self.filterButton)
        # when the filter button is clicked, apply the filter
        self.filterButton.clicked.connect(lambda: self.applyFilter(self.filterword.text(), self.filterCriteria.currentText(), self.selectedColumn))

    
    def setupRetirementArea(self):
        # add default retirement age field
        self.retirementAge = qtw.QLineEdit()
        self.retirementAge.setPlaceholderText('Retirement Age')
        self.ritermentAnalysisArea.addWidget(self.retirementAge)
        self.ritermentAnalysisArea.addWidget(self.retirementColumns)

        self.dateFormat = qtw.QComboBox()
        self.dateFormat.addItem('Select Date Format')
        # add date formats with slashes
        self.dateFormat.addItem('MM/DD/YYYY')
        self.dateFormat.addItem('DD/MM/YYYY')
        self.dateFormat.addItem('YYYY/MM/DD')
        self.dateFormat.addItem('YYYY/DD/MM')
        # add date formats with dashes
        self.dateFormat.addItem('MM-DD-YYYY')
        self.dateFormat.addItem('DD-MM-YYYY')
        self.dateFormat.addItem('YYYY-MM-DD')
        self.dateFormat.addItem('YYYY-DD-MM')

        self.selectedDateFormat = 'DD/MM/YYYY'
        # when the select field is changed, set the selected date format
        self.dateFormat.currentIndexChanged.connect(lambda: self.setSelectedDateFormat(self.dateFormat.currentText()))
        self.ritermentAnalysisArea.addWidget(self.dateFormat)

        self.runRetirementAnalysisButton = qtw.QPushButton('Run Analysis')
        self.runRetirementAnalysisButton.setFixedSize(qtc.QSize(200, 30))
        self.runRetirementAnalysisButton.setStyleSheet("background-color: #509BA6;")
        self.ritermentAnalysisArea.addWidget(self.runRetirementAnalysisButton)
        # when the run button is clicked, run the retirement analysis
        self.runRetirementAnalysisButton.clicked.connect(lambda: self.runRetirementAnalysis(self.retirementAge.text(), self.selectedColumn, self.selectedDateFormat))
    

    def setupDistributionArea(self):
        # add a line edit for the distribution location
        self.distributionLocation = qtw.QLineEdit()
        self.distributionLocation.setPlaceholderText('Location')
        self.distributionAnalysisArea.addWidget(self.distributionLocation)
        # add default retirement age field
        self.distributionAnalysisArea.addWidget(self.distributionColumns)
        # add a line edit for the population size
        self.populationSize = qtw.QLineEdit()
        self.populationSize.setPlaceholderText('Population Size')
        self.distributionAnalysisArea.addWidget(self.populationSize)
        # add a button to run the analysis
        self.runDistributionAnalysisButton = qtw.QPushButton('Run Analysis')
        self.runDistributionAnalysisButton.setFixedSize(qtc.QSize(200, 30))
        self.runDistributionAnalysisButton.setStyleSheet("background-color: #509BA6;")
        self.distributionAnalysisArea.addWidget(self.runDistributionAnalysisButton)
        # when the run button is clicked, run the distribution analysis
        self.runDistributionAnalysisButton.clicked.connect(lambda: self.runDistributionAnalysis(self.distributionLocation.text(), self.selectedColumn, self.populationSize.text()))
        
    
    def createTable(self):
        self.progressBar.show()
        self.fileLoader = Excelloader(self)
        self.fileLoader.start()
        # when finished call self.prepareAnalysisColumns() and self.progressBar.hide()
        self.fileLoader.finished.connect(self.prepareAnalysisColumns)
        # update progress bar
        self.fileLoader.progress.connect(self.progressBar.setValue)
    
    def prepareAnalysisColumns(self):
        self.progressBar.hide()
        # clear items from self.filterColumns
        self.filterColumns.clear()
        self.filterColumns.addItem('Select Column')
        # clear items from self.retirementColumns
        self.retirementColumns.clear()
        self.retirementColumns.addItem('Select Column')
        # clear items from self.distributionColumns
        self.distributionColumns.clear()
        self.distributionColumns.addItem('Select Column')
        for i in range(self.table.columnCount()):
            self.filterColumns.addItem(str(i))
            self.retirementColumns.addItem(str(i))
            self.distributionColumns.addItem(str(i))
        self.filterColumns.setCurrentText(self.selectedColumn)
        self.retirementColumns.setCurrentText(self.selectedColumn)
        self.distributionColumns.setCurrentText(self.selectedColumn)
    
    def runRetirementAnalysis(self, retirementAge, selectedColumn, selectedDateFormat):
        if retirementAge and selectedColumn != 'Select Column' and selectedDateFormat != 'Select Date Format':
            # run the retirement analysis
            self.analysis = Analyze(self, 'Retirement Analysis', params={'retirementAge': retirementAge, 'selectedColumn': selectedColumn, 'selectedDateFormat': selectedDateFormat})
            self.analysis.start()
            # show progress bar
            self.progressBar.show()
            self.analysis.progress.connect(self.progressBar.setValue)
            self.analysis.finished.connect(lambda: self.progressBar.hide())
        else:
            self.showMessageBox('Please fill in all fields.')
    
    def applyFilter(self, filterWord, filterCriteria, selectedColumn):
        if filterWord and selectedColumn != 'Select Column':
            # apply the filter
            self.filter = Filter(self, params={'filterWord': filterWord, 'filterCriteria':filterCriteria, 'selectedColumn': selectedColumn})
            self.filter.start()
            # show progress bar
            self.progressBar.show()
            self.filter.progress.connect(self.progressBar.setValue)
            self.filter.finished.connect(lambda: self.progressBar.hide())
        else:
            self.showMessageBox('Please fill in all fields.')
    
    def runDistributionAnalysis(self, location, selectedColumn, populationSize):
        self.matches = 0
        if location and selectedColumn != 'Select Column' and populationSize:
            # run the retirement analysis
            self.analysis = Analyze(self, 'Distribution Analysis', params={'location': location, 'selectedColumn': selectedColumn, 'populationSize': populationSize})
            self.analysis.start()
            # show progress bar
            self.progressBar.show()
            self.analysis.progress.connect(self.progressBar.setValue)
            self.analysis.matches.connect(self.updateMatches)
            self.analysis.finished.connect(lambda: self.progressBar.hide())
            self.analysis.finished.connect(lambda: self.drawChart({'population':float(self.populationSize.text()), 'matches':float(self.matches)}, 'Distribution Analysis'))
        else:
            self.showMessageBox('Please fill in all fields.')
    
    def updateMatches(self, matches):
        self.matches = matches
    
    def drawChart(self, data, title):
        # get storagefolder from settings.json
        settings = json.load(open('settings.json'))
        storagefolder = settings['storagefolder']
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'distribution{timestamp}.png'
        filename = os.path.join(storagefolder, filename)
        filename.replace('\\', '/')
        # Create a bar chart
        plt.bar(data.keys(), data.values())
        plt.suptitle(title)
        # plt.xticks(rotation='82.5')
        plt.savefig(filename,dpi=400)
        plt.close()
        # create popup window and show the chart
        self.popup = qtw.QDialog()
        self.popup.setWindowTitle('Chart')
        self.popup.setFixedSize(qtc.QSize(500, 500))
        self.popup.setStyleSheet("background-color: #F5F5F5;")
        # self.popup.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        # self.popup.setWindowModality(qtc.Qt.ApplicationModal)
        self.popup.show()
        # self.popup.setAttribute(qtc.Qt.WA_DeleteOnClose)
        self.popup.layout = qtw.QVBoxLayout()
        self.popup.setLayout(self.popup.layout)
        self.image = qtw.QLabel()
        self.image.setPixmap(gui.QPixmap(filename))
        # fit the image to the popup window
        self.image.setScaledContents(True)
        # self.popup.image.setAlignment(qtc.Qt.AlignCenter)
        self.popup.layout.addWidget(self.image)
        self.popup.show()



    
    def showMessageBox(self, message):
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle('Error')
        msg.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def setSelectedDateFormat(self, dateFormat):
        self.selectedDateFormat = dateFormat

    def setSelectedColumn(self, column):
        self.selectedColumn = column

    
    def setSelectedAnalysis(self, text):
        global FILETOANALYZE
        FILETOANALYZE = None
        self.selectedAnalysis = text if text != 'Pick Analysis to run' else 'Retirement Analysis'
        self.analysisChoice.setCurrentText(self.selectedAnalysis)
        if self.selectedAnalysis == 'Retirement Analysis':
            # remove all layouts except the analysis area
            for i in range(self.analysisLayout.count()):
                if i != 0:
                    widget = self.analysisLayout.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)
            # add the retirement analysis area to the analysis area
            self.analysisLayout.addLayout(self.ritermentAnalysisArea)
        elif self.selectedAnalysis == 'Distribution Analysis':
            # remove all layouts except the analysis area
            for i in range(self.analysisLayout.count()):
                if i != 0:
                    widget = self.analysisLayout.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)
            # add the distribution analysis area to the analysis area
            self.analysisLayout.addLayout(self.distributionAnalysisArea)
    
    def showContextMenu(self, pos):
        # create menu for the selected area on table
        menu = qtw.QMenu()
        # create a delete row action
        deleteRowAction = menu.addAction('Delete Row')
        # when delete row action is clicked, delete the selected row
        deleteRowAction.triggered.connect(lambda: self.deleteRow(self.table.currentRow()))
        # create a delete column action
        deleteColumnAction = menu.addAction('Delete Column')
        # when delete column action is clicked, delete the selected column
        deleteColumnAction.triggered.connect(lambda: self.deleteColumn(self.table.currentColumn()))
        # # create a delete selection action
        # deleteSelectionAction = menu.addAction('Delete Selection')
        # # when delete selection action is clicked, delete the selected area
        # deleteSelectionAction.triggered.connect(lambda: self.deleteSelection(self.table.selectedRanges()))
        # show the menu at the position of the click
        menu.exec(self.table.mapToGlobal(pos))
    
    def deleteRow(self, row):
        # delete the selected row
        self.table.removeRow(row)
    
    def deleteColumn(self, column):
        # delete the selected column
        self.table.removeColumn(column)
        self.prepareAnalysisColumns()
    
    def deleteSelection(self, selection):
        # delete only the rows and columns selected
        for range in selection:
            self.table.removeRow(range.topRow())
            self.table.removeColumn(range.leftColumn())
        



    def savefile(self, filename=None):
        global FILETOANALYZE
        if not filename:
            # create a file dialog to select .xlsx and .xls or .csv file
            filename, _ = qtw.QFileDialog.getSaveFileName(self, 'Save File', '', 'Excel Files (*.xlsx *.xls *.csv)')
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.table.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, qtc.Qt.Orientation.Horizontal)
            sheet.write(0, c+1, text, style=style)

        for r in range(model.rowCount()):
            text = model.headerData(r, qtc.Qt.Orientation.Vertical)
            sheet.write(r+1, 0, text, style=style)

        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r+1, c+1, text)
        if filename:
            wbk.save(filename)
            FILETOANALYZE = filename
            self.filename = filename
    
    def savefileas(self):
        global FILETOANALYZE
        filename,_ = qtw.QFileDialog.getSaveFileName(self, 'Save File', '', "Excel Files (*.xlsx *.xls *.csv)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.table.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, qtc.Qt.Orientation.Horizontal)
            sheet.write(0, c+1, text, style=style)

        for r in range(model.rowCount()):
            text = model.headerData(r, qtc.Qt.Orientation.Vertical)
            sheet.write(r+1, 0, text, style=style)

        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r+1, c+1, text)
        if filename:
            wbk.save(filename)
            FILETOANALYZE = filename
            self.filename = filename


class editWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, chosenfilename)
        # convert the given image file to text
        self.converter = Converter(chosenfilepath, 'text')
        self.converter.start()
        self.converter.finished.connect(lambda: self.setupUi(window))
        # create a widget that shows a loading gif using qmovie
        self.loader = gui.QMovie(os.path.join('static', 'loading.gif'))
        self.loadingWidget = qtw.QLabel()
        self.loadingWidget.setMovie(self.loader)
        self.loadingWidget.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.loadingWidget)
        self.loader.start()


    def setupUi(self, window):
        # remove the loading widget
        self.mainLayout.removeWidget(self.loadingWidget)
        self.path = ''
        self.editor = Editor()
        # set a listener that listens for file changes
        self.listener = Listener()
        self.listener.start()
        self.listener.newfile.connect(lambda: self.editor.setText(TEXT))
        # editor should always start font color black
        self.editor.setTextColor(gui.QColor(0, 0, 0))
        # set editor background color to white using stylesheet
        self.editor.setStyleSheet("background-color: white;")
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.toolBar = qtw.QHBoxLayout()
        self.mainLayout.addLayout(self.toolBar)
        self.mainLayout.addLayout(self.mainContent)
        # create toolbar options and add to the toolbar layout
        # paste
        self.pasteIcon = gui.QIcon(os.path.join('static', 'editor', 'clipboard-paste-document-text.png'))
        self.pasteButton = qtw.QPushButton(self.pasteIcon, '')
        self.pasteButton.setToolTip('Paste')
        self.toolBar.addWidget(self.pasteButton)
        self.pasteButton.clicked.connect(self.editor.paste)
        # copy
        self.copyIcon = gui.QIcon(os.path.join('static', 'editor', 'document-copy.png'))
        self.copyButton = qtw.QPushButton(self.copyIcon, '')
        self.copyButton.setToolTip('Copy')
        self.toolBar.addWidget(self.copyButton)
        self.copyButton.clicked.connect(self.editor.copy)
        # cut
        self.cutIcon = gui.QIcon(os.path.join('static', 'editor', 'scissors.png'))
        self.cutButton = qtw.QPushButton(self.cutIcon, '')
        self.cutButton.setToolTip('Cut')
        self.toolBar.addWidget(self.cutButton)
        self.cutButton.clicked.connect(self.editor.cut)
        # undo
        self.undoIcon = gui.QIcon(os.path.join('static', 'editor', 'arrow-curve-180-left.png'))
        self.undoButton = qtw.QPushButton(self.undoIcon, '')
        self.undoButton.setToolTip('Undo')
        self.toolBar.addWidget(self.undoButton)
        self.undoButton.clicked.connect(self.editor.undo)
        # redo
        self.redoIcon = gui.QIcon(os.path.join('static', 'editor', 'arrow-curve.png'))
        self.redoButton = qtw.QPushButton(self.redoIcon, '')
        self.redoButton.setToolTip('Redo')
        self.toolBar.addWidget(self.redoButton)
        self.redoButton.clicked.connect(self.editor.redo)
        # save
        self.saveIcon = gui.QIcon(os.path.join('static', 'editor', 'disk.png'))
        self.saveButton = qtw.QPushButton(self.saveIcon, '')
        self.saveButton.setToolTip('Save')
        self.toolBar.addWidget(self.saveButton)
        self.saveButton.clicked.connect(self.file_save)
        # save as
        self.saveAsIcon = gui.QIcon(os.path.join('static', 'editor', 'disk--pencil.png'))
        self.saveAsButton = qtw.QPushButton(self.saveAsIcon, '')
        self.saveAsButton.setToolTip('Save as')
        self.toolBar.addWidget(self.saveAsButton)
        self.saveAsButton.clicked.connect(self.file_saveas) 
        # add font selector to the toolbar
        self.fontSelector = qtw.QFontComboBox()
        self.fontSelector.setCurrentFont(gui.QFont('Arial', 12))
        self.fontSelector.currentFontChanged.connect(self.editor.setFont)
        self.toolBar.addWidget(self.fontSelector)
        # add font size selector to the toolbar
        self.fontSizeSelector = qtw.QSpinBox()
        self.fontSizeSelector.setRange(1, 100)
        self.fontSizeSelector.setValue(12)
        self.fontSizeSelector.valueChanged.connect(self.editor.setFontPointSize)
        self.toolBar.addWidget(self.fontSizeSelector)
        # add bold, italic and underline buttons to the toolbar
        self.boldIcon = gui.QIcon(os.path.join('static', 'editor', 'edit-bold.png'))
        self.boldButton = qtw.QPushButton(self.boldIcon, '')
        self.boldButton.setToolTip('Bold')
        self.toolBar.addWidget(self.boldButton)
        self.boldButton.clicked.connect(lambda x: self.editor.setFontWeight(gui.QFont.Bold if x else gui.QFont.Normal))
        self.italicIcon = gui.QIcon(os.path.join('static', 'editor', 'edit-italic.png'))
        self.italicButton = qtw.QPushButton(self.italicIcon, '')
        self.italicButton.setToolTip('Italic')
        self.toolBar.addWidget(self.italicButton)
        self.italicButton.clicked.connect(lambda x: self.editor.setFontItalic(True if x else False))
        self.underlineIcon = gui.QIcon(os.path.join('static', 'editor', 'edit-underline.png'))
        self.underlineButton = qtw.QPushButton(self.underlineIcon, '')
        self.underlineButton.setToolTip('Underline')
        self.toolBar.addWidget(self.underlineButton)
        self.underlineButton.clicked.connect(lambda x: self.editor.setFontUnderline(True if x else False))
        # add text alignment buttons to the toolbar
        self.leftAlignIcon = gui.QIcon(os.path.join('static', 'editor', 'edit-alignment.png'))
        self.leftAlignButton = qtw.QPushButton(self.leftAlignIcon, '')
        self.leftAlignButton.setToolTip('Left Align')
        self.toolBar.addWidget(self.leftAlignButton)
        self.leftAlignButton.clicked.connect(lambda x: self.editor.setAlignment(qtc.Qt.AlignmentFlag.AlignLeft))
        self.centerAlignIcon = gui.QIcon(os.path.join('static', 'editor', 'edit-alignment-center.png'))
        self.centerAlignButton = qtw.QPushButton(self.centerAlignIcon, '')
        self.centerAlignButton.setToolTip('Center Align')
        self.toolBar.addWidget(self.centerAlignButton)
        self.centerAlignButton.clicked.connect(lambda x: self.editor.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter))
        self.rightAlignIcon = gui.QIcon(os.path.join('static', 'editor', 'edit-alignment-right.png'))
        self.rightAlignButton = qtw.QPushButton(self.rightAlignIcon, '')
        self.rightAlignButton.setToolTip('Right Align')
        self.toolBar.addWidget(self.rightAlignButton)
        self.rightAlignButton.clicked.connect(lambda x: self.editor.setAlignment(qtc.Qt.AlignmentFlag.AlignRight))
        # create a text editor area with white background and two buttons at the bottom
        self.mainContent.addWidget(self.editor)
        # create buttons layout
        self.buttonsLayout = qtw.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonsLayout)
        # create a button for saving the file and add it to the left side of the mainContent layout
        self.saveButton = qtw.QPushButton('Save')
        self.saveButton.setFixedSize(qtc.QSize(200, 30))
        # set button color to #509BA6
        self.saveButton.setStyleSheet("background-color: #509BA6;")
        self.saveButton.clicked.connect(self.file_save)
        self.buttonsLayout.addWidget(self.saveButton)
        # create a button for converting the file and add it to the left side of the mainContent layout
        self.cancelButton = qtw.QPushButton('Cancel')
        self.cancelButton.setFixedSize(qtc.QSize(200, 30))
        # set button color to #509BA6
        self.cancelButton.setStyleSheet("background-color: #509BA6;")
        self.cancelButton.clicked.connect(lambda: cancelEdit(window))
        self.buttonsLayout.addWidget(self.cancelButton)
        # get text from the ocr library
        self.editor.setText(TEXT)
    
    def dialog_critical(self, s):
        dlg = qtw.QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(qtw.QMessageBox.Icon.Critical)
        dlg.show()
    
    def file_save(self):
        if not self.path:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()
        text = self.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = qtw.QFileDialog.getSaveFileName(self, "Save file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
        if not path:
            # If dialog is cancelled, will return ''
            return
        text = self.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = qtc.QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())
    
    def update_title(self):
        filename = os.path.basename(self.path) if self.path else "Untitled"
        self.setWindowTitle(f"{filename} - {os.environ.get('APP_NAME')} ")
    

class settingsWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, 'Settings')
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.mainLayout.addLayout(self.mainContent)
        # load settings.json
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        # create a widget that displays the settings
        self.settingsWidget = qtw.QWidget()
        self.settingsLayout = qtw.QVBoxLayout()
        self.settingsWidget.setLayout(self.settingsLayout)
        self.mainContent.addWidget(self.settingsWidget)
        # create a list of settings options with icon and text on the left and button to change settings on the right
        self.settingsList = qtw.QListWidget()
        self.settingsLayout.addWidget(self.settingsList)
        self.settingsList.addItem(qtw.QListWidgetItem(gui.QIcon(os.path.join('static', 'settings.png')), 'Storage Folder: ' + os.path.basename(settings['storagefolder'])))
        # make the text bold and 50px
        self.settingsList.item(0).setFont(gui.QFont('Arial', 20))
        self.settingsList.addItem(qtw.QListWidgetItem(gui.QIcon(os.path.join('static', 'settings.png')), 'Scan Folder: ' + os.path.basename(settings['scanfolder'])))
        self.settingsList.item(1).setFont(gui.QFont('Arial', 20))
        self.settingsList.addItem(qtw.QListWidgetItem(gui.QIcon(os.path.join('static', 'settings.png')), 'Mode: ' + str(settings['mode'])+' mode'))
        self.settingsList.item(2).setFont(gui.QFont('Arial', 20))
        # when list item is selected print the text of the item
        self.settingsList.itemClicked.connect(lambda: changeSettings(window, self, self.settingsList.currentItem().text().split(':')[0]))
        self.settingsList.setStyleSheet("background-color: #509BA6;")

class scannedDocumentsWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, 'Scanned Documents')
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.mainLayout.addLayout(self.mainContent)
        # create a widget that displays the scanned documents
        self.scannedDocumentsWidget = qtw.QWidget()
        self.scannedDocumentsLayout = qtw.QVBoxLayout()
        self.scannedDocumentsWidget.setLayout(self.scannedDocumentsLayout)
        self.mainContent.addWidget(self.scannedDocumentsWidget)
        # create a list of scanned documents with icon and text on the left and button to open the document on the right
        self.scannedDocumentsList = qtw.QListWidget()
        self.scannedDocumentsLayout.addWidget(self.scannedDocumentsList)
        # make the text bold and 50px
        self.scannedDocumentsList.setStyleSheet("background-color: #509BA6;")
        # get list of all documents in the scanfolder
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            for file in os.listdir(settings['scanfolder']):
                # check if file is an image
                if file.endswith('.png') or file.endswith('.jpg'):
                    self.scannedDocumentsList.addItem(qtw.QListWidgetItem(gui.QIcon(os.path.join('static', 'document.png')), os.path.basename(file)))
        # when list item is selected print the text of the item
        self.scannedDocumentsList.itemClicked.connect(lambda: previewImage(self, settings['scanfolder'], self.scannedDocumentsList.currentItem().text()))

class storageWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, 'Storage')
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.mainLayout.addLayout(self.mainContent)
        # create a widget that displays the scanned documents
        self.storageWidget = qtw.QWidget()
        self.storageLayout = qtw.QVBoxLayout()
        self.storageWidget.setLayout(self.storageLayout)
        self.mainContent.addWidget(self.storageWidget)
        # create a list of scanned documents with icon and text on the left and button to open the document on the right
        self.storageList = qtw.QListWidget()
        self.storageLayout.addWidget(self.storageList)
        # make the text bold and 50px
        self.storageList.setStyleSheet("background-color: #509BA6;")
        # get list of all documents in the scanfolder
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            for file in os.listdir(settings['storagefolder']):
                # check if file is an pdf, docx, or txt
                if file.endswith('.pdf') or file.endswith('.docx') or file.endswith('.txt'):
                    # check if search bar has content and filter the list
                    if self.searchBar.text() != '':
                        if self.searchBar.text() in file:
                            self.storageList.addItem(qtw.QListWidgetItem(gui.QIcon(os.path.join('static', 'document.png')), os.path.basename(file)))
                    else:
                        self.storageList.addItem(qtw.QListWidgetItem(gui.QIcon(os.path.join('static', 'document.png')), os.path.basename(file)))

class userGuideWindow(qtw.QWidget):
    def __init__(self, window) ->None:
        super().__init__()
        createPrerequisites(window, self, 'User Guide')
        # create a mainContent layout with button for picking files and a select field for picking file types
        self.mainContent = qtw.QVBoxLayout()
        self.mainLayout.addLayout(self.mainContent)
        # create a widget that displays the user guide pdf file
        self.userGuideWidget = qtw.QWidget()
        self.userGuideLayout = qtw.QVBoxLayout()
        self.userGuideWidget.setLayout(self.userGuideLayout)
        self.mainContent.addWidget(self.userGuideWidget)
        # create a pdf viewer widget
        self.userGuidePdf = QWebEngineView()
        self.userGuideLayout.addWidget(self.userGuidePdf)
        self.PDF = os.path.abspath(os.path.join('static', 'userguide.pdf'))
        self.PDF = 'file://' + self.PDF
        # display the pdf file
        self.userGuidePdf.load(qtc.QUrl.fromUserInput('%s?file=%s' % (PDFJS, self.PDF)))

class Filter(qtc.QThread):
    progress = qtc.pyqtSignal(int)
    def __init__(self, window, params):
        super().__init__()
        self.window = window
        self.params = params

    def run(self):
        word = self.params['filterWord']
        criteria = self.params['filterCriteria']
        selectedColumn = int(self.params['selectedColumn'])
        # loop through self.table and delete all rows where the selected older than the retirement age
        deleted_rows = 0
        total_rows = self.window.table.rowCount()
        for row in range(self.window.table.rowCount()):
            text = self.window.table.item(row-deleted_rows, selectedColumn).text()
            if criteria == 'is greater than':
                # use regex to remove all non-numeric characters
                text = re.sub('[^0-9]', '', text)
                if re.match(r'^\d+$', text) and re.match(r'^\d+$', word):
                    if not int(text) > int(word):
                        self.window.table.removeRow(row-deleted_rows)
                        deleted_rows += 1
            elif criteria == 'is less than':
                text = re.sub('[^0-9]', '', text)
                if re.match(r'^\d+$', text) and re.match(r'^\d+$', word):
                    if not int(text) < int(word):
                        self.window.table.removeRow(row-deleted_rows)
                        deleted_rows += 1
            elif criteria == 'contains':
                # use regex to check if the text contains the word
                if not re.search(r'\b%s\b' % word, text, re.IGNORECASE):
                    self.window.table.removeRow(row-deleted_rows)
                    deleted_rows += 1
            elif criteria == 'does not contain':
                # use regex to check if the text contains the word
                if re.search(r'\b%s\b' % word, text, re.IGNORECASE):
                    self.window.table.removeRow(row-deleted_rows)
                    deleted_rows += 1
            elif criteria == 'is equal to':
                if not text.lower() == word.lower():
                    self.window.table.removeRow(row-deleted_rows)
                    deleted_rows += 1
            elif criteria == 'is not equal to':
                if text.lower() == word.lower():
                    self.window.table.removeRow(row-deleted_rows)
                    deleted_rows += 1
            # update the progress bar
            self.progress.emit(int((row / total_rows) * 100))

class Analyze(qtc.QThread):
    progress = qtc.pyqtSignal(int)
    matches = qtc.pyqtSignal(int)
    def __init__(self, window, type, params):
        super().__init__()
        self.window = window
        self.type = type
        self.params = params

    def run(self):
        if self.type == 'Retirement Analysis':
            retirementAge = int(self.params['retirementAge'])
            selectedColumn = int(self.params['selectedColumn'])
            selectedDateFormat = self.params['selectedDateFormat']
            # loop through self.table and delete all rows where the selected older than the retirement age
            deleted_rows = 0
            total_rows = self.window.table.rowCount()
            for row in range(self.window.table.rowCount()):
                dob = self.window.table.item(row-deleted_rows, selectedColumn).text()
                try:
                    if selectedDateFormat == 'MM/DD/YYYY':
                        dob = datetime.datetime.strptime(dob, '%m/%d/%Y')
                    elif selectedDateFormat == 'DD/MM/YYYY':
                        dob = datetime.datetime.strptime(dob, '%d/%m/%Y')
                    elif selectedDateFormat == 'YYYY/MM/DD':
                        dob = datetime.datetime.strptime(dob, '%Y/%m/%d')
                    elif selectedDateFormat == 'YYYY/DD/MM':
                        dob = datetime.datetime.strptime(dob, '%Y/%d/%m')
                    elif selectedDateFormat == 'MM-DD-YYYY':
                        dob = datetime.datetime.strptime(dob, '%m-%d-%Y')
                    elif selectedDateFormat == 'DD-MM-YYYY':
                        dob = datetime.datetime.strptime(dob, '%d-%m-%Y')
                    elif selectedDateFormat == 'YYYY-MM-DD':
                        dob = datetime.datetime.strptime(dob, '%Y-%m-%d')
                    elif selectedDateFormat == 'YYYY-DD-MM':
                        dob = datetime.datetime.strptime(dob, '%Y-%d-%m')
                    # get the current date
                    currentDate = datetime.datetime.now()
                    # get the difference between the current date and the value
                    difference = currentDate - dob
                    # get the difference in years
                    currentAge = int(difference.days / 365.25)
                    # if the difference in years is greater than the retirement age, remove the row
                    should_retire = currentAge <= retirementAge
                    if should_retire:
                        self.window.table.removeRow(row-deleted_rows)
                        deleted_rows += 1
                except:
                    pass
                # update the progress bar
                self.progress.emit(int((row / total_rows) * 100))
        elif self.type == 'Distribution Analysis':
            location = self.params['location']
            selectedColumn = int(self.params['selectedColumn'])
            populationSize = int(self.params['populationSize'])
            # loop through self.table and count the number of rows where the selected column contains the location
            total_rows = self.window.table.rowCount()
            matches = 0
            for row in range(self.window.table.rowCount()):
                text = self.window.table.item(row, selectedColumn).text()
                # use regex to check if the text contains the word
                if re.search(r'\b%s\b' % location, text, re.IGNORECASE):
                    matches += 1
                # update the progress bar
                self.progress.emit(int((row / total_rows) * 100))
                self.matches.emit(matches)
                

class Excelloader(qtc.QThread):
    progress = qtc.pyqtSignal(int)
    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        global DATA
        DATA = loadExcel(self.window.filename)
        DATA.fillna('', inplace=True)
        self.window.table.setRowCount(DATA.shape[0])
        self.window.table.setColumnCount(DATA.shape[1])
        columns = [ str(i) for i in DATA.columns ]
        self.window.table.setHorizontalHeaderLabels(columns)
        # returns pandas array object
        total_rows = DATA.shape[0]
        for row in DATA.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = qtw.QTableWidgetItem(str(value))
                self.window.table.setItem(row[0], col_index, tableItem)
            # update the progress bar
            self.progress.emit(int((row[0] / total_rows) * 100))
        self.window.table.setColumnWidth(2, 300)

        # when the table is right clicked, show a context menu
        self.window.table.setContextMenuPolicy(qtc.Qt.ContextMenuPolicy.CustomContextMenu)
        self.window.table.customContextMenuRequested.connect(self.window.showContextMenu)


class Converter(qtc.QThread):
    def __init__(self, filepath, filetype):
        super().__init__()
        self.filepath = filepath
        self.filetype = filetype
    def run(self):
        # if filetype is text
        # convert image to text using the getText method from app.model
        global TEXT, DATA
        if self.filetype == 'text':
            text = getText(self.filepath)
            if text:
                self.text = text
                TEXT += self.text+'\n'
        # if filetype is table
        # convert image to text using the getText method from app.model
        elif self.filetype == 'table':
            data = getExcel(self.filepath)
            if not data.empty:
                self.data = data
                DATA = self.data
    
class Listener(qtc.QThread):
    newfile = qtc.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.scanfolder = ""
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            self.scanfolder = settings['scanfolder']
    def run(self):
        global TEXT, ALREADY_CONVERTED_FILES
        # check scanfolder every 5 seconds
        while True:
            # check if there are new files in the scanfolder
            for file in os.listdir(self.scanfolder):
                if file not in ALREADY_CONVERTED_FILES:
                    # check if file is an image
                    if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
                        # ensure file is readable
                        if os.access(os.path.join(self.scanfolder, file), os.R_OK):
                            try:
                                # create a thread to convert the image to text
                                converter = Converter(os.path.join(self.scanfolder, file), 'text')
                                converter.start()
                                converter.wait()
                                # send signal to the main thread to add the text to the text box
                                self.newfile.emit(converter.text)
                                ALREADY_CONVERTED_FILES.append(file)
                            except Exception as e:
                                print(e)
                                pass
            time.sleep(5)


def main():
    app = qtw.QApplication(sys.argv)
    window = qtw.QMainWindow()
    window.content = mainWindow(window)
    window.setWindowTitle(os.environ.get('APP_NAME'))
    window.setWindowIcon(gui.QIcon(os.path.join('static', 'icon.png')))
    window.setStyleSheet("background-color: #CBDFE0")
    # set the window size
    # window.resize(windowHieght, windowWidth)
    window.setGeometry(150, 100, windowHieght, windowWidth)
    # add menu bar
    menuBar = window.menuBar()
    # create a file menu
    fileMenu = menuBar.addMenu('File')
    # add open file option
    openFile = gui.QAction('Open file', window)
    openFile.setShortcut('Ctrl+O')
    openFile.triggered.connect(lambda: chooseFile(window.centralWidget()))
    fileMenu.addAction(openFile)
    # add exit button to file menu
    exitButton = gui.QAction('Close', window)
    exitButton.setShortcut('Ctrl+Q')
    exitButton.triggered.connect(lambda: exit(window))
    fileMenu.addAction(exitButton)
    # create a settings menu
    settingsMenu = menuBar.addMenu('Settings')
    # add settings button to settings menu
    settingsButton = gui.QAction('Change settings', window)
    settingsButton.setShortcut('Ctrl+S')
    settingsButton.triggered.connect(lambda: navigateTo(window, 'settingsWindow'))
    settingsMenu.addAction(settingsButton)
    # add storage option to settings menu
    storage = gui.QAction('Storage folder', window)
    storage.triggered.connect(lambda: changeSettings(window, storageWindow(window), 'Storage Folder'))
    settingsMenu.addAction(storage)
    # add scan option to settings menu
    scan = gui.QAction('Scan folder', window)
    scan.triggered.connect(lambda: changeSettings(window, scannedDocumentsWindow(window), 'Scan Folder'))
    settingsMenu.addAction(scan)
    # add mode option to settings menu
    mode = gui.QAction('Mode', window)
    mode.triggered.connect(lambda: changeSettings(window, settingsWindow(window), 'Mode'))
    settingsMenu.addAction(mode)
    # create a help menu
    helpMenu = menuBar.addMenu('Help')
    # add about option to help menu
    about = gui.QAction('About HOD', window)
    # about.triggered.connect(lambda: aboutWindow(window))
    helpMenu.addAction(about)
    # add user guide option to help menu
    userGuide = gui.QAction('User Guide', window)
    userGuide.triggered.connect(lambda: navigateTo(window, 'userGuideWindow'))
    helpMenu.addAction(userGuide)
    window.setCentralWidget(window.content)
    window.show()
    checkSettings(window)
    sys.exit(app.exec())

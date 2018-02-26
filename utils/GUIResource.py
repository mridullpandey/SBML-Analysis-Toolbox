import sys
from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as pyplot

import random

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("PyQT Tuts!")
        self.setWindowIcon(QtGui.QIcon('python.ico'))

        # Initialize menu bar and selections
        extractAction = QtGui.QAction("&GET TO THE CHOPPER!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):

        # A figure instance to plot on
        self.figure = pyplot.figure()

        # This is the canvas widget that displays the figure
        # it takes the figure instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # This is the navigation widget, it takes the canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # A button connected to the plot method
        self.btn = QtGui.QPushButton('Plot')
        self.btn.clicked.connect(self.plot)

        # Set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn)
        self.setLayout(layout)

        extractAction = QtGui.QAction(QtGui.QIcon('python.ico'), 'Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)

        checkBox = QtGui.QCheckBox("Enlarge Window", self)
        checkBox.resize(checkBox.minimumSizeHint())
        checkBox.move(100, 25)
        checkBox.stateChanged.connect(self.enlarge_window)

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)

        self.btn = QtGui.QPushButton("Download", self)
        self.btn.move(200, 120)
        self.btn.clicked.connect(self.download)

        self.show()

    def plot(self):
        ''' plot some random stuff '''
        # Random data
        data = [random.random() for i in range(10)]

        # Create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # Plot data
        ax.plot(data, '*-')

        # Refresh canvas
        self.canvas.draw()

    # Create progress bar -- Useful for simulations
    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)

    # Radio boxes -- Good for selecting what to run
    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(100, 100, 1000, 600)
        else:
            self.setGeometry(100, 100, 500, 300)

    # Exit dialogue
    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Exit',
                                            "Do you really want to quit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass


def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()
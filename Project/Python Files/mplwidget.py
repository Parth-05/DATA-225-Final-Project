from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

class MplWidget(QWidget):
    def __init__(self, parent=None, width=5, height=40, dpi=100):
        super(MplWidget, self).__init__(parent)
        
        # Create Figure and FigureCanvas objects
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvas(self.figure)

        # self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.canvas.updateGeometry()

        
    # Create a QVBoxLayout and add the canvas to it
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        

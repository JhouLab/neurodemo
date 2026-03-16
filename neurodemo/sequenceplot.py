# -*- coding: utf-8 -*-
"""
NeuroDemo - Physiological neuron sandbox for educational purposes
Luke Campagnola 2015
"""

import pyqtgraph as pg
from . import qt

from .analysisplot import AnalysisPlot   # simpler code-based analyzer
from .traceanalyzer import TraceAnalyzer  # user friendly analyzer


class SequencePlotWindow(qt.QWidget):
    def __init__(self):
        qt.QWidget.__init__(self)
        self.cached_mode = 'ic'
        self.layout = qt.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.hold_check = qt.QCheckBox("Hold data")
        self.hold_check.setChecked(True)
        self.layout.addWidget(self.hold_check, 0, 0)
        self.clear_btn = qt.QPushButton("Clear data")
        self.layout.addWidget(self.clear_btn, 0, 1)
        self.clear_btn.clicked.connect(self.clear_data)

        self.splitter = qt.QSplitter(qt.Qt.Orientation.Vertical)
        self.layout.addWidget(self.splitter, 1, 0, 1, 2)
        
        self.plot_layout = pg.GraphicsLayoutWidget()
        self.splitter.addWidget(self.plot_layout)
        self.plots = {}
        self.plotted_data = []

        self.analyzer = TraceAnalyzer(self)
        self.splitter.addWidget(self.analyzer)
        
        #self.analyzer = AnalysisPlot()
        #self.splitter.addWidget(self.analyzer)

    def add_plot(self, key, label):
        plot = self.plot_layout.addPlot(labels={'left': label, 'bottom': ('Time', 's')})
        if 'soma.V' in self.plots:
            plot.setXLink(self.plots['soma.V'])
            
        self.plot_layout.nextRow()
        self.plots[key] = plot

    def remove_plot(self, key):
        plot = self.plots.pop(key)
        self.plot_layout.removeItem(plot)
        plot.hide()
        plot.setParentItem(None)
        
    def plot(self, t, data, info):
        if not self.hold_check.isChecked():
            self.clear_data()

        # If mode has changed, clear all time plots, and update cached mode
        if self.cached_mode != info['mode']:
            self.cached_mode = info['mode']
            self.clear_data()

        if info['seq_len'] == 0:
            pen = 'w'
        else:
            pen = (info['seq_ind'], info['seq_len'] * 4./3.)
        
        for k, plt in self.plots.items():
            plt_data = plt.plot(t, data[k], pen=pen)  # Add to time plots
            self.plotted_data.append((plt_data, plt))
            plt.setLimits(xMin=min(t), xMax=max(t))  # Prevent user from zooming out too far
        try:
            # Add analysis results to analyzer, which can use it to generate scatterplot
            self.analyzer.add_data(t, data, info)
        except:
            pg.debug.printExc('Error analyzing data:')
        self.show()
        
    def clear_data(self):
        for item, plt in self.plotted_data:
            plt.removeItem(item)
        self.plotted_data = []
        self.analyzer.clear()
    
    def plot_triggers(self, t, d):
        for k, plt in self.plots.items():
            plt.plot([t,t], [-d, d], pen=pg.mkPen(color="w", width=1.5))

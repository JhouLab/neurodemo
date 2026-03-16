from __future__ import annotations
import numpy as np
import pyqtgraph as pg
from scipy.special import y1_zeros

from . import qt
import pyqtgraph.parametertree as pt
from lmfit import Model
from lmfit.models import ExponentialModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # This import is circular, so we don't do it at runtime
    from neurodemo.sequenceplot import SequencePlotWindow


class TraceAnalyzer(qt.QWidget):
    def __init__(self, seq_plotter: SequencePlotWindow):
        qt.QWidget.__init__(self)
        self.plotter = seq_plotter
        
        self.main_layout = qt.QGridLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.hsplitter = qt.QSplitter(qt.Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.hsplitter)
        
        self.ptree = pt.ParameterTree(showHeader=False)
        self.hsplitter.addWidget(self.ptree)
        
        self.table = pg.TableWidget()
        self.hsplitter.addWidget(self.table)
        self.table.verticalHeader().hide()
        
        self.analysis_plot = EvalPlotter()
        self.hsplitter.addWidget(self.analysis_plot)
        
        self.hsplitter.setSizes([300, 200, 400])
        
        self.clear()
        
        self.params = TraceAnalyzerGroup(seq_plot=self.plotter, name="Analyzers")
        self.params.need_update.connect(self.update_analyzers)

        self.ptree.setParameters(self.params)
        self.ptree.header().setSectionResizeMode(0, qt.QHeaderView.ResizeMode.Stretch)

    def clear(self):
        self.data = []
        self.table.clear()
        self.analysis_plot.clear_plot()
        
    def add_data(self, t, data, info):
        self.params.set_inputs(data.dtype.names) # Populate dropdown menu of inputs that user can select for this analyzer, e.g. soma.V
        self.data.append((t, data, info))
        self.update_analysis()

    def update_analyzers(self):
        analyzer_dict = dict()
        # Analyzer parameter tree has changed
        for analyzer in self.params.children():
            requested_plot = self.plotter.plots[analyzer['Input']]
            if analyzer.current_plot is not requested_plot:
                if analyzer.current_plot is not None:
                    analyzer.current_plot.removeItem(analyzer.rgn)        # Remove cursors from previous plot
                requested_plot.addItem(analyzer.rgn, ignoreBounds=True)   # Add cursors to current plot
                analyzer.current_plot = requested_plot

            # Build dictionary of analyzers, to pass to EvalPlotter for making unit inference
            analyzer_dict[analyzer.name()] = analyzer

        self.analysis_plot.update_unit_inference(analyzer_input_dict=analyzer_dict)
        self.update_analysis()

    def update_analysis(self):
        # We get here either after new data is added, or if analysis parameter tree is changed
        fields = ['cmd'] + [analyzer.name() for analyzer in self.params.children()]
        data = np.empty(len(self.data), dtype=[(str(f), float) for f in fields])

        seq_list = []
        for i, rec in enumerate(self.data):
            t, d, info = rec
            data['cmd'][i] = info['amp']   # Get amplitude of the current pulse segment
            for analysis in self.params.children():
                data[analysis.name()][i] = analysis.process(t, d)

            seq_list.append(info['seq_ind'])  # Pulse sequence number is used by analyzer to identify boundaries between consecutive sequences (so it can plot each in a different color)
        self.table.setData(data)

        self.analysis_plot.update_data(data, seq_list)
        

class TraceAnalyzerGroup(pt.parameterTypes.GroupParameter):
    need_update = qt.Signal()    
    added_new = qt.Signal()

    def __init__(self, seq_plot: SequencePlotWindow, **kwds):
        analyses = ['min', 'max', 'mean', 'exp_tau', 'spike_count', 'spike_latency']
        self.inputs = []
        self.cached_mode = "ic"
        self.plotter = seq_plot
        pt.parameterTypes.GroupParameter.__init__(self, addText='Add analysis..', addList=analyses, **kwds)

    def addNew(self, typ):
        param = TraceAnalyzerParameter(name=typ, analysis_type=typ, inputs=self.inputs, autoIncrementName=True)
        self.addChild(param)  # Name might be auto-incremented after calling addChild() if it conflicts with existing analyzer. E.g. "mean" may become "mean2"
        if self.cached_mode == "vc":
            # If voltage clamp mode, then default to soma.PatchClamp.I, if available
            if 'soma.PatchClamp.I' in self.inputs:
                param.child('Input').setValue('soma.PatchClamp.I')

        an: EvalPlotter = self.plotter.analyzer.analysis_plot

        # If y1 is blank, populate it with newly added analyzer. We don't do this for y2, as this sometimes leads
        # to overlappoing plots with different (and incompatible) units
        if str(an.y1_code.text()).lower() == '':
            an.y1_code.setText(param.name())

        param.need_update.connect(self.need_update)
        self.need_update.emit()
        
    def set_inputs(self, inputs):
        # Currently this is updated every 20ms, for all children, which seems inefficient.
        # Should we update only if inputs are different?
        self.inputs = list(inputs)
        self.inputs.remove('t')   # Analyzer doesn't operate on time variable, so don't add it to dropdown menu
        for ch in self.children():
            ch.set_input_list(self.inputs)

    def set_mode(self, mode_string):
        self.cached_mode = mode_string


class TraceAnalyzerParameter(pt.parameterTypes.GroupParameter):
    need_update = qt.Signal(object)  # self

    def __init__(self, **kwds):
        kwds.update({'removable': True, 'renamable': True})
        childs = [
            dict(name='Input', type='list', limits=kwds.pop('inputs')),
            dict(name='Type', type='list', value=kwds.pop('analysis_type'), limits=['mean', 'min', 'max', 'exp_tau', 'spike_count', 'spike_latency']),
            dict(name='Start', type='float', value=0, suffix='s', siPrefix=True, step=5e-3),
            dict(name='End', type='float', value=10e-3, suffix='s', siPrefix=True, step=5e-3),
            dict(name='Threshold', type='float', value=-30e-3, suffix='V', siPrefix=True, step=5e-3, visible=False),
        ]
        kwds['children'] = childs + kwds.get('children', [])
        
        pt.parameterTypes.GroupParameter.__init__(self, **kwds)
        self.sigTreeStateChanged.connect(self.tree_changed)

        self.current_plot = None

        self.rgn = pg.LinearRegionItem([self['Start'], self['End']])
        self.rgn_label = pg.InfLineLabel(self.rgn.lines[0], text=self.name(), angle=90, anchors=[(0, 0), (0, 0)])
        self.rgn.sigRegionChanged.connect(self.region_changed)

        self.show_threshold_param()
    
    def tree_changed(self, root, changes):
        for param, change, val in changes:
            if change == 'parent' and val is None:
                # Remove linear region item (i.e. pair of cursors) when corresponding analyzer is removed.
                param.current_plot.removeItem(param.rgn)
            if change not in ('value', 'name'):
                continue
            if param is self.child('Start') or param is self.child('End'):
                self.rgn.sigRegionChanged.disconnect(self.region_changed)
                try:
                    self.rgn.setRegion([self['Start'], self['End']])
                finally:
                    self.rgn.sigRegionChanged.connect(self.region_changed)
            elif param is self.child('Type'):
                self.show_threshold_param()
            elif param is self and change == 'name':
                self.rgn_label.setFormat(self.name())  # Note use of setFormat() rather than setText(), which works temporarily but then reverts to original name.
            self.need_update.emit(self)

    def show_threshold_param(self):
        needs_threshold = self['Type'] in ['spike_count', 'spike_latency']
        self.child('Threshold').setOpts(visible=needs_threshold)

    def region_changed(self):
        start, end = self.rgn.getRegion()
        self.sigTreeStateChanged.disconnect(self.tree_changed)
        try:
            self['Start'] = start
            self['End'] = end
        finally:
            self.sigTreeStateChanged.connect(self.tree_changed)
            
        self.need_update.emit(self)
            
    def set_input_list(self, inputs):
        self.child('Input').setLimits(inputs)

    def process(self, t, data):
        dt = t[1] - t[0]
        i1 = int(self['Start'] / dt)
        i2 = int(self['End'] / dt)
        try:
            data = data[self['Input']][i1:i2]
        except ValueError:
            # Input signal not present, most likely because this is an older sequence run before user added it
            return None

        t = t[i1:i2]
        typ = self['Type']
        if typ == 'mean':
            return data.mean()
        elif typ == 'min':
            return data.min()
        elif typ == 'max':
            return data.max()
        elif typ.startswith('spike'):
            spikes = np.argwhere((data[1:] > self['Threshold']) & (data[:-1] < self['Threshold']))[:,0]
            if typ == 'spike_count':
                return len(spikes)
            elif typ == 'spike_latency':
                if len(spikes) == 0:
                    return np.nan
                else:
                    return spikes[0] * dt
        elif typ == 'exp_tau':
            return self.measure_tauDecay(data, t)
        elif typ == 'expTauRise4':
            return(self.measure_tauRise4(data, t))
            
    def measure_tau_old(self, data, t):
        from scipy.optimize import curve_fit
        dt = t[1] - t[0]
        def expfn(x, yoff, amp, tau):
            return yoff + amp * np.exp(-x / tau)
        guess = (data[-1], data[0] - data[-1], t[-1] - t[0])
        fit = curve_fit(expfn, t-t[0], data, guess)
        return fit[0][2]

    def measure_tauDecay(self, data, t):
        model = ExponentialModel()
        pars = model.guess(data-data[-1], x=t-t[0])
        result = model.fit(data-data[-1], pars,  x=t-t[0])
        return result.params['decay'] # fit[0][2]            
        
    def measure_tauRise4(self, data, t):
        # this is not working quite right yet... 
        print('taurise4')
        def expfn4(x, amp, tau):
            return amp * ((1.0-np.exp(-x / tau))**4.0)
        emodel = Model(expfn4)
        params = emodel.make_params()
        d = data-data[0]
        tp = t-t[0]
        emodel.set_param_hint('tau', value=t[-1]-t[0], min=0.0001)
        emodel.set_param_hint('amp', value=data[-1]-data[0])
        result = emodel.fit(d[1:], params, x=tp[1:])
        print(result.params)
        return result.params['tau'] # fit[0][2]       


class EvalPlotter(qt.QWidget):
    def __init__(self):
        qt.QWidget.__init__(self)
        self.main_layout = qt.QGridLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        
        self.x_label = qt.QLabel('X data')
        self.y1_label = qt.QLabel('Y1 data (o)')
        self.y2_label = qt.QLabel('Y2 data (+)')
        self.main_layout.addWidget(self.x_label, 0, 0)
        self.main_layout.addWidget(self.y1_label, 1, 0)
        self.main_layout.addWidget(self.y2_label, 2, 0)

        self.x_code = qt.QLineEdit('cmd')
        self.y1_code = qt.QLineEdit()
        self.y2_code = qt.QLineEdit()
        self.main_layout.addWidget(self.x_code, 0, 1)
        self.main_layout.addWidget(self.y1_code, 1, 1)
        self.main_layout.addWidget(self.y2_code, 2, 1)

        self.x_units_label = qt.QLabel('units')
        self.y1_units_label = qt.QLabel('units')
        self.y2_units_label = qt.QLabel('units')
        self.main_layout.addWidget(self.x_units_label, 0, 2)
        self.main_layout.addWidget(self.y1_units_label, 1, 2)
        self.main_layout.addWidget(self.y2_units_label, 2, 2)

        self.x_units_text = qt.QLineEdit('A')
        self.y1_units_text = qt.QLineEdit()
        self.y2_units_text = qt.QLineEdit()
        self.main_layout.addWidget(self.x_units_text, 0, 3)
        self.main_layout.addWidget(self.y1_units_text, 1, 3)
        self.main_layout.addWidget(self.y2_units_text, 2, 3)

        self.plot = pg.PlotWidget()
        self.main_layout.addWidget(self.plot, 3, 0, 1, 4)

#        self.hold_plot_btn = qt.QPushButton('Hold Plot')
#        self.main_layout.addWidget(self.hold_plot_btn, 3, 0, 1, 2)
        self.clear_plot_btn = qt.QPushButton('Clear Plots')
        self.main_layout.addWidget(self.clear_plot_btn, 4, 2, 1, 2)

        # Text boxes to select X and Y data
        self.x_code.editingFinished.connect(self.replot_after_var_change)
        self.y1_code.editingFinished.connect(self.replot_after_var_change)
        self.y2_code.editingFinished.connect(self.replot_after_var_change)

        # Text boxes to specify X and Y units (now autodetected, if possible)
        self.x_units_text.editingFinished.connect(self.replot)
        self.y1_units_text.editingFinished.connect(self.replot)
        self.y2_units_text.editingFinished.connect(self.replot)

        # Checkbox to hold previous traces. This will be overridden if user changes X/Y data source
#        self.hold_plot_btn.clicked.connect(self.hold_plot)

        # Button to clear plot
        self.clear_plot_btn.clicked.connect(self.clear_plot)

        # Cached state variables used to guess units
        self.mode_string = None
        self.analyzer_input_dict = None

    def update_data(self, data, info_list):
        self.data = data
        self.info_list = info_list
        self.replot()

    def infer_unit(self, signal_val):
        # Use heuristics to guess whether unit is A or V. If unable to guess, return None to keep unit unchanged from before.
        # This works best if user enters a simple analsyis name, e.g. "mean", into the text box. Any complex expression,
        # e.g. "mean + 1", breaks this heuristic.
        if signal_val == "":
            return None
        elif signal_val == 'cmd':
            # Determine cmd unit based on whether we are in IC or VC mode
            if self.mode_string == 'ic':
                return "A"
            elif self.mode_string == 'vc':
                return "V"
            else:
                return None
        else:
            if self.analyzer_input_dict is None:
                return None

            # If 'signal_val' is not 'cmd', then it is usually analyzer name, like 'mean', 'min', 'max', etc.
            # Use dictionary to look up the input signal
            try:
                analyzer = self.analyzer_input_dict[signal_val]
                input_val = analyzer['Input']
                input_type = analyzer['Type']
            except KeyError:
                return None

            if input_type.endswith('tau'):
                return "s"
            elif input_type.endswith('count'):
                return ""
            elif input_type.endswith('latency'):
                return "s"

            # Mean/min/max inputs infer uints from input type
            if input_val.endswith('I'):
                return "A"
            elif input_val.endswith('V'):
                return "V"
            elif input_val.endswith('G'):
                return "S"
            elif input_val.endswith('OP'):  # Open probability
                return ""
            elif input_val.endswith('cmd'):
                return self.infer_unit('cmd')
            else:
                return None

    def update_unit_inference(self, mode_string=None, analyzer_input_dict=None):

        if mode_string is not None or analyzer_input_dict is not None:
            # If mode or analyzer input changed, then units could have changed and remove stored curves
            self.plot.clear()
            # Cache changed state for future inference
            if mode_string is not None:
                self.mode_string = mode_string
            if analyzer_input_dict is not None:
                self.analyzer_input_dict = analyzer_input_dict  # Cache value for future use

        # Infer X-value unit
        tmp = self.infer_unit(self.x_code.text())
        if tmp is not None:
            self.x_units_text.setText(tmp)

        # Infer Y1-value unit
        tmp = self.infer_unit(self.y1_code.text())
        if tmp is not None:
            self.y1_units_text.setText(tmp)

        # Infer Y2-value unit
        tmp = self.infer_unit(self.y2_code.text())
        if tmp is not None:
            self.y2_units_text.setText(tmp)

    def replot_after_var_change(self):
        # User has selected a new X or Y variable
        self.update_unit_inference()
        self.replot()

    def replot(self):
        data = self.data

        if data is None:
            self.plot.clear()
            return

        ns = {}
        for k in data.dtype.names:
            ns[k.replace(' ', '_')] = data[k]
        xcode = str(self.x_code.text()).lower()  # Read user input text for X-axis values
        y1_code = str(self.y1_code.text()).lower()  # Read user input text for Y-axis values
        y2code = str(self.y2_code.text()).lower()  # Read user input text for Y-axis values
        if xcode == '' or (y1_code == '' and y2code == ''):
            # Can't plot unless we have x-values and at least one y
            self.plot.clear()
            return

        try:
            x = eval(xcode, ns)
        except:
            pg.debug.printExc('Error evaluating plot x values:')
            self.x_code.setStyleSheet("QLineEdit { border: 2px solid red; }")
            return
        else:
            self.x_code.setStyleSheet("")

        y1 = None
        y2 = None

        try:
            if y1_code != '':
                y1 = eval(y1_code, ns)
        except:
            pg.debug.printExc('Error evaluating plot y1 values:')
            self.y1_code.setStyleSheet("QLineEdit { border: 2px solid red; }")
        else:
            self.y1_code.setStyleSheet("")

        try:
            if y2code != '':
                y2 = eval(y2code, ns)
        except:
            pg.debug.printExc('Error evaluating plot y2 values:')
            self.y2_code.setStyleSheet("QLineEdit { border: 2px solid red; }")
        else:
            self.y2_code.setStyleSheet("")

        if y1 is None and y2 is None:
            # No valid y-values
            return

        start_idx = [i for i, val in enumerate(self.info_list) if val == 0]

        self.plot.clear()

        for idx, pos in enumerate(start_idx):
            # Plot each sequence in a different color
            if idx + 1 == len(start_idx):
                # Last value in sequence
                pos_end = len(x)
            else:
                pos_end = start_idx[idx + 1]

            _x = x[pos:pos_end]
            if y1 is not None:
                _y1 = y1[pos:pos_end]
            if y2 is not None:
                _y2 = y2[pos:pos_end]

            if y1 is not None:
                self.plot.plot(x=_x, y=_y1, symbol='o', symbolBrush=(idx, 10))  # Plot
            if y2 is not None:
                self.plot.plot(x=_x, y=_y2, symbol='+', symbolBrush=(idx, 10))  # Plot

        self.plot.setLabels(bottom=(xcode, self.x_units_text.text()),
                            left=(y1_code, self.y1_units_text.text()))
        
    def clear_plot(self):
        self.data = None
        self.replot()

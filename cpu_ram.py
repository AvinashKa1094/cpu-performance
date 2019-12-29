import sys
from PyQt5 import QtGui
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import psutil as p
MAXITERS = 200
class CPUMonitor(FigureCanvas):
    def __init__(self):
        self.before = self.prepare_cpu_usage()
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 100)
        self.ax.set_autoscale_on(False)
        self.user, self.nice, self.sys, self.idle =[], [], [], []
        self.l_user, = self.ax.plot([],self.user, label='User %')
        self.l_nice, = self.ax.plot([],self.nice, label='Nice %')
        self.l_sys, = self.ax.plot([],self.sys, label='Sys %')
        self.l_idle, = self.ax.plot([],self.idle, label='Idle %')
        self.ax.legend()
        self.fig.canvas.draw()
        self.cnt = 0
        self.timerEvent(None)
        self.timer = self.startTimer(1000)
    def prepare_cpu_usage(self):
        t = p.cpu_times()
        if hasattr(t, 'nice'):
            return [t.user, t.nice, t.system, t.idle]
        else:
            return [t.user, 0, t.system, t.idle]
    def get_cpu_usage(self):
        now = self.prepare_cpu_usage()
        delta = [now[i]-self.before[i] for i in range(len(now))]
        total = sum(delta)
        self.before = now
        return [(100.0*dt)/total for dt in delta]
    def timerEvent(self, evt):
        result = self.get_cpu_usage()
        self.user.append(result[0])
        self.nice.append(result[1])
        self.sys.append( result[2])
        self.idle.append(result[3])
        self.l_user.set_data(range(len(self.user)), self.user)
        self.l_nice.set_data(range(len(self.nice)), self.nice)
        self.l_sys.set_data( range(len(self.sys)), self.sys)
        self.l_idle.set_data(range(len(self.idle)), self.idle)
        self.fig.canvas.draw()
        if self.cnt == MAXITERS:
            self.killTimer(self.timer)
        else:
            self.cnt += 1
widget = CPUMonitor()
widget.setWindowTitle("CPU Usage Realtime")
widget.show()

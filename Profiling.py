import time
from functools import wraps
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
import psutil



def timeTracker(Profiler):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            Profiler.functionTime = end - start

        return wrap
    return decorator


class Profiling:
    def __init__(self, ax, fieldVisualiser):
        self.ax = ax
        self.textComponents = list()
        self.mainText = None
        self.previousTPSCheckTime = 0
        self.functionTime = 0
        self.fieldVisualiser = fieldVisualiser
        self.buttons = list()
        self.hideButtonAx = None
        self.tps = 0
        self.fps = 0
        self.tickNumber = 0


    def startingText(self):
        self.mainText = self.ax.text(0, 0.99, 'initiating...', va='top')

        class Index:
            ind = 0

            def toggleAxVisibility(me, event):
                if self.fieldVisualiser.ax.get_visible():
                    self.fieldVisualiser.ax.set_visible(False)
                else:
                    self.fieldVisualiser.ax.set_visible(True)

            def minimize(me, event):
                self.ax.set_visible(False)
                self.fieldVisualiser.ax.set_visible(False)
                self.buttons[0].ax.set_visible(False)
                self.buttons[1].ax.set_visible(False)
                self.buttons[2].ax.set_visible(True)
                self.fieldVisualiser.fig.set_size_inches(0.1, 0.2)


            def maximize(me, event):
                print(self.buttons)
                self.ax.set_visible(True)
                self.fieldVisualiser.ax.set_visible(False)
                self.buttons[0].ax.set_visible(True)
                self.buttons[1].ax.set_visible(True)
                self.buttons[2].ax.set_visible(False)
                self.fieldVisualiser.fig.set_size_inches(8, 6)




        callback = Index()
        togvis = self.fieldVisualiser.fig.add_axes([0.76, 0, 0.2, 0.075])
        btogvis = Button(togvis, 'Toggle visibility')
        btogvis.on_clicked(callback.toggleAxVisibility)
        self.buttons.append(btogvis)

        minimise = self.fieldVisualiser.fig.add_axes([0.55, 0, 0.2, 0.075])
        bminimise = Button(minimise, 'Minimize')
        bminimise.on_clicked(callback.minimize)
        self.buttons.append(bminimise)

        maximize = self.fieldVisualiser.fig.add_axes([0, 0, 1, 1])
        bmaximize = Button(maximize, 'Maximize')
        bmaximize.on_clicked(callback.maximize)
        self.buttons.append(bmaximize)
        self.buttons[2].ax.set_visible(False)
        '''
        self.hideButtonAx = self.fieldVisualiser.fig.add_axes([0.01, 0.01, 0.2, 0.075])
        hideButton = Button(self.hideButtonAx, 'hide couriers')
        self.buttons.append(hideButton)
        hideButton.on_clicked(self.fieldVisualiser.hideCourierMovement)
        showButtonAx = self.ax.inset_axes([0.22, 0.01, 0.2, 0.075])
        showButton = Button(showButtonAx, 'show couriers')
        self.buttons.append(showButton)
        showButton.on_clicked(self.fieldVisualiser.showCourierMovement)
        '''

    def onclick(self, event):
        print(event.xdata, event.ydata)
        if event.inaxes is self.hideButtonAx:
            print('in')

    def tickProfiling(self):
        self.updateFPS()
        self.updateFunctionTime()
        self.updateFrameNumber()
        self.updateText()
        self.updateTotalRequestsReceived()

    def updateText(self):
        text = ''
        for textComponent in self.textComponents:
            text += textComponent[0]+': '+str(textComponent[1])+'\n'
        self.textComponents.clear()
        self.mainText.set_text(text)

    def updateFunctionTime(self):
        self.textComponents.append(('Function Time', self.functionTime))

    def updateFPS(self):
        if self.tickNumber % 10 == 0:
            now = time.time()
            if now-self.previousTPSCheckTime == 0:
                self.tps = 'inf'
                self.fps = 'inf'
            else:
                self.tps = 10/(now - self.previousTPSCheckTime)
                self.fps = self.tps/2
            self.previousTPSCheckTime = now
        self.textComponents.append(('TPS', round(self.tps, 2)))
        self.textComponents.append(('FPS', round(self.fps, 2)))

    def updateFrameNumber(self):
        self.tickNumber += 1
        # print(self.frameNumber)
        self.textComponents.append(('Tick Number', self.tickNumber))

    def updateTotalRequestsReceived(self):
        self.textComponents.append(('Requests Received', self.fieldVisualiser.totalReceivedRequests))

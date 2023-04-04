import time
from functools import wraps
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
        # self.buttons = list()
        self.hideButtonAx = None
        self.tps = 0
        self.fps = 0
        self.tickNumber = 0

    def startingText(self):
        self.mainText = self.ax.text(0, 0.99, 'initiating...', va='top')
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
        self.textComponents.append(('TPS', self.tps))
        self.textComponents.append(('FPS', self.fps))

    def updateFrameNumber(self):
        self.tickNumber += 1
        # print(self.frameNumber)
        self.textComponents.append(('Tick Number', self.tickNumber))

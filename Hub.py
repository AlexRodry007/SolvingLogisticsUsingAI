
class Hub:
    def __init__(self, node, services, pos, pyplotAx, ticksToReceive=60):
        self.services = services
        self.node = node
        self.ticksToReceive = ticksToReceive
        self.x = pos[node][0]
        self.y = pos[node][1]
        self.ax = pyplotAx
        self.dot, = self.ax.plot(self.x, self.y, marker='o', color='black', zorder=0, lw=5,
                                 markersize=23, markeredgewidth=3)

    def getService(self, serviceToGet):
        return serviceToGet in self.services, self.ticksToReceive

    def deleteRequest(self):
        self.dot.remove()

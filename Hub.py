
class Hub:
    def __init__(self, node, services, pos, pyplotAx):
        self.services = services
        self.node = node
        self.x = pos[node][0]
        self.y = pos[node][1]
        self.ax = pyplotAx
        self.dot, = self.ax.plot(self.x, self.y, 'y+', zorder=5)

    def getService(self, serviceToGet):
        return serviceToGet in self.services

    def deleteRequest(self):
        self.dot.remove()
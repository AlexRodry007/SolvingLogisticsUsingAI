
class Request:
    def __init__(self, node, serviceRequest, pos, pyplotAx):
        self.serviceRequest = serviceRequest
        self.node = node
        self.x = pos[node][0]
        self.y = pos[node][1]
        self.ax = pyplotAx
        self.dot, = self.ax.plot(self.x, self.y, 'r+', zorder=5)

    def receiveService(self, receivedService):
        return receivedService == self.serviceRequest

    def deleteRequest(self):
        self.dot.remove()

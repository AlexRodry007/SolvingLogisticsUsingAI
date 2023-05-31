
class Hub:
    def __init__(self, node, services, pos=None, pyplotAx=None, ticksToReceive=60):
        self.services = services
        self.node = node
        self.ticksToReceive = ticksToReceive

        # Дивимось чи вказані параметри необхідні для візуалізації
        if node is None or pos is None or pyplotAx is None:
            # Якщо ні - позначаємо що депо є неанімованим
            self.animated = False
        else:
            # Якщо так - позначаємо що депо є анімованим
            self.animated = True

            # Дізнаємось координати вузла, де знаходиться депо
            self.x = pos[node][0]
            self.y = pos[node][1]

            # Встановлюємо де буде намальоване депо
            self.ax = pyplotAx

            # Малюємо депо
            self.dot, = self.ax.plot(self.x, self.y, marker='o', color='black', zorder=0,
                                     lw=5, markersize=23, markeredgewidth=3)

    # Ця функція повертає успішність намагання забрати товар, та час який це зайняло
    def getService(self, serviceToGet):
        return serviceToGet in self.services, self.ticksToReceive

    # Ця функція видаляє депо
    def deleteRequest(self):
        self.dot.remove()

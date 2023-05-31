import random


class Request:
    def __init__(self, node, serviceRequest, pos=None, ax=None, ticksToServe=60):
        self.serviceRequest = serviceRequest
        self.ticksToServe = ticksToServe
        self.node = node

        # Ідентифікатор кур'єра, який повинен видалити запит
        self.delayedDeletion = -1

        # Дивимось чи вказані параметри необхідні для візуалізації
        if node is None or pos is None or ax is None:
            # Якщо ні - позначаємо що запит є неанімованим
            self.animated = False
        else:
            # Якщо так - позначаємо що запит є анімованим
            self.animated = True

            # Дізнаємось координати вузла, де знаходиться запит
            self.x = pos[node][0]
            self.y = pos[node][1]

            # Встановлюємо де буде намальований запит
            self.ax = ax

            # Малюэмо запит
            self.dot, = self.ax.plot(self.x, self.y, marker='o', color='#848ac4',
                                     zorder=0, lw=5, markersize=23, markeredgewidth=3)

    # Ця функція повертає час який зайняло доставка товару, або -1 якщо товар не підійшов
    def receiveService(self, receivedService):
        if receivedService == self.serviceRequest:
            return self.ticksToServe
        else:
            return -1

    # Ця функція видаляє запит
    def deleteRequest(self):
        if self.animated:
            self.dot.remove()


class RequestGenerator:
    def __init__(self, chanceToSpawn, outOf, possibleServices):
        self.chanceToSpawn = chanceToSpawn
        self.outOf = outOf
        self.possibleServices = possibleServices

    # Ця функція створює запит з певною ймовірністю
    def generateRequest(self, node, pos=None, ax=None):
        # Генеруєм випадкове число та перевіряємо чи воно менше ніж необхідне
        if random.randint(1, self.outOf) <= self.chanceToSpawn:
            # Беремо випадковий товар зі списку
            service = self.possibleServices[random.randint(0, len(self.possibleServices)-1)]

            # Створюємо і повертаємо запит
            return Request(node, service, pos, ax)

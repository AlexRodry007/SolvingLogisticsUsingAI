import networkx as nx
import random


class CourierMovement:

    def __init__(self, xCoord=None, yCoord=None, pyplotAx=None):
        self.ticksOfMovementLeft = 0

        if xCoord is None or yCoord is None or pyplotAx is None:
            self.animated = False
        else:
            self.animated = True
            self.x = xCoord
            self.y = yCoord
            self.xVelocity = 0
            self.yVelocity = 0
            self.ax = pyplotAx
            self.dot, = self.ax.plot(self.x, self.y, marker='o', color='black', zorder=5, lw=5,
                                     markersize=5, markeredgewidth=3, animated=False)

    def moveTo(self, xCoord, yCoord):
        if self.animated:
            self.x = xCoord
            self.y = yCoord
            self.dot.set_xdata(xCoord)
            self.dot.set_ydata(yCoord)

    def startMovementToCoord(self, xTargetCoord=None, yTargetCoord=None, ticksToReachTarget=0):
        if self.animated:
            self.xVelocity = (xTargetCoord - self.x) / ticksToReachTarget
            self.yVelocity = (yTargetCoord - self.y) / ticksToReachTarget
        self.ticksOfMovementLeft = ticksToReachTarget

    def stopMovementToCoord(self):
        if self.animated:
            self.xVelocity = 0
            self.yVelocity = 0
        self.ticksOfMovementLeft = 0

    def iterateMovement(self):
        if self.ticksOfMovementLeft > 0:
            if self.animated:
                self.moveTo(self.x + self.xVelocity, self.y + self.yVelocity)
            self.ticksOfMovementLeft -= 1
        else:
            self.stopMovementToCoord()
        if self.animated:
            return self.dot
        else:
            if self.ticksOfMovementLeft == 0:
                return False
            else:
                return True


class Courier:
    def __init__(self, courierName, aiName, pos=None, currentNode=0,
                 pyplotAx=None, hivemind=None, oneStepBehind=False,
                 fieldCalculator=None, id=0):
        # Калькулятор або візуалізатор поля, в якому знаходиться кур'єр
        self.fieldCalculator = fieldCalculator

        # Ім'я, яке ніде не використовується
        self.name = courierName

        # Перевірка чи є кур'єр анімованим, чи ні
        if pos is None or pyplotAx is None:
            self.courierMovement = CourierMovement()
        else:
            self.courierMovement = CourierMovement(pos[currentNode][0],
                                                   pos[currentNode][1], pyplotAx)
        # Поведінка кур'єра
        self.courierAi = CourierAi(aiName, self, currentNode, hivemind)

        # Товар, ячкий кур'єр перевозить
        self.carryingService = None

        # Формат видалення виконаних запитів
        self.oneStepBehind = oneStepBehind

        # Нагорода та Покарання
        self.reward = 0
        self.punishment = 0

        # Унікальний ідентифікаційний номер
        self.id = id

    def iterateCourier(self, action=None):
        # Якщо кур'єр не зайнятий
        if self.courierAi.freeze <= 0:
            # Ітеруємо "інтелект" кур'єра, пропонуємо дію, якщо вона є
            self.courierAi.iterateAi(action)

            # Якщо необхідно, кур'єр власноруч видаляє виконані запити
            if self.oneStepBehind:
                self.fieldCalculator.killRequests(self.id)

            # Прораховуєм команди для руху
            self.courierAi.hivemind.moveToFinalNode(self)

            # Рухаємо кур'єра
            courierMovement = self.courierMovement.iterateMovement()
            self.courierAi.endOfTheMoveCheck()

            # Отримуємо або доставляємо товар
            self.courierAi.provideOrGetService()
        else:
            # Зменшуємо кількість часу що залишилось бути зайнятим
            courierMovement = False
            self.courierAi.freeze -= 1

        # Повертаємо чи рухався кур'єр чи ні
        return courierMovement

    def noPathAndMovement(self):
        return len(self.courierAi.courierPath) == 0 and self.courierMovement.ticksOfMovementLeft == 0 \
            and self.courierAi.freeze <= 0


class CourierAi:

    def __init__(self, name, courier, currentNode, hivemind):
        self.name = name
        self.courier = courier
        self.currentNode = currentNode
        self.currentTargetNode = currentNode
        self.finalTargetNode = None
        self.hivemind = hivemind
        self.courierPath = ()
        self.freeze = 0

    def endOfTheMoveCheck(self):
        if self.courier.courierMovement.ticksOfMovementLeft == 0:
            self.currentNode = self.currentTargetNode

    def provideOrGetService(self):
        if self.freeze <= 0:
            self.hivemind.provideOrGetService(self.courier)

    def iterateAi(self, action=None):
        self.hiveMindAi(action)

    def hiveMindAi(self, action=None):
        self.hivemind.getCommands(self.courier, action)

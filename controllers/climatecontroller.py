from testdata import*
from canBus import*
from controller import*
import threading
class ClimateController(Controller):
    def __init__(self, networkManager):
        super(networkManager)
        self.testData = TestData()
        self.testData.loadData()
        self.CANBusController = canBus()

        registerAction("shutdown", shutdown)
        registerAction("Idle", Idle)
        t = threading.Thread.__init__(self)
        t.start()

    def shutdown(self):   #shutdowns the climatecontroller
        t.close()
        sys.exit()
    def Idle(self):       #updates the controller when the car is in idle
        pass
    def run(self):
        self.testData.update()

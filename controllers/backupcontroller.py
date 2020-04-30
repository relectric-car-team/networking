from TestData import*
from Controller import*
class BackupController(Controller):
    def __init__(self):
        self.testData = TestData()
        self.testData.loadData()

        registerAction("shutdown", shutdown)
        registerAction("update", update)
        registerAction("Idle", Idle)

    def shutdown(self):   #shutdowns the BackupController
        sys.exit()
    def update(self):     #updates the controller to the current data
        pass
    def Idle(self):       #updates the controller when the car is in idle
        pass

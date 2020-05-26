import logging as log
from controller import *
from controllers import *
from networkmanager import NetworkManager
import sys


class Systems:
    """ The Systems class is the main object that encapsulates the program for
    the electric car central systems. It consists of a set of 'controller'
    modules that each contribute separate functions to control and manage
    different sub-systems in the car (battery, motor, climate control,
    etc). In addition, this class owns an instance of NetworkManager,
    an object containing instances of all the necessary abstracted networking
    interfaces needed to communicate with the aforementioned sub-systems.
    The NetworkManager is passed to each controller upon initialization.
    """

    def __init__(self):
        """ Creates and initializes the network manager and all of the
        controllers.
        """
        log.info("Initializing systems...")
        self.__controllers = []
        self.__networkManager = NetworkManager(("localhost", 4000), [])
        self.__controllers.append(MotorController(self.__networkManager))
        self.__controllers.append(BatteryController(self.__networkManager))
        self.__controllers.append(ClimateController(self.__networkManager))
        self.__controllers.append(SensorController(self.__networkManager))
        self.__controllers.append(BackupController(self.__networkManager))
        self.__loop()  # Note there is currently no end condition.

    def __get_data(self, name: str) -> any:
        """ Finds and returns the value of the specified variable that belongs
        to one	of the controllers.

        name - A string to identify the variable.
        """
        for controller in self.__controllers:
            try:
                log.debug("Getting data variable '{0}'.".format(name))
                return controller.get_variable(name, False)
            except ControllerError:
                log.error("Failed to get data variable '{0}'.".format(name))
                return None

    def __set_data(self, name: str, value: any) -> None:
        """ Finds and sets the value of the specified variable that belongs
        to one of the controllers.

        name - A string to identify the variable.
        value - New value for the specified variable.
        """
        for controller in self.__controllers:
            try:
                controller.set_variable(name, value)
                log.debug("Set data variable '{0}' with value "
                          "{1}".format(name, value))
            except ControllerError:
                log.error("Failed to set data variable '{0}' with value "
                          "{1}".format(name, value))

    def __send_action(self, name: str, args: Tuple[any]) -> None:
        """ Calls the action specified by a controller with the provided
        arguments.

        name - A string to identify the action.
        args - Tuple of arguments to pass to the function.
        """
        for controller in self.__controllers:
            try:
                controller.perform_action(name, args)
                log.debug("Performed action '{0}' with arguments "
                          "{1}.".format(name, args))
            except ControllerError:
                log.error("Failed to perform action '{0}' with arguments "
                          "{1}.".format(name, args))

    def __loop(self):
        """ The main program loop for the systems computer. Listens for external
         requests and services them accordingly with the actions of controllers.
        The	format of requests directed to the actions of controllers is a
        dictionary with the format {"type": ["action"|"get"|"set"],
        "name": ["name"], ["args": []], ["value": any]}.
        """
        log.info("Starting main loop...")
        while True:
            request = self.__networkManager.get_pinet().get_request()
            if request is not None:
                response = None
                if request["type"] == "action":
                    response = self.__send_action(request["name"],
                                                 tuple(request["args"]))
                elif request["type"] == "get":
                    response = self.__get_data(request["name"])
                elif request["type"] == "set":
                    try:
                        self.__set_data(request["name"], request["value"])
                        response = True
                    except ControllerError:
                        response = False
                self.__networkManager.get_pinet().send_response(
                    request["requestKey"],
                    response, request["peer"])

    def shutdown(self) -> None:
        """ Safely shuts the controllers down. """
        log.info("Shutting systems down...")
        for controller in self.__controllers:
            controller.shutdown()


# Main module entry point.
if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='./logs/systems.log',
                    filemode='w',)
    consoleLog = log.StreamHandler(sys.stdout)
    consoleLog.setLevel(log.INFO)
    consoleFormat = log.Formatter('%(levelname)-8s %(message)s')
    consoleLog.setFormatter(consoleFormat)
    log.getLogger('').addHandler(consoleLog)
    log.basicConfig()
    systems = Systems()

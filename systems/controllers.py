import attr


def _type_validator(instance: object, variable: attr.Attribute,
                    new_value: any):
    """Type validation for @attr.s - on_setattr().

    Args:
        instance (object): Instance the new attribute is being set on
        variable (attr.Attribute): Instance attribute
        new_value (any)

    Raises:
        TypeError: Thrown if type mismatch

    Returns:
        new_value
    """
    current_variable_type = variable.type
    new_value_type = type(new_value)
    if current_variable_type != new_value_type:
        raise TypeError(f"Trying to set type {new_value_type} "
                        f"on attribute of type {current_variable_type}")
    return new_value


class ControllerDecorator:
    """Utility decorator for attr.attrs and dict-like properties.

    Allows us to do things like::

        @Controller
        class DummyController:
            variable: int = 0

        dummy = DummyController()
        dummy['variable'] = 4
        variable = dummy['variable]
    ::
    """

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def asdict(self):
        return attr.asdict(self)

    def __call__(self, class_):
        class_.__getitem__ = ControllerDecorator.__getitem__
        class_.__setitem__ = ControllerDecorator.__setitem__
        class_ = attr.attrs(class_,
                            slots=True,
                            auto_attribs=True,
                            eq=False,
                            on_setattr=_type_validator)
        class_.asdict = ControllerDecorator.asdict
        return class_


Controller = ControllerDecorator()


@Controller
class BackupController:
    """Controller class for backup sensors.

    Attributes:
        speed (int): Defaults to 0.
        distance (int): Defaults to 0.
    """
    speed: int = 0
    distance: int = 0


@Controller
class BatteryController:
    """Controller class for battery sensors.

    Attributes:
        voltage (int): Defaults to 0.
        distance (int): Defaults to 0.
    """
    voltage: int = 0
    temperature: int = 0


@Controller
class ClimateController:
    """Controller class for climate sensors.

    Attributes:
        weathertemperature (int): Defaults to 0.
        fanpower (int): Defaults to 0.
    """
    weathertemperature: int = 0
    fanpower: int = 0


@Controller
class MotorController:
    """Controller class for motor sensors.

    Attributes:
        speed (int): Defaults to 0.
        voltage (int): Defaults to 0.
        temperature (int): Defaults to 0.
        rpm (int): Defaults to 0.
    """
    speed: int = 0
    voltage: int = 0
    temperature: int = 0
    rpm: int = 0


@Controller
class SensorController:
    """Controller class for distance sensors.

    Attributes:
        distancefront (int): Defaults to 0.
        distanceback (int): Defaults to 0.
    """
    distancefront: int = 0
    distanceback: int = 0


controllers = {
    "backup": BackupController(),
    "battery": BatteryController(),
    "climate": ClimateController(),
    "motor": MotorController(),
    "sensor": SensorController()
}

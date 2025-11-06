from src.iot.thing import Thing


class Lamp(Thing):
    def __init__(self):
        super().__init__("Lamp", "a test lamp")
        self.power = False

        # Define properties - using asynchronous getters
        self.add_property("power", "Is the light on?", self.get_power)

        # Define methods - use an asynchronous method handler
        self.add_method("TurnOn", "turn on the light", [], self._turn_on)

        self.add_method("TurnOff", "turn off lights", [], self._turn_off)

    async def get_power(self):
        return self.power

    async def _turn_on(self, params):
        self.power = True
        return {"status": "success", "message": "light is on"}

    async def _turn_off(self, params):
        self.power = False
        return {"status": "success", "message": "light is off"}

from INA219 import INA219


upsTopics = {
    "/ups/voltage": "get_voltage",
    "/ups/power": "get_power",
    }


class UpsTools:
    def __init__(self):
        self.ina219 = INA219(addr=0x43)
        self.upsTopic = upsTopics

    def update(self):
        from zmqTool import ZmqTool
        zmq_tool = ZmqTool()

        while True:
            for topic, function_name in self.upsTopic.items():
                if zmq_tool.listen_message(topic) == "update":
                    function = getattr(self, function_name, None)
                    if function:
                        result = function()
                        zmq_tool.publish_message(topic, str(result))

    def get_voltage(self):
        voltage = str(round(self.ina219.getBusVoltage_V(), 2)) + " V"
        return voltage

    def get_power(self):
        power = str(round(self.ina219.getPower_W(), 2)) + " W"
        return power




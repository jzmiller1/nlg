from documents import Message, RelativeVariation, Measurement, AbsoluteSpec


class MonthlyTemperatureMsg(Message):
    """MonthlyTemperatureMsg class."""

    def __init__(self, period, temperature):
        self.period = period
        self.temperature = temperature

    def __repr__(self):
        return "MonthlyTemperatureMsg({}, {})".format(self.period,
                                                      self.temperature)


class MonthlyTemperature(Message):
    """Stuff"""

    def __init__(self, data, message=MonthlyTemperatureMsg):
        self.data = data
        self.message = message

    def getMessage(self, limits):
        self.data.execute("""SELECT AVG(high) FROM  WHERE month=?;""",
                          (limits['month'],))
        avg = self.data.fetchone()
        # Should really use RelativeVariation(1, Measurement('degreesCentigrade', 2))
        # using just average for now
        return self.message(limits['month'],
                            AbsoluteSpec(avg))

    @staticmethod
    def temp_category(value):
        if value <= 0:
            return 'freezing'
        elif 0 <= value < 5:
            return 'very cold'
        elif 5 <= value < 10:
            return 'cold'
        elif 10 <= value < 15:
            return 'cool'
        elif 15 <= value < 20:
            return 'mild'
        elif 20 <= value < 25:
            return 'warm'
        elif 25 <= value < 30:
            return 'very warm'
        elif 30 <= value < 35:
            return 'hot'
        elif 35 <= value < 40:
            return 'very hot'
        elif value >= 40:
            return 'extremely hot'


class MonthlyRainfallMsg(Message):
    """MonthlyTemperatureMsg class."""

    def __init__(self, period, rainfall):
        self.period = period
        self.rainfall = rainfall


class RainEventMsg(Message):
    """RainEventMsg class.  Described on pg 90."""

    def __init__(self, period, day, rainType):
        self.period = period
        self.day = day
        self.rainType = rainType

    def __repr__(self):
        return "RainEventMsg({}, {}, {})".format(self.period,
                                                 self.day,
                                                 self.rainType)


class RainEvents(Message):
    """Stuff"""

    def __init__(self, data, message=RainEventMsg):
        self.data = data
        self.message = message

    @staticmethod
    def category(value):
        if 0 <= value < 0.5:
            return 'light'
        elif 0.5 <= value < 1:
            return 'moderate'
        elif 1 <= value < 2:
            return 'heavy'
        elif value >= 2:
            return 'extremely heavy'

    def getAllMessages(self, limits):
        self.data.execute("""SELECT * FROM rainEvents WHERE month=?;""",
                          (limits['month'],))
        return [self.message(month, day, self.category(rain))
                for month, day, rain in self.data.fetchall()]

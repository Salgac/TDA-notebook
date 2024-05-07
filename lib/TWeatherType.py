from enum import Enum, auto


class TWeatherType(Enum):
    CLEAR = auto()
    RAIN = auto()
    OVERCAST = auto()
    PARTIALLY_CLOUDY = auto()
    ALL = auto()


Mapper = {
    TWeatherType.CLEAR: "Clear",
    TWeatherType.RAIN: "Rain",
    TWeatherType.OVERCAST: "Overcast",
    TWeatherType.PARTIALLY_CLOUDY: "Partially cloudy",
}

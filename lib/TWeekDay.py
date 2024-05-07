from enum import Enum, auto


class TWeekDay(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()
    ALL = auto()


Mapper = {
    TWeekDay.MONDAY: "Monday",
    TWeekDay.TUESDAY: "Tuesday",
    TWeekDay.WEDNESDAY: "Wednesday",
    TWeekDay.THURSDAY: "Thursday",
    TWeekDay.FRIDAY: "Friday",
    TWeekDay.SATURDAY: "Saturday",
    TWeekDay.SUNDAY: "Sunday",
}

from enum import Enum, auto


class TDataType(Enum):
    EMB_1 = auto()
    EMB_2 = auto()
    TRACKB_1 = auto()
    TRACKB_2 = auto()
    BELL = auto()
    SLIP_SLIDE = auto()
    ALL = auto()


Mapper = {
    TDataType.EMB_1: "NudzBr_1",
    TDataType.EMB_2: "NudzBr_2",
    TDataType.TRACKB_1: "KolBr_1",
    TDataType.TRACKB_2: "KolBr_2",
    TDataType.BELL: "Zvonec",
    TDataType.SLIP_SLIDE: "Sklz_Smyk",
}

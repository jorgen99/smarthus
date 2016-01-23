# coding=utf-8
from events.sensor import Sensor

class Constants:
    def __init__(self):
        pass

    TEMPERATURE_ID = 10
    LIGHT_RELAY = Sensor("12930598", "10")
    MOVEMENT_SENSOR = Sensor("12066258", "10")
    LIGHT_SWITCH_MORNING = Sensor("538870", "1")
    LIGHT_SWITCH_DIM = Sensor("42594", "1")
    VALID_PROTOCOLS = ["mandolyn", "arctech"]
    MOOD_LIGHTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    NIGHT_LIGHTS = [9]
    MORNING_LIGHTS = [2, 4, 9, 12]
    MOTION_CONTROLLED_LGHTS = [13]
    DIM_LEVEL = 80
    ON = "turnon"
    OFF = "turnoff"

# id Namn                        House      Unit     Group
# --------------------------------------------------------------
#    Ljussensor                  12930598   10       0
#    Rörelse                     12066258   10       0
#
#  1 Lampa kontoret              22222001    1
#  2 Laminohörnan                11990530    1
#  3 Elias fönster               11990530    2
#  4 Lampan i hörnet             11990530    3
#  5 Gästrummet                  11990530    4
#  6 Alvas fönster               11990530    5
#  7 Sovrummet                   11990530    6
#  8 Kaninlampan                 22222001    2
#  9 Gristavlan                  22222001    3
# 10 Ledig                       22222001    4
# 11 Växthuset                   22222001    5
# 
# --------------------------------------------------
# 
#  1 Lampa kontoret       22222001   1
#  4 Lampan i hörnet      22222001   4
# 
#  2 Laminohörnan         11990530   1
#  3 Elias fönster        11990530   2
#  5 Gästrummet           11990530   4
#  6 Alvas fönster        11990530   5
#  7 Sovrummet            11990530   6
# 12 Fönster uppe         11990530   7
# 
#  8 Kaninlampan          22222001   2
#  9 Gristavlan           22222001   3
# 11 Växthuset            22222001   5
# 10 Petras lampa         22222001   6
# 
# 13 Tvättstugan          00000001   1
# 20 Element garage       00000001   2


# Skymmningsrelä
# model:selflearning;house:12930598;unit:10;group:0;method:turnoff

# Rörelsevakt
# model:selflearning;house:12066258;unit:10;group:0;method:turnon

# Temperatur ute
# protocol:mandolyn;id:11;model:temperaturehumidity;temp:9.0;humidity:67

# Temperatur växthus
#


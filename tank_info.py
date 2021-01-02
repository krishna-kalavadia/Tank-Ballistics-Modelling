# Class structure is so I can later add more attributes to tank objects such as the ability to select various guns put
# on the same model of tank, various ammo types and so on

# M1A1 Abrams Info
# Source: http://afvdb.50megs.com/usa/m1abrams.html
# Source: https://www.armyrecognition.com/united_states_army_heavy_armoured_vehicles_tank_uk/m1a1_abrams_main_battle_tank_technical_data_sheet_specifications_description_pictures_video.html
class TankM1A1:
    def __init__(self):
        self.muzzle_velocity = 1575  # m/s
        self.max_gun_elevation = 20  # degrees
        self.max_gun_depression = 10  # degrees
        self.gun_height = 1.89  # m


# Challenger 1 Info
# Source: https://en.wikipedia.org/wiki/Challenger_1
class TankChallenger1:
    def __init__(self):
        self.muzzle_velocity = 1370  # m/s
        self.max_gun_elevation = 20  # degrees
        self.max_gun_depression = 10  # degrees
        self.gun_height = 2.1  # m (estimate)


# M4A1 Sherman Info
# Source: http://afvdb.50megs.com/usa/m4sherman.html
class TankM4A1:
    def __init__(self):
        self.muzzle_velocity = 731  # m/s
        self.max_gun_elevation = 25  # degrees
        self.max_gun_depression = 12  # degrees
        self.gun_height = 2.24  # m


# Churchill IV Info
# Source: https://milart.blog/2020/09/07/the-churchill-mark-iv-infantry-tank-in-service-with-the-canadian-army-overseas-december-1942-to-may-1943/
class TankChurchill4:
    def __init__(self):
        self.muzzle_velocity = 853  # m/s
        self.max_gun_elevation = 20  # degrees
        self.max_gun_depression = 12.5  # degrees
        self.gun_height = 2.2   # m (estimate)

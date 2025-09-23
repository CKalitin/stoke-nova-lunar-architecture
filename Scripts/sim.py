import utils

second_stage = utils.Stage(
    dry_mass=5543,  # kg
    lox_mass=15250,  # kg
    fuel_mass=2750,  # kg
    thrust=111000,  # N
    isp_avg=440,  # s
    payload=5000  # kg
)

first_stage = utils.Stage(
    dry_mass=14553,  # kg
    fuel_mass=40800,  # kg
    lox_mass=142900,  # kg
    thrust=3110000,  # N
    isp_avg=340,  # s
    payload=second_stage
)

s1_dv = utils.get_stage_dv(first_stage)
s2_dv = utils.get_stage_dv(second_stage)

s1_landing_propellant_mass = utils.get_landing_propellant_mass(first_stage, initial_velocity=400, throttle=1/7*0.9)
s2_landing_propellant_mass = utils.get_landing_propellant_mass(second_stage, initial_velocity=100, throttle=1)
s2_deorbit_propellant_mass = utils.get_propellant_mass_for_dv(second_stage, delta_v=100, final_mass=second_stage.terminal_mass() + s2_landing_propellant_mass) # Include landing propellant

stage_1_dv_with_landing = utils.get_stage_dv(first_stage, final_mass=first_stage.terminal_mass() + s1_landing_propellant_mass)
stage_2_dv_with_deorbit_and_landing = utils.get_stage_dv(second_stage, final_mass=second_stage.terminal_mass() + s2_landing_propellant_mass + s2_deorbit_propellant_mass)

print("Stage 1 delta-v:", s1_dv, "m/s")
print("Stage 1 delta-v with landing propellant:", stage_1_dv_with_landing, "m/s")
print("Stage 1 landing propellant mass:", s1_landing_propellant_mass, "kg")
print("")
print("Stage 2 delta-v:", s2_dv, "m/s")
print("Stage 2 delta-v with deorbit and landing propellant:", stage_2_dv_with_deorbit_and_landing, "m/s")
print("Stage 2 landing propellant mass:", s2_landing_propellant_mass, "kg")
print("Stage 2 deorbit propellant mass:", s2_deorbit_propellant_mass, "kg")
print("")
print("Expendable delta-v:", s1_dv + s2_dv, "m/s")
print("Partially reusable delta-v:", stage_1_dv_with_landing + s2_dv, "m/s")
print("Fully reusable delta-v:", stage_1_dv_with_landing + stage_2_dv_with_deorbit_and_landing, "m/s")
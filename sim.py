from __future__ import annotations # For float | 'Stage' type hint
import math
from dataclasses import dataclass

G = 9.80665 # Acceleration due to gravity in m/s^2

@dataclass
class Stage:
    dry_mass: float  # kg
    lox_mass: float  # kg
    fuel_mass: float  # kg
    thrust: float  # N
    isp_avg: float  # s, average during burn (ie SL vs Vac for an ascent stage)
    residuals: float = 0.001 # Percentage of wet mass that can't be used
    payload: float | 'Stage' = 0.0 # kg or another Stage object
    
    def __post_init__(self):
        # Calculate and store the oxidizer-to-fuel ratio + fuel and oxidizer propellant mass ratios
        self.of_ratio = self.lox_mass / self.fuel_mass if self.fuel_mass > 0 else 0.0
        self.fuel_ratio = self.fuel_mass / (self.fuel_mass + self.lox_mass) if (self.fuel_mass + self.lox_mass) > 0 else 0.0
        self.lox_ratio = self.lox_mass / (self.fuel_mass + self.lox_mass) if (self.fuel_mass + self.lox_mass) > 0 else 0.0
    
    def wet_mass(self) -> float:
        # return wet mass as sum of dry, propellant, and payload masses
        return self.dry_mass + self.propellant_mass() + self.payload_mass()
    
    def propellant_mass(self) -> float:
        # Total propellant mass (fuel + oxidizer)
        return self.fuel_mass + self.lox_mass
    
    def terminal_mass(self) -> float:
        # Payload + Dry + residuals mass for calculating mass at end of a burn
        if type(self.payload) is Stage:
            return self.payload.wet_mass() + self.dry_mass + (self.wet_mass() * self.residuals)
        return self.payload + self.dry_mass + (self.wet_mass() * self.residuals)

    def payload_mass(self) -> float:
        if type(self.payload) is Stage:
            return self.payload.wet_mass()
        return self.payload
    
    def mass_flow_rate(self) -> float:
        # Mass flow rate in kg/s
        return self.thrust / (self.isp_avg * G)
    
    def change_propellant_mass(self, delta_mass: float) -> None:
        # Change the propellant mass by a given amount, updating both fuel and oxidizer masses using the O:F ratio
        self.fuel_mass += delta_mass * self.fuel_ratio
        self.lox_mass += delta_mass * self.lox_ratio
        
    def exhaust_velocity(self) -> float:
        # Calculate exhaust velocity in m/s
        return self.isp_avg * G

second_stage = Stage(
    dry_mass=8045,  # kg
    lox_mass=15250,  # kg
    fuel_mass=2750,  # kg
    thrust=111000,  # N
    isp_avg=440,  # s
    payload=3000  # kg
)

first_stage = Stage(
        dry_mass=17050,  # kg
        fuel_mass=40800,  # kg
        lox_mass=142900,  # kg
        thrust=3110000,  # N
        isp_avg=340,  # s
        payload=second_stage
    )

def get_stage_dv(stage, final_mass=None):
    # Return full burn delta-v (inclusive of residuals), or the dV for burning a specific amount of propellant
    if final_mass is None:
        return stage.exhaust_velocity() * math.log(stage.wet_mass() / stage.terminal_mass())
    if final_mass <= stage.terminal_mass():
        print(f"Warning: Final mass exceeds terminal mass of stage.\n{final_mass} <= {stage.terminal_mass()}.\n{stage}")
    return stage.exhaust_velocity() * math.log(stage.wet_mass() / final_mass)

def get_landing_propellant_mass(stage, initial_velocity=400, throttle=1/7*0.9, verbose=False):
    # With time going backwards from landing, calculate acceleration for every time step
    # This simulates the rocket ascending and gaining propellant as it does
    # I failed at solving the integral
    
    # Terminal velocity for a 620 BC object (Stage 2) on Earth is 99.63 m/s - https://grok.com/chat/486f5557-3e2e-4b87-88de-913e8e5c8344
    
    vel = 0
    time = 0
    time_step = 0.1 # seconds
    mass = stage.terminal_mass() - stage.payload_mass() # This is inclusive of residuals
    while vel < initial_velocity and time < 1000:
        acceleration = stage.thrust * throttle / mass - G
        vel += acceleration * time_step
        mass += stage.mass_flow_rate() * throttle * time_step
        time += time_step
        if verbose:
            print(f"Time: {time:.1f}s, Velocity: {vel:.1f} m/s, Mass: {mass:.1f} kg, Acceleration: {acceleration:.2f} m/s²")
    return stage.mass_flow_rate() * throttle * time

def get_propellant_mass_for_dv(stage, delta_v, initial_mass=None, final_mass=None):
    # Return the propellant mass required for a given delta v burn
    # Specifing intial_mass starts the burn at that mass
    # Specifying final_mass ends the burn at that mass, where initial mass would be final_mass + propellant mass
    
    # Shuttle deorbit burn was apparently 90 m/s, up to 150 m/s https://space.stackexchange.com/questions/12011/how-could-a-90-m-s-delta-v-be-enough-to-commit-the-space-shuttle-to-landing
    # Formulas derived from Tsiolkovsky rocket equation
    
    if initial_mass is not None:
        final_mass = initial_mass * math.exp(-delta_v / stage.exhaust_velocity())
        return initial_mass - final_mass
    if final_mass is not None:
        initial_mass = final_mass * math.exp(delta_v / stage.exhaust_velocity())
        return initial_mass - final_mass
    print("Error: Must specify either initial_mass or final_mass")

s1_dv = get_stage_dv(first_stage)
s2_dv = get_stage_dv(second_stage)

s1_landing_propellant_mass = get_landing_propellant_mass(first_stage, initial_velocity=400, throttle=1/7*0.9)
s2_landing_propellant_mass = get_landing_propellant_mass(second_stage, initial_velocity=100, throttle=1)
s2_deorbit_propellant_mass = get_propellant_mass_for_dv(second_stage, delta_v=100, final_mass=second_stage.terminal_mass() + s2_landing_propellant_mass) # Include landing propellant

stage_1_dv_with_landing = get_stage_dv(first_stage, final_mass=first_stage.terminal_mass() + s1_landing_propellant_mass)
stage_2_dv_with_deorbit_and_landing = get_stage_dv(second_stage, final_mass=second_stage.terminal_mass() + s2_landing_propellant_mass + s2_deorbit_propellant_mass)

print("")
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
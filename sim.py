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
    
    # return wet mass as sum of dry, propellant, and payload masses
    def wet_mass(self) -> float:
        return self.dry_mass + self.fuel_mass + self.lox_mass + self.payload_mass()
    
    # Payload + Dry + residuals mass for calculating mass at end of a burn
    def terminal_mass(self) -> float:
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

def get_stage_dv(stage):
    exhaust_velocity = stage.isp_avg * G # m/s
    return exhaust_velocity * math.log(stage.wet_mass() / stage.terminal_mass())

def get_landing_propellant_mass(stage, initial_velocity=400, throttle=1/7*0.9):
    # With time going backwards from landing, calculate acceleration for every time step
    # This simulates the rocket ascending and gaining propellant as it does
    # I failed at solving the integral
    
    vel = 0
    time = 0
    time_step = 0.1 # seconds
    mass = stage.terminal_mass() - stage.payload_mass() # This is inclusive of residuals
    while vel < initial_velocity and time_step < 1000:
        acceleration = stage.thrust * throttle / mass - G
        vel += acceleration * time_step
        mass += stage.mass_flow_rate() * throttle * time_step
        time += time_step
        print(f"Time: {time:.2f}s, Velocity: {vel:.2f} m/s, Mass: {mass:.2f} kg, Acceleration: {acceleration} m/s²")
    return stage.mass_flow_rate() * throttle * time

stage_1_dv = get_stage_dv(first_stage)
stage_2_dv = get_stage_dv(second_stage)

print(get_landing_propellant_mass(first_stage))

print("Stage 1 delta-v:", stage_1_dv, "m/s")
print("Stage 2 delta-v:", stage_2_dv, "m/s")
print("Total delta-v:", stage_1_dv + stage_2_dv, "m/s")
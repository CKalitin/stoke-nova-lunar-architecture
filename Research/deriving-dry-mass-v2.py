# See deriving-dry-mass.md for some explanation of methodology

import math
    
STAINLESS_DENSITY = 7930 # kg/m³ (Stainless Steel 304)
TANK_WALL_THICKNESS_S1 = 0.003 # m (3mm)
TANK_WALL_THICKNESS_S2 = 0.002 # m (2mm) - using thinner walls for S2
HEATSHIELD_THICKNESS = 0.01 # m (1cm steel)
THRUST_STRUCTURE_RATIO = 0.16 # 16% of total dry mass, see deriving-dry-mass.md

# Stage dimensions (from the markdown)
S1_LENGTH = 27.1 # m
S1_DIAMETER = 3.7 # m
S2_LENGTH = 12.8 # m
S2_DIAMETER = 4.3 # m

NET_DRY_MASS = 20096 # kg

S1_ENGINE_MASS = 453 # kg per engine
S2_ENGINE_MASS = 188 # kg per engine

NUM_ENGINES_S1 = 7

S2_OTHER_MASS = 1000 # kg (avionics, plumbing, RCS, etc.)
S1_THRUST_STRUCTURE_DRY_MASS_FRACTION = 0.16 # 16% of total stage dry mass, see deriving-dry-mass.md

def calculate_cylindrical_surface_area(length, diameter):
    """Calculate surface area of cylindrical sidewalls"""
    return length * diameter * math.pi

def calculate_hemispherical_surface_area(diameter):
    """Calculate surface area of hemispherical ends"""
    radius = diameter / 2
    return 2 * math.pi * radius**2

def calculate_total_tank_surface_area(length, diameter):
    """Calculate total tank surface area (cylinder + 2 hemispheres)"""
    sidewalls = calculate_cylindrical_surface_area(length, diameter)
    ends = calculate_hemispherical_surface_area(diameter)
    return sidewalls + ends

def calculate_tank_wall_mass(length, diameter, thickness, density=STAINLESS_DENSITY):
    """Calculate tank wall mass"""
    surface_area = calculate_total_tank_surface_area(length, diameter)
    volume = surface_area * thickness
    return volume * density

def calculate_heatshield_mass(diameter, thickness=HEATSHIELD_THICKNESS, density=STAINLESS_DENSITY):
    """Calculate heatshield mass (flat surface approximation)"""
    radius = diameter / 2
    area = math.pi * radius**2
    volume = area * thickness
    return volume * density

def print_dict(d, indent=0):
    for key, value in d.items():
        print(' ' * indent + f"{key}: {value:,.0f} kg")
    print()

def calculate_s2_dry_mass(thickness=TANK_WALL_THICKNESS_S2):
    """Calculate S2 dry mass given tank wall thickness"""
    tank_wall_mass = calculate_tank_wall_mass(S2_LENGTH, S2_DIAMETER, thickness)
    heatshield_mass = calculate_heatshield_mass(S2_DIAMETER)
    engine_mass = S2_ENGINE_MASS
    other_mass = S2_OTHER_MASS
    
    total_dry_mass = tank_wall_mass + heatshield_mass + engine_mass + other_mass

    return {
        "tank_wall_mass": tank_wall_mass,
        "heatshield_mass": heatshield_mass,
        "engine_mass": engine_mass,
        "other_mass": other_mass,
        "total_dry_mass": total_dry_mass
    }
    
def calculate_s1_dry_mass(s2_dry_mass, net_dry_mass, thickness=TANK_WALL_THICKNESS_S1):
    """Calculate S1 dry mass given S2 dry mass"""
    total_dry_mass = net_dry_mass - s2_dry_mass
    tank_wall_mass = calculate_tank_wall_mass(S1_LENGTH, S1_DIAMETER, TANK_WALL_THICKNESS_S1)
    engine_mass = S1_ENGINE_MASS * NUM_ENGINES_S1
    thrust_structure_mass = total_dry_mass * S1_THRUST_STRUCTURE_DRY_MASS_FRACTION
    other_mass = total_dry_mass - tank_wall_mass - engine_mass - thrust_structure_mass
    
    return {
        "tank_wall_mass": tank_wall_mass,
        "engine_mass": engine_mass,
        "thrust_structure_mass": thrust_structure_mass,
        "other_mass": other_mass,
        "total_dry_mass": total_dry_mass
    }
    
s2_dict = calculate_s2_dry_mass()
s1_dict = calculate_s1_dry_mass(s2_dict['total_dry_mass'], NET_DRY_MASS)

print("S2 Dry Mass Breakdown:")
print_dict(s2_dict, indent=2)

print("S1 Dry Mass Breakdown:")
print_dict(s1_dict, indent=2)
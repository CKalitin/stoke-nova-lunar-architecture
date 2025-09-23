import utils

second_stage = utils.Stage(
    dry_mass = 7577, # dry_mass=5543,  # kg
    lox_mass=15250,  # kg
    fuel_mass=2750,  # kg
    thrust=111000,  # N
    isp_avg=440,  # s
    payload=5000  # kg
)

first_stage = utils.Stage(
    dry_mass = 12518, # dry_mass=14553,  # kg
    fuel_mass=40800,  # kg
    lox_mass=142900,  # kg
    thrust=3110000,  # N
    isp_avg=345,  # s
    payload=second_stage
)

# A 0 payload lunar landing with 6,100 m/s of dV is possible with 5577 kg upper stage

# 7577 kg 2nd stage and 12518 kg 1st stage is the optimized result for 3000 kg payload to LEO with full reusability, ~5000 kg partial, ~6000 kg full

# My original values of 5543 kg and 14553 kg give ~5000 kg fully reusable. Hopefully! But not what they've said, 3t full.

# "Direct access to GTO, TLI, and other high-energy orbits" yea what's this on their website? Suggests far lower dry mass.

"""
3,000 kg to LEO (100% reusable)
7,000 kg to LEO (max payload)
2,500 kg to GTO
1,250 kg to TLI
800 kg to C3 = 0
ALRIGHT I CAN DO SOMETHING WITH THIS!!! Gonna be some slightly annoying optimization but that's something! I need a new optimization script
"""

def optimize_stage_dry_masses(target_payload_mass, s1, s2, reuse_fraction="expendable", target_dv=9000, allowable_dv_variance=1, verbose=False, print_result=False):
    # Adjust stage masses until we have a good fit for the payload numbers at varying reuse fractions
    # Assume a 200 km reference LEO orbit requireing 9000 m/s delta-v to reach
    # Reuse fraction can be expendable, partially_reusable, or fully_reusable

    s2.payload = target_payload_mass
    
    # Binary search for best mass fit (Subtracting or adding mass from s1 to s2)
    search_range = 5000
    high = s1.dry_mass + search_range # kg
    low = s1.dry_mass - search_range # kg
    
    stack_dv = 0 # m/s
    s1_dv = 0 # m/s
    s2_dv = 0 # m/s
    
    initial_s1_dry_mass = s1.dry_mass
    initial_s2_dry_mass = s2.dry_mass
    
    iterations = 0
    
    # If we get no iterations, I still want these values defined for the output
    stack_dv, s1_dv, s2_dv = utils.get_stack_dv(s1, s2, reuse_fraction, verbose=verbose)
    
    while abs(stack_dv - target_dv) > allowable_dv_variance and iterations < 100:
        mid = (high + low) / 2
        
        s1.dry_mass = mid
        s2.dry_mass = initial_s2_dry_mass + (initial_s1_dry_mass - s1.dry_mass)

        stack_dv, s1_dv, s2_dv = utils.get_stack_dv(s1, s2, reuse_fraction, verbose=verbose)

        if verbose:
            print(f"Iteration {iterations}: s1 dry mass: {s1.dry_mass:.2f} kg, s2 dry mass: {s2.dry_mass:.2f} kg, stack delta-v: {stack_dv:.2f} m/s, s1 dV: {s1_dv:.2f} m/s, s2 dV: {s2_dv:.2f} m/s")

        if stack_dv < target_dv:
            low = mid
        else:
            high = mid
            
        iterations += 1

    if print_result:
        print(f"Final iteration {iterations}: s1 dry mass: {s1.dry_mass:.2f} kg, s2 dry mass: {s2.dry_mass:.2f} kg, stack delta-v: {stack_dv:.2f} m/s, s1 dV: {s1_dv:.2f} m/s, s2 dV: {s2_dv:.2f} m/s ({reuse_fraction})")

    return s1.dry_mass, s2.dry_mass, stack_dv, iterations

def get_stack_payload_capacity_to_dv(s1, s2, target_dv=9000, allowance_payload_variance=1, reuse_fraction="expendable", verbose=False, print_result=False):
    # Binary search to find maximum payload capacity for a given delta-v target
    low = 0  # kg
    high = 20000  # kg
    best_payload = 0
    iterations = 0
    
    while high - low > allowance_payload_variance and iterations < 100:
        mid = (high + low) / 2
        s2.payload = mid
        
        stack_dv, s1_dv, s2_dv = utils.get_stack_dv(s1, s2, reuse_fraction, verbose=verbose)
        
        if verbose:
            print(f"Iteration {iterations}: Testing payload {mid} kg, stack delta-v: {stack_dv:.2f} m/s")
        
        if stack_dv >= target_dv:
            low = mid
            best_payload = mid
        else:
            high = mid
            
        iterations += 1
    
    if print_result:
        print(f"Final iteration {iterations}: Maximum payload capacity: {best_payload:.1f} kg for {stack_dv:.1f} m/s delta-v ({reuse_fraction})")
    
    return best_payload, stack_dv, iterations

def print_stack_payload_capacity_vs_reuse_fraction(s1, s2):
    for reuse_fraction in ["expendable", "partially_reusable", "fully_reusable"]:
        payload_capacity, stack_dv, iterations = get_stack_payload_capacity_to_dv(s1, s2, target_dv=9000, allowance_payload_variance=1, reuse_fraction=reuse_fraction, verbose=False, print_result=False)
        print(f"{reuse_fraction}: {payload_capacity:.1f} kg, ", end="")
    print("")

print_result = True

show_unoptimized = True # Unoptimized meaning we're using the raw dry mass values I entered
show_optimized = True

if show_unoptimized == True:
    optimize_stage_dry_masses(target_payload_mass=second_stage.payload_mass(), s1=first_stage, s2=second_stage, reuse_fraction="expendable", target_dv=9000, allowable_dv_variance=9000, verbose=False, print_result=print_result)
    print("Unoptimized Results: ", end="")
    print_stack_payload_capacity_vs_reuse_fraction(first_stage, second_stage)
    print("")
    
if show_optimized == True:
    optimize_stage_dry_masses(target_payload_mass=7000, s1=first_stage, s2=second_stage, reuse_fraction="expendable", target_dv=9000, allowable_dv_variance=1, verbose=False, print_result=print_result)
    print("Expendable optimized: ", end="")
    print_stack_payload_capacity_vs_reuse_fraction(first_stage, second_stage)
    print("")

    optimize_stage_dry_masses(target_payload_mass=5000, s1=first_stage, s2=second_stage, reuse_fraction="partially_reusable", target_dv=9000, allowable_dv_variance=1, verbose=False, print_result=print_result)
    print("Partial Reuse optimized: ", end="")
    print_stack_payload_capacity_vs_reuse_fraction(first_stage, second_stage)
    print("")

    optimize_stage_dry_masses(target_payload_mass=3000, s1=first_stage, s2=second_stage, reuse_fraction="fully_reusable", target_dv=9000, allowable_dv_variance=1, verbose=False, print_result=print_result)
    print("Full Reuse optimized: ", end="")
    print_stack_payload_capacity_vs_reuse_fraction(first_stage, second_stage)
    print("")

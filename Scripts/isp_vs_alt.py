import math

# ISP = F / (m_dot * g0)
# where F is thrust, m_dot is mass flow rate, and g0 is standard gravity

# m_dot = F / (g0 * ISP)
# Where m_dot is mass flow rate in kg/s, F is thrust in N, g0 is standard gravity (9.80665 m/s^2), and ISP is specific impulse in seconds
# Note that this equation only applied in vacuum and I'm ignoring that

# Thrust = m_dot * v_e + (P_exit - P_atm) * A_exit
# thrust = m_dot * g * ISP + (P_exit - P_atm) * A_exit
# where P_exit is exit pressure, P_atm is atmospheric pressure at a given altitude, and A_exit is exit area, v_e is effective exhaust velocity

# https://grok.com/chat/6bd8c560-96cb-4048-b4cf-97d192c558ab

# For the Zenith stage 1 engine, assume the same performance as Raptor, maybe a couple seconds less ISP
# Raptor SL ISP is 327 s

# https://www.flickr.com/photos/stokespace/54120238412/
# Eyeballing from this photo, exit diameter is 227 px and that guy is 609 px tall
# Assuming he is 5'9" (average US height) (1.75 m)
# 227/609 * 1.75 = 0.65 m
# Exit area = pi * (d/2)^2
# A_exit = pi * (0.65/2)^2 = 0.33 m^2

G = 9.80665  # Acceleration due to gravity in m/s^2

thrust = 444300 # N
ISP_Sl = 327 # s SL
P_exit = 101325 # Pa perfect expansion at sea level, varying this by 1 kPa changes m_dot by 0.2 kg/s
P_atm = 101325 # Pa
A_exit = 0.33 # m^2  Estimated from photo

# The engine is slightly overexpanded at sea level, but I'm fine with being slightly off
# https://www.flickr.com/photos/stokespace/54213704909/

# The correct approach:
# For a rocket engine, mass flow rate is constant, but thrust changes with altitude
# thrust = m_dot * g * ISP + (P_exit - P_atm) * A_exit

# First, we need to find the mass flow rate using known values
# We know: thrust_sl, ISP_sl, P_exit, P_atm_sl, A_exit
# Rearranging: m_dot = (thrust_sl - (P_exit - P_atm_sl) * A_exit) / (g * ISP_sl)

def calculate_mass_flow_rate(thrust_sl, isp_sl, p_exit, p_atm_sl, a_exit):
    """Calculate the actual mass flow rate of the engine"""
    return (thrust_sl - (p_exit - p_atm_sl) * a_exit) / (G * isp_sl)

# Calculate the actual mass flow rate
m_dot_actual = calculate_mass_flow_rate(thrust, ISP_Sl, P_exit, P_atm, A_exit)
print(f"Actual mass flow rate: {m_dot_actual:.1f} kg/s")

# Now we can calculate performance at any altitude
def calculate_thrust_at_altitude(m_dot, isp, p_exit, p_atm_alt, a_exit):
    """Calculate thrust at any altitude given atmospheric pressure"""
    return m_dot * G * isp + (p_exit - p_atm_alt) * a_exit

def calculate_isp_at_altitude(thrust_alt, m_dot, p_exit, p_atm_alt, a_exit):
    """Calculate ISP at any altitude"""
    return (thrust_alt - (p_exit - p_atm_alt) * a_exit) / (m_dot * G)

# Example: Calculate vacuum performance
thrust_vac = calculate_thrust_at_altitude(m_dot_actual, ISP_Sl, P_exit, 0, A_exit)
isp_vac = calculate_isp_at_altitude(thrust_vac, m_dot_actual, P_exit, 0, A_exit)

print(f"Vacuum thrust: {thrust_vac:.0f} N")
print(f"Vacuum ISP: {isp_vac:.1f} s")

# This is retarded, start over
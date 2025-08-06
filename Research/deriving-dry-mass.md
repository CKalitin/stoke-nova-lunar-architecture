
# Deriving Dry Mass

### Centaur Dry Mass

Centaur D-1T on the Viking 1 mission launched August 20 1975.
https://grok.com/chat/0f4cd01b-efbe-4133-b38a-fd2126ab4f95

Fun source on satellite dry mass by subsystem:
https://www.researchgate.net/figure/ehicle-dry-mass-breakout-by-subsystem_fig1_267862769

Dry Mass: 2,130 kg (differing from wikipedia value or 1,827 kg)

RL-10(A?) Mass: 140 kg per engine
Engine mass total: 280 kg

Total Tank Surface Area (including hemispherical ends): 88 m²
Total Tank Mass (8 g/cm³ & 0.51 mm thickness): 359.04 kg

### Tank Walls

Assume 3mm thick 3XX stainless steel for tank walls.

Assuming Stainless Steel 304, density is ~7.93 g/cm³ or 7930 kg/m³.
Stainless density varies from 7.5 to 8.0, so error bars can be 0.5 g/cm³, and thickness uncertainty. Or, better idea, do this later in the process.

S1:  
Sidewalls Surface Area: 27.1 m * 3.7 m * π = 315.01 m²
Hemispherical Ends Surface Area: 2 * 2 * π * (3.7 m / 2)² = 43.009 m²
Total S1 Surface Area: 315.01 m² + 43.008 m² = 358.02 m²
S1 Wall Volume: 358.02 m² * 0.003 m = 1.074 m³
S1 Dry Mass: 1.074 m³ * 7930 kg/m³ = 8,520 kg

S2:
Sidewalls Surface Area (Overestimate): Sqrt(4.3^2 + 12.8^2) * 4.3 m * π = 182.41 m²
Hemispherical Ends Surface Area: 2 * 2 * π * (4.3 m / 2)² = 58.088 m²
Total S2 Surface Area: 182.41 m² + 58.088 m² = 240.50 m²
S2 Wall Volume: 240.50 m² * 0.003 m = 0.7215 m³
S2 Dry Mass: 0.7215 m³ * 7930 kg/m³ = 5,720 kg

Or, with 2mm thick walls:
S2 Wall Volume: 240.50 m² * 0.002 m = 0.481 m³
S2 Dry Mass: 0.481 m³ * 7930 kg/m³ = 3,810 kg
Savings of 1,910 kg.

### Engines

First stage TWRs:
- Raptor 1: 89
- Raptor 2: 141
- Raptor 3: 184
- Merlin 1C: 68
- Merlin 1D: 183
- Viking 5C: 99
- LE-7: 64

Assume 100:1 TWR for Zenith first stage engines. Better than Raptor 1, but worse than Raptor 2 and Merlin 1D. I imagine this will increase in the future.

Zenith mass: 453 kg

Hydrolox upper stage engines:
- RL-10C: 50
- J-2: 73

Hydrolox aerospikes:
- J-2T: 63
- XRS-2200: 35
- RS-2200: 83 (never built)

Assume 60:1 TWR for Andromeda upper stage engine. Not including heat shield.

Andromeda mass: 188 kg

First stage engine mass: 453 kg * 7 = 3,171 kg

Raptor SL ISP: 327 s

Hydrolox aerospike ISPs:
- J-2T: 441 s
- XRS-2200: 436 s
- RS-2200: 455 s (never built)

### Heatshield

Shuttle:
https://en.wikipedia.org/wiki/Space_Shuttle_thermal_protection_system

Space shuttle tiles were 140 kg/m^3
The carbon-carbon was 1986 kg/m^3

Weight breakdown:
Felt: 532 kg
Low-temp tiles: 1,010 kg
High-temp tiles: 4,410 kg
Carbon-carbon: 1,700 kg
Misc: 918 kg
Total: 8,570 kg

Apollo:
https://www.encyclopedia.com/science/news-wires-white-papers-and-books/heat-shields
Thickness: 7 cm
Diameter: 3.9 m
Mass: 1,360 kg

Andromeda (Assume 1cm steel):
Diameter: 4.3 m
Thickness: 0.01 m
Area of flat surface: π * (4.3 m / 2)² = 14.53 m²
Volume: 14.53 m² * 0.01 m = 0.1453 m³
Mass: 0.1453 m³ * 7930 kg/m³ = 1,150 kg

Note that this is less massive than the Apollo heat shield, while being bigger and metal. Maybe not right.

### S1 Thrust Structure

Saturn 5 S1C:
https://en.wikipedia.org/wiki/S-IC
Thrust Structure Mass: 22,000 kg
Total Dry Mass: 137,000 kg
Thrust Structure Ratio: 16.1%
Thrust: 34,000 kN (3,470,000 kg)

Ariane 5 Stage 1:
https://airbusdefenceandspacenetherlands.nl/slide/ariane-5
https://en.wikipedia.org/wiki/Ariane_5
Engine Thrust Frame: 2,000 kg
Total Dry Mass: 12,200 kg
Thrust Structure Ratio: 16.4%
Thrust: 960 kN (98,000 kg) (SL)

Go with 16% thrust structure ratio for S1.
This includes engine shielding. The stage is going to be heavier than an expendable one, but will also require more hardware because of reuse.

### Other mass

Assume 1 extra tonne for avionics, plumbing, RCS, and other systems for S2. Everything else goes to S1.

### Final Dry Mass

S2 (3mm thick tanks):
Tank Walls: 5,720 kg
Engine: 188 kg
Heatshield: 1,150 kg
Other: 1,000 kg
Total: 8,045 kg

S2 (2mm thick tanks):
Tank Walls: 3,810 kg
Engine: 188 kg
Heatshield: 1,150 kg
Other: 1,000 kg
Total: 6,148 kg

S1 Dry Mass: 25,096 kg - 8,045 kg = 17,051 kg

S1:
Tank Walls: 8,520 kg
Engines: 3,171 kg
Thrust Structure: 17,051 kg * 0.16 = 2,728 kg
Other: 17,051 kg - 8,520 kg - 3,171 kg - 2,728 kg = 2,632 kg
Total: 17,051 kg

S1 Dry Mass: 17,050 kg
S2 Dry Mass: 8,045 kg

S1/Total Dry Mass Ratio: 17,051 kg / (17,051 kg + 8,045 kg) = 0.68
S2/Total Dry Mass Ratio: 8,045 kg / (17,051 kg + 8,045 kg) = 0.32

Now, to simulate and back fit the data to try to come to the real payload mass conclusions.

### Starship Dry Mass

https://en.wikipedia.org/wiki/SpaceX_Starship

Ship V1: 100t?
Booster V1: 275t?

Ship V1 Dry Mass Ratio = 100t / (100t + 275t) = 0.27
Booster V1 Dry Mass Ratio = 275t / (100t + 275t) = 0.73

### Falcon 9 (FT) Dry Mass

https://en.wikipedia.org/wiki/Falcon_9_Full_Thrust#Rocket_specifications

S1 Dry Mass: 22,200 kg
S2 Dry Mass: 4,000 kg
Fairing Dry Mass: 1,700 kg
Net Mass: 27,900 kgd

S1 Dry Mass Ratio: 22,200 kg / 27,900 kg = 0.80
S2 Dry Mass Ratio: 4,000 kg / 27,900 kg = 0.14
Fairing Dry Mass Ratio: 1,700 kg / 27,900 kg = 0.06
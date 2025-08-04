# Draft Environment Assessment Vehicle Stats

### Full vehicle:
Height: 40.2 m (132 ft)  
Gross liftoff weight: 226,796 kg (500,000 lb)  

Net LOX Mass: 158,150 kg
Net Fuel Mass: 43,550 kg
Net Propellant Mass: 201,700 kg
Dry Mass: 25,096 kg

### Stage 1:
Height: 27.1 m (89 ft)  
Diameter: 3.7 m (12 ft)  

LOX Mass: 142,900 kg (315,000 lb)  
LNG Mass: 40,800 kg (90,000 lb)  
Net Mass: 183,700 kg (405,000 lb)

Thrust (Sea level): 3,110 kN (317,000 kg)
Thrust (SVL, per engine): 444.3 kN (45,300 kg)

TWR (Sea level): 1.40

### Stage 2:
(including payload fairing)  
Height: 12.8 m (43 ft)  
Diameter: 4.3 m (14 ft)  

LOX Mass: 15,250 kg (33,600 lb)  
LH2 Mass: 2,750 kg (6,060 lb)  
Net Mass: 18,000 kg (39,660 lb)

Thrust (Vacuum): 111 kN (11300 kg)

# EmlynSpace pixel counting Stats:
https://x.com/EmlynSpace/status/1864048440759435767

Assuming diameters are the same.

Full Height: ~40.2 m  
S1 Height: ~29.7 m  
S2 Height: ~10.5 m  

S1:S2 proportion changed, but mostly the same.  
Depending on how different dry mass is between both cases, I can decide if the render or environment assessment is what I should go with.  
Either way, my error bars will have to be substantial, and propagated. Monte Carlo mini.

# Deriving Dry Mass

### Centaur Dry Mass

Centaur D-1T on the Viking 1 mission launched August 20 1975.
https://grok.com/chat/0f4cd01b-efbe-4133-b38a-fd2126ab4f95

Fun source on satellite dry mass by subsystem:
https://www.researchgate.net/figure/ehicle-dry-mass-breakout-by-subsystem_fig1_267862769

Dry Mass: 2,130 kg (differing from wikipedia value or 1,827 kg)

RL-10 Mass: 140 kg per engine
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

Hydrolox upper stage engines:
- RL-10C: 50
- J-2: 73

Hydrolox aerospikes:
- J-2T: 63
- XRS-2200: 35
- RS-2200: 83 (never built)

Assume 65:1 TWR for Andromeda upper stage engine. Not including heat shield.

Zenith mass: 453 kg
Andromeda mass: 175 kg

First stage engine mass: 453 kg * 7 = 3,171 kg


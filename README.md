# Milky Way and Andromeda Galaxy Collision Simulation
**Science Project: The Development of a Mathematical Model to Study the Dynamics and Orbital Trajectories in the Milky Way and Andromeda Galaxy Collision**
**Wirithpol Kanjana-alongkorn**
**Photiphat Rattanarangsiwat**
**Advisor: Mr. Tawatchai Suklom**
**Institution: Suankularb Wittayalai School**

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Numba](https://img.shields.io/badge/Optimized_with-Numba-orange.svg)
![Blender](https://img.shields.io/badge/Rendered_in-Blender-darkorange.svg)

## About The Project
This project focuses on developing an N-body dynamical simulation to study the collision and merger of the Milky Way and Andromeda galaxies. The simulation processes a system of 5,801 particles under limited computational resources. The model's results were validated using the principles of energy conservation and Keplerian orbital trajectories.

## Key Features and Methodology
*   **Physics Engine:** Implemented Leapfrog integration to maintain energy stability over long-term simulations.
*   **Gravitational Softening:** Applied gravitational softening techniques to prevent infinite gravitational forces during close particle encounters.
*   **Parallel Computing:** Accelerated CPU processing performance using parallel computing via the `Numba` (JIT Compiler) library.
*   **3D Visualization:** Exported coordinate data to render realistic 3D animations using `Blender 4.4`.

## Results and Visualization
*(Insert graphics or GIFs here by replacing the placeholder links)*

### 1. Morphological Evolution
![Galaxy Collision Render](media/your_blender_render.gif)
*The core merger and the formation of tidal tails.*

### 2. Energy Drift Evaluation
![Energy Drift Plot](media/energy_drift_plot.png)
*The total energy drift throughout the simulation was 6.12%, which is within an acceptable threshold.*

## How to Run
1. Clone this repository:
   ```bash
   git clone [https://github.com/tarhongkrub/PY5.git](https://github.com/tarhongkrub/PY5.git)

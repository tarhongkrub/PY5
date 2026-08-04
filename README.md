# Milky Way and Andromeda Galaxy Collision Simulation
**Science Project: The Development of a Mathematical Model to Study the Dynamics and Orbital Trajectories in the Milky Way and Andromeda Galaxy Collision**

**Authors:** Photiphat Rattanarangsiwat, Wirithpol Kanjana-alongkorn  
**Advisor:** Mr. Tawatchai Suklom  
**Institution:** Suankularb Wittayalai School (Gifted Science Program)[cite: 1, 2]

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Numba](https://img.shields.io/badge/Optimized_with-Numba-orange.svg)
![Blender](https://img.shields.io/badge/Rendered_in-Blender-darkorange.svg)

---

## About The Project
This project focuses on developing an N-body dynamical simulation to study the collision and merger of the Milky Way and Andromeda galaxies[cite: 1, 2]. Based on observational data from the Hubble Space Telescope and Gaia satellite, these two massive galaxies are approaching each other and are predicted to merge in the future[cite: 1, 2]. Because this cosmic event spans billions of years, computer simulations using numerical methods are indispensable[cite: 1]. The model successfully processes a system of **5,801 mass particles** under limited computational resources while maintaining high physical realism[cite: 1, 2].

---

## Key Features and Methodology
* **Physics Engine & Leapfrog Integration:** Implemented a symplectic Leapfrog integration method for its time-reversibility, ensuring long-term energy conservation and stability[cite: 1].
* **Gravitational Softening:** Applied a softening parameter ($\epsilon$) into the force calculation to prevent infinite gravitational forces (singularities) during close particle encounters[cite: 1].
* **Parallel Computing:** Accelerated CPU processing performance to match C-compiled languages using Just-In-Time (JIT) compilation via the `Numba` library[cite: 1].
* **System Validation:** Rigorously cross-verified against fundamental conservation laws (total energy and angular momentum) and pre-collision Keplerian trajectories[cite: 1].
* **3D Visualization:** Exported 3D spatial coordinates and RGB color datasets to render realistic morphological evolutions using **Blender 4.4**[cite: 1, 2].

---

## Results and Visualization

[https://s6.ezgif.com/tmp/ezgif-6c00b8e823f82a56.gif]

### 1. Morphological Evolution
(https://s6.ezgif.com/tmp/ezgif-6c00b8e823f82a56.gif)  
*The simulation categorizes the morphological evolution into four distinct phases[cite: 1]:*
1. **Approach Phase:** Galaxies move toward each other following Keplerian trajectories[cite: 1].
2. **First Pericenter Passage:** Occurring at approximately 2.3 billion years, intense tidal forces strip material from the original structures, forming elongated tidal tails[cite: 1].
3. **Energy Dissipation Phase:** Rapid decrease in inter-galactic distance due to kinetic energy dissipation and linear momentum transfer[cite: 1].
4. **Complete Merger:** At approximately 5.5 billion years, the galactic cores coalesce into a single center, resulting in the formation of a newly established elliptical galaxy[cite: 1, 2].

### 2. Energy Drift & System Stability
![Energy Drift Plot]
(https://1drv.ms/i/c/1885e1794a1f1ed6/IQBsPr1PSYSrR63VZfKTfbH5ASmJs1sEP4chMAl08A0wGtE?e=Wz2ngI)  
* **Energy Conservation:** The calculated total energy drift throughout the simulation was **6.12%**, meaning the total energy deviates from the initial value by 6.12% due to limitations of numerical integration in high-density regions, which remains within an acceptable threshold[cite: 1].
* **Angular Momentum:** The total angular momentum of the solitary galaxy system remained constant over time, confirming that the system is free from external torques and verifying model stability[cite: 1].

### 3. Influence of Initial Conditions (Impact Angle)
The study established a direct relationship between the initial impact angle and the merger timescale[cite: 1, 2]:
* **Prograde Merger (Low Angle $<30^\circ$):** First pericenter at ~2.15 Gyr, complete merger at ~4.20 Gyr (Fast merger)[cite: 1, 2].
* **Polar Merger (High Angle $>30^\circ$):** First pericenter at ~2.25 Gyr, complete merger at ~6.85 Gyr (Delayed merger)[cite: 1, 2].
(https://1drv.ms/i/c/1885e1794a1f1ed6/IQDuieLdvWcjT6Zgo0OIVmkxARZXxJs19eRDXK_RrDIzeVY?e=oP4lio)
---

## 🚀 How to Run

1. **Clone this repository:**
   ```bash
   git clone [https://github.com/tarhongkrub/PY5.git](https://github.com/tarhongkrub/PY5.git)
   cd PY5

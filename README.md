# Milky Way and Andromeda Galaxy Collision Simulation
**Science Project: The Development of a Mathematical Model to Study the Dynamics and Orbital Trajectories in the Milky Way and Andromeda Galaxy Collision**

**Authors:** Photiphat Rattanarangsiwat, Wirithpol Kanjana-alongkorn  
**Advisor:** Mr. Tawatchai Suklom  
**Institution:** Suankularb Wittayalai School (Gifted Science Program)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Numba](https://img.shields.io/badge/Optimized_with-Numba-orange.svg)
![Blender](https://img.shields.io/badge/Rendered_in-Blender-darkorange.svg)

---

## About The Project
This project focuses on developing an N-body dynamical simulation to study the collision and merger of the Milky Way and Andromeda galaxies[cite: 1, 2]. Based on observational data from the Hubble Space Telescope and Gaia satellite, these two massive galaxies are approaching each other and are predicted to merge in the future. Because this cosmic event spans billions of years, computer simulations using numerical methods are indispensable. The model successfully processes a system of **5,801 mass particles** under limited computational resources while maintaining high physical realism].

---

## Key Features and Methodology
* **Physics Engine & Leapfrog Integration:** Implemented a symplectic Leapfrog integration method for its time-reversibility, ensuring long-term energy conservation and stability.
* **Gravitational Softening:** Applied a softening parameter ($\epsilon$) into the force calculation to prevent infinite gravitational forces (singularities) during close particle encounters.
* **Parallel Computing:** Accelerated CPU processing performance to match C-compiled languages using Just-In-Time (JIT) compilation via the `Numba` library.
* **System Validation:** Rigorously cross-verified against fundamental conservation laws (total energy and angular momentum) and pre-collision Keplerian trajectories.
* **3D Visualization:** Exported 3D spatial coordinates and RGB color datasets to render realistic morphological evolutions using **Blender 4.4**.
* **HUBBLE SPACE Telescope's** datasets applied for Andromeda galaxy physics properties 

---

## Results and Visualization

![Galaxy Collision Render](media/<img width="800" height="213" alt="ezgif com-video-to-gif-converter (2)" src="https://github.com/user-attachments/assets/577f178e-ae5e-4935-a0b4-dbca610964b7" />
)

### 1. Morphological Evolution
(https://s6.ezgif.com/tmp/ezgif-6c00b8e823f82a56.gif)  
*The simulation categorizes the morphological evolution into four distinct phases*
1. **Approach Phase:** Galaxies move toward each other following Keplerian trajectories.
2. **First Pericenter Passage:** Occurring at approximately 2.3 billion years, intense tidal forces strip material from the original structures, forming elongated tidal tails.
3. **Energy Dissipation Phase:** Rapid decrease in inter-galactic distance due to kinetic energy dissipation and linear momentum transfer.
4. **Complete Merger:** At approximately 5.5 billion years, the galactic cores coalesce into a single center, resulting in the formation of a newly established elliptical galaxy.

### 2. Energy Drift & System Stability
![Energy Drift Plot](media/https://1drv.ms/i/c/1885e1794a1f1ed6/IQBnkWUiNqEiR5Ck5FZS9B_EAQUIil7REwP8qHa9_jqzIJQ?e=5QXkAd)
* **Energy Conservation:** The calculated total energy drift throughout the simulation was **6.12%**, meaning the total energy deviates from the initial value by 6.12% due to limitations of numerical integration in high-density regions, which remains within an acceptable threshold.
* **Angular Momentum:** The total angular momentum of the solitary galaxy system remained constant over time, confirming that the system is free from external torques and verifying model stability.

### 3. Influence of Initial Conditions (Impact Angle)
The study established a direct relationship between the initial impact angle and the merger timescale:
* **Prograde Merger (Low Angle $<30^\circ$):** First pericenter at ~2.15 Gyr, complete merger at ~4.20 Gyr (Fast merger).
* **Polar Merger (High Angle $>30^\circ$):** First pericenter at ~2.25 Gyr, complete merger at ~6.85 Gyr (Delayed merger).
(https://1drv.ms/i/c/1885e1794a1f1ed6/IQDuieLdvWcjT6Zgo0OIVmkxARZXxJs19eRDXK_RrDIzeVY?e=oP4lio)
---

## 🚀 How to Run

1. **Clone this repository:**
   ```bash
   git clone [https://github.com/tarhongkrub/PY5.git](https://github.com/tarhongkrub/PY5.git)
   cd PY5

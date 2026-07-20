import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit, prange
from scipy.spatial.transform import Rotation

# --- 1. ตั้งค่ามาตรวัดดาราศาสตร์ (Astronomical Settings) ---
# สมมติ: 1 Unit ใน Simulation = 2 kpc
UNIT_LENGTH_KPC = 2.0
# สมมติ: 1 Time Step = ~10 ล้านปี (Myr) โดยประมาณ

N_disk = 2400  # ดาวในจาน
N_bulge = 500  # ดาวในใจกลาง
G = 1.0
dt = 0.01
steps = 800
epsilon = 0.2  # Softening


# --- 2. Physics Engine (Numba High Performance) ---
@njit(parallel=True, fastmath=True)
def compute_accel_numba(pos, mass, G, eps_sq):
    N = pos.shape[0]
    acc = np.zeros((N, 3), dtype=np.float64)
    for i in prange(N):
        for j in range(N):
            if i == j: continue
            dx = pos[j, 0] - pos[i, 0]
            dy = pos[j, 1] - pos[i, 1]
            dz = pos[j, 2] - pos[i, 2]

            dist_sq = dx * dx + dy * dy + dz * dz + eps_sq
            inv_dist = 1.0 / np.sqrt(dist_sq)
            inv_dist3 = inv_dist * inv_dist * inv_dist

            f = G * mass[j] * inv_dist3
            acc[i, 0] += f * dx
            acc[i, 1] += f * dy
            acc[i, 2] += f * dz
    return acc


# --- 3. ฟังก์ชันสร้างกาแล็กซี (Scaleable) ---
def create_galaxy(N_d, N_b, offset, velocity, tilt_deg, color_theme, size_scale=1.0):
    # ปรับขนาดตาม scale (Andromeda ใหญ่กว่า Milky Way)
    disk_scale = 3.0 * size_scale

    # 1. Disk
    r_d = np.random.exponential(scale=disk_scale, size=N_d)
    theta_d = np.random.uniform(0, 2 * np.pi, N_d)
    z_d = np.random.normal(0, 0.2 * size_scale, N_d)
    x_d, y_d = r_d * np.cos(theta_d), r_d * np.sin(theta_d)

    # Velocity (Rotation Curve)
    M_enc = (1 - np.exp(-r_d / disk_scale)) * N_d + (r_d / (r_d + 1.0)) * N_b
    v_circ = np.sqrt(G * M_enc / (r_d + 0.1))
    vx_d, vy_d = -v_circ * np.sin(theta_d), v_circ * np.cos(theta_d)
    vz_d = np.zeros(N_d)

    # 2. Bulge
    a = 1.0 * size_scale
    x_rnd = np.random.rand(N_b)
    r_b = a * np.sqrt(x_rnd) / (1 - np.sqrt(x_rnd))
    theta_b = np.arccos(2 * np.random.rand(N_b) - 1)
    phi_b = np.random.uniform(0, 2 * np.pi, N_b)
    x_b = r_b * np.sin(theta_b) * np.cos(phi_b)
    y_b = r_b * np.sin(theta_b) * np.sin(phi_b)
    z_b = r_b * np.cos(theta_b)

    v_disp = np.sqrt(G * N_b / (2 * a))
    vx_b, vy_b, vz_b = np.random.normal(0, v_disp, (3, N_b))

    # Combine
    pos = np.vstack([np.column_stack([x_d, y_d, z_d]), np.column_stack([x_b, y_b, z_b])])
    vel = np.vstack([np.column_stack([vx_d, vy_d, vz_d]), np.column_stack([vx_b, vy_b, vz_b])])

    # Rotate & Move
    if tilt_deg != 0:
        r = Rotation.from_euler('x', tilt_deg, degrees=True)
        pos = r.apply(pos)
        vel = r.apply(vel)

    pos += np.array(offset)
    vel += np.array(velocity)

    # Mass (Bulge หนักกว่า Disk หน่อย)
    mass = np.concatenate([np.ones(N_d), np.full(N_b, 1.5)]) * size_scale  # Galaxy ใหญ่มวลเยอะกว่า

    # Colors & Sizes
    colors = np.zeros((N_d + N_b, 4))
    sizes = np.zeros(N_d + N_b)

    if color_theme == 'MW':  # Milky Way (Blue/Cyan)
        colors[:N_d] = [0.0, 0.7, 1.0, 0.3]
        sizes[:N_d] = 0.5
        colors[N_d:] = [1.0, 1.0, 0.9, 0.8]
        sizes[N_d:] = 2.0
    else:  # Andromeda (Red/Magenta)
        colors[:N_d] = [1.0, 0.2, 0.4, 0.3]
        sizes[:N_d] = 0.5
        colors[N_d:] = [1.0, 0.9, 0.8, 0.8]
        sizes[N_d:] = 2.0

    return pos, vel, mass, colors, sizes


# --- 4. สร้างกาแล็กซี ---
print("Simulating Milky Way (Blue) vs Andromeda (Red)...")

# Milky Way: เล็กกว่า, มุมเอียงน้อย
p1, v1, m1, c1, s1 = create_galaxy(N_disk, N_bulge, offset=[-20, 5, 0], velocity=[0.5, -0.2, 0],
                                   tilt_deg=-30, color_theme='MW', size_scale=1.0)

# Andromeda: ใหญ่กว่า (1.3 เท่า), มุมเอียงเยอะ
p2, v2, m2, c2, s2 = create_galaxy(N_disk, N_bulge, offset=[20, -5, 0], velocity=[-0.5, 0.2, 0],
                                   tilt_deg=70, color_theme='M31', size_scale=1.3)

# รวมข้อมูล
pos = np.vstack([p1, p2]).astype(np.float64)
vel = np.vstack([v1, v2]).astype(np.float64)
mass = np.concatenate([m1, m2]).astype(np.float64)
colors = np.vstack([c1, c2])
sizes = np.concatenate([s1, s2])
acc = np.zeros_like(pos)
eps_sq = epsilon ** 2

# Compile Numba
compute_accel_numba(pos[:10], mass[:10], G, eps_sq)

# --- 5. Visualization 3 Views ---
# สร้าง 3 กราฟเรียงกัน (XY, XZ, YZ)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), facecolor='black')

axes = [ax1, ax2, ax3]
planes = [(0, 1), (0, 2), (1, 2)]  # (x,y), (x,z), (y,z)
titles = ['Top View (XY Plane)', 'Side View (XZ Plane)', 'Front View (YZ Plane)']
x_labels = ['x (kpc)', 'x (kpc)', 'y (kpc)']
y_labels = ['y (kpc)', 'z (kpc)', 'z (kpc)']

scatters = []
limit_kpc = 50 * UNIT_LENGTH_KPC  # ขอบเขตการมองเห็นประมาณ 100 kpc

for i, ax in enumerate(axes):
    ax.set_facecolor('black')
    ax.set_aspect('equal')
    # ตั้งค่าแกนเป็นหน่วย kpc
    ax.set_xlim(-limit_kpc, limit_kpc)
    ax.set_ylim(-limit_kpc, limit_kpc)
    ax.set_xlabel(x_labels[i], color='gray')
    ax.set_ylabel(y_labels[i], color='gray')
    ax.set_title(titles[i], color='white', fontsize=10)
    ax.tick_params(axis='both', colors='gray', labelsize=8)
    ax.grid(color='gray', linestyle='--', linewidth=0.3, alpha=0.3)

    # แปลงพิกัดเริ่มต้นเป็น kpc เพื่อพล็อต
    idx_x, idx_y = planes[i]
    sc = ax.scatter(pos[:, idx_x] * UNIT_LENGTH_KPC,
                    pos[:, idx_y] * UNIT_LENGTH_KPC,
                    c=colors, s=sizes)
    scatters.append(sc)

# Text บอกเวลา
time_text = fig.text(0.5, 0.95, 'Time: 0 Myr', ha='center', color='white', fontsize=14)
fig.suptitle(f"Milky Way & Andromeda Collision Simulation", color='white', fontsize=16, y=0.98)


def update(frame):
    global pos, vel, acc

    # Physics Loop
    vel += acc * dt / 2.0
    pos += vel * dt
    acc = compute_accel_numba(pos, mass, G, eps_sq)
    vel += acc * dt / 2.0

    # Update Graphic (3 Views)
    for i, sc in enumerate(scatters):
        idx_x, idx_y = planes[i]
        # อัปเดตตำแหน่งโดยคูณหน่วย kpc
        data = np.column_stack((pos[:, idx_x] * UNIT_LENGTH_KPC,
                                pos[:, idx_y] * UNIT_LENGTH_KPC))
        sc.set_offsets(data)

    # สมมติ 1 frame ~ 5 Myr
    time_val = frame * 5
    time_text.set_text(f'Time: {time_val} Myr')

    return scatters + [time_text]


ani = FuncAnimation(fig, update, frames=steps, interval=20, blit=False)
plt.show()

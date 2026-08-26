import numpy as np
import os
import csv
from numba import njit, prange
from scipy.spatial.transform import Rotation

#1. ตั้งค่ามาตรวัดดาราศาสตร์ (Astronomical Settings) #adjustable
N_disk = 2400
N_bulge = 500
G = 1.0
dt = 0.01
steps = 800  # จำนวนเฟรมที่จะบันทึก
epsilon = 0.1


#2. Physics Engine (Numba High Performance)
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


# 3. ฟังก์ชันสร้างกาแล็กซี
def create_galaxy(N_d, N_b, offset, velocity, tilt_deg, color_theme, size_scale=1.0):
    disk_scale = 3.0 * size_scale

    r_d = np.random.exponential(scale=disk_scale, size=N_d)
    theta_d = np.random.uniform(0, 2 * np.pi, N_d)
    z_d = np.random.normal(0, 0.2 * size_scale, N_d)
    x_d, y_d = r_d * np.cos(theta_d), r_d * np.sin(theta_d)

    M_enc = (1 - np.exp(-r_d / disk_scale)) * N_d + (r_d / (r_d + 1.0)) * N_b
    v_circ = np.sqrt(G * M_enc / (r_d + 0.1))
    vx_d, vy_d = -v_circ * np.sin(theta_d), v_circ * np.cos(theta_d)
    vz_d = np.zeros(N_d)

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

    pos = np.vstack([np.column_stack([x_d, y_d, z_d]), np.column_stack([x_b, y_b, z_b])])
    vel = np.vstack([np.column_stack([vx_d, vy_d, vz_d]), np.column_stack([vx_b, vy_b, vz_b])])

    if tilt_deg != 0:
        r = Rotation.from_euler('x', tilt_deg, degrees=True)
        pos = r.apply(pos)
        vel = r.apply(vel)

    pos += np.array(offset)
    vel += np.array(velocity)

    mass = np.concatenate([np.ones(N_d), np.full(N_b, 1.5)]) * size_scale

    colors = np.zeros((N_d + N_b, 4))
    if color_theme == 'MW':
        colors[:N_d] = [0.0, 0.7, 1.0, 1.0]
        colors[N_d:] = [1.0, 1.0, 0.9, 1.0]
    else:
        colors[:N_d] = [1.0, 0.2, 0.4, 1.0]
        colors[N_d:] = [1.0, 0.9, 0.8, 1.0]

    return pos, vel, mass, colors



# 4. ตั้งค่าแบบจำลอง และ บันทึก CSV

print(" เริ่มกระบวนการจำลองข้อมูล...")

# ทางช้างเผือก (จานอ้างอิง เอียง 0 องศา วิ่งตรงไปแกน X)
p1, v1, m1, c1 = create_galaxy(N_disk, N_bulge, offset=[-20, 0, 0], velocity=[0.5, 0, 0],
                               tilt_deg=0, color_theme='MW', size_scale=1.0) #adjustable

# แอนดรอเมดา (เอียง 77 องศา, ความเร็วตามขวางสูง Vy = 0.75)
p2, v2, m2, c2 = create_galaxy(N_disk, N_bulge,
                               offset=[20, 0, 0],
                               velocity=[-0.5, 10.0, 0],
                               tilt_deg=77, color_theme='M31', size_scale=1.3) #adjustable

pos = np.vstack([p1, p2]).astype(np.float64)
vel = np.vstack([v1, v2]).astype(np.float64)
mass = np.concatenate([m1, m2]).astype(np.float64)
colors = np.vstack([c1, c2])

acc = np.zeros_like(pos)
eps_sq = epsilon ** 2

# Compile Numba ก่อนรันจริง
compute_accel_numba(pos[:10], mass[:10], G, eps_sq)

# สร้างโฟลเดอร์เก็บข้อมูล
output_dir = "galaxy_csv_GAIA"
os.makedirs(output_dir, exist_ok=True)

# Physics Loop & Export CSV
for i in range(steps):
    vel += acc * dt / 2.0
    pos += vel * dt
    acc = compute_accel_numba(pos, mass, G, eps_sq)
    vel += acc * dt / 2.0

    # เขียนไฟล์ CSV ทีละเฟรม
    filename = os.path.join(output_dir, f"frame_{i:04d}.csv")
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z", "r", "g", "b", "a"])
        for j in range(pos.shape[0]):
            writer.writerow([pos[j, 0], pos[j, 1], pos[j, 2], colors[j, 0], colors[j, 1], colors[j, 2], colors[j, 3]])

    # พิมพ์บอกสถานะทุกๆ 100 เฟรม
    if (i + 1) % 100 == 0:
        print(f"   > บันทึกแล้ว {i + 1}/{steps} เฟรม")

print(f"\n บันทึกข้อมูล GAIA ครบทั้ง {steps} เฟรมเรียบร้อยแล้ว")
print(f"สามารถนำโฟลเดอร์ '{output_dir}' ไปเปิดใน Blender")
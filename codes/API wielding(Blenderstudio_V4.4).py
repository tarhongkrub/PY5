import bpy
import csv
import os

# ==========================================
# [จุดที่ต้องแก้ไข] ใส่ที่อยู่โฟลเดอร์ CSV ของคุณตรงนี้ (เช่น โฟลเดอร์ HST)
# ตัวอย่าง: r"C:\Users\User\PycharmProjects\PythonProject14\galaxy_csv_GAIA"
csv_folder_path = r"C:\Users\user\OneDrive\Scipj\galaxy_csv_GAIA"
# ==========================================

obj_name = "GalaxySimulation"
mesh_name = "GalaxyMesh"

def setup_galaxy_object():
    # ตรวจสอบว่ามีไฟล์เฟรมแรกไหม (frame_0000.csv)
    first_file = os.path.join(csv_folder_path, "frame_0000.csv")
    if not os.path.exists(first_file):
        print(f"Error: Could not find {first_file}")
        return None

    # อ่านไฟล์แรกเพื่อนับจำนวนดาวและสร้างจุดเริ่มต้น
    verts = []
    colors = [] # เก็บค่าสี RGBA แบบ Array แบนราบ (Flat list)
    
    with open(first_file, 'r') as f:
        reader = csv.reader(f)
        next(reader) # ข้ามบรรทัด Header (x,y,z,r,g,b,a)
        for row in reader:
            # ดึงพิกัด
            verts.append((float(row[0]), float(row[1]), float(row[2])))
            # ดึงสี r, g, b, a (คอลัมน์ที่ 3, 4, 5, 6)
            colors.extend([float(row[3]), float(row[4]), float(row[5]), float(row[6])])

    # ตรวจสอบว่ามี Object ชื่อ GalaxySimulation อยู่แล้วหรือไม่
    if obj_name in bpy.data.objects:
        obj = bpy.data.objects[obj_name]
        mesh = obj.data
        mesh.clear_geometry() # ล้างแค่จุดข้างใน แต่เก็บโหนด Material/Geometry ไว้
    else:
        # ถ้าไม่มี ค่อยสร้างใหม่
        mesh = bpy.data.meshes.new(mesh_name)
        obj = bpy.data.objects.new(obj_name, mesh)
        bpy.context.collection.objects.link(obj)
    
    # สร้าง vertices เข้าไปใน Mesh
    mesh.from_pydata(verts, [], [])
    
    # ตรวจสอบและสร้าง Color Attribute ชื่อ "StarColors" ให้ตรงกับโหนดใน Shading
    if "StarColors" not in mesh.color_attributes:
        color_attr = mesh.color_attributes.new(name="StarColors", type='FLOAT_COLOR', domain='POINT')
    else:
        color_attr = mesh.color_attributes["StarColors"]
    
    # อัดข้อมูลสีลงไปรวดเดียว (เร็วกว่า For-loop)
    color_attr.data.foreach_set("color", colors)
    mesh.update()

    return obj

# ฟังก์ชันที่จะรันทุกครั้งที่เปลี่ยนเฟรมบน Timeline
def update_galaxy(scene):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return

    frame = scene.frame_current
    filename = f"frame_{frame:04d}.csv" 
    filepath = os.path.join(csv_folder_path, filename)

    if not os.path.exists(filepath):
        return # หมดเฟรมแล้ว หรือหาไฟล์ไม่เจอ

    new_coords = []
    new_colors = []
    
    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                # ดึงพิกัด (List แบนราบ)
                new_coords.extend([float(row[0]), float(row[1]), float(row[2])])
                # ดึงสี RGBA (List แบนราบ)
                new_colors.extend([float(row[3]), float(row[4]), float(row[5]), float(row[6])])

        # อัปเดตตำแหน่งจุดด้วย foreach_set (ทำให้เล่น Animation ได้ลื่นไหล)
        obj.data.vertices.foreach_set("co", new_coords)
        
        # อัปเดตสี (เผื่อมีการรวมดาราจักรแล้วสีผสมกัน)
        if "StarColors" in obj.data.color_attributes:
            color_layer = obj.data.color_attributes["StarColors"]
            color_layer.data.foreach_set("color", new_colors)
            
        obj.data.update() # บอกให้ Blender รีเฟรชภาพ
        
    except Exception as e:
        print(f"Error reading frame {frame}: {e}")

# --- ส่วนของการรันสคริปต์ ---

print("กำลังโหลดข้อมูลดาราจักร...")
obj = setup_galaxy_object()

if obj:
    # เคลียร์ Handler เก่าออก เพื่อไม่ให้มันทำงานซ้อนกันเวลาเรากดรันสคริปต์หลายรอบ
    bpy.app.handlers.frame_change_pre.clear()
    
    # ผูกฟังก์ชัน update_galaxy เข้ากับ Timeline
    bpy.app.handlers.frame_change_pre.append(update_galaxy)
    print(f"โหลดข้อมูลสำเร็จ กด Spacebar หรือ Play บน Timeline")

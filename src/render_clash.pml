reinitialize
bg_color white
set ray_shadows, 0
set antialias, 2

python
import os

cwd = os.getcwd()
candidates = [cwd, os.path.join(cwd, "src"), os.path.abspath(os.path.join(cwd, os.pardir))]
repo_root = cwd
for candidate in candidates:
    data_dir = os.path.join(candidate, "data")
    fig_dir = os.path.join(candidate, "figures")
    if os.path.isdir(data_dir) or os.path.isdir(fig_dir):
        repo_root = candidate
        break

data_dir = os.path.join(repo_root, "data")
fig_dir = os.path.join(repo_root, "figures")
os.makedirs(data_dir, exist_ok=True)
os.makedirs(fig_dir, exist_ok=True)
cmd.set("fetch_path", data_dir)
cmd.set("ray_opaque_background", 0)
python end

# Fetch structure if it is not already loaded.
if not cmd.get_names("all"):
    fetch 5UHC, type=cif
hide everything

# Style protein chain and binding pocket
show cartoon, chain C
color gray85, chain C

select rfp, resn RFP
show sticks, rfp
color salmon, rfp and elem C

# Select pocket residue 456
select pocket_res, chain C and resi 456
show sticks, pocket_res
color marine, pocket_res and elem C
label pocket_res, "SER456"

# Render steric clash vectors and overlapping van der Waals radii
distance clash_vectors, pocket_res, rfp, cutoff=2.8
set dash_color, red
set dash_width, 4
set dash_gap, 0.25

show spheres, pocket_res or rfp
set sphere_transparency, 0.40, pocket_res or rfp
show nb_spheres, pocket_res or rfp
set nb_sphere_radius, 0.9, pocket_res or rfp

# Center camera and export figure
zoom rfp or pocket_res, 7
ray 1600, 1200
python
import os
repo_root = os.getcwd()
for candidate in [repo_root, os.path.join(repo_root, "src"), os.path.abspath(os.path.join(repo_root, os.pardir))]:
    fig_dir = os.path.join(candidate, "figures")
    if os.path.isdir(fig_dir):
        cmd.png(os.path.join(fig_dir, "molecular_steric_clash.png"), dpi=300, quiet=1)
        break
python end

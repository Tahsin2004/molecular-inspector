reinitialize
bg_color white
set ray_shadows, 0
set antialias, 2

# Fetch structure
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

# Render steric clash vectors and overlapping van der Waals radii
distance clash_vectors, pocket_res, rfp, cutoff=2.8
set dash_color, red
set dash_width, 4

show spheres, pocket_res or rfp
set sphere_transparency, 0.40, pocket_res or rfp

# Center camera and export figure
zoom rfp or pocket_res, 7
ray 1600, 1200
png figures/molecular_steric_clash.png, dpi=300
quit

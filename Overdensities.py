# Import required packages 
import yt
import numpy as np
import matplotlib.pyplot as plt
import scipy 
import scipy.stats
from scipy.stats import norm
import glob 

z_arr = np.array([])
scale_arr = np.array([])
var_arr = np.array([])
mass = []

yt.enable_parallelism()

ss = np.array([101])

storage = {}
#read in random location text file 
locs = np.loadtxt('Data_new/random_locations_1600mpc_full.txt')

for stor_dict, num in yt.parallel_objects(ss, -1, storage=storage):
    units = {"length": (1.0, "Mpc/h")}
    
    if num < 10:
        file = '/disk12/legacy/GVD_C700_l1600n2048_SLEGAC/dm_gadget/data/snapdir_00' + str(num) + '/snapshot_00' + str(num) + '.0.hdf5'
    elif num < 100:
        file = '/disk12/legacy/GVD_C700_l1600n2048_SLEGAC/dm_gadget/data/snapdir_0' + str(num) + '/snapshot_0' + str(num) + '.0.hdf5'
    else:    
        file = '/disk12/legacy/GVD_C700_l1600n2048_SLEGAC/dm_gadget/data/snapdir_' + str(num) + '/snapshot_' + str(num) + '.0.hdf5'
    ds=yt.load(file, unit_base =units)
    ds.parameters["format revision"] =2
         
    #set radius of all density spheres 
    rad = 20


    # Find current redshift and scale factor
    z = ds.current_redshift

    a = 1 / (1 + z)
    region = ds.r[:,:,:]


    # Method to determine mean density of region 
    dust_mass, clump_mass = region.quantities.total_mass()
    box_size = ds.domain_width[0]
    rho_mean  = (clump_mass) / (box_size*a)**3
     
    
    # Give units to sphere radius to match 
    # domain width units 
    l_units = ds.length_unit

    r_un = rad  *  l_units

    radius = r_un.to("code_length")

    V = ((4*np.pi)/3) * (radius)**3
    masses = rho_mean * V
    mass.append(masses)


    # Overdensity storage
    delta_i = np.array([])
    rho_mean = clump_mass/(box_size*a)**3
    # Method to determine density of a given sphere
    for c in locs: 
        sphere = ds.sphere(c, radius)
        vol = ((4*np.pi)/3) * ((a * radius)**3)
        rho_sphere = (sphere.quantities.total_mass()[1]) / vol
        d = (rho_sphere - rho_mean) /rho_mean

        delta_i = np.append(delta_i, d)
    
    # Store delta array with redshift key in dictionary
    stor_dict.result = delta_i 
    
    #stor_dict.result_id = z
    

if yt.is_root():
    
        
    deltas = []

    z = []

    # get the data from storage

    for zs, dels in sorted(storage.items()):

        z.append(zs)

        deltas.append(dels)
    
        
    z_arr = np.array(z)

    delta_arr = np.array(deltas)

    mass = np.array(mass)


    # write the data
    
    with open(f"Data_new/Mass_Calcs/z_{rad}_mass.txt", 'w') as fo:
    
        for i in range(len(z)):
        
            fo.write(str(z[i]) + "\n")
    

    with open(f"Data_new/Mass_Calcs/delta_{rad}_mass.txt", 'w') as fo:

        for x in delta_arr:

            for y in x:

                fo.write(str(y) + " ")

            fo.write("\n")

    with open(f"Data_new/Mass_Calcs/masses_{rad}.txt", 'w') as fo: 

        for i in range(len(mass)):

   
            fo.write(str(mass[i]) + "\n")


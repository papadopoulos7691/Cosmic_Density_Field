import yt 
import numpy as np 
import yt.extensions.legacy 

file = "/disk12/legacy/GVD_C700_l1600n2048_SLEGAC/dm_gadget/halos_h5/hlist_0.333760.h5"
ds = yt.load(file)
ad = ds.all_data()
z = ds.current_redshift
print(z)
masses = ad['Mvir']
mass_arr = np.array(masses)

with open('Data_new/halo_masses_2.txt', 'w') as fo:

    for j in range(len(mass_arr)):

        fo.write(str(mass_arr[j]) + "\n")




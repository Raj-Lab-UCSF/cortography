import nibabel
import itertools
import numpy as np
import pandas as pd

from tqdm import tqdm
from scipy.io import savemat
from atlasreader import atlasreader
from nilearn._utils import check_niimg

#### Calculate voxel data:
Yeo_labels = open('../data/atlases/Yeo/Yeo2011_17Networks_MNI152.txt', 'r')
Yeo_labels = Yeo_labels.read().split('\n')
Yeo_labels.insert(0,"None") #I believe the areas were numbered 1-7 with "0" reserved for white matter

#### Read Yeo matrix:
Yeo_template = "../data/atlases/Yeo/Yeo2011_17Networks_MNI152.nii"
Yeo = nibabel.load(Yeo_template)
Yeo_data = Yeo.get_fdata()

#### Loop through MNI-152 template Yeo_data
DK_data =  atlasreader.get_atlas('desikan_killiany')['image'].get_data()
DK_atlas = atlasreader.get_atlas('desikan_killiany')

Yeo_affine = check_niimg(Yeo_template).affine
DK_affine = check_niimg(atlasreader.get_atlas('desikan_killiany')['image']).affine

#### compute the DK voxel based distribution of networks per region:
DK_dict_voxels = {}
DK_dict_counts = {}

for n in tqdm(atlasreader.get_atlas("desikan_killiany")['labels']['name']):
    DK_dict_counts.update({n: {Yeo_label:0 for Yeo_label in Yeo_labels}})
    DK_dict_voxels.update({n: {Yeo_label:[] for Yeo_label in Yeo_labels}})


for DK_i in range(0, DK_data.shape[0]):
    for DK_j in range(0, DK_data.shape[1]):
        for DK_k in range(0, DK_data.shape[2]):
            DK_voxel_label  = DK_data[DK_i, DK_j, DK_k]
            DK_voxel_region = atlasreader.get_label(DK_atlas, DK_voxel_label)

            if DK_voxel_region != 'Unknown':

                xyz = atlasreader.coord_ijk_to_xyz(DK_affine, [DK_i, DK_j, DK_k])
                Yeo_ijk = atlasreader.coord_xyz_to_ijk(Yeo_affine, xyz)[0]

                Yeo_voxel_label = int(Yeo_data[Yeo_ijk[0], Yeo_ijk[1], Yeo_ijk[2]])
                Yeo_voxel_region = Yeo_labels[Yeo_voxel_label]

                DK_dict_counts[DK_voxel_region][Yeo_voxel_region] += 1
                DK_dict_voxels[DK_voxel_region][Yeo_voxel_region].append(xyz[0])


# Save 17 networks map... in .mat format?
savemat('DK_dict17_voxels.mat', DK_dict_voxels)
savemat('DK_dict17_counts.mat', DK_dict_counts)
# save as python:
np.save('DK_dict_voxels.npy', DK_dict_voxels)
np.save('DK_dict_counts.npy', DK_dict_counts)

# convert opandas dataframe:
pd.DataFrame(DK_dict_counts)

# Prepare the data for CSV:
# read in atlas names
DK_region_names = pd.read_csv("../data/dk_names.csv").set_index('Atlas')
DK_dict_86_regions = {}
for region in DK_region_names.index:
    DK_dict_86_regions.update({region:DK_dict_counts[region]})

# transform into a pandas dataframe:
DK_dict_counts = pd.DataFrame(DK_dict_86_regions)
# drop none:
DK_dict_counts = DK_dict_counts.drop(['None'])

# Normalize:
DK_df_normalized = DK_dict_counts.div(DK_dict_counts.sum(axis=0). axis = 1)

# save to file
DK_df_normalized.to_csv('DK_Yeo17_normalized.csv')

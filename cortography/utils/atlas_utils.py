import pandas as pd
import os
from scipy.io import loadmat
import numpy as np
from nilearn import plotting

def get_file_path(filename):
    """Find filename in the relative directory `../data/` .

    Args:
        filename (str): file we're looking for in the ./data/ directory.

    Returns:
        str: absolute path to file "filename" in ./data/ dir.

    """
    here_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(here_dir, '../data/', filename)

    return file_dir

def load_atlas(atlas="DK", portion="all"):
    """Load atlas data and returns it as a pandas dataframe.

    Args:
        atlas (str): Atlas name: "DK" or "AAL".
        portion (str): Options are: "LR", "RL", "LRLR", "LRRL".

    Returns:
        atlas (pd.DataFrame): Database with atlas information.

    """
    if atlas == "DK":
        filepath = get_file_path("atlases/DK/dk_all.csv")
        dk = pd.read_csv(filepath)

        if portion == 'all':
            indices = dk.index

        else:

            cortical_df = dk[dk['Cortex']=='cortical']
            subcortical_df = dk[dk['Cortex']=='subcortical']

            cort_L_idx = cortical_df[cortical_df['Hemisphere']=='Left'].index
            cort_R_idx = cortical_df[cortical_df['Hemisphere']=='Right'].index

            subcort_L_idx = subcortical_df[subcortical_df['Hemisphere']=='Left'].index
            subcort_R_idx = subcortical_df[subcortical_df['Hemisphere']=='Right'].index

            if portion == 'LR':
                indices = list(cort_L_idx) + list(cort_R_idx)

            elif portion == 'RL':
                indices = list(cort_R_idx) + list(cort_L_idx)

            elif portion == 'LRLR':
                indices = list(cort_L_idx) + list(cort_R_idx)
                indices += list(subcort_L_idx) + list(subcort_R_idx)

            elif portion == 'LRRL':
                indices = list(cort_L_idx) + list(cort_R_idx)
                indices += list(subcort_R_idx) + list(subcort_L_idx)

            elif portion == 'RLLR':
                indices = list(cort_R_idx) + list(cort_L_idx)
                indices += list(subcort_L_idx) + list(subcort_R_idx)
    else:
        raise NameError("Atlas option not found.")

    return dk.loc[indices].set_index('Name')

def load_connectivity(atlas="DK", portion="RLLR"):

    if atlas == "DK":
        conn_filepath = get_file_path("connectivity_matrices/dk_connectivity.mat")
        connectivity = pd.DataFrame(loadmat(conn_filepath)['meanACS'])
        atlas = load_atlas(atlas="DK", portion=portion)
        regions_to_drop = ['Left-VentralDC',
                           'Left-choroid-plexus',
                           'Right-VentralDC',
                           'Right-choroid-plexus']
        atlas = load_atlas('DK','RLLR').drop(regions_to_drop)
        region_names = atlas.index
        connectivity.columns = list(region_names)
        connectivity.index = list(region_names)

        return(connectivity)

def load_laplacian(n=0):

    laplacian_filepath = get_file_path('connectivity_matrices/laplacians.mat')
    laplacian = pd.DataFrame(loadmat(laplacian_filepath)['laplacians'][0][0][n])
    DK = load_atlas(atlas="DK", portion="LRRL")
    DK = DK.drop(['Right-choroid-plexus',
                  'Left-choroid-plexus',
                  'Right-VentralDC',
                  'Left-VentralDC'], axis=0)

    laplacian.columns = list(DK.index)
    laplacian.index = list(DK.index)

    return(laplacian)

def plot_glass_brains(color, coords, size):

    num_regions = len(coords)

    connec = np.array([[0]*num_regions]*num_regions)

    plotting.plot_connectome(connec, coords, node_size = size, node_color=color, display_mode='lyrz')

def return_brain_paint_df(df, DK_convention='ctx', MAX=4):
    """
    Given a df with columns in the DK atlas,
    return a copy df with columns as required by brain_paint
    DK_ordering = naming convention according to cortography DK file
    MAX = max range of values in the df
    return_mean = returns a df with mean values of all subjects
    """
    DK = load_atlas('DK')

    brain_painter_regions = ['bankssts','caudalanteriorcingulate','caudalmiddlefrontal','cuneus','entorhinal',
                             'frontalpole','fusiform','inferiorparietal','inferiortemporal','insula',
                             'isthmuscingulate','lateraloccipital','lateralorbitofrontal','lingual',
                             'medialorbitofrontal','middletemporal','paracentral','parahippocampal',
                             'parsopercularis','parsorbitalis','parstriangularis','pericalcarine',
                             'postcentral','posteriorcingulate','precentral','precuneus',
                             'rostralanteriorcingulate','rostralmiddlefrontal','superiorfrontal',
                             'superiorparietal','superiortemporal','supramarginal','temporalpole',
                             'transversetemporal','unknown','Accumbens-area','Caudate',
                             'Cerebellum-White-Matter','Inf-Lat-Vent','Pallidum','Thalamus-Proper',
                             'Amygdala','Cerebellum-Cortex','Hippocampus','Lateral-Ventricle','Putamen','VentralDC']


    #1. generate empty df with brain painter columns
    brain_painter_df = pd.DataFrame(index=df.index)

    #2. for each brain painter region, find the equivalent region in the df
        #2.1 if found, get values
        #2.2 if not found, append zeros
    DK_left = DK[DK['Hemisphere'] == 'Left']
    regions_not_found = []
    for region in brain_painter_regions:
        if DK_convention == 'ctx':
            # name is in the form "ctx-lh-bankssts"
            standard_name = DK_left[DK_left['Other Name 5'] == region].index
        else:
            # name is in the form of one of the columns in the DK df
            standard_name = DK_left[DK_left['Other Name 5'] == region][DK_convention]

        if len(standard_name) > 0:
            brain_painter_df[region] = df[standard_name[0]]
        else:
            brain_painter_df[region] = 0.0
            regions_not_found.append(region)

    #3. Scale data between 0 and MAX
    def minmaxscaler(X, min_val, max_val):
        X_scaled = MAX * (X - min_val) / (max_val - min_val)
        return(X_scaled)

    scaled_df = brain_painter_df.copy()
    min = scaled_df.values.min()
    max = scaled_df.values.max()

    for column in scaled_df.columns:
        scaled_df[column] = minmaxscaler(scaled_df[column], min, max)

    scaled_df = scaled_df.abs()

    scaled_df.index.name = 'Image-name-unique'

    return(scaled_df)

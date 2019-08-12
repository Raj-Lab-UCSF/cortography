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
        portion (str): Options are: "cortical", "subcortical", "all".

    Returns:
        atlas (pd.DataFrame): Database with atlas information.

    """
    if atlas == "DK":
        filepath = get_file_path("dk_all.csv")
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

    else:
        raise NameError("Atlas option not found.")

    return dk.loc[indices]

def load_connectivity(atlas="DK", portion="all"):

    if atlas == "DK" and portion == "all":
        conn_filepath = get_file_path("dk_connectivity.mat")
        connectivity = pd.DataFrame(loadmat(conn_filepath)['meanACS'])
        region_names = load_atlas(atlas="DK", portion="all").Name[:86]
        connectivity.columns = list(region_names)
        connectivity.index = list(region_names)

        return(connectivity)

def load_laplacian(n=0):

    laplacian_filepath = get_file_path('laplacians.mat')
    laplacians = pd.DataFrame(loadmat(laplacian_filepath)['laplacians'][0][0][n])
    region_names = load_atlas(atlas="DK", portion="all").Name[:86]

    laplacians.columns = list(region_names)
    laplacians.index = list(region_names)

    return(laplacians)

def plot_glass_brains(color, coords, size):

    num_regions = len(coords)

    connec = np.array([[0]*num_regions]*num_regions)

    plotting.plot_connectome(connec, coords, node_size = size, node_color=color, display_mode='lyrz')

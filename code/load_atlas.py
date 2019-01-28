import pandas as pd
import os

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

def load_atlas(atlas="DK", portion="cortical"):
    """Load atlas data and returns it as a pandas dataframe.

    Args:
        atlas (str): Atlas name: "DK" or "AAL".
        portion (str): Options are: "cortical", "subcortical", "all".

    Returns:
        atlas (pd.DataFrame): Database with atlas information.

    """
    if atlas == "DK" and portion == "cortical":
        filepath = get_file_path("dk_cortical.csv")
        atlas = pd.read_csv(filepath)

    return atlas

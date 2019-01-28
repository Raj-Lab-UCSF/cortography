import pandas as pd

def load_atlas(atlas="DK", portion="cortical"):
    """Load atlas data and returns it as a pandas dataframe.

    Args:
        atlas (str): Atlas name: "DK" or "AAL".
        portion (str): Options are: "cortical", "subcortical", "all".

    Returns:
        atlas (pd.DataFrame): Database with atlas information.

    """
    if atlas == "DK" and portion == "cortical":
        atlas = pd.read_csv("../data/dk_cortical.csv")

    return atlas

DK = load_atlas()

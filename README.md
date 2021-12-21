# Cortography
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pfdamasceno/rajutils/master?urlpath=https%3A%2F%2Fgithub.com%2Fpfdamasceno%2Frajutils%2Fblob%2Fmaster%2Frajutils%2Fnotebooks%2FDK%2520connectome%2520ordering.ipynb)
---

- Cortography (CORTical cartOGRAPHY) is a repository of utility tools and curated, collaborative collection of cortical and subcortical atlases for neuroimaging research.
- The atlas utilities are based on [Andreas Horn's](http://andreas-horn.de) detailed [collection of atlas parcellations](http://www.lead-dbs.org/helpsupport/knowledge-base/atlasesresources/cortical-atlas-parcellations-mni-space).
- If you find any inaccurate information, or know of an atlas not currently in this list, feel free to fork this repository, include the missing atlas, and submit a Pull Request. Happy mapping.

# Utilities
- Collection of useful functions for the Raj lab

## Installation instructions:
- run `pip install .` inside the rajutils folder

## Example usage
```
>>> from cortography.utils import atlas_utils
>>> atlas_utils.load_atlas(atlas='DK', portion='LRRL')
```

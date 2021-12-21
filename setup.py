from setuptools import setup

setup(name='cortography',
      version='0.1',
      description='Set of python tools useful to the Raj lab',
      url='https://github.com/Raj-Lab-UCSF/cortography',
      author='Pablo F. Damasceno',
      author_email='pablo.damasceno@ucsf.edu',
      license='MIT',
      packages = setuptools.find_packages(),
      include_package_data = True,
      package_data = {
            '': ['*.txt', '*.xml', '*.csv', '*.md','*.nii','*.nii.gz','*.npy'],
      },
      zip_safe=False)

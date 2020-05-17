import setuptools
#
# import pdoc 


mods = ['LeanIX']

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name='leanix-py',
  version='0.0.3',
  description='Functionality to support the development with LeanIX REST APIs',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/JeffGebhart/leanix-python-library',
  author='Jeff Gebhart',
  author_email='jeff@gebhart.ca',
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
  #Packages that are included in the project
  packages=mods,
  #Package requirements that 
  install_requires=['requests']
)
import setuptools 

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name='leanix',
  version='0.1',
  description='Functionality to support the development with LeanIX REST APIs',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/leanix-public/leanix-python-library',
  author='Christoph for LeanIX',
  author_email='christoph.walpert@leanix.net',
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
  #Packages that are included in the project
  packages=[],
  #Package requirements that 
  install_requires=['json','pandas','requests','base64','time']
)
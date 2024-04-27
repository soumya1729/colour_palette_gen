from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'Color-Palette-Generator',
  version = '0.0.2',
  license='MIT',
  description = 'Generate Colour Palettes with Python',
  long_description=long_description,
  long_description_content_type = 'text/markdown',
  author = 'SM',
  url = 'https://github.com/soumya1729/Color-palette-generator',
  keywords = [
    'matplotlib',
    'python plots'
  ],
  install_requires=[
    'matplotlib>=3.5.1',
    'opencv-python>=4.9.0.80',
    'numpy>=1.25.2'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)

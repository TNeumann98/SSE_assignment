from setuptools import setup

setup(name='mkipp',
    version='0.1.20201207',
    description='Kippenhahn plotter for MESA star',
    url='https://github.com/orlox/mkipp',
    author='Pablo Marchant',
    author_email='a@b.c',
    license='GNU GPL',
    packages=['mkipp', 'mesa_data', 'kipp_data'],
    install_requires=['numpy']) #, 'math', 'h5py', 'matplotlib', 'collections', 're'
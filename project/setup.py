from setuptools import setup, Extension
import os

# Define the C extension module
ridemate_module = Extension(
    'ridemate',
    sources=['ridemate_bridge.c', 'customer.c', 'vehicle.c', 'rental.c', 'utils.c'],
    include_dirs=[os.path.abspath('.')],
    define_macros=[('PY_SSIZE_T_CLEAN', None)],
)

# Setup configuration
setup(
    name='ridemate',
    version='1.0',
    description='RideMate C Extension',
    ext_modules=[ridemate_module],
)

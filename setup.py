from setuptools import setup

dependencies = ['pytest', 'pytest-cov']
extra_packages = {
    'testing': ['tox']
}

setup(
    name='http-server',
    description='client communicates with the server',
    version='0.1',
    author='Carlos Cadena, Chris Hudson',
    author_email='cs.cadena@gmail.com',
    license='MIT',
    py_modules='client, server',
    package_dir={'': 'src'},
    install_requires=dependencies,
    extras_require=extra_packages,
    entry_points={}
)

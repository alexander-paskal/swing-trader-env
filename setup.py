from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='swing_trader_env',
   version='0.0',
   description='A gym-like environment for swing trading simulation',
   license="MIT",
   long_description=long_description,
   author='Alex Paskal',
   author_email='alexcpaskal@gmail.com',
   url="https://github.com/alexander-paskal/swing-trader-env",
   packages=['swing_trader_env'],  #same as name
   install_requires=[
       'pandas',
       
    ], #external packages as dependencies
   scripts=[
           ]
)
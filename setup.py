from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='JAYADHI AI for ALL',
    version='0.1.0',
    author='Karthik',
    description='AI/ML backend for the JAYADHI Educational Platform, providing sentiment analysis, personalization, and adaptive learning algorithms.',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

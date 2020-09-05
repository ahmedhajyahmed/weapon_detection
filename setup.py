from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup_args = dict(
    name='weapon_detection',
    version='0.1',
    description='package containing a deep learning model for detecting firearm in a picture',
    long_description='package containing a deep learning model for detecting firearm in a picture',
    classifiers=[
            'Programming Language :: Python :: 3.6.6',
            'Topic :: image Processing :: weapon detection',
          ],
    packages=find_packages(),
    author='Ahmed Haj Yahmed',
    author_email='hajyahmedahmed@gmail.com',
    keywords=['Weapon detection', 'Weapon classification', 'Image classification'],
)

install_requires = requirements

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
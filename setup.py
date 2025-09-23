from setuptools import setup, find_packages

setup(
    name='api-client-hub',
    version='0.1.0',
    author='LuisH019',
    description='Uma biblioteca para operar com APIs SOAP e REST de forma robusta e fácil.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LuisH019/api-client-hub',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'Requests==2.32.5',
        'zeep==4.3.2'
    ],
)
from setuptools import find_packages, setup
import pathlib


description = 'A Python wrapper for the Misskey API'
readme_file = pathlib.Path(__file__).parent/'README.md'
with readme_file.open(encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mi.py',
    version='0.0.2',
    install_requires=['websockets', 'requests'],
    url='https://github.com/yupix/mi.py',
    author='yupix',
    author_email='yupi0982@outlook.jp',
    license='MIT',
    python_requires='>=3.8, <4.0',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: MIT License',
    ]
)

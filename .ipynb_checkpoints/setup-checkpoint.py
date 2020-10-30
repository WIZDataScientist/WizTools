from setuptools import setup, find_packages

setup(
    name='wiz_ds_toolz',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='WIZ',
    description='python package for data science',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'pandas', 'seaborn', 'matplotlib'],
    #url='https://github.com/BillMills/python-package-example',
    author='Wilson Zhou',
    author_email='wilsonzhou92@gmail.com'
)
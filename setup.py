from setuptools import setup


setup(
    name='imagenetviewer',
    version='0.2',
    #description='',
    #long_description=open('README.md', 'r').read(),
    #long_description_content_type='text/markdown',
    #url='https://github.com/yashenkoxciv/imagenetviewer',
    author='Artem Yaschenko',
    author_email='yashenkoxciv@gmail.com',
    packages=['imagenetviewer'],
    install_requires=open('requirements.txt', 'r').read().split('\n')
)
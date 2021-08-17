from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='blackjacksimulator',
    version='2.0.0',
    description='''
    A CLI Blackjack multiplayer simulator including all standard in-game decisions. 
    ''',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Nicolás Moro',
    author_email='n.moro811@gmail.com',
    packages=['blackjacksimulator'],
    url='https://github.com/NMoro811/blackjack-simulator',
    license=license,
    keywords = 'blackjack, simulator, multiplayer, cli, game, card, cards',
    install_requires=['os', 'time', 'random'],
)

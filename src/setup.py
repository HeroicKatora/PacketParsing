import os.path
import setuptools

setuptools.setup(
    name='gpp',
    version='0.1.0a1.dev1',
    description='Parsing binary stream data with structures defined via XML and Python',
    url='https://github.com/HeroicKatora/PacketParsing',
    author='HeroicKatora',
    license='MIT',
    packages=setuptools.find_packages(where=os.path.dirname(__file__), exclude=['tests', 'xml']),
    install_requires=['lxml', 'bitstring', 'parse'],
    package_data={'gpp': ['*.xml', '*.xsd']}
)

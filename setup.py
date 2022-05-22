from distutils.core import setup
import py2exe

setup(
    console=['accm.py'],
    name="Account Manager accm",
    version="1.0.0",
    license="MIT-license",
    description="""Save all your accounts in a local database on your device 
    which can be connected to those accounts. This will be more protective 
    than having your browser remember all about you until your login 
    information! Say goodbye to forget your password """
)


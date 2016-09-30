try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'python hwi',
    'author': 'Yu Ruidong',
    'url': 'git@github.com:yuruidong/python-hwi.git',
    'author_email': 'yrd_1989@126.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pyhwi'],
    'script': [],
    'name': 'python-hwi'
}

setup(**config)

import pathlib
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

def get_requirements(path: str):
    return [l.strip() for l in open(path)]

setup(
    name='Fastest Google Translator',
    version='1.0.1',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=', '.join(['Hien Vu', '']),
    author_email=', '.join(['hienvq23@gmail.com', '']),
    url='',
    packages=find_packages(),
    keywords='',
    install_requires=get_requirements("requirements.txt"),
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'transipy=transipy.main:main'
        ],
    },
)

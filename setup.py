import pathlib
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

def get_requirements(path: str):
    return [l.strip() for l in open(path)]

setup(
    name='transipy',
    version='1.0.5',
    description='Transipy is your one-stop solution for lightning-fast and accurate document translation.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=', '.join(['Hien Vu', '']),
    author_email=', '.join(['hienvq23@gmail.com', '']),
    url='https://github.com/NeiH4207/transipy',
    packages=find_packages(),
    keywords='google translate, translation, document translation, language translation',
    install_requires=get_requirements("requirements.txt"),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'transipy=transipy:main'
        ],
    },
)

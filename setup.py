import os
from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

about = {}
with open(os.path.join("imagebot", "__version__.py")) as f:
    exec(f.read(), about)

VERSION = about["__version__"]

setup(
    version=VERSION,
    name="image-bot-cv2",
    packages=find_packages(),
    description=f"Image matching/comparison based on open-cv",
    author="Johnny Huang",
    author_email="jnhyperion@gmail.com",
    url="https://github.com/jnhyperion/ImageBot",
    keywords="opencv image matching comparison",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
)

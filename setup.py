from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    version="0.0.1",
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

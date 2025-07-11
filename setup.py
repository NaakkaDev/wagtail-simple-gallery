import os
from setuptools import find_packages, setup
from wagtail_simple_gallery import __version__

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="wagtail-simple-gallery",
    version=__version__,
    author="Teemu Nieminen",
    author_email="naakka.dev+wsg@gmail.com",
    description="A simple gallery app for Wagtail.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/NaakkaDev/wagtail-simple-gallery",
    keywords="wagtail cms model page templatetags",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=4.2",
        "wagtail>=5.0",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)

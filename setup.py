from setuptools import setup
from mkdocs_simple_blog import __version__


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="clic-in-litex",
    fullname='clic-in-litex',
    author='clic-in-litex',
    version=__version__,
    author_email='saket.sinha89@gmail.com',
    url='https://github.com/disdi/clic-in-litex',
    description="Mkdocs Blog Theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        'mkdocs>=1.6.1'
    ],
    packages=["clic_in_litex"],
    package_data={'clic_in_litex': ['*', '*/*', '*/*/*']},
    include_package_data=True,
    python_requires=">=3.8",
    zip_safe=True,
    entry_points={
        'mkdocs.themes': [
            'simple-blog = clic_in_litex',
        ]
    },
)

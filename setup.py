from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Get version from environment or default
VERSION = os.getenv("PACKAGE_VERSION", "1.0.0")

setup(
    name="wyscout-scraper",
    version=VERSION,
    author="jirpo9",
    description="Professional web scraper for Wyscout Data Glossary with PDF generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jirpo9/wyscout-scraper",
    project_urls={
        "Bug Reports": "https://github.com/jirpo9/wyscout-scraper/issues",
        "Source": "https://github.com/jirpo9/wyscout-scraper",
    },
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "monitoring": ["prometheus-client>=0.15.0"],
        "async": ["aiohttp>=3.8.0", "asyncio>=3.4.3"],
    },
    entry_points={
        "console_scripts": [
            "wyscout-scraper=src.scraper:main",
            "wyscout-pdf=src.pdf_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["templates/*.html", "styles/*.css"],
    },
    zip_safe=False,
    keywords="web-scraping, wyscout, football, soccer, pdf-generation, data-extraction",
    platforms=["any"],
)
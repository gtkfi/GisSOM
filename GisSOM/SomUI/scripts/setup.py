from setuptools import setup, find_packages

setup(
        name="nextsomcore",
        version="0.1",
        packages=find_packages(),
        include_package_data=True,
        test_suite="test", 
        scripts=['nextsom_wrap.py'],
        install_requires=["matplotlib", "numpy", "scipy", "sklearn"],
        author="Janne Kallunki",
        author_email="janne.kallunki@gtk.fi",
        description="Script for creating self organizing maps",
)

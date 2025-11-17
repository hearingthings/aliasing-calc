from setuptools import setup, find_packages

setup(
    name="aliasing-calc",
    version="0.1.0",
    description="Creative aliasing calculator for audio decimation",
    author="Aliasing Calc Contributors",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "viz": ["matplotlib>=3.3.0"],
        "dev": ["pytest>=6.0.0", "pytest-cov>=2.10.0"],
    },
    entry_points={
        "console_scripts": [
            "aliasing-calc=aliasing_calc.cli:main",
        ],
    },
    python_requires=">=3.8",
)

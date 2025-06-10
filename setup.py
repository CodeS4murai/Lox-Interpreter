from setuptools import setup, find_packages  # type: ignore
setup(
    name="lox-interpreter",
    version="0.1.0",
    author="Sam",
    description="A Lox-interpreter implementation in Python from crafting interpreters ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lox-interpreter",  
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[       
    ],
    entry_points={
        "console_scripts": [
            "lox=core.main:main",  
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Interpreters",
    ],
)

from setuptools import setup, find_packages

setup(
    name="todo-console-app",
    version="0.1.0",
    description="A console-based todo application",
    author="Developer",
    author_email="developer@example.com",
    packages=find_packages(),
    install_requires=[
        # No external dependencies - using only built-in Python libraries
    ],
    entry_points={
        'console_scripts': [
            'todo-app=src.main:main',
        ],
    },
    python_requires='>=3.13',
)
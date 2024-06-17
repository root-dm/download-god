from setuptools import setup, find_packages

setup(
    name="download_god",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'download-god=app:main',
        ],
    },
    package_data={
        '': ['assets/frame0/*', 'credentials.json'],
    },
    data_files=[('', ['credentials.json'])],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Google Drive download manager",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/download_god",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

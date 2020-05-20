import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='YoutubeDowloader-MattGonley',
    version='1.2',
    packages=setuptools.find_packages(),
    url='https://github.com/mattgonley/YoutubeDowloader',
    license='',
    author='Matt Gonley',
    author_email='',
    description='Youtube downloader for playlists and videos',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"],
    python_requires='>=3.0')

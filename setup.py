from setuptools import setup, find_packages

setup(
    name='nlprep',
    version='0.1.57',
    description='Download and pre-processing data for nlp tasks',
    url='https://github.com/voidful/nlprep',
    author='Voidful',
    author_email='voidful.stack@gmail.com',
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    keywords='nlp tfkit classification generation tagging deep learning machine reading',
    packages=find_packages(),
    install_requires=[
        # accessing files from S3 directly
        "boto3",
        # filesystem locks e.g. to prevent parallel downloads
        "filelock",
        # for downloading models over HTTPS
        "requests",
        # progress bars in model download and training scripts
        "tqdm >= 4.27",
        # Open Chinese convert (OpenCC) in pure Python.
        "opencc-python-reimplemented",
        # tool for handling textinquirer
        "nlp2 >= 1.8.27",
        # generate report
        "pandas-profiling >= 2.8.0",
        # dataset
        "nlp >= 0.3.0",
        # phrase segmentation
        "phraseg >= 1.1.8",
        # tokenizer support
        "transformers==3.3.0",
        # input panel
        "inquirer",
        "BeautifulSoup4",
        "lxml"
    ],
    entry_points={
        'console_scripts': ['nlprep=nlprep.main:main']
    },
    zip_safe=False,
)

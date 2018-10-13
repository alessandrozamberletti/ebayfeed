import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ebayfeed',
    version='2018.10.7',
    author='alez',
    author_email='alez.pypi@gmail.com',
    url='https://github.com/alessandrozamberletti/ebayfeed',
    description='Download item feeds from eBay RESTful APIs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=[
        'ebayfeed'
    ],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    keywords='ebayfeed ebay-api ebay-rest-api ebay-oauth',
    zip_safe=True
)

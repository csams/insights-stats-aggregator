from setuptools import setup, find_packages


DEVELOP = set([
    'ipython',
    'pytest',
    'setuptools',
    'twine',
    'wheel',
])

RUNTIME = set([
    "s3fs",
    "retry",
    "pika",
])


if __name__ == "__main__":
    setup(
        name="insights-stats-worker",
        version="0.0.1",
        description="Service for aggregating rule hit stats",
        long_description=open("README.md").read(),
        long_description_content_type='text/markdown',
        url="https://github.com/csams/insights-stats-aggregator",
        packages=find_packages(),
        package_data={'': ['LICENSE']},
        license='Apache 2.0',
        install_requires=list(RUNTIME),
        extras_require={
            'develop': list(DEVELOP | RUNTIME),
        },
        classifiers=[
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],
        include_package_data=True
    )

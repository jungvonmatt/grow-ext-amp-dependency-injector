from setuptools import setup

setup(
    name='grow-ext-amp-dependency-injector',
    version='1.0.0',
    license='Apache License 2.0',
    author='Jung von Matt/tech GmbH',
    author_email='nextalster-developer@jvm.de',
    include_package_data=False,
    packages=[
        'amp_dependency_injector',
    ],
    install_requires=[
        'lxml==4.2.5'
    ],
)

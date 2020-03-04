from setuptools import find_packages, setup

setup(
    name="sendit_api-test",
    version="0.0.1",
    # Include all the python modules except `tests`.
    packages=find_packages(exclude=["tests"]),
    description="Customizing test",
    long_description="A long description of my custom package tested with tox",
    install_requires=[
        "Django>=3.0.2",
        "djangorestframework>=3.11.0",
        "psycopg2>=2.8.4",
        # Additional requirements, or
        # parse the requirements file and add it here
    ],
    classifiers=["Programming Language :: Python",],  # noqa
)

from setuptools import setup

setup(
    name="choose-master",
    version="1.0.0",
    packages=['choose-master'],
    author="Venkata Edara",
    author_email="redara@redhat.com",
    description="package to choose ovirt node to get gluster volume metrics",
    license="BSD",
    url="https://github.com/gluster/gluster-collectd",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: System :: Networking",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
    ],

    long_description="""\
    This Python module uses the ovirt sdk to get list of online ovirt nodes
    chooses one of them to get volume metrics using ovirt python sdk. fetching
    volume metrics from each node is costly operation so we are choosing only on
    node to get metrics for gluster volumes.
    """
)

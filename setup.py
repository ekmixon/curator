import os
import re
import sys
from setuptools import setup

# Utility function to read from file.
def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version():
    VERSIONFILE="curator/_version.py"
    verstrline = fread(VERSIONFILE).strip()
    vsre = r"^__version__ = ['\"]([^'\"]*)['\"]"
    if mo := re.search(vsre, verstrline, re.M):
        VERSION = mo[1]
    else:
        raise RuntimeError(f"Unable to find version string in {VERSIONFILE}.")
    if build_number := os.environ.get('CURATOR_BUILD_NUMBER', None):
        return VERSION + f"b{build_number}"
    return VERSION

def get_install_requires():
    return [
        'elasticsearch>=7.12.0,<8.0.0',
        'urllib3==1.26.4',
        'requests>=2.25.1',
        'boto3>=1.17.57',
        'requests_aws4auth>=1.0.1',
        'click>=7.0,<8.0',
        'pyyaml==5.4.1',
        'voluptuous>=0.12.1',
        'certifi>=2020.12.5',
        'six>=1.15.0',
    ]

try:
    ### cx_Freeze ###
    from cx_Freeze import setup, Executable
    try:
        import certifi
        cert_file = certifi.where()
    except ImportError:
        cert_file = ''
    # Dependencies are automatically detected, but it might need
    # fine tuning.


    base = 'Console'

    icon = 'Elastic.ico' if os.path.exists('Elastic.ico') else None
    curator_exe = Executable(
        "run_curator.py",
        base=base,
        targetName = "curator",
    )
    curator_cli_exe = Executable(
        "run_singleton.py",
        base=base,
        targetName = "curator_cli",
    )
    repomgr_exe = Executable(
        "run_es_repo_mgr.py",
        base=base,
        targetName = "es_repo_mgr",
    )
    build_dict = { 
        "build_exe": dict(
            packages = [],
            excludes = [],
            include_files = [cert_file],
        )
    }
    if sys.platform == "win32":
        curator_exe = Executable(
            "run_curator.py",
            base=base,
            targetName = "curator.exe",
            icon = icon
        )
        curator_cli_exe = Executable(
            "run_singleton.py",
            base=base,
            targetName = "curator_cli.exe",
            icon = icon
        )
        repomgr_exe = Executable(
            "run_es_repo_mgr.py",
            base=base,
            targetName = "es_repo_mgr.exe",
            icon = icon
        )

        msvcrt = 'vcruntime140.dll'
        build_dict = { 
            "build_exe": {
                "include_files": [cert_file, msvcrt],
                "include_msvcr": True, 
                "silent": True,
            },
            "bdist_msi": {
                "upgrade_code": fread("msi_guid.txt"),
                "all_users": True,
                "add_to_path": True,
                "summary_data": {"author": "Elastic", "comments": "version {0}".format(get_version())},
                "install_icon": icon,
            }
        }

    setup(
        name="elasticsearch-curator",
        version=get_version(),
        author="Elastic",
        author_email="info@elastic.co",
        description="Tending your Elasticsearch indices",
        long_description=fread('README.rst'),
        url="http://github.com/elastic/curator",
        download_url=f"https://github.com/elastic/curator/tarball/v{get_version()}",
        license="Apache License, Version 2.0",
        install_requires=get_install_requires(),
        setup_requires=get_install_requires(),
        keywords="elasticsearch time-series indexed index-expiry",
        packages=["curator"],
        include_package_data=True,
        entry_points={
            "console_scripts": [
                "curator = curator.cli:cli",
                "curator_cli = curator.curator_cli:main",
                "es_repo_mgr = curator.repomgrcli:repo_mgr_cli",
            ]
        },
        classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
        ],
        test_suite="test.run_tests.run_all",
        tests_require=["mock", "nose", "coverage", "nosexcover"],
        options=build_dict,
        executables=[curator_exe, curator_cli_exe, repomgr_exe],
    )

    ### end cx_Freeze ###
except ImportError:
    setup(
        name="elasticsearch-curator",
        version=get_version(),
        author="Elastic",
        author_email="info@elastic.co",
        description="Tending your Elasticsearch indices",
        long_description=fread('README.rst'),
        url="http://github.com/elastic/curator",
        download_url=f"https://github.com/elastic/curator/tarball/v{get_version()}",
        license="Apache License, Version 2.0",
        install_requires=get_install_requires(),
        keywords="elasticsearch time-series indexed index-expiry",
        packages=["curator"],
        include_package_data=True,
        entry_points={
            "console_scripts": [
                "curator = curator.cli:cli",
                "curator_cli = curator.curator_cli:main",
                "es_repo_mgr = curator.repomgrcli:repo_mgr_cli",
            ]
        },
        classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
        ],
        test_suite="test.run_tests.run_all",
        tests_require=["mock", "nose", "coverage", "nosexcover"],
    )

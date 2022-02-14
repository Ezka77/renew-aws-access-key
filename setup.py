from setuptools import setup, find_packages
import os

README = """AWS/Boto3 script to re-new IAM access key"""

requires = ["click", "colorama", "boto3", "wheel"]

setup(
    name="AWS access key renew",
    version="0.1",
    description="AWS access key renew",
    long_description=README,
    author="Ezka77",
    author_email="",
    url="",
    classifiers=[
        "Programming Language :: Python",
        "Private :: Do Not Upload",
    ],
    keywords="aws renew access key useless",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points="""\
      [console_scripts]
      aws_renew_access_key = aws_renew_access_key:main
      """,
)

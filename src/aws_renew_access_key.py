#!/usr/bin/env python3

import boto3
import click
import configparser
import pprint
import os.path
import sys


AWS_CREDS_FILE = os.path.expanduser("~/.aws/credentials")


class ExitError(Exception):
    pass


class FailureError(Exception):
    def __init__(self, message: str, errno: int = 1):
        self.message = message
        self.errno = errno


def list_access_keys() -> list:
    client = boto3.client("iam")
    response = client.list_access_keys()
    try:
        return response["AccessKeyMetadata"]
    except KeyError:
        raise FailureError("Error listing acces key: response empty", 2)


def renew_key(keyid: str, section: str = "default", creds: str = AWS_CREDS_FILE):
    click.secho("Start AWS-IAM access key renew process", fg="yellow")
    try:
        client = boto3.client("iam")
        client.delete_access_key(AccessKeyId=keyid)
        click.secho(f"AWS-IAM key '{keyid}' deleted", fg="yellow")
        response = client.create_access_key()
        data = response["AccessKey"]
        click.secho(f"AWS-IAM key '{data['AccessKeyId']}' created", fg="yellow")
        # update current configuration
        update_aws_creds(
            data["AccessKeyId"],
            data["SecretAccessKey"],
            section=section,
            aws_file=creds,
        )
        click.secho(f"configuration file updated: {creds}", fg="blue")
        click.secho("success! access key renewed.", fg="green")
    except (IndexError, KeyError):
        click.secho("Aborted", fg="red", err=True)
        sys._exit(5)
    except ExitError as err:
        click.secho(err, err=True)
    except FailureError as err:
        click.secho(err.message, err=True)
        sys._exit(err.errno)


def update_aws_creds(
    key: str, secret: str, section: str = "default", aws_file: str = AWS_CREDS_FILE
):
    # read ~/aws/credentials
    config = configparser.ConfigParser()
    with open(aws_file, "r") as cf:
        config.read_file(cf)
        # set new values
    try:
        config.set(section, "aws_access_key_id", key)
        config.set(section, "aws_secret_access_key", secret)
    except configparser.NoSectionError:
        raise FailureError("INI section missing, operation cancelled", 3)
    except TypeError:
        raise FailureError("key or secret is not a string!", 4)
    # write file
    with open(aws_file, "w") as cf:
        config.write(cf)


@click.command()
@click.option(
    "--list", "list_only", is_flag=True, help="list current available access key"
)
@click.option(
    "--creds",
    default=AWS_CREDS_FILE,
    type=click.Path(exists=True),
    help="path to AWS credentials file",
)
@click.option(
    "--section", default="default", help="section name in AWS configuration file"
)
@click.option("--keyid", "-k", default="", help="The keyid to renew")
def main(list_only, creds, section, keyid):
    # list access keys
    curr_keys = list_access_keys()
    if list_only:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(curr_keys)
        return

    if not keyid:
        config = configparser.ConfigParser()
        config.read(creds)
        keyid = config[section]["aws_access_key_id"]

    if len(curr_keys) > 1 and not keyid:
        raise ExitError(
            "More than one access key, please choose one with" "--keyid option!"
        )
    # delete & create keys
    renew_key(keyid, section, creds)


if __name__ == "__main__":
    main()

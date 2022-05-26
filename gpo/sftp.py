"""
sftp letter writer service
"""
import csv
import logging
import math
import base64
import io

import paramiko

from . import models

log = logging.getLogger(__name__)


def write(file: io.StringIO | paramiko.SFTPFile, letters: list[models.Letter]):
    """
    Write letter data to file

    001|955
    002|FAKEY MCFAKERSON|123 FAKE ST||GREAT FALLS|MT|59010|Q82GZBP71C|January 11, 2022|January 21, 2022|Example Sinatra App|https://secure.login.gov
    003|JIMMY TESTERSON|456 FAKE RD|Apt 1|FAKE CITY|CA|40323|4WVGPG0Z5Z|January 11, 2022|January 21, 2022|Example Rails App|https://secure.login.gov
    004|MIKE MCMOCKDATA|789 TEST AVE||FALLS CHURCH|VA|20943|5HVFT58WJ0|January 11, 2022|January 21, 2022|Example Java App|https://secure.login.gov
    005|...
    ...
    956|...

    Formatting Contract:
    Removed: | (delimiter), \n (lineterminator), \r
    Everything else verbatim, no quoting
    """

    writer = csv.writer(
        file, delimiter="|", lineterminator="\n", quotechar=None, quoting=csv.QUOTE_NONE
    )
    num_lines = len(letters) + 1

    # number of digits in the row index
    num_index_digits = math.trunc(math.log(num_lines, 10)) + 1
    # row index width is a least 2 and is enough to fit number of digits in the index
    width = max(2, num_index_digits)

    header = [f"{1:0{width}}", len(letters)]
    writer.writerow(header)

    for i, val in enumerate(letters, start=2):

        # row with index
        row = val.as_list(f"{i:0{width}}")

        # remove any | or \n that might be in the data
        sanitized_row = map(
            lambda x: x.replace("|", "").replace("\n", "").replace("\r", ""), row
        )
        writer.writerow(sanitized_row)


def write_sftp(
    letters: list[models.Letter], ssh_settings, file_name: str, dest_dir: str
):
    """
    Write letters to sftp endpoint
    """
    with paramiko.SSHClient() as ssh_client:
        host_key = paramiko.RSAKey(data=base64.b64decode(ssh_settings.GPO_HOSTKEY))
        ssh_client.get_host_keys().add(ssh_settings.GPO_HOST, "ssh-rsa", host_key)
        ssh_client.connect(
            ssh_settings.GPO_HOST,
            username=ssh_settings.GPO_USERNAME,
            password=ssh_settings.GPO_PASSWORD,
        )
        with ssh_client.open_sftp() as sftp:
            sftp.chdir(dest_dir)
            try:
                with sftp.open(file_name, mode="wx") as file:
                    write(file, letters)
            except PermissionError as err:
                log.error(
                    "Error Creating file likely because it already exists: %s", err
                )
                raise SftpError from err


class SftpError(PermissionError):
    """
    Error with sftp operation
    """

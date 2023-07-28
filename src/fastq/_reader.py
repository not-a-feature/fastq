"""
fastq: A simple toolbox for fastq files.

This is the reader part.

@author: Jules Kreuer / not_a_feature
License: GPL-3.0
"""

from ._fastq import fastq_object

from zipfile import ZipFile
import gzip
import tarfile

from os import path
from typing import Iterator


def __maybeByteToStr(maybeByte) -> str:
    if isinstance(maybeByte, bytes):
        return maybeByte.decode("utf-8").rstrip()
    return str(maybeByte).rstrip()


def read(file_path: str, upper: bool = True) -> Iterator[fastq_object]:
    """
    Reads a compressed or non-compressed fastq file and returns a list of fastq_objects.
    Zip, tar, gz, tar.gz files are supported.
    Attention: Encoding characters (backslash) will work under certain conditions.

    Input:
        file_path: str, path to folder / file
        upper: bool, cast sequence to upper-case letters.

    Returns:
        fastq_objects: list of fastq_object
    """

    if not path.isfile(file_path):
        raise FileNotFoundError("Fastq File not found!")

    handlers = []
    file_type = path.splitext(file_path)[1]

    # .zip file
    if file_type == ".zip":
        zipHandler = ZipFile(file_path, "r")
        # Create handler for every file in zip
        for inner_file in zipHandler.namelist():  # type:ignore
            handlers.append(zipHandler.open(inner_file, "r"))  # type:ignore
    # .tar file
    elif file_type == ".tar":
        tarHandler = tarfile.open(file_path, "r")
        # Create handler for every file in tar
        for inner_file in tarHandler.getmembers():  # type:ignore
            handlers.append(tarHandler.extractfile(inner_file))  # type:ignore
    # .gz file
    elif file_type == ".gz":
        # tar.gz file
        inner_file_type = path.splitext(path.splitext(file_path)[0])[1]
        if inner_file_type == ".tar":
            # Create handler for every file in tar.gz
            tarHandler = tarfile.open(file_path, "r")
            for inner_file in tarHandler.getmembers():  # type:ignore
                handlers.append(tarHandler.extractfile(inner_file))  # type:ignore
        else:
            # .gz file
            handlers = [gzip.open(file_path, "r")]  # type:ignore
    else:
        handlers = [open(file_path, "r")]  # type:ignore

    for h in handlers:
        with h:
            head = ""
            body = ""
            qstr = ""

            for maybeByte in h:
                # Header
                head = __maybeByteToStr(maybeByte)

                # Break if line is empty (newline at EOF)
                if head == "":
                    break
                # Body (Sequence)
                maybeByte = next(h)
                body = __maybeByteToStr(maybeByte)

                # Skip quality identifier
                maybeByte = next(h)

                # QString
                maybeByte = next(h)
                qstr = __maybeByteToStr(maybeByte)

                # append element
                yield fastq_object(head, body, qstr)

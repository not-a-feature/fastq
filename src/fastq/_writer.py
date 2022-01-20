"""
fastq: A simple toolbox for fastq files.

This is the writer part.

@author: Jules Kreuer / not_a_feature
License: GPL-3.0
"""

from ._fastq import fastq_object as superFQ


class fastq_object(superFQ):
    def write(self, file_path: str, mode="w"):
        """
        Writes this fastq_object to a file.
        """
        write(self, file_path, mode)


def write(fastq_pairs, file_path: str, mode="w") -> None:
    """
    Writes a list of fastq_objects or a single one to a file.
    Takes fastq_objects as input.
    """

    if not isinstance(fastq_pairs, list):
        fastq_pairs = [fastq_pairs]

    with open(file_path, mode) as f:
        for fq in fastq_pairs:
            f.write(f"{fq}\n")
    return None

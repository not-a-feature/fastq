from ._fastq import print_fastq
from ._reader import read
from ._writer import write, fastq_object

__all__ = [
    "fastq_object",
    "read",
    "write",
    "print_fastq",
]

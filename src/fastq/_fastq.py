"""
fastq: A simple toolbox for fastq files

See: https://github.com/not-a-feature/fastq
Or:  https://pypi.org/project/fastq/

@author: Jules Kreuer / not_a_feature
License: GPL-3.0
"""

# Usual translation dictionary according to
# https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG1

from miniFasta import fasta_object


class fastq_object():
    def __init__(self, head: str, body: str, qstr: str):
        """
        Object to keep a fastq entry.
        Input:
            head:    str, head of fastq entry.
            body:    str, body of fastq entry.
            qstr:    str, quality string.
        """
        if head.startswith("@"):
            self.head = head
        else:
            self.head = f"@{head}"

        self.body = body
        self.qstr = qstr
        if not len(self.body) == len(self.qstr):
            raise RuntimeError("Quality-string has not the same length as the sequence.")

    def __str__(self) -> str:
        """
        Magic method to allow fastq_object printing.
        """
        return f'{self.head}\n{self.body}\n+\n{self.qstr}'

    def __repr__(self) -> str:
        """
        Magic method to allow printing of fastq_object representation.
        """
        return f'fastq_object("{self.head}", "{self.body}", """{self.qstr}""")'

    def __eq__(self, o) -> bool:
        """
        Magic method to allow equality check on fastq_objects.
        Does not check for header or quality equality.
        """
        return self.body == o.body  # type:ignore

    def __len__(self) -> int:
        """
        Magic method to allow len() on fastq_objects.
        Does not check for header-length equality.
        """
        return len(self.body)

    def toFasta(self) -> fasta_object:
        """
        Converts fastq_object to fasta_object of miniFasta package.
        Quality String will be dropped.
        """
        return fasta_object(self.head[1:], self.body)


def print_fastq(fastq) -> None:
    """
    Prints a single or a list of fastq_objects.
    """

    if not isinstance(fastq, list):
        fastq = [fastq]

    for fq in fastq:
        print(fq)
    return None

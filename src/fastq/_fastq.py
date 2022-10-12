"""
fastq: A simple toolbox for fastq files

See: https://github.com/not-a-feature/fastq
Or:  https://pypi.org/project/fastq/

@author: Jules Kreuer / not_a_feature
License: GPL-3.0
"""

from miniFasta import fasta_object
from statistics import mean, median, variance
from typing import Dict
from dataclasses import dataclass


@dataclass
class fastq_object:
    head: str
    body: str
    qstr: str

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

        self.body: str = body
        self.qstr: str = qstr

        self._lazyInfo = False
        self.info = dict()

        if not len(self.body) == len(self.qstr):
            raise RuntimeError("Quality-string has not the same length as the sequence.")

    def getHead(self) -> str:
        """
        Getter method to return the head / sequence id.
        """
        return self.head

    def getSeq(self) -> str:
        """
        Getter method to return the sequence.
        """
        return self.body

    def getQual(self) -> str:
        """
        Getter method to return the quality string.
        """
        return self.qstr

    def getInfo(self) -> Dict[str, float]:
        """
        Returnes summary statistics of this fastq_object as dict.
        """
        return self.info

    @property  # type: ignore
    def body(self) -> str:
        """
        Property function to return body.
        """
        return self._body  # type: ignore

    @body.setter
    def body(self, value: str) -> None:
        """
        Reset summary statistics when setting a new body.
        """
        self._lazyInfo = False
        self._info = dict()  # type: Dict[str, float]
        self._body = value

    @property  # type: ignore
    def qstr(self) -> str:
        """
        Property function to return qstr.
        """
        return self._qstr  # type: ignore

    @qstr.setter
    def qstr(self, value: str) -> None:
        """
        Reset summary statistics when setting a new qstr.
        """
        self._lazyInfo = False
        self._info = dict()
        self._qstr = value

    @property
    def info(self) -> Dict[str, float]:
        """
        Returnes summary statistics of this fastq_object as dict.
        """
        if self._lazyInfo:
            self._info = info(self)
            self._lazyInfo = True
        return self._info

    @info.setter
    def info(self, value: Dict[str, float]) -> None:
        """
        Property function to set info.
        """
        self._info = value
        self._lazyInfo = True

    def __str__(self) -> str:
        """
        Magic method to allow fastq_object printing.
        """
        return f"{self.head}\n{self.body}\n+\n{self.qstr}"

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

    def __hash__(self):
        """
        Magic method to allow hash() on fastq_objects.
        """
        return hash(self.head + self.body + self.qstr)

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


def info(fastq: fastq_object) -> Dict[str, float]:
    """
    Computes summary statistics of a fastq file.
    This assumes that the quality score is encoded using the ACII + 33 formula (Illumina Encoding).
    """
    body = fastq.body.upper()
    a_num = sum((1 if b == "A" else 0 for b in body))
    g_num = sum((1 if b == "G" else 0 for b in body))
    t_num = sum((1 if b == "T" else 0 for b in body))
    c_num = sum((1 if b == "C" else 0 for b in body))

    gc_content = (g_num + c_num) / len(body)
    at_content = 1 - gc_content

    phred_scores = [ord(q) - 33 for q in fastq.qstr]

    phred_scores.sort()

    qual_mean = mean(phred_scores)
    qual_median = median(phred_scores)
    qual_var = variance(phred_scores)
    qual_min = phred_scores[0]
    qual_max = phred_scores[-1]

    summary = {
        "a_num": a_num,
        "g_num": g_num,
        "t_num": t_num,
        "c_num": c_num,
        "gc_content": gc_content,
        "at_content": at_content,
        "qual": qual_mean,
        "qual_median": qual_median,
        "qual_variance": qual_var,
        "qual_min": qual_min,
        "qual_max": qual_max,
    }

    return summary

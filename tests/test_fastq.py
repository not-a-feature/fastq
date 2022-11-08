import fastq as fq

from os import path, remove
from miniFasta import fasta_object

test0 = [
    fq.fastq_object(
        head="@M01967:23:000000000-AG773:1:1001:09936:3208 1:N:0:290",
        body="GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT",
        qstr="!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65",
    ),
    fq.fastq_object(head="@Mini", body="ATGC", qstr="!!!!"),
]


def test_write_read():
    file_path = path.join(path.dirname(__file__), "write_fastq_test.fastq")

    fq_list = [
        fq.fastq_object("@AQ", "ACGTACGTCATG", "!-!-!-!-!-!-"),
        fq.fastq_object("@PQ", "ACGTACGTCA", "LLLLLLLLLL"),
    ]

    fq.write(fq_list, file_path)

    fq_read = list(fq.read(file_path))
    remove(file_path)
    assert fq_list == fq_read


def test_write_byself():
    file_path = path.join(path.dirname(__file__), "write_fastq_test.fastq")

    fq_single = fq.fastq_object("@Pacific dolphin", "ZHUJ", "ACAC")

    fq_single.write(file_path)

    fo_read = list(fq.read(file_path))
    remove(file_path)
    assert [fq_single] == fo_read


def test_print_fastq_by_func(capsys):
    file_path = path.join(path.dirname(__file__), "test_data/test0.fastq")
    fq_list = list(fq.read(file_path))
    fq.print_fastq(fq_list)

    # check if it prints the sequences correctly
    c = capsys.readouterr()
    assert (
        c.out
        == """@M01967:23:000000000-AG773:1:1001:09936:3208 1:N:0:290
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
+
!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
@Mini
ATGC
+
!!!!
"""
    )


def test_len_fastq():
    assert len(fq.fastq_object("@test", "abc", "abc")) == 3


def test_str_fastq():
    assert str(fq.fastq_object("test", "abc", "---")) == "@test\nabc\n+\n---"


def test_eq_fastq():
    foa = fq.fastq_object("@test", "abc", "!!!")
    fob = fq.fastq_object("@different header", "abc", "!!!")
    foc = fq.fastq_object("@different body", "zzz", "!!!")

    assert foa == foa
    assert fob == foa
    assert foa == fob
    assert not foa == foc
    assert not foc == foa


def test_hash_fastq():
    foa = fq.fastq_object("@test", "abc", "!!!")
    fob = fq.fastq_object("@test", "abc", "!!!")
    foc = fq.fastq_object("@different header", "abc", "!!!")

    assert hash(foa) == hash(fob)
    assert not hash(fob) == hash(foc)


def test_getter():
    fo = fq.fastq_object("@test", "abc", "!!!")
    assert fo.head == fo.getHead()
    assert fo.body == fo.getSeq()
    assert fo.qstr == fo.getQual()


def test_fastqTofasta():
    fa = fasta_object(">Test", "AGTC")
    fq_single = fq.fastq_object("@Test", "AGTC", "!!!!")

    assert fq_single.toFasta() == fa

import fastq as fq
import pytest
from os import path


test0 = [
    fq.fastq_object(
        head="@M01967:23:000000000-AG773:1:1001:09936:3208 1:N:0:290",
        body="GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT",
        qstr="!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65",
    ),
    fq.fastq_object(head="@Mini", body="ATGC", qstr="!!!!"),
]

longBody = "".join(
    [
        "GACCGCCTCCTGCCAATAAGAGCTAACGCGCACAGGTACGCGT",
        "AAGACCGTGTGCACGAACGCATTCCGAACGCAATACGATTAAGAACCCAAG",
    ]
)
longQstr = "".join(
    [
        """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMN""",
        """OPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~""",
    ]
)  # noqa: W605

test1 = [
    fq.fastq_object(head="@HWUSI-EAS100R:6:73:941:1973#0/", body=longBody, qstr=longQstr),
    fq.fastq_object(
        head="@SRR001666.1 071112_SLXA-EAS1_s_7:5:1:817:345 length=36",
        body="GGGTGATGGCCGCTGCCGATGGCGTCAAATCCCACC",
        qstr="IIIIIIIIIIIIIIIIIIIIIIIIIIIIII9IG9IC",
    ),
]

multi = test0.copy()
multi.extend(test1)


@pytest.mark.parametrize(
    "file_path, expected",
    [
        (path.join(path.dirname(__file__), "test_data/test0.fastq"), test0),
        (path.join(path.dirname(__file__), "test_data/test1.fastq"), test1),
        (path.join(path.dirname(__file__), "test_data/test.fastq.zip"), test0),
        (path.join(path.dirname(__file__), "test_data/test.fastq.tar"), test0),
        (path.join(path.dirname(__file__), "test_data/test.fastq.tar.gz"), test0),
        (path.join(path.dirname(__file__), "test_data/test.fastq.gz"), test0),
        (path.join(path.dirname(__file__), "test_data/test.multi.zip"), multi),
        (path.join(path.dirname(__file__), "test_data/test.multi.tar"), multi),
        (path.join(path.dirname(__file__), "test_data/test.multi.tar.gz"), multi),
    ],
)
def test_read(file_path, expected):
    assert list(fq.read(file_path)) == expected

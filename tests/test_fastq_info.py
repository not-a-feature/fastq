import fastq as fq


def test_fastq_info():
    fo = fq.fastq_object(
        "@test",
        "ACGTACGTACGTACGTACGTTTTTTAAAAAAAAAAAAAAAA",
        """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI""",
    )

    info = fo.info
    info2 = fo.getInfo()
    assert info == info2
    assert info["a_num"] == 21
    assert info["c_num"] == 5
    assert info["g_num"] == 5
    assert info["t_num"] == 10
    assert info["gc_content"] == 10 / 41
    assert info["qual"] == 20
    assert info["qual_min"] == 0
    assert info["qual_max"] == 40

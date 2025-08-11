<img src="https://github.com/not-a-feature/fastq/raw/main/fastq.png" width=300px alt="fastq logo"></img>

A simple FASTQ toolbox for small to medium size projects without strange dependencies.

[![DOI](https://zenodo.org/badge/450063403.svg)](https://zenodo.org/badge/latestdoi/450063403)
![Test Badge](https://github.com/not-a-feature/fastq/actions/workflows/tests.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Download Badge](https://img.shields.io/pypi/dm/fastq.svg)
![Python Version Badge](https://img.shields.io/pypi/pyversions/fastq)


FASTQ files are text-based files for storing nucleotide sequences and its corresponding quality scores.
Reading such files is not particularly difficult, yet most off the shelf packages are overloaded with strange dependencies.

fastq offers an alternative to this and brings many useful functions without relying on third party packages.

## Installation
Using pip  / pip3:
```bash
pip install fastq
```
Or by source:
```bash
git clone git@github.com:not-a-feature/fastq.git
cd fastq
pip install .
```

## How to use
fastq offers easy to use functions for fastq handling.
The main parts are:
- read()
- write()
- fastq_object()
    - head
    - body
    - qstr
    - info
    - toFasta()
    - len() / str() / eq()

## Reading FASTQ files
`read()` is a fastq reader which is able to handle compressed and non-compressed files.
Following compressions are supported: zip, tar, tar.gz, gz. If multiple files are stored inside an archive, all files are read.
This function returns a iterator of fastq_objects.

```python
import fastq as fq
fos = fq.read("dolphin.fastq") # Iterator of fastq entries.
fos = list(fos) # Cast to list
fos = fq.read("reads.tar.gz") # Is able to handle compressed files.
```

### fastq_object()
The core component of fastq is the ```fastq_object()```.

This object represents an FASTQ entry and consists of a head and body.

```python
import fastq as fq
fo = fq.fastq_object("@M01967:23:0", "GATTTGGGG", "!''*((((*")
fo.getHead() or fo.head # @M01967:23:0
fo.getSeq()  or fo.body # GATTTGGGG
fo.getQual() or fo.qstr # !''*((((*
```

When `fastq_object(..).info` is requested, some summary statistics are computed and returned as dict.
This computation is "lazy". I.e. the first query takes longer than the second.
If the body or qstr is changed, info is automatically reset.

```python
fo.getInfo() or fo.info
{'a_num': 1, 'g_num': 5,             # Absolute counts of AGTC
 't_num': 3, 'c_num': 0,             #
 'gc_content': 0.5555555555555556,   # Relative GC content
 'at_content': 0.4444444444444444,   # Relative AT content
 'qual': 6.444444444444445,          # Mean quality (Illumina Encoding)
 'qual_median': 7,                   # Median quality
 'qual_variance': 7.027777777777778, # Variance of quality
 'qual_min': 0, 'qual_max': 9}       # Min / Max quality
```

### Following methods are defined on a `fastq_object()`:

```python
str(fo) # will return:
# @M01967:23:0
# GATTTGGGG
# +
# !''*((((*


# Body length
len(fo) # will return 10, the length of the body

# Equality
# Checks only the body, not the header and not the quality string
print(fo == fo) # True

fo_b = fq.fastq_object("@different header", "GATTTGGGG", "!!!!!!!!!")
print(fo == fo_b) # True

fo_c = fq..fastq_object(">Different Body", "ZZZZ", "!--!")
print(fo == fo_c) # False
```

## Writing FASTQ files
`write()` is a basic fastq writer.
It takes a single or a list of fastq_objects and writes it to the given path.

The file is usually overwritten. Set `write(fo, "path.fastq", mode="a")` to append file.

```python
fos = fq.read("dolphin.fastq") # Iterator of fastq entries
fos = list(fos)

fq.write(fos, "new.fastq")
```

## License

Copyright (C) 2024 by Jules Kreuer - @not_a_feature

This piece of software is published unter the GNU General Public License v3.0
TLDR:

| Permissions      | Conditions                   | Limitations |
| ---------------- | ---------------------------- | ----------- |
| ✓ Commercial use | Disclose source              | ✕ Liability |
| ✓ Distribution   | License and copyright notice | ✕ Warranty  |
| ✓ Modification   | Same license                 |             |
| ✓ Patent use     | State changes                |             |
| ✓ Private use    |                              |             |

Go to [LICENSE.md](https://github.com/not-a-feature/fastq/blob/main/LICENSE) to see the full version.

![fastq](https://github.com/not-a-feature/fastq/raw/main/fastq.png)

A simple FASTA toolbox for small to medium size projects without dependencies.

![Test Badge](https://github.com/not-a-feature/fastq/actions/workflows/tests.yml/badge.svg)
![Python Version Badge](https://img.shields.io/pypi/pyversions/fastq)
![Download Badge](https://img.shields.io/pypi/dm/fastq.svg)

FASTA files are text-based files for storing nucleotide or amino acid sequences.
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
The five main parts are:
- fastq_object()
    - toFasta()
    - len() / str() / eq()
- read()
- write()


### fastq_object()
The core component of fastq is the ```fastq_object()```. This object represents an FASTA entry and consists of a head and body.

```python 
import fastq as fq
fo = fq.fastq_object("@M01967:23:0", "GATTTGGGG", "!''*((((*")
print(fo.head) # @M01967:23:0
print(fo.body) # GATTTGGGG
print(fo.qstr) # !''*((((*

### Following functions are defined on a fastq_object():

str(fo) # will return:
# @M01967:23:0
# GATTTGGGG
# +
# !''*((((*


# Body length
len(fo) # will return 10, the length of the body

# Equality 
print(fo == fo) # True
    
fo_b = fq.fastq_object("@different header", "GATTTGGGG", "!!!!!!!!!")
print(fo == fo_b) # True

fo_c = fq..fastq_object(">Different Body", "ZZZZ", "!--!")
print(fo == fo_c) # False
```

## Reading FASTQ files
`read()` is a fastq reader which is able to handle compressed and non-compressed files.
Following compressions are supported: zip, tar, tar.gz, gz. If multiple files are stored inside an archive, all files are read. 
This function returns a list of fastq_objects. 

```python
fos = fq.read("dolphin.fastq") # List of fastq entries.
fos = fq.read("reads.tar.gz") # Is able to handle compressed files.
```

## Writing FASTA files
`write()` is a basic fastq writer.
It takes a single or a list of fastq_objects and writes it to the given path. 

The file is usually overwritten. Set `write(fo, "path.fastq", mode="a")` to append file.

```python
fos = fq..read("dolphin.fastq") # List of fastq entries
fq..write(fos, "new.fastq")
```

## License
```
Copyright (C) 2021 by Jules Kreuer - @not_a_feature
This piece of software is published unter the GNU General Public License v3.0
TLDR:

| Permissions      | Conditions                   | Limitations |
| ---------------- | ---------------------------- | ----------- |
| ✓ Commercial use | Disclose source              | ✕ Liability |
| ✓ Distribution   | License and copyright notice | ✕ Warranty  |
| ✓ Modification   | Same license                 |             |
| ✓ Patent use     | State changes                |             |
| ✓ Private use    |                              |             |
```
Go to [LICENSE.md](https://github.com/not-a-feature/fastq/blob/main/LICENSE) to see the full version.

## Dependencies
In addition to packages included in Python 3, this piece of software uses 3rd-party software packages for development purposes that are not required in the published version.
Go to [DEPENDENCIES.md](https://github.com/not-a-feature/fastq/blob/main/DEPENDENCIES.md) to see all dependencies and licenses.
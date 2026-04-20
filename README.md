# tdiff

[![Build Status](https://github.com/davidbrochart/tdiff/workflows/test/badge.svg)](https://github.com/davidbrochart/tdiff/actions)

A Textual diff application.

## Usage

To diff two files:
```bash
tdiff path/to/file1 path/to/file2
```

To diff git changes:
```bash
tdiff git  # shows local git changes
tdiff git HEAD~1
tdiff git 1a5d251eacd5a146d710f436592815ac2efa1b52
```

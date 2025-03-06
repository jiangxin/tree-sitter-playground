# tree-sitter-playground

[English](README.md) | [简体中文](README.zh-CN.md)

[tree-sitter](https://tree-sitter.github.io/tree-sitter/) is a widely used code parsing tool that supports many programming languages and can parse code into an Abstract Syntax Tree (AST). The official website provides an [online playground](https://tree-sitter.github.io/tree-sitter/7-playground.html) that can convert code into AST in real-time.

However, the official playground has some limitations:
* Limited language support, while the `tree-sitter` command's built-in playground is complex to configure and run.
* The displayed AST only includes named nodes, anonymous nodes are not shown.
* The association between code and AST is one-way - you can only locate code by clicking AST nodes, but not vice versa.

## Features

`tree-sitter-playground` is a desktop application developed with Python + Qt/PySide6, providing better local tree-sitter code parsing visualization.

* Support for more languages.
* AST displays both named nodes and anonymous nodes (nodes starting with a dot).
* Bidirectional association between code and AST - clicking on code highlights AST nodes, and vice versa.

## Screenshots

Rich language support:

![Supported languages](images/languages.png)

Bidirectional association between code and AST:

![tree-sitter-playground](images/tree-sitter-playground.png)

## Installation and Running

This software is developed in Python and can run on Python 3.6 or higher.

First, make sure Python is installed.

1. Clone the repository:

   ```bash
   git clone https://github.com/jiangxin/tree-sitter-playground.git
   cd tree-sitter-playground
   ```

2. Upgrade pip. For lower versions like Python 3.7, without upgrading pip, you may not be able to find matching PySide6 packages.

   ```bash
   python -m pip install -U pip
   ```

3. Install Python dependencies:

   For Python 3.9 or higher, run:

   ```bash
   pip install -r requirements.txt
   ```

   For Python 3.6 ~ 3.8, run:

   ```bash
   pip install -r requirements/py36.txt
   ```

4. Run tree-sitter-playground:

   ```bash
   python tree-sitter-playground.py
   ```

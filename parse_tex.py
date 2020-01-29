#!/bin/bash
NOTEBOOK_DIR=/Users/mark/Dropbox/duke/local/notes/lab_notebook/
STANDALONE_DIR=/Users/mark/Dropbox/duke/local/notes/lab_notebook/latex/standalone_tex_docs/
LATEX_DIR=/Users/mark/Dropbox/duke/local/notes/lab_notebook/latex/
if [ ! -d ${STANDALONE_DIR} ]; then
    mkdir ${STANDALONE_DIR}
fi
for file in ${NOTEBOOK_DIR}*.ipynb; do jupyter nbconvert --to latex ${file}; done
mv ${NOTEBOOK_DIR}*.tex ${STANDALONE_DIR}
mv ${NOTEBOOK_DIR}*_files ${LATEX_DIR}
parse_tex.py

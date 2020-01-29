#!/usr/local/bin/python3
import os
import datetime

def write_body_to_file(file_string, save_to):
    '''Write the main body of LaTex file *file_string* (the portion after the
    preamble, encapsulated by the begin{document} and end{document} commands)
    to a new file *save_to*
    '''
    if not os.path.exists(os.path.dirname(save_to)):
        os.makedirs(os.path.dirname(save_to))
    if os.path.exists(file_string):
        with open(file_string, 'r') as f, open(save_to, 'w') as g:
            start_recording = False
            for line in f:
                if line.strip() == r'\maketitle':
                    start_recording = True
                    continue
                if line.startswith(r'\end{document}'):
                    break
                if start_recording:
                    g.write(line)
    return 0

def get_lab_pages(path):
    '''Get the names of jupyter notebooks in path, and return them
    in a sorted list.  Does not enter subdirectories.
    '''
    file_gen = os.walk(path)
    dirpath, dirnames, filenames = next(file_gen)
    lab_pages = []
    for f in filenames:
        if f.endswith('.ipynb'):
            lab_pages.append(f)
    sorted_lab_pages = sorted(lab_pages)
    return dirpath, sorted_lab_pages

def make_lab_notebook_pages(path_to_standalone_tex, write_to):
    '''Create files containing only the main body of all LaTex files contained
    in the directory *path_to_standalone_tex*, and save them into the
    directory *write_to*.  The new files are saved with names old_name.tex -->
    old_name_body.tex.
    '''
    dirpath, sorted_tex_files = get_tex_files(path_to_standalone_tex)
    for page in sorted_tex_files:
        save_to = write_to + page.strip('.tex') + '_body.tex'
        write_body_to_file(os.path.join(dirpath,page), save_to)
    return 0

def get_tex_preamble(tex_file):
    '''Return a string containing only the LaTeX preamble for the LaTeX file
    *tex_file*, starting with the line after documentclass{}
    '''
    preamble_string = ''
    with open(tex_file, 'r') as fil:
        for line in fil:
            if line.strip().startswith(r'\documentclass'):
                continue
            if line.startswith(r'\begin{document}'):
                break
            preamble_string += line
    return preamble_string

def get_tex_files(path_to_tex):
    '''Returns *dirpath*, the path to the directory *path_to_tex*, and a list
    of all LaTeX files in *path_to_tex*, sorted alphabetically.
    '''
    file_gen = os.walk(path_to_tex)
    dirpath, dirnames, filenames = next(file_gen)
    tex_files = []
    for f in filenames:
        if f.endswith('.tex'):
            tex_files.append(f)
    return dirpath, sorted(tex_files)


def create_tex_notebook(write_to, tex_source, preamble_source, notebook_name):
    '''Write a new file in directory *write_to*, with file name
    *notebook_name*.  The new file is a latex report with chapters specified
    by a list of latex body-only files stored in the directory *tex_source*,
    with preamble taken from a LaTeX file *preamble_source*.
    '''
    tex_dirpath, tex_files = get_tex_files(tex_source)
    preamble = get_tex_preamble(preamble_source)
    with open(write_to + notebook_name, 'w') as f:
        f.write(r'\documentclass[11pt]{report}' + '\n')
        f.write(r'\usepackage{hyperref}' + '\n')
        f.write(preamble)
        f.write(r'\begin{document}')
        f.write('\n')
        f.write(r'\tableofcontents')
        f.write('\n')
        for tex_f in tex_files:
            date = tex_f[0:8]
            year = int(date[0:4])
            month = int(date[4:6])
            day = int(date[6:8])
            _day = datetime.date(year, month, day)
            calendar = _day.strftime('%b %d, %Y')
            f.write('\\chapter*{{{}}}\n'.format(calendar))
            f.write('\\addcontentsline{{toc}}{{chapter}}{{{}}}\n'.format(calendar))
            f.write('\\input{{{}}}\n'.format('body_tex_docs/' + tex_f))
        f.write(r'\end{document}')

write_to = '/Users/mark/Dropbox/duke/local/notes/lab_notebook/latex/body_tex_docs/'
path_to_standalone_tex = '/Users/mark/Dropbox/duke/local/notes/lab_notebook/latex/standalone_tex_docs/'
write_tex_path = '/Users/mark/Dropbox/duke/local/notes/lab_notebook/latex/'
tex_source = '/Users/mark/Dropbox/duke/local/notes/lab_notebook/latex/body_tex_docs/'
preamble_source = '/Users/mark/Dropbox/duke/local/notes/lab_notebook/latex/standalone_tex_docs/20200118.tex'

make_lab_notebook_pages(path_to_standalone_tex, write_to)
create_tex_notebook(write_tex_path, tex_source, preamble_source, 'full_notebook.tex')


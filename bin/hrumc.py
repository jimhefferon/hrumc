#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run the abstracts from the Hudson River Undergrad Math Conference.
"""
__version__ = '0.9.5'
__author__ = 'Jim Hefferon jhefferon at smcvt.edu'
__license__ = 'GPL 3'

import sys, os, os.path, re, pprint, argparse, traceback, time
import tempfile, shutil, glob
import subprocess

# Global variables spare me from putting them in the call of each fcn.
VERBOSE = False
DEBUG = False

class HRUMCException(Exception):
    pass


def warn(s):
    t = 'WARNING: '+s+"\n"
    sys.stderr.write(t)
    sys.stderr.flush()

def error(s):
    t = 'ERROR! '+s
    sys.stderr.write(t)
    sys.stderr.flush()
    sys.exit(10)

LATEX_INCLUDE_FN = "abs"
LATEX_TEMPLATE = r"""\documentclass[12pt]{article}
\usepackage{cmap}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb} 
\usepackage[T1]{fontenc} 
\usepackage{fbb}

\usepackage{ragged2e} %% for RaggedRight

\newcommand{\abstracttitle}[1]{\textbf{#1}}
\newcommand{\abstractlevel}[1]{\textrm{This talk is Level~#1}}
\newcommand{\abstractspeaker}[1]{\textsc{#1}}

%% Abstract 
%% #1 title 
%% #2 author 
%% #3 level 
%% #4 abstract body
\renewcommand{\abstract}[4]{%% \newcommand is \long by default
   \begin{center} \abstracttitle{#1} \end{center}
   \begin{center} \abstractspeaker{#2} \end{center} 
   \begin{center} \abstractlevel{#3} \end{center} 
   \noindent #4 
} 
\pagestyle{empty}
\begin{document}\thispagestyle{empty} 
\include{%s} 
\end{document}
""" % (LATEX_INCLUDE_FN,)


LATEX_ALL_TEMPLATE_TOP = r"""\documentclass[11pt]{article}
\usepackage{cmap}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb} 
\usepackage[T1]{fontenc} 
\usepackage{fbb}
\usepackage[top=0.5in,bottom=0.75in,right=0.5in]{geometry}

\usepackage{ragged2e} %% for RaggedRight
\newcommand{\abstracttitle}[1]{\textbf{#1}}
\newcommand{\abstractlevel}[1]{\textrm{(Level~#1)}}
\newcommand{\abstractspeaker}[1]{\textsc{#1}}

%% Abstract 
%% #1 title 
%% #2 author 
%% #3 level 
%% #4 abstract body
\renewcommand{\abstract}[4]{%% \newcommand is \long by default
   \abstracttitle{#1} \\
   \abstractlevel{#3}  
   \abstractspeaker{#2} \\
   \noindent #4 
} 
\pagestyle{plain}
\begin{document}\RaggedRight
"""



def latex_each(fn,pdfdirname="/output/"):
    """Make a temp dir, copy the file to it, run latex there,
    and copy the .pdf back
    """
    starting_dir = os.getcwd()
    # make a tmp dir and go there
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
    os.mkdir('tmp')
    tmp_dir_name = tempfile.mkdtemp(prefix='tmp', dir='tmp')
    os.chdir(tmp_dir_name)
    shutil.copyfile(starting_dir+'/'+fn,'./'+LATEX_INCLUDE_FN+'.tex')
    # Write the template to the basename of the included file
    jobname = os.path.splitext(os.path.basename(fn))[0]
    if VERBOSE:
        print("  LaTeX-ing the file",jobname+'.')
    f = open(jobname+'.tex','w')
    f.write(LATEX_TEMPLATE)
    f.close()
    # run pdflatex
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    subprocess.call(['pdfcrop','--margins','12',jobname+'.pdf'],stdout=subprocess.DEVNULL)
    # subprocess.call(['dvips','-E',jobname+'.dvi','-o',jobname+'.eps'],stdout=subprocess.DEVNULL)
    # subprocess.call(['ps2pdf',jobname+'.eps', jobname+'.pdf'],stdout=subprocess.DEVNULL)
    shutil.copyfile('./'+jobname+'-crop.pdf', pdfdirname+'/'+jobname+'.pdf')
    # clean up
    os.chdir(starting_dir)
    shutil.rmtree('tmp')


def latex_all(jobname, filelist):
    """Make a temp dir, copy all files to it, run latex there to create a 
    single doc, and copy the .pdf back
    """
    starting_dir = os.getcwd()
    # make a tmp dir
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
    os.mkdir('tmp')
    tmp_dir_name = tempfile.mkdtemp(prefix='tmp', dir='tmp')
    # copy all the .tex files to the tmp dir
    for fn in filelist:
        shutil.copyfile(starting_dir+'/'+fn,tmp_dir_name+'/'+fn)
    # go to the tmp dir
    os.chdir(tmp_dir_name)
    # Write the template and include all the .tex files
    f = open(jobname+'.tex','w')
    f.write(LATEX_ALL_TEMPLATE_TOP)
    for fn in filelist:
        print(r"\medskip\par\noindent\llap{%s:\ }\input{%s}" % (fn, fn),file=f)
    print(r"\end{document}",file=f)
    f.close()
    if VERBOSE:
        print("  LaTeX-ing the file of all abstracts: ",jobname+'.')
    # run pdflatex
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    shutil.copyfile('./'+jobname+'.pdf', starting_dir+'/'+jobname+'.pdf')
    # clean up
    os.chdir(starting_dir)
    shutil.rmtree('tmp')


OUTPUT_DIR_NAME = os.getcwd()+'/output'
#==================================================================
def main (args):
    # create a clean output dir
    if os.path.isdir(OUTPUT_DIR_NAME):
        shutil.rmtree(OUTPUT_DIR_NAME)
    os.mkdir(OUTPUT_DIR_NAME)
    # get all .tex files in this dir
    filelist = glob.glob("*.tex")
    filelist.sort()
    for fn in filelist:
        # for each .tex file, run latex
        latex_each(fn, pdfdirname=OUTPUT_DIR_NAME)
    latex_all('hrumcall',filelist)

#==================================================================
if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=globals()['__doc__'])
        parser.add_argument('-v','--version', action='version', version='%(prog)s '+globals()['__version__'])
        parser.add_argument('-D', '--debug', action='store_true', default=False, help='run debugging code')
        parser.add_argument('-V', '--verbose', action='store_true', default=False, help='verbose output')
        args = parser.parse_args()
        args = vars(args)
        if ('debug' in args) and args['debug']: 
            DEBUG = True
        if ('verbose' in args) and args['verbose']: 
            VERBOSE = True
        main(args)
        if VERBOSE: 
            print('elapsed secs: ', "%0.2f" % (time.time()-start_time,))
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print('UNEXPECTED OUTCOME')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

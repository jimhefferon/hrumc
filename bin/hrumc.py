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

DEFAULT_PROGRAM_NAME = "hrumc2016.tex"  # name of the conference program

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
\newcommand{\affiliation}[1]{ (#1)}

%% Abstract 
%% #1 title 
%% #2 author 
%% #3 level 
%% #4 subject
%% #5 abstract body
\renewcommand{\abstract}[5]{%% \newcommand is \long by default
   \begin{center} \abstracttitle{#1} \end{center}
   \begin{center} \abstractspeaker{#2} \end{center} 
   \begin{center} \abstractlevel{#3} \end{center} 
   \noindent #5
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
\newcommand{\abstractlevel}[1]{\textit{Level~#1}}
\newcommand{\abstractspeaker}[1]{\textsc{#1}}
\newcommand{\affiliation}[1]{ (#1)}
\newcommand{\abstractsubject}[1]{\textrm{#1}}

%% Abstract 
%% #1 title 
%% #2 author 
%% #3 level 
%% #4 subject 
%% #5 abstract body
\renewcommand{\abstract}[5]{%% \newcommand is \long by default
   \abstractsubject{#4} 
   \abstractlevel{#3}  \\
   \abstracttitle{#1} \\
   \abstractspeaker{#2} \\ 
   \noindent #5 
} 
\pagestyle{plain}
\begin{document}\RaggedRight
"""


LATEX_ROOMS_TEMPLATE_TOP = r"""\documentclass[12pt]{article}
\usepackage{cmap}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb} 
\usepackage[T1]{fontenc} 
\usepackage{fbb}
\usepackage[top=0.75in,bottom=0.75in,right=1in,left=1in]{geometry}

\usepackage{ragged2e} %% for RaggedRight
\usepackage{enumitem} %% for description

\newcommand{\sessionhead}[1]{\vspace*{3ex}\begin{center}\Large \textbf{Session #1}\end{center}}
\newcommand{\session}[3]{\begin{center}{\large \textbf{#1}} \\[1ex] Chair: #3\end{center}}
\newcommand{\at}[2]{%
  \begin{description}[font=\normalfont,leftmargin=2em,labelwidth=0em,topsep=0ex plus 1pt] 
    \RaggedRight
    \item[\abstracttime{#1}]
    \input{#2}
  \end{description}
}
\newcommand{\abstracttime}[1]{#1}
% Times
\newcommand{\timeformat}[2]{#1:#2}
\newcommand{\Ia}{\timeformat{10}{00}-\timeformat{10}{15}}
\newcommand{\Ib}{\timeformat{10}{20}-\timeformat{10}{35}}
\newcommand{\Ic}{\timeformat{10}{40}-\timeformat{10}{55}}
\newcommand{\IIa}{\timeformat{1}{40}-\timeformat{1}{55}}
\newcommand{\IIb}{\timeformat{2}{00}-\timeformat{2}{15}}
\newcommand{\IIc}{\timeformat{2}{20}-\timeformat{2}{35}}
\newcommand{\IIIa}{\timeformat{3}{30}-\timeformat{3}{45}}
\newcommand{\IIIb}{\timeformat{4}{00}-\timeformat{4}{15}}
\newcommand{\IIIc}{\timeformat{4}{20}-\timeformat{4}{35}}

\newcommand{\abstracttitle}[1]{\textbf{#1}}
\newcommand{\abstractlevel}[1]{\textrm{Level~#1}}
\newcommand{\abstractspeaker}[1]{\textsc{#1}}
\newcommand{\affiliation}[1]{ (#1)}

%% Abstract 
%% #1 title 
%% #2 author 
%% #3 level 
%% #4 subject 
%% #5 abstract body
\renewcommand{\abstract}[5]{%% \newcommand is \long by default
   \abstracttitle{#1} 
   \abstractspeaker{#2} 
   \abstractlevel{#3}  
} 

\newenvironment{room}[1]{%
  \begin{center}\fontsize{60}{75}\selectfont #1\end{center}
  \vspace*{-2ex}
}{%
  \clearpage
}

\pagestyle{empty}
\begin{document}\RaggedRight
"""


def make_rooms(inputfn, filelist, outputfn="rooms"):
    """Make the signs for the rooms.
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
    # regexes for reading the file
    sessionhead_re = re.compile(r"\\sessionhead\{([^\}]*)\}.*")
    session_re = re.compile(r"\\session\{([^\}]*)\}\{([^\}]*)\}\{([^\}]*)\}.*")
    at_re = re.compile(r"\\at\{([^\}]*)\}\{([^\}]*)\}.*")
    # There are two passes.  First we get the rooms, then we stuff the map
    rooms = {}  # map room number -> list of strings 
    # get the rooms
    fin = open(starting_dir+'/'+inputfn,'r')
    state = "BEFORE_PARALLEL_SESSIONS"
    linenumber = 0
    for line in fin:
        linenumber += 1
        if state == "BEFORE_PARALLEL_SESSIONS":
            if line.startswith("% ===== BEGIN PARALLEL SESSIONS"):
                state = "IN_PARALLEL_SESSIONS"
        elif state == "IN_PARALLEL_SESSIONS":
            if line.startswith("\session{"): # contains a room name
                m = session_re.match(line)
                if m:
                    rooms[m.group(2)]=[]
                else:
                    raise HRUMCException('Expected a match for line number '+str(linenumber)+', the line '+line)
            elif line.startswith("% ===== END PARALLEL SESSIONS"):
                state = "AFTER_PARALLEL_SESSIONS"
        if state == "AFTER_PARALLEL_SESSIONS":
            pass
    fin.close()
    if DEBUG:
        print("DEBUG: first pass Rooms:",rooms)
    # populate the rooms
    fin = open(starting_dir+'/'+inputfn,'r')
    parallelsessionnumber = None
    sessionname, sessionroom, sessionchair = None, None, None
    attime, atabstract  =  None, None
    state = "BEFORE_PARALLEL_SESSIONS"
    linenumber = 0
    for line in fin:
        linenumber +=1
        if state == "BEFORE_PARALLEL_SESSIONS":
            if line.startswith("% ===== BEGIN PARALLEL SESSIONS"):
                state = "IN_PARALLEL_SESSIONS"
        elif state == "IN_PARALLEL_SESSIONS":
            if line.startswith("\\sessionhead{"): # new parallel session
                m = sessionhead_re.match(line)
                if m:
                    parallelsessionnumber = m.group(1)
                    for k in rooms:
                        rooms[k].append("\\sessionhead{"+parallelsessionnumber+"}")
                else:
                    raise HRUMCException('Expected a match for the line number '+str(linenumber)+', session head line '+line)
            elif line.startswith("\\session{"):
                m = session_re.match(line)
                if m:
                    sessionname, sessionroom, sessionchair = m.group(1), m.group(2), m.group(3)
                    rooms[sessionroom].append("\\session{%s}{%s}{%s}" % (sessionname,sessionroom,sessionchair))
                else:
                    raise HRUMCException('Expected a match for line number '+str(linenumber)+', the session line '+line)
            elif line.startswith("\\at{"):
                # print("line starts with at")
                m = at_re.match(line)
                if m:
                    attime, atabstract = m.group(1), m.group(2)
                    rooms[sessionroom].append(r"\at{%s}{%s}" % (attime,atabstract))
                else:
                    raise HRUMCException('Expected a match for line number '+str(linenumber)+', the at line '+line)
            elif line.startswith("% ===== END PARALLEL SESSIONS"):
                state = "AFTER_PARALLEL_SESSIONS"
            else:
                pass  # blank line
        if state == "AFTER_PARALLEL_SESSIONS":
            pass
    fin.close()        
    if DEBUG:
        print("DEBUG: second pass Rooms:",rooms)
    # Make the output file
    fout = open(outputfn+'.tex','w')
    print(LATEX_ROOMS_TEMPLATE_TOP, file=fout)
    for k in rooms:
        print(r"\begin{room}{%s}" % (k,), file=fout)
        print("\n".join(rooms[k]), file=fout)
        print(r"\end{room}", file=fout)
    print(r"\end{document}", file=fout)
    fout.close()
    # shutil.copyfile('./'+jobname+'-crop.pdf', pdfdirname+'/'+jobname+'.pdf')
    # clean up
    os.chdir(starting_dir)
    # shutil.rmtree('tmp')



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
    """Make a single .pdf that contains all abstracts.
      jobname  Name of .pdf file
      filelist  List of all abstract .tex filenames
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
    filelist.remove(args['file'])
    filelist.sort()
    # for fn in filelist:
    #     latex_each(fn, pdfdirname=OUTPUT_DIR_NAME)
    latex_all('hrumcall',filelist)
    # make_rooms(args['file'],filelist)

#==================================================================
if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=globals()['__doc__'])
        parser.add_argument('-f','--file', action='store', default=DEFAULT_PROGRAM_NAME,help='name of the .tex of the program for the conference')
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

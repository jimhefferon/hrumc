#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run the abstracts from the Hudson River Undergrad Math Conference.  Optionally 
also generate a single doc with all abstracts, and also a doc of information 
for each room, incuding instructions for session chairs and a sign for the
door.
"""
__version__ = '1.0.0'
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
  \DeclareUnicodeCharacter{00A0}{~} %% no break space
\usepackage{amsmath,amssymb} 
\usepackage{xfrac}
\usepackage[T1]{fontenc} 
\usepackage{fbb}

\usepackage{ragged2e} %% for RaggedRight

\newcommand{\authorref}[2]{#1 #2}

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
%% Notes  Usedin some other docs to show whether presenter has requested 
%% special facilities, etc.
%%  #1 The notes
\newcommand{\notes}[1]{\relax}

\pagestyle{empty}
\begin{document}\thispagestyle{empty} 
\include{%s} 
\end{document}
""" % (LATEX_INCLUDE_FN,)


LATEX_ALL_TEMPLATE_TOP = r"""\documentclass[11pt]{article}
\usepackage{cmap}
\usepackage[utf8]{inputenc}
  \DeclareUnicodeCharacter{00A0}{~} %% no break space
\usepackage{amsmath,amssymb} 
\usepackage{xfrac}
\usepackage[T1]{fontenc} 
\usepackage{fbb}
\usepackage[top=0.5in,bottom=0.75in,right=0.5in]{geometry}

\usepackage{ragged2e} %% for RaggedRight

\newcommand{\authorref}[2]{#1 #2}

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
% Notes  Used to show whether presenter has requests
% special facilities, etc.
%  #1 The notes
\newcommand{\notes}[1]{\par\textit{NOTES:} #1}

\pagestyle{plain}
\begin{document}\RaggedRight
"""


LATEX_ROOMS_TEMPLATE_TOP = r"""\documentclass[12pt]{article}
\usepackage{cmap}
\usepackage[utf8]{inputenc}
  \DeclareUnicodeCharacter{00A0}{~} %% no break space
\usepackage{amsmath,amssymb} 
\usepackage{xfrac}
\usepackage[T1]{fontenc} 
\usepackage{fbb}
\usepackage[top=0.75in,bottom=0.75in,right=1in,left=1in]{geometry}

\usepackage{ragged2e} %% for RaggedRight
\usepackage{enumitem} %% for description

\newcommand{\sessionhead}[1]{\vspace*{3ex}\begin{center}\Large \textbf{Session #1}\end{center}}
\newcommand{\session}[3]{\begin{center}{\large \textbf{#1}} \\[1ex] Chair: #3\end{center}\vspace*{-0.5ex}}
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
\newcommand{\IId}{\timeformat{2}{40}-\timeformat{2}{55}}

\newcommand{\IIIa}{\timeformat{3}{30}-\timeformat{3}{45}}
\newcommand{\IIIb}{\timeformat{3}{50}-\timeformat{4}{05}}
\newcommand{\IIIc}{\timeformat{4}{10}-\timeformat{4}{25}}

\newcommand{\authorref}[2]{#1 #2}

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
%% Notes  Used in some other docs to show whether presenter has requested 
%% special facilities, etc.
%%  #1 The notes
\newcommand{\notes}[1]{\relax}

\newenvironment{room}[1]{%
  \begin{center}\fontsize{60}{75}\selectfont #1\end{center}
  \vspace*{-2ex}
}{%
  \clearpage
}

\pagestyle{empty}
\begin{document}\RaggedRight
"""


LATEX_CHAIR_TEMPLATE = r"""\documentclass[11pt]{article}
\usepackage{cmap}
\usepackage[utf8]{inputenc}
  \DeclareUnicodeCharacter{00A0}{~} %% no break space
\usepackage{amsmath,amssymb} 
\usepackage{xfrac}
\usepackage[T1]{fontenc} 
\usepackage{fbb}
\usepackage[top=0.5in,bottom=0.5in,right=1in,left=1in]{geometry}

\usepackage{ragged2e} %% for RaggedRight
\usepackage{enumitem} %% for description

\newcommand{\sessionhead}[1]{\vspace*{3ex}\begin{center}\Large \textbf{Chair Instructions for Parallel Session #1}\end{center}}
\newcommand{\session}[3]{\begin{center}{\large \textbf{Session name: #1}} \\[1ex]
  {\large \textbf{Room: #2}} \\[1ex] {\large \textbf{Chair: #3}}\end{center}\vspace*{0ex}}

\newcommand{\instructions}[3]{\setlength{\parindent}{2em}\setlength{\parskip}{.5ex}
Thank you for volunteering to be session chair.
\par
At the start of the session say, ``Welcome to #1.
I am the session chair, #3.
A word for speakers: we must keep strictly to the schedule.  
Each talk lasts fifteen minutes, with a few minutes afterward for questions.  
I will hold up five fingers to let you know when five minutes are left, 
and one finger for one minute.
Any overrun will come from the question period.''
\par
As session chair, your main job is to keep the session on time.
You need an accurate clock, such as your cell phone.
When there are five minutes left, hold up five fingers and make sure the speaker sees you.
When there is one minutes left, hold up one finger.
If the speaker runs over by two minutes then say, ``Sorry for interrupting but it is time to wrap up in a sentence or two.''
If the speaker is four minutes over then stand and say, ``I'm afraid that the time is complete and people need to be able to move to their next session.  Anyone with questions can approach the speaker later.''
\par
If a speaker ends early, or if a speaker does not show, 
do not start the next speaker early.
Instead wait for the scheduled time.
\par
In addition to managing the time, you should introduce each speaker before they start (try to speak to them between talks to find who is talking in a multi-author presentation and to see how to pronounce names).
After each talk, thank the speaker and initiate a brief applause.  
If there is time before the next speaker, ask if there are any questions.
In case there are no questions, during the talk you should prepare one.
After questions, again thank the speaker and introduce the next talk.
\par
Finally, if there are technology problems then you can either grab a student volunteer in the hallway or dial extension 2959 on the room phone.
\par\vspace*{2ex}
\begin{center}\large\textbf{Session schedule}\end{center}}

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
\newcommand{\IId}{\timeformat{2}{40}-\timeformat{2}{55}}

\newcommand{\IIIa}{\timeformat{3}{30}-\timeformat{3}{45}}
\newcommand{\IIIb}{\timeformat{3}{50}-\timeformat{4}{05}}
\newcommand{\IIIc}{\timeformat{4}{10}-\timeformat{4}{25}}

\newcommand{\authorref}[2]{#1 #2}

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
%% Notes  Used in some other docs to show whether presenter has requested 
%% special facilities, etc.
%%  #1 The notes
\newcommand{\notes}[1]{\relax}

\newenvironment{room}[1]{%
  \vspace*{1ex plus 0.5fill}
  \begin{center}
    \fontsize{40}{65}\selectfont 
    Session chair instructions: \\
    #1
  \end{center}
  \vspace*{1ex plus 1fill}
}{%
  \clearpage
}

\pagestyle{empty}
\setlength{\parindent}{2em}
\begin{document}\RaggedRight
"""


def make_rooms(inputfn, filelist, outputfn="rooms"):
    """Make the signs for the rooms.
    Assumes this is run from the 'input' directory, holding all the .tex 
    abstracts.
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
    try:
        fin = open(starting_dir+'/../'+inputfn,'r')
    except Exception as e:
        raise HRUMCException("unable to make rooms; unable to open "+inputfn+": "+str(e))
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
    chairs = {}
    for k in rooms:
        chairs[k] = rooms[k].copy()
    # populate the rooms
    fin = open(starting_dir+'/../'+inputfn,'r')
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
                        chairs[k].append("\\clearpage\\sessionhead{"+parallelsessionnumber+"}")
                else:
                    raise HRUMCException('Expected a match for the line number '+str(linenumber)+', session head line '+line)
            elif line.startswith("\\session{"):
                m = session_re.match(line)
                if m:
                    sessionname, sessionroom, sessionchair = m.group(1), m.group(2), m.group(3)
                    rooms[sessionroom].append("\\session{%s}{%s}{%s}" % (sessionname,sessionroom,sessionchair))
                    chairs[sessionroom].append("\\session{%s}{%s}{%s}\n" % (sessionname,sessionroom,sessionchair))
                    chairs[sessionroom].append("\\instructions{%s}{%s}{%s}\n" % (sessionname,sessionroom,sessionchair))
                else:
                    raise HRUMCException('Expected a match for line number '+str(linenumber)+', the session line '+line)
            elif line.startswith("\\at{"):
                # print("line starts with at")
                m = at_re.match(line)
                if m:
                    attime, atabstract = m.group(1), m.group(2)
                    rooms[sessionroom].append(r"\at{%s}{%s}" % (attime,atabstract))
                    chairs[sessionroom].append(r"\at{%s}{%s}" % (attime,atabstract))
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
    # Drop the temp dir
    # shutil.rmtree('tmp')
    # Make the output file
    fout = open(outputfn+'.tex','w')
    print(LATEX_ROOMS_TEMPLATE_TOP, file=fout)
    for k in rooms:
        print(r"\begin{room}{%s}" % (k,), file=fout)
        print("\n".join(rooms[k]), file=fout)
        print(r"\end{room}", file=fout)
    print(r"\end{document}", file=fout)
    fout.close()
    fout = open(outputfn+'chair.tex','w')
    print(LATEX_CHAIR_TEMPLATE, file=fout)
    for k in rooms:
        print(r"\begin{room}{%s}" % (k,), file=fout)
        print("\n".join(chairs[k]), file=fout)
        print(r"\end{room}", file=fout)
    print(r"\end{document}", file=fout)
    fout.close()
    # LaTeX the files
    jobname = os.path.splitext(os.path.basename(outputfn))[0]
    if VERBOSE:
        print("  LaTeX-ing the file",jobname+'.')
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    shutil.copyfile(jobname+'.pdf',starting_dir+'/'+jobname+'.pdf')
    jobname = os.path.splitext(os.path.basename(outputfn+'chair'))[0]
    if VERBOSE:
        print("  LaTeX-ing the file",jobname+'.')
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    subprocess.call(['pdflatex',jobname],stdout=subprocess.DEVNULL)
    shutil.copyfile(jobname+'.pdf',starting_dir+'/'+jobname+'.pdf')
    # clean up
    os.chdir(starting_dir)
    shutil.rmtree('tmp')



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
def main(args):
    # create a clean output dir
    if os.path.isdir(OUTPUT_DIR_NAME):
        shutil.rmtree(OUTPUT_DIR_NAME)
    os.mkdir(OUTPUT_DIR_NAME)
    # get all .tex files in this dir
    filelist = glob.glob("*.tex")
    try:                              # remove hrumc2xxx.tex, if it is there
        filelist.remove(args['file']) 
    except:
        pass
    filelist.sort()
    if not(args['nopdfs']):
        for fn in filelist:
            latex_each(fn, pdfdirname=OUTPUT_DIR_NAME)
    if not(args['noabstractlist']):
        latex_all('hrumcall',filelist)
    if not(args['noroomlist']):
        make_rooms(args['file'],filelist)

#==================================================================
if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=globals()['__doc__'])
        parser.add_argument('-a','--noabstractlist', action='store_true', default=False, help='suppress generation of a single list of all abstracts')
        parser.add_argument('-f','--file', action='store', default=DEFAULT_PROGRAM_NAME,help='name of the .tex of the program for the conference; default: '+DEFAULT_PROGRAM_NAME)
        parser.add_argument('-p','--nopdfs', action='store_true', default=False, help='suppress generation of separate pdfs for each abstract')
        parser.add_argument('-r','--noroomlist', action='store_true', default=False, help='suppress the generation of information sheets for each room')
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

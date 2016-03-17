% hrumc.cls
% 2015-Jan-30 Jim Hefferon jhefferon at smcvt.edu

% --- Class structure: identification part
% ---
\ProvidesClass{hrumc}[2015/03/09 version 1.00 HRUMC class]
\NeedsTeXFormat{LaTeX2e}

% --- Class structure: initial code part
% ---


% --- Class structure: declaration of options part
% ---
% This class extends the article class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

% --- Class structure: execution of options part
% ---
\ProcessOptions \relax

% --- Class structure: declaration of options part
% ---
\LoadClass[twocolumn]{article}

% --- Class structure: main code part
% ---

% ....... conditional compilation .....
\RequirePackage{etoolbox}

% call with pdflatex "\def\printabstracts{}\input{hrumc2016}" to get them
\newbool{PrintAbstracts}
\ifdefined\printabstracts
  \booltrue{PrintAbstracts}
\else
  \boolfalse{PrintAbstracts}
\fi

\RequirePackage{amsmath,amssymb}

% ..... input and output encodings ........
\usepackage[utf8]{inputenc} % allow utf input files
  \DeclareUnicodeCharacter{00A0}{~} %% no break space
\usepackage{cmap}  % make PDF file copy-and-paste-able


% ...... fonts .........
% \usepackage{tgpagella}
\usepackage[T1]{fontenc}
\usepackage{fbb}

% ...... colors .........
% https://color.adobe.com/Tech-Office-color-theme-23615/edit/?copy=true
\usepackage[dvipsnames]{xcolor}
\definecolor{standoutcolor}{HTML}{8A0917}
\definecolor{backgroundcolor}{HTML}{ACCFCC}
\definecolor{whitecolor}{HTML}{FFFFFF}
\definecolor{graycolor}{HTML}{B8AE9C}
\definecolor{bordercolor}{HTML}{595241}


% Page layout
\RequirePackage[left=0.75in,right=0.75in,top=0.75in,bottom=0.75in]{geometry}

\setlength{\parskip}{0ex}
\setlength{\parindent}{0ex}

\RequirePackage{fancyhdr}
\fancypagestyle{firstpage}{%
  \fancyhf{} % clear all six fields
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}
\fancypagestyle{followingpage}{%
  \fancyhf{} % clear all six fields
  \fancyhead[RE,LO]{\textit{\@memosubject, \show@date}}
  \fancyhead[LE,RO]{\textit{page \thepage}}
  \setlength{\headheight}{14pt}
  \renewcommand{\headrulewidth}{1pt}
  \renewcommand{\footrulewidth}{0pt}
}
% \pagestyle{followingpage}
% \AtBeginDocument{\thispagestyle{firstpage}}
\pagestyle{empty}
\AtBeginDocument{\thispagestyle{empty}}


% ........ Hyper references .............

\RequirePackage{hyperref}
\hypersetup{
    bookmarks=true,         % show bookmarks bar?
    unicode=false,          % non-Latin characters in Acrobat’s bookmarks
    pdftoolbar=true,        % show Acrobat’s toolbar?
    pdfmenubar=true,        % show Acrobat’s menu?
    pdffitwindow=false,     % window fit to page when opened
    pdfstartview={FitH},    % fits the width of the page to the window
    pdftitle={Hudson River Undergraduate Mathematics Conference},    % title
    pdfauthor={Jim Hefferon},     % author
    pdfsubject={Hudson River Undergraduate Mathematics Conference},   % subject of the document
    pdfcreator={Jim Hefferon},   % creator of the document
    pdfproducer={Jim Hefferon}, % producer of the document
    pdfkeywords={Hudson River, Undergraduate Mathematics Conference, HRUMC}, % list of keywords
    pdfnewwindow=true,      % links in new PDF window
    colorlinks=true,       % false: boxed links; true: colored links
    linkcolor=black,          % color of internal links (change box color with linkbordercolor)
    citecolor=black,        % color of links to bibliography
    filecolor=black,      % color of file links
    urlcolor=black           % color of external links
}
\RequirePackage{breakurl}


% ........ Abstracts .............
\RequirePackage{enumitem}
\RequirePackage{ragged2e}  % for RaggedRight


% .......... author ref .............
% Divide author name for indexing
\newcommand{\swallowpagenumber}[1]{\relax}
\newcommand{\authorref}[2]{#1 #2%
  \index{#2, #1 \protect\textit{\sessionname}|swallowpagenumber}}
\AtBeginDocument{\renewcommand\indexname{Index of Authors}}

% .......... abstract .............
\newcommand{\abstracttime}[1]{#1}
\newcommand{\abstracttitle}[1]{\textit{#1}}
\newcommand{\abstractlevel}[1]{\textrm{(Level~#1)}}
\newcommand{\abstractspeaker}[1]{\textsc{#1}}
\newcommand{\affiliation}[1]{(#1)}
\newcommand{\abstractsubject}[1]{\textrm{#1}}

% Abstract
%  #1 title
%  #2 author
%  #3 level
%  #4 subject
%  #5 abstract body
\renewcommand{\abstract}[5]{% \newcommand is \long by default, #4 can have pars
  \RaggedRight
  \abstracttitle{#1}
  \abstractlevel{#3} 
  \abstractspeaker{#2}
  \ifbool{PrintAbstracts}{#5}{}
}

% Notes  Used in some other docs to show whether presenter has requested 
% special facilities, etc.
%  #1 The notes
\newcommand{\notes}[1]{\relax}


% \at  abstract and time
%  #1 time
%  #2 name of file containing the abstract
\newcommand{\at}[2]{%
  \begin{description}[font=\normalfont,leftmargin=2em,labelwidth=0em,topsep=0ex plus 1pt] 
    \RaggedRight
    % \item[\abstracttime{#1}]
    \ifbool{PrintAbstracts}{%
       \item[\abstracttime{#1}]}{%      
       \item[\href{http://joshua.smcvt.edu/hrumc/#2.pdf}{{\abstracttime{#1}}}]}
    % \href{http://joshua.smcvt.edu/hrumc/#2.pdf}{\input{#2}}
    \input{input/#2}
  \end{description}
}

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


% ............. Session .............
\RequirePackage{mdframed}
\mdfdefinestyle{Framed}{linecolor=black,linewidth=0pt, % 0.4pt,
       innertopmargin=4pt,innerbottommargin=4pt,
       leftmargin=0pt,rightmargin=0pt,
       innerleftmargin=0pt,innerrightmargin=0pt,
       backgroundcolor=backgroundcolor}

% \session  Title of session
%  #1 session name e.g. "Algebra I"
%  #2 room, e.g. "STE 106"
%  #3 chair, e.g. "Leonard Euler"
\newcommand{\sessionname}{unknown session}
\newcommand{\session}[3]{%
  \renewcommand{\sessionname}{#1}
  \begin{mdframed}[style=Framed]
    \color{bordercolor}
    \textbf{#1} \hspace{1em plus 1fill}#2  \\
    \hbox{}           \hspace{1em plus 1fill}Chair: #3
  \end{mdframed}%
  \nopagebreak[2]
}


\usepackage[overload]{textcase}
% sessionhead  head for session one, session two, etc.
%   #1  session name; 'one', 'two', etc.
\newcommand{\sessionhead}[1]{%
\clearpage %
\ifbool{PrintAbstracts}{%
    \begin{center} \color{standoutcolor}
      \Large \textbf{\MakeTextUppercase{Parallel Sessions #1}} \\
      {\color{bordercolor}\rule{\textwidth}{1pt}}
    \end{center}\vspace{3ex plus 1ex minus 1ex}
}{%
\twocolumn[
  \begin{@twocolumnfalse}
    \begin{center} \color{standoutcolor}
      \Large \textbf{\MakeTextUppercase{Parallel Sessions #1}} \\
      {\color{bordercolor}\rule{\textwidth}{1pt}}
    \end{center}\vspace{3ex plus 1ex minus 1ex}
  \end{@twocolumnfalse}
] 
}}



% .......... campus map .............
\RequirePackage{graphicx}
\usepackage{tikz}
\newcommand{\circled}[2][]{% http://tex.stackexchange.com/a/218842/339
  \tikz[baseline=(char.base)]{%
    \node[shape = circle, fill=red!20, draw, inner sep = 2.8pt]
    (char) {\phantom{\ifblank{#1}{#2}{#1}}};%
    \node at (char.center) {\makebox[0pt][c]{\large #2}};}}
\robustify{\circled}
\newsavebox{\mapbox}
\savebox{\mapbox}{\includegraphics{map.png}} 

% For campus map

% For map legend: 
% #1  number; 1, 2, etc
% #2  text; "Register here"
\newcommand{\mapkey}[2]{\circled{#1}\hspace{0.75em}#2}

% For parking
\newcommand{\parkingP}{\textsf{\textbf{P}}}
\newcommand{\parking}{% http://tex.stackexchange.com/a/218842/339
  \tikz[baseline=(char.base)]{%
    \node[shape = rectangle, fill=white, draw, inner sep = 2.8pt]
    % (char) {\phantom{\ifblank{#1}{#2}{#1}}};%
    (char) {{\parkingP}};%
    \node at (char.center) {{\parkingP}};}}
\robustify{\circled}

% Campus map
%  LaTeX picture environment drawn on top of a graphic
% #1 file name of graphic; defaults to "map.png" 
\newenvironment{map}[1][map.png]{%
  \savebox{\mapbox}{\includegraphics{#1}}% 
  \begin{center}\large
    \setlength{\unitlength}{1.0in}
}{%
  \end{center}
}


% ........ Front cover ...........
\newcommand{\fronttitle}[1]{%
  \begin{center}
     {\color{graycolor}\Large HRUMC #1} \\[1.5ex]
    \Huge\bfseries Hudson River\\
      Undergraduate Mathematics Conference
  \end{center}
}

\newenvironment{frontgraphic}{%
  \begin{center}
    \setlength{\unitlength}{1in}
    \begin{picture}(0,2)
}{%
    \end{picture}
  \end{center}
}

\newcommand{\frontfoot}{%
  \begin{center}
    \Large\bfseries Saint Michael's College \\
     Colchester Vermont \\
     2016-Apr-02
  \end{center}
}



% ........ Inside cover ...........
\newcommand{\wifi}[2]{%
  \begin{flushleft}
    \large\bfseries Wifi information
  \end{flushleft}
  \hspace*{2em}Use the network ``#1'' 
     with the password ``#2''.
}

\newenvironment{scheduleoverview}{%
  \begin{flushleft}
    \large\textbf{Schedule overview}
  \end{flushleft} % \vspace{0.7ex}
  % \begin{center}
  \hspace*{2em}
  \renewcommand{\arraystretch}{1.2}  % space lines out a bit
  \begin{tabular}{@{}r@{--}*{2}{l@{\hspace*{1.5em}}}l@{}}
}{%
  \end{tabular}
  % \end{center}
}

% Notice of where to find the abstracts
\newcommand{\fullprogram}[1]{%
  \ifbool{PrintAbstracts}{}{%
    \begin{flushleft}
      \large\textbf{Program PDF}
    \end{flushleft} % \vspace{0.7ex}
    \hspace*{2em}
    The full program, including the abstracts, is available
    at \burl{#1}.% allows the link to be line-broken vs \href{#1}{#1}.% 
  }}


\newenvironment{help}{%
  \begin{flushleft}
    \large\textbf{If you need help}
  \end{flushleft}
  \begin{description}[font=\normalfont\bfseries,leftmargin=2em,labelwidth=0em,topsep=0ex plus 1pt] 
    \RaggedRight
}{%
  \end{description}
}



% ........ Welcome ..............
\newcommand{\welcome}[2]{
\begin{flushleft}
  \color{standoutcolor}\Large\textbf{Welcome everyone!}
\end{flushleft}
Welcome to the #1\ annual 
Hudson River Undergraduate Mathematics Conference (HRUMC). 
Whether you are a student at your first
conference or an experienced speaker, we hope that you will find 
today beneficial, rewarding, and inspiring, 
and that you will make new friends and connections.
Our aim is to build an atmosphere that includes
the message, ``We are glad that you are joining the mathematics community!''

HRUMC features fifteen minute talks by students and faculty, 
and a longer plenary address.
Each year, we invite students and faculty from  
universities and colleges in New York and New England to send abstracts
for the short talks. 
These describe research projects,
independent study projects, or any other independent work by students 
and faculty. 

If you are a first time attendee then
spend a little time with this program.
Study the titles and the abstracts to identify some talks that 
grab your interest. 
Note that each of the short talks is marked as Level~1 or Level~2.
The Level~1 talks are accessible to all mathematics students and faculty, 
while Level~2 talks are aimed at advanced undergraduates and faculty. 

Note also that each session has a Chair. 
One of their jobs is to keep all talks strictly to the schedule.
This means that you can easily move from room to room to see talks~--- 
you know that each talk that you attend will end on time, 
and each next one will start when it says it will.

If you are a first time presenter then we especially say, ``Welcome!''
Giving a presentation can be daunting, but is also energizing.
The session Chair will be able to help with any questions that you have, 
including any technology questions.

Presenter or attendee,
we hope you enjoy the conference
and that you will you will learn a great deal.
If you have any questions, please, just ask someone. 

The first HRUMC was held in 1994 at Siena College in Loudonville, NY.
You can check out the website for information about previous meetings, 
pictures from this year's
conference, as well as information about next year's conference:
\href{http://www.skidmore.edu/hrumc}{http://www.skidmore.edu/hrumc}.

Without the dedication, diligence, and enthusiasm of the local
organizers and the student and faculty participants over the years, 
HRUMC would not have become an annual tradition. 
This conference has been successful because the students and faculty of the 
participating institutions have made it successful. 
Keep in mind as you listen to the talks 
that whether you are speaking this year or not, you can look forward to
sharing your work at next year's conference, 
hosted by #2.}

\newcommand{\support}[1]{%
{\bfseries
#1 % 
We also thank all of the
student and faculty volunteers who contributed their time, talents, energy, 
and enthusiasm.}}

\newenvironment{hrumcsteering}{%
  \begin{tabular}[t]{@{}l@{}}
    \textbf{HRUMC Committee}     \\
}{%
  \end{tabular}
}


\newenvironment{localsteering}{%
  \begin{tabular}[t]{@{}l@{}}
    \textbf{Site Arrangements} \\
}{%
  \end{tabular}
}





% ........ Plenary ..............
\newcommand{\plenaryhead}[2]{
  \begin{center}
    \LARGE\textbf{Institutional Greeting and Invited Address}
  \end{center}
  \vspace*{1ex}
  \begin{center}
  \begin{tabular}{l}
    \large\textbf{Welcoming Remarks:} #1 \\[0.7ex]
    \large\textbf{Introduction of the Speaker:} #2 
  \end{tabular}
  \end{center}
}

\RequirePackage{lipsum}
% plenary
%  #1 talk title
%  #2 speaker name
%  #3 speaker affiliation
%  #4 speaker bio
\newsavebox{\speakerbio}
\newenvironment{plenary}[4]{\setlength{\parskip}{1ex}
  \savebox{\speakerbio}{\begin{minipage}{\textwidth}\setlength{\parskip}{1ex}\vspace*{3ex}\textbf{Biography}\par #4\end{minipage}}
  \begin{center}
    \Large\textbf{Keynote address: #1}\\[1.25ex]
    \large\textbf{#2}\\[0.35ex]
    \large{#3}
  \end{center}
  \vspace*{1.5ex}
  \textbf{Abstract}
}{%
  \usebox{\speakerbio}
}
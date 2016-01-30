% hrumc.cls
% 2015-Jan-30 Jim Hefferon jhefferon at smcvt.edu

% --- Class structure: identification part
% ---
\ProvidesClass{hrumc}[2015/01/30 version 1.00 HRUMC class]
\NeedsTeXFormat{LaTeX2e}

% --- Class structure: initial code part
% ---

% what is meeting? 
% \def\@committeename{}
% \newcommand{\setcommittee}[1]{\def\@committee{#1}}
% \newcommand{\show@committee}{\@committee}

% who to? 
% \def\@memoto{Self}
% \newcommand{\setmemoto}[1]{\def\@memoto{#1}}
% \newcommand{\show@memoto}{\@memoto}
% % what role do they have (e.g., chair)
% \newcommand{\role}[2]{#1~(#2)}
% \newcommand{\chair}[1]{\role{#1}{Chair}}
% \newcommand{\secretary}[1]{\role{#1}{Secretary}}

% % who from? 
% \global\let\@memofromt\@empty
% \newcommand{\setmemofrom}[1]{\def\@memofrom{#1}}
% \let\memofrom\setmemofrom %
% \newcommand{\show@memofrom}{\@memofrom}

% % subject?
% \global\let\@memosubject\@empty
% \newcommand{\setmemosubject}[1]{\def\@memosubject{#1}}
% \newcommand{\show@memosubject}{\@memosubject}

% % who to cc?
% \global\let\@memocc\@empty
% \newcommand{\setmemocc}[1]{\def\@memocc{#1}}
% \let\memocc\setmemocc %
% \newcommand{\show@memocc}{\@memocc}

% % what day is it?
% \def\@date{\today}
% \newcommand{\setdate}[1]{\def\@date{#1}}
% \newcommand{\show@date}{\@date}

% --- Class structure: declaration of options part
% ---
% This class extends the article class
% Read all the documentclass options; pass them to article, unless the file
% named "<currentoption>.memo" exists, in which case it is loaded
%\DeclareOption*{\InputIfFileExists{\CurrentOption.min}{}{%
%    \PassOptionsToClass{\CurrentOption}{article}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
% \DeclareOption*{\InputIfFileExists{\CurrentOption.memo}{}{%
%     \PassOptionsToClass{\CurrentOption}{article}}}

% --- Class structure: execution of options part
% ---
% \ExecuteOptions{twocolumn}

\ProcessOptions \relax

% --- Class structure: declaration of options part
% ---
\LoadClass[twocolumn]{article}

% --- Class structure: main code part
% ---

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
\RequirePackage[left=0.8in,right=0.8in,top=0.8in,bottom=0.8in]{geometry}

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



% ........ Abstracts .............
\RequirePackage{enumitem}
\RequirePackage{ragged2e}  % for RaggedRight

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
    linkcolor=red,          % color of internal links (change box color with linkbordercolor)
    citecolor=black,        % color of links to bibliography
    filecolor=black,      % color of file links
    urlcolor=black           % color of external links
}

\newcommand{\abstracttime}[1]{#1}
\newcommand{\abstracttitle}[1]{\textit{#1}}
\newcommand{\abstractlevel}[1]{\textrm{(Level~#1)}}
\newcommand{\abstractspeaker}[1]{\textsc{#1}}

% Abstract
%  #1 title
%  #2 author
%  #3 level
\renewenvironment{abstract}[3]{%
  % \begin{description}[font=\normalfont,leftmargin=2em,labelwidth=0em] 
    \RaggedRight
    \abstracttitle{#1}
    \abstractlevel{#3}
    \abstractspeaker{#2}
}{%
  % \end{description}
}

% \at  abstract and time
%  #1 time
%  #2 name of file containing the abstract
\newcommand{\at}[2]{%
  \begin{description}[font=\normalfont,leftmargin=2em,labelwidth=0em, ] 
    \RaggedRight
    \item[\abstracttime{#1}]
    \href{http://joshua.smcvt.edu/hrumc/#2.pdf}{\input{#2}}
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
\newcommand{\IIIa}{\timeformat{3}{30}-\timeformat{3}{45}}
\newcommand{\IIIb}{\timeformat{4}{00}-\timeformat{4}{15}}
\newcommand{\IIIc}{\timeformat{4}{20}-\timeformat{4}{35}}


% ............. Session .............
\RequirePackage{mdframed}
\mdfdefinestyle{Framed}{linecolor=black,linewidth=0pt, % 0.4pt,
       leftmargin=0pt,rightmargin=0pt,
       innerleftmargin=0pt,innerrightmargin=0pt,
       backgroundcolor=backgroundcolor}
\RequirePackage{tabularx}

% \session  Title of session
%  #1 session name
%  #2 room
%  #3 chair
\newcommand{\session}[3]{%
  \begin{mdframed}[style=Framed]
    \color{bordercolor}
    \begin{tabularx}{\columnwidth}{lXr}
      \textbf{#1}    &&#2  \\
                     &&Chair: #3
    \end{tabularx}
  \end{mdframed}%
}

\usepackage[overload]{textcase}
\newcommand{\sessionhead}[1]{%
\clearpage %
\twocolumn[
  \begin{@twocolumnfalse}
    \begin{center} \color{standoutcolor}
      \Large \textbf{\MakeTextUppercase{Session #1}} \\
      {\color{bordercolor}\rule{\textwidth}{1pt}}
    \end{center}\vspace{3ex}
  \end{@twocolumnfalse}
] 
}
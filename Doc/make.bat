@@echo off
setlocal

set SVNROOT=http://svn.python.org/projects
::if "%PYTHON%" EQU "" set PYTHON=..\pcbuild\python
if "%HTMLHELP%" EQU "" if "%ProgramFiles(x86)%" EQU "" set HTMLHELP=%ProgramFiles%\HTML Help Workshop\hhc.exe
if "%HTMLHELP%" EQU "" if "%ProgramFiles(x86)%" NEQ "" set HTMLHELP=%ProgramFiles(x86)%\HTML Help Workshop\hhc.exe
if "%DISTVERSION%" EQU "" for /f "usebackq" %%v in (`tools\sphinxext\patchlevel.py`) do set DISTVERSION=%%v

if "%1" EQU "" goto help
if "%1" EQU "html" goto build
if "%1" EQU "htmlhelp" goto build
if "%1" EQU "epub" goto build
if "%1" EQU "latex" goto build
if "%1" EQU "latexpdf" goto latexpdf
if "%1" EQU "text" goto build
if "%1" EQU "suspicious" goto build
if "%1" EQU "linkcheck" goto build
if "%1" EQU "changes" goto build
if "%1" EQU "checkout" goto checkout
if "%1" EQU "update" goto update

:help
set this=%~n0
echo HELP
echo.
echo %this% checkout
echo %this% update
echo %this% html
echo %this% htmlhelp
echo %this% epub
echo %this% latex
echo %this% latexpdf
echo %this% text
echo %this% suspicious
echo %this% linkcheck
echo %this% changes
echo.
goto end

:checkout
::svn co %SVNROOT%/external/Sphinx-0.6.5/sphinx tools/sphinx
hg clone https://bitbucket.org/uchida/sphinx -b py27ja-release tools/sphinx
::svn co %SVNROOT%/external/docutils-0.6/docutils tools/docutils
svn export http://docutils.svn.sourceforge.net/svnroot/docutils/tags/docutils-0.7/docutils tools/docutils
svn co %SVNROOT%/external/Jinja-2.3.1/jinja2 tools/jinja2
svn co %SVNROOT%/external/Pygments-1.3.1/pygments tools/pygments
goto end

:update
::svn update tools/sphinx
hg --cwd tools/sphinx pull -ufb py27ja-release
svn update tools/docutils
svn update tools/jinja2
svn update tools/pygments
goto end

:build
if not exist build mkdir build
if not exist build\%1 mkdir build\%1
if not exist build\doctrees mkdir build\doctrees
tools\sphinx-build.py -b%1 -dbuild\doctrees . build\%*
if "%1" EQU "htmlhelp" "%HTMLHELP%" build\htmlhelp\python%DISTVERSION:.=%.hhp
goto end

:latexpdf
if not exist build mkdir build
if not exist build\latex mkdir build\latex
if not exist build\doctrees mkdir build\doctrees
tools\sphinx-build.py -blatex -dbuild\doctrees . build\latex
cd build\latex
for %%f in (*.pdf *.png *.gif *.jpg *.jpeg) do extractbb %%f
for %%f in (*.tex) do platex -kanji=utf8 %LATEXOPTS% %%f
for %%f in (*.tex) do platex -kanji=utf8 %LATEXOPTS% %%f
for %%f in (*.tex) do platex -kanji=utf8 %LATEXOPTS% %%f
for %%f in (*.idx) do mendex -U -f -d `basename %%f .idx`.dic -s python.ist %%f
for %%f in (*.tex) do platex -kanji=utf8 %LATEXOPTS% %%f
for %%f in (*.tex) do platex -kanji=utf8 %LATEXOPTS% %%f
for %%f in (*.dvi) do dvipdfmx %%f
goto end

:end

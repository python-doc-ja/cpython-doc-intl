#!/usr/bin/env python
# coding: utf-8

import difflib
import filecmp
import os
from shutil import copyfile
from fnmatch import fnmatch

class HtmlDiffMod(difflib.HtmlDiff):
    _table_template = """
        <table class="diff" id="difflib_chg_%(prefix)s_top"
               cellspacing="0" cellpadding="0" rules="groups" >
            <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
            %(header_row)s
            <tbody>
    %(data_rows)s        </tbody>
        </table>"""

    def _format_line(self,side,flag,linenum,text):
        """Returns HTML markup of "from" / "to" text lines

        side -- 0 or 1 indicating "from" or "to" text
        flag -- indicates if difference on line
        linenum -- line number (used for line number column)
        text -- line text to be marked up
        """
        try:
            linenum = '%d' % linenum
            id = ' id="%s%s"' % (self._prefix[side],linenum)
        except TypeError:
            # handle blank lines where linenum is '>' or ''
            id = ''
        # replace those things that would get confused with HTML symbols
        text=text.replace("&","&amp;").replace(">","&gt;").replace("<","&lt;")

        # make space non-breakable so they don't get compressed or line wrapped
        text = text.replace(' ','&nbsp;').rstrip()

        fmt = '<td class="diff_header"%s>%s</td><td nowrap="nowrap">%s</td>' 
        fmt0= '<td class="diff_header"%s>%s-</td><td nowrap="nowrap">%s</td>' 
        fmt1= '<td class="diff_header"%s>%s+</td><td nowrap="nowrap">%s</td>' 

        if flag:
            fmt = fmt1 if side else fmt0

        return fmt % (id,linenum,text)

    def make_table(self,fromlines,tolines,fromdesc='',todesc='',context=False,
                   numlines=5):
        """Returns HTML table of side by side comparison with change highlights

        Arguments:
        fromlines -- list of "from" lines
        tolines -- list of "to" lines
        fromdesc -- "from" file column header string
        todesc -- "to" file column header string
        context -- set to True for contextual differences (defaults to False
            which shows full differences).
        numlines -- number of context lines.  When context is set True,
            controls number of lines displayed before and after the change.
            When context is False, controls the number of lines to place
            the "next" link anchors before the next change (so click of
            "next" link jumps to just before the change).
        """

        # make unique anchor prefixes so that multiple tables may exist
        # on the same page without conflict.
        self._make_prefix()

        # change tabs to spaces before it gets more difficult after we insert
        # markkup
        fromlines,tolines = self._tab_newline_replace(fromlines,tolines)

        # create diffs iterator which generates side by side from/to data
        if context:
            context_lines = numlines
        else:
            context_lines = None
        diffs = difflib._mdiff(fromlines,tolines,context_lines,linejunk=self._linejunk,
                      charjunk=self._charjunk)

        # set up iterator to wrap lines that exceed desired width
        if self._wrapcolumn:
            diffs = self._line_wrapper(diffs)

        diffs = list(diffs)  # OVERWRITED HERE

        # collect up from/to lines and flags into lists (also format the lines)
        fromlist,tolist,flaglist = self._collect_lines(diffs)

        # process change flags, generating middle column of next anchors/links
        fromlist,tolist,flaglist,next_href,next_id = self._convert_flags(
            fromlist,tolist,flaglist,context,numlines)

        s = []
        fmt_diff = '            <tr><td class="diff_next"%s>%s</td>%s</tr>' + \
              '<tr><td class="diff_next">%s</td>%s</tr>\n'  # OVERWRITED HERE
        fmt_0 = '<tr><td class="diff_next"%s>%s</td>%s</tr>\n'  # OVERWRITED HERE

        fmt0 = '            <tr><td class="diff_next"%s>%s</td>%s</tr>' 
        for i in range(len(flaglist)):
            if flaglist[i] is None:
                # mdiff yields None on separator lines skip the bogus ones
                # generated for the first line
                if i > 0:
                    s.append('        </tbody>        \n        <tbody>\n')
            elif flaglist[i] == True:  # OVERWRITED HERE
                if diffs[i][0][0]:
                    s.append( fmt_0 % (next_id[i], next_href[i], fromlist[i]) )
                if diffs[i][1][0]:     
                    s.append( fmt_0 % (next_id[i], next_href[i], tolist[i]) )
            else:
                s.append( fmt0 % (next_id[i],next_href[i],fromlist[i] ))

        if fromdesc or todesc:
            header_row = '<thead><tr>%s%s</tr></thead>' % (  # OVERWRITED HERE
                '<th class="diff_next"><br /></th>',
                '<th colspan="2" class="diff_header">%s =&gt; %s</th>' % (fromdesc, todesc))
        else:
            header_row = ''

        table = self._table_template % dict(
            data_rows=''.join(s),
            header_row=header_row,
            prefix=self._prefix[1])

        return table.replace('\0+','<span class="diff_add">'). \
                     replace('\0-','<span class="diff_sub">'). \
                     replace('\0^','<span class="diff_chg">'). \
                     replace('\1','</span>'). \
                     replace('\t','&nbsp;')
join = os.path.join

def walkfiles(directory, pattern="*"):
    for dirpath, dirs, files in os.walk(directory):
        for fn in files:
            if fnmatch(fn, pattern):
                yield join(dirpath, fn)

def makepairrst(fromdir, todir):
    """fromdir と todir からファイル一覧を出して、
    (両方にあるファイルlist、 from にしか無いファイルlist、 to にしか無いファイルlist)
    のタプルを返す。"""
    from_list = sorted(walkfiles(fromdir, '*.rst'), reverse=True)
    to_list = sorted(walkfiles(todir, '*.rst'), reverse=True)

    both = []
    only_f = []
    only_t = []

    def popfrom():
        return from_list.pop()[len(fromdir)+1:]
    def popto():
        return to_list.pop()[len(todir)+1:]

    f_top = popfrom()
    t_top = popto()

    while from_list and to_list:
        if f_top < t_top:
            only_f.append(f_top)
            f_top = popfrom()
        elif t_top < f_top:
            only_t.append(t_top)
            t_top = popto()
        else:
            both.append(f_top)
            f_top = popfrom()
            t_top = popto()

    if f_top == t_top:
        both.append(f_top)
    else:
        only_f.append(f_top)
        only_t.append(t_top)

    return both, only_f, only_t

def makepatch2(from_dir, to_dir, diff_dir):
    both, only_from, only_to = makepairrst(from_dir, to_dir)
    print '==deleted files=='
    for fn in only_from:
        print fn
    print '==new files=='
    for fn in only_to:
        print fn

    samefiles = []
    difffiles = []

    differ = difflib.Differ()
    htmlwriter = HtmlDiffMod()

    for fn in both:
        from_fn = os.path.join(from_dir, fn)
        to_fn = os.path.join(to_dir, fn)

        if filecmp.cmp(from_fn, to_fn):
            samefiles.append(fn)
            continue
        difffiles.append(fn)

        #from_lines = open(from_fn).readlines()
        #to_lines = open(to_fn).readlines()

        diff_fn = os.path.join(diff_dir, fn) + '.diff'
        html_fn = os.path.join(diff_dir, fn) + '.html'

        if not os.path.exists(os.path.dirname(diff_fn)):
            os.makedirs(os.path.dirname(diff_fn))

        open(html_fn, 'w').write(
            htmlwriter.make_file(
                open(from_fn), open(to_fn),
                from_fn, to_fn,
                True, 8
                ))

        st = os.system("diff -U 12 '%s' '%s' > '%s'" % (from_fn, to_fn, diff_fn))
        if st == 0:
            print >>sys.stderr, fn, ": filecmp.cmp() == False but diff == 0"


    print '==same files=='
    for fn in samefiles:
        print fn

    print '==diff files=='
    for fn in difffiles:
        print fn



def makepatch(left, right, dest):
    print left, right, dest
    for root,dirs,files in os.walk(right):
        if ".svn" in root: continue
        assert root.startswith(right)
        rel_root = root[len(right)+1:]
        dirpath = join(dest, rel_root)
        if not os.path.exists(dirpath):
            print "mkdir %s" % dirpath
            os.mkdir(dirpath)
        for f in files:
            lpath = join(left, rel_root, f)
            rpath = join(right, rel_root, f)
            dpath = join(dest, rel_root, f)

            if os.path.exists(lpath):
                cmd = """diff -U 12 '%s' '%s' > '%s.diff'""" % (lpath, rpath, dpath)
                print cmd
                os.system(cmd)
            else:
                print "new: %s" % rpath
                copyfile(rpath, dpath)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print "makepatch.py fromdir todir patchdir"
        sys.exit(1)
    makepatch2(*sys.argv[1:])


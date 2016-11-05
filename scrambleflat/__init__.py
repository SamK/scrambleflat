#!/usr/bin/python
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>

= Description

Scramble a file

= Notes:

This file tends to be PEP-8 compliant. Use these commands to be
proud of your work:

* using pep8:

  pep8 --show-source --show-pep8 scrambleflat

* using pyling:

  pylint --report=n scrambleflat

"""

import os
import re
import argparse

__version__ = '0'
__author__ = 'Samuel Krieg'


class Scrambler:
    """ A nice dsecription goes here
    """

    def __init__(self):
        self.dictionnary = {}
        self.regterms = {}

        self.make_transtable = False
        self.transtable = {}

    def build_regexps(self, regtermsfiles=None):
        """Create a list of regular expressions
        """
        for fichier in regtermsfiles:
            filename = os.path.split(fichier.name)[1]
            num = 1
            for line in fichier:
                line = line.strip()
                if line != '' and not line.startswith('#'):
                    self.regterms[filename + str(num)] = line
                num += 1

    def build_dictionnary(self, termsfiles=None):
        """Creates a dictionnary of terms to hide
        """
        for fichier in termsfiles:
            filename = os.path.split(fichier.name)[1]
            num = 1
            for line in fichier:
                line = line.strip()
                if line != '':
                    cle = line
                    self.dictionnary[cle] = filename + str(num)
                num += 1

    def strtr(self, strng):
        """Search and replace
           Source: http://stackoverflow.com/a/10931514/238913
        """
        # pylint: disable-msg=C0103
        buff = []
        i, n = 0, len(strng)
        while i < n:
            # pour chaque lettre
            match = False
            t1 = 'osef'
            for s, r in self.dictionnary.items():
                #search in dictionnaries
                if strng[i:len(s) + i] == s:
                    buff.append(r)
                    t1 = strng[i:len(s) + i]
                    i = i + len(s)
                    match = True
                    t2 = r
                    break
            for s, r in self.regterms.items():
                #search in regexps
                pattern = '^' + r
                regmatch = re.search(pattern, strng[i:])
                if regmatch:
                    match_len = regmatch.end()
                    match_str = strng[i:i + match_len]
                    replacematch = "reg-" + s + "-" + \
                                   str(len(self.dictionnary))
                    buff.append(replacematch)
                    i = i + match_len
                    match = True
                    t1 = match_str
                    t2 = replacematch
                    self.dictionnary[t1] = t2
                    if self.make_transtable:
                        if not t1 in self.transtable:
                            self.transtable[t1] = t2
                    break
            if not match:
                buff.append(strng[i])
                i = i + 1
            else:
                if self.make_transtable:
                    if not t1 in self.transtable:
                        self.transtable[t1] = t2

        return ''.join(buff)

    def scramble(self, line):
        """do the scramble for one line
        """
        return self.strtr(line)


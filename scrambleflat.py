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

Website: https://github.com/samyboy/scrambleflat

This file tends to be PEP-8 compliant. Use these commands to be
proud of your work:

* using pep8:

  pep8 --show-source --show-pep8 scrambleflat

* using pyling:

  pylint --report=n scrambleflat

"""

import sys
import argparse
import scrambleflat

__version__ = '0'
__author__ = 'Samuel Krieg'


def parse_arguments():
    """Try to parse the command line arguments given by the user"""
    # pylint: disable-msg=C0103

    version_string = "%(prog)s-%(version)s by %(author)s" % \
                     {"prog": "%(prog)s", "version": __version__, \
                     "author": __author__}

    p = argparse.ArgumentParser(description="Scrambles a flat file",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('-V', '--version', action='version',
                   help="shows program version", version=version_string)
    p.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'),
                   default=sys.stdin,
                   help='the source file to scramble ' \
                   '(default: standard input)')
    p.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                   default=sys.stdout,
                   help='the scrambled file (default: standard output)')
    p.add_argument('-t', '--terms', nargs='+',
                   type=argparse.FileType('r'),
                   help='the file that contains all the terms that must be \
                   scrambled. Each term is replaced by the concatenation of \
                   the file name provided by --terms and its line number \
                   in the input file.')
    p.add_argument('-r', '--regterms', nargs='+', type=argparse.FileType('r'),
                   help='Same as -t but contains regular expressions')

    args = p.parse_args()

    if args.terms is None and args.regterms is None:
        p.error("input, option -t/--terms or -r/--regterms is required")

    return args


def main():
    """the main function
    """

    # get the arguments
    args = parse_arguments()
    make_transtable = True

    scrambler = scrambleflat.Scrambler()
    if args.terms:
        scrambler.build_dictionnary(args.terms)
    if args.regterms:
        scrambler.build_regexps(args.regterms)

    scrambler.make_transtable = make_transtable

    for line in args.infile:
        args.outfile.write(scrambler.scramble(line))

    """
    print "transtable:"
    for a, b in scrambler.transtable.items():
        print "[%s] = \"%s\"" % (a, b)

    print "dico"
    for a, b in scrambler.dictionnary.items():
        print "[%s] = \"%s\"" % (a, b)
    """


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        """exit code 130 says it's Ctrl-C:
           see more: http://www.tldp.org/LDP/abs/html/exitcodes.html
        """
        sys.exit(130)

### EOF ###

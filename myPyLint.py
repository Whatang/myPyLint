'''
Created on 1 Aug 2010

@author: Mike Thomas

Make ignore options work with pylint/pydev.

Pass this script the location of pylint.bat/pylint as an option:
--lint-location=<path to pylint>
'''

import os
import glob

def main(argv):
    #print
    options = [arg for arg in argv
               if arg.startswith("--")]
    args = [arg for arg in argv
            if not arg.startswith("--")]
    lintLocation = None
    for opt in options:
        if opt.startswith("--lint-location="):
            lintLocation = opt.split("=")[1]
            break
    if lintLocation is None:
        print "lint not specified"
        sys.exit(1)
    options = [opt for opt in options
               if not opt.startswith("--lint-location")]
    ignoredBases = []
    ignoreOptions = [opt for opt in options
                     if opt.startswith("--ignore=")]
    ignoredBases.extend(opt.split("=")[1] for opt in ignoreOptions)
    rcFiles = [opt for opt in options
               if opt.startswith("--rcfile=")]
    for rcOpt in rcFiles:
        rcFile = rcOpt.split("=")[1]
        with open(rcFile) as handle:
            for longLine in handle:
                for line in longLine.split("\n"):
                    line = line.strip()
                    if line.startswith("ignore="):
                        theseIgnores = line.split("=")[1]
                        theseIgnores = theseIgnores.split(",")
                        ignoredBases.extend(b.strip() for b in theseIgnores)
    #print "Ignored bases: " + ",".join(ignoredBases)
    #print "pylint requested on files: " + ",".join(args)
    for base in ignoredBases:
        args = [f for f in args
                if
                f not in glob.glob(os.path.join(os.path.dirname(f), base)) ]
    #print args
    if len(args):
        import subprocess
        callArgs = [lintLocation]
        callArgs.extend(options)
        callArgs.extend(args)
        #print callArgs
        subprocess.call(callArgs)
if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

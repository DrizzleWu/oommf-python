import os
import subprocess
import sys


def retrieve_oommf_path():

    # Environment variable OOMMF_PATH should point to the directory which
    # contains 'oommf.tcl'
    if 'OOMMF_PATH' not in os.environ:
        msg = """Please set OOMMF_PATH environment variable to point to
        the directory that contains oommf.tcl. In bash, you can write
        export OOMMF_PATH=/yourhome/youpath/to/oommf

    This can be added to the ~/.bashrc, for example, to be executed
    automatically.

    Cowardly stopping here.
    """

        print(msg)
        sys.exit(1)
    else:
        oommf_path = os.environ['OOMMF_PATH']

    return oommf_path

oommf_path = retrieve_oommf_path()


def call_oommf(argstring):
    """Convenience function to call OOMMF: Typical usage

    p = call_oommf("+version")
    p.wait()
    stdout, stderr = p.stdout.read(), p.stderr.read()

    """

    p = subprocess.Popen(os.path.join(oommf_path, 'oommf.tcl') +
                         ' ' + argstring,
                         shell=True, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    return p


def get_version():
    """Return OOMMF version as string, something like 1.2.0.5"""
    p = call_oommf('+version')
    p.wait()
    stderr = p.stderr.read()     # version is returned in stderr
    s_oommftcl, versionstring = stderr.split()[0:2]
    return versionstring


def get_oommf_path():
    return oommf_path
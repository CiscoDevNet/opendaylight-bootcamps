# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

""" Layer of abstraction that represents any concrete interpreter such as iPython. 

    See also: https://www.artima.com/weblogs/viewpost.jsp?thread=4829 
    for blog by Guido van van Rossum on how main() should return exit codes.
    
    See also: EX_OK (and other exit code constants) in module 'os'.

    Note: as at 10-June-2015 the exit code constants are absent on the MS-Windows platform.

    On OSX:
    SYSEXITS.H -- Exit status codes for system programs.
  
      This include file attempts to categorize possible error
      exit statuses for system programs, notably delivermail
      and the Berkeley network.
  
      Error numbers begin at EX__BASE to reduce the possibility of
      clashing with other exit statuses that random programs may
      already return.  The meaning of the codes is approximately
      as follows:
  
      EX_USAGE -- The command was used incorrectly, e.g., with
          the wrong number of arguments, a bad flag, a bad
          syntax in a parameter, or whatever.
      EX_DATAERR -- The input data was incorrect in some way.
          This should only be used for user's data & not
          system files.
      EX_NOINPUT -- An input file (not a system file) did not
          exist or was not readable.  This could also include
          errors like "No message" to a mailer (if it cared
          to catch it).
      EX_NOUSER -- The user specified did not exist.  This might
          be used for mail addresses or remote logins.
      EX_NOHOST -- The host specified did not exist.  This is used
          in mail addresses or network requests.
      EX_UNAVAILABLE -- A service is unavailable.  This can occur
          if a support program or file does not exist.  This
          can also be used as a catchall message when something
          you wanted to do doesn't work, but you don't know
          why.
      EX_SOFTWARE -- An internal software error has been detected.
          This should be limited to non-operating system related
          errors as possible.
      EX_OSERR -- An operating system error has been detected.
          This is intended to be used for such things as "cannot
          fork", "cannot create pipe", or the like.  It includes
          things like getuid returning a user that does not
          exist in the passwd file.
      EX_OSFILE -- Some system file (e.g., /etc/passwd, /etc/utmp,
          etc.) does not exist, cannot be opened, or has some
          sort of error (e.g., syntax error).
      EX_CANTCREAT -- A (user specified) output file cannot be
          created.
      EX_IOERR -- An error occurred while doing I/O on some file.
      EX_TEMPFAIL -- temporary failure, indicating something that
          is not really an error.  In sendmail, this means
          that a mailer (e.g.) could not create a connection,
          and the request should be reattempted later.
      EX_PROTOCOL -- the remote system returned something that
          was "not possible" during a protocol exchange.
      EX_NOPERM -- You did not have sufficient permission to
          perform the operation.  This is not intended for
          file system problems, which should use NOINPUT or
          CANTCREAT, but rather for higher level permissions.
 """

from __future__ import print_function as _print_function
import os
import sys
from os.path import isabs
import imp

# successful termination
EX_OK = getattr(os, "EX_OK", 0)

# configuration error
EX_CONFIG = getattr(os, "EX_CONFIG", 78)

# temporary failure; user is invited to retry
EX_TEMPFAIL = getattr(os, "EX_TEMPFAIL", 75)

# command line usage error
EX_USAGE = getattr(os, "EX_USAGE", 64)

#  data format error
EX_DATAERR = getattr(os, "EX_DATAERR", 65)

# service unavailable
EX_UNAVAILABLE = getattr(os, "EX_UNAVAILABLE", 69)

# internal software error
EX_SOFTWARE = getattr(os, "EX_SOFTWARE", 70)

# permission denied
EX_NOPERM = getattr(os, "EX_NOPERM", 77)

def sys_exit(code):
    """Swallow the SystemExit exception if it would adversely impact the interpreter."""
    try:
        global __IPYTHON__
        __IPYTHON__
        if code == EX_OK:
            # No need to print anything or raise exception.
            pass
        else:
            # Do not call sys.exit because iPython halts processing of the Notebook.
            print('exit code', code, file=sys.stderr)
    except NameError:
        # System exit raises an exception which seems overkill but is the standard.
        sys.exit(code)

def load_module(module_name, module_file_name, module_dir):
    """ Load a Python module from a specific file and return it.
    
    Any file extension in the module_file_name is ignored.
    The module is loaded from the compiled-python file if it exists (extension 
    .pyc). If the config file is newer than the compiled file then the compiled 
    file is ignored.
    
    The module does not need to be on the Python path.
    
    If the module_file_name is an absolute path then the module_dir is ignored, 
    otherwise the module_file_name is joined to the module_dir. 
    """
    (module_file_name, _) = os.path.splitext(module_file_name)
    if isabs(module_file_name):
        uri = module_file_name
    else:
        uri = os.path.join(module_dir, module_file_name)
        uri = os.path.normpath(uri)
    source_file_name = uri + '.py'
    compiled_file_name = uri + '.pyc'
    if os.path.exists(compiled_file_name):
        if os.path.exists(source_file_name) \
        and os.path.getmtime(source_file_name) > os.path.getmtime(compiled_file_name): 
            module = imp.load_source(module_name, source_file_name)
        else:
            module = imp.load_compiled(module_name, compiled_file_name)
    elif os.path.exists(source_file_name):
        module = imp.load_source(module_name, source_file_name)
    else:
        raise ImportError('Module not found:', source_file_name)
    assert module.__name__ == module_name
    return module

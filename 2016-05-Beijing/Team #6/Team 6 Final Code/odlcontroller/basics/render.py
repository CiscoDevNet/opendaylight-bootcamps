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

''' Convenience functions to display rich text, such as HTML.

    This module detects the display mode, which is normally 'plain' but can be 'rich'.
    The 'rich' mode recognises the iPython type 'DisplayObject'.
    The 'rich' mode converts types 'list', 'tuple' and 'dict' to HTML TABLE.
    The 'plain' mode delegates to built-in function 'print'.
    
    When this module is imported into iPython it delegates to function 'display';
    otherwise output is printed to stdout using the built-in 'print' function. 
'''

from __future__ import print_function
from collections import OrderedDict
from tabulate import tabulate
try:
    from IPython.display import display
    from IPython.core.display import DisplayObject, HTML
except ImportError:
    display = print
    class DisplayObject(object):
        def __init__(self, data=None):
            self.data = data
    class HTML(DisplayObject):
        pass

from tabulate import _isnumber as _isnumber_standard

def _isnumber_exclude_bool(cell_value):
    """Consider type 'bool' to be non-numeric."""
    return False if isinstance(cell_value, bool) else _isnumber_standard(cell_value)

# Verify that the 'tabulate' module behaves undesirably.
assert _isnumber_standard != _isnumber_exclude_bool, "Expected no monkey-patch (yet)."
assert _isnumber_standard(True) and _isnumber_standard(False), 'Expected boolean to be numeric.'

# Monkey-patch the 'tabulate' module such that boolean is not numeric.
import tabulate as tabulate_module
tabulate_module._isnumber = _isnumber_exclude_bool
assert not tabulate_module._isnumber(True) and not tabulate_module._isnumber(False), 'Expected boolean to be non-numeric.'

def _display_stdout(value, **kwargs):
    if isinstance(value, DisplayObject):
        print(value.data, **kwargs)
    else:
        print(value, **kwargs)

_display = _display_stdout

def _html_headings(columns):
    return ''.join(['<th>%s</th>' % k for k in columns])
    
def _html_cells(columns):
    return ''.join(['<td>%s</td>' % v for v in columns])

def _html_rows(rows):
    if len(rows) == 0:
        return '<tr><td><em>Empty</em></td></tr>'
    peek = rows[0]
    if hasattr(peek, '__dict__'):
        r = []
        r.append('<tr>%s</tr>' % _html_headings(vars(peek).keys()))
        for row in rows:
            r.append('<tr>%s</tr>' % _html_cells(vars(row).values()))
        return "\n".join(r)
    else:
        return "\n".join(['<tr><td>%s</td></tr>' % str(v) for v in rows])

def _html_matrix(value):
    return HTML('<table>\n%s\n</table>' % _html_rows(value))

def _html_entries(value):
    return "\n".join(['<tr><th>%s</th><td>%s</td></tr>' % (str(k), str(v)) for (k, v) in value.items()])

def _html_dict(value):
    return HTML('<table>\n%s\n</table>' % _html_entries(value))

def _display_rich(*args, **kwargs):
    ''' Display rich text, such as HTML

    This function recognises type 'DisplayObject' as 'rich'.
    Types 'list', 'dict' and 'tuple' and are converted to type 'DisplayObject'.
    Function 'display' is applied to 'DisplayObject'.
    Other types, including 'string', are printed by applying the built-in 'print' function.
    '''
    if len(args) > 1:
        any_rich = False
        for arg in args:
            if isinstance(arg, DisplayObject):
                any_rich = True
        if any_rich:
            # Display each arg separately.
            for arg in args:
                _display_rich(arg, **kwargs)
        else:
            _display(_html_matrix(args))
    elif len(args) == 1:
        arg = args[0]
        if isinstance(arg, DisplayObject):
            _display(arg)
        elif hasattr(arg, '__dict__'):
            entries = vars(arg)
            _display(_html_dict(entries))
        elif isinstance(arg, (list, tuple)):
            _display(_html_matrix(arg))
        else:
            print(arg, **kwargs)

def _plain_tabulate_dict(arg):
    """
    Return textual representation of dict as table layout.
    
    Table design:             
    - one table row for each field of dict.
    - each row has columns 'field' and 'value'.
    """
    assert isinstance(arg, dict)
    return tabulate([[field, value] for field, value in arg.items()], headers=('name', 'value'))

# Sequence types that 'tabulate' recognises. 
# There may be additional types related to 3rd party libraries.
_columnar = (list, dict, tuple)

def _print_plain_table(tabular_data, **kwargs):
    '''
    Print the arguments in a tabular format using plain text.
    '''
    if isinstance(tabular_data, tuple):
        if '_asdict' in dir(tabular_data):
            # title of table is name of type.             
            table_title = type(tabular_data).__name__
            print(table_title)
            tuple_as_dict = OrderedDict(zip(tabular_data._fields, tabular_data))
            # Note: on Python 3, unreliable: tabular_data._asdict()
            # fails for type DeviceControl   
            # it returns an empty dict (no exception raised).                       
            print(_plain_tabulate_dict(tuple_as_dict))
            return
        else:
            pass
    elif isinstance(tabular_data, dict):
        print(_plain_tabulate_dict(tabular_data))
        return
    
    if 'headers' in kwargs:
        if not kwargs['headers'] in ('firstrow', 'keys'):
            kwargs['headers'] = _vectorise(kwargs['headers'])
    elif len(tabular_data) > 0:
        firstrow = tabular_data[0]
        if isinstance(firstrow, dict) or isinstance(firstrow, tuple) and '_asdict' in dir(firstrow):
            kwargs['headers'] = 'keys'
        
    if len(tabular_data) > 0:
        if not 'numalign' in kwargs:
            # Override default setting numalign='decimal' because it is expensive to compute.
            # The caller of this method can explicitly set numalign='decimal'.                      
            kwargs['numalign'] = 'right'

        # Transform a 1D table to 2D by making each row into a list.
        tabular_data = [arg if isinstance(arg, _columnar) else (arg, ) for arg in tabular_data]
        print(tabulate(tabular_data, **kwargs))
    else:
        assert tabular_data is None or len(tabular_data) == 0, 'Expected no data, got %s' % tabular_data
        print(tabulate([[str(None) for _ in kwargs.get('headers', (None,))]], **kwargs))

def _vectorise(arg):
    """
    If arg is scalar then transform to a vector.
    
    The return type is always tuple, list or dict.
    If the type of 'arg' is not one of these then it is considered to be scalar.
    If 'arg' is scalar then a sequence is returned that contains 'arg'.
    
    A string is considered scalar by this function.
    The Python language considers type string to be a sequence.
    """
    return arg if isinstance(arg, (tuple, list, dict)) else (arg, )

print_table = _print_plain_table

try:
    __IPYTHON__
    print_table = _display_rich
    _display = display
except NameError:
    pass

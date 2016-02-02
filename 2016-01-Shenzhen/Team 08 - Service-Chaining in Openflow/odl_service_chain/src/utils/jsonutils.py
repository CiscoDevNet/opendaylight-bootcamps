import inspect
import sys
import functools
import xmlrpclib
import six
import datetime
import itertools

DEFAULT_DATETIME_FORMAT='%Y-%m-%dT%H:%M:%S.%f'
_simple_types = (six.string_types + six.integer_types
                 + (type(None), bool, float))
_nasty_type_tests = [inspect.ismodule, inspect.isclass, inspect.ismethod,
                     inspect.isfunction, inspect.isgeneratorfunction,
                     inspect.isgenerator, inspect.istraceback, inspect.isframe,
                     inspect.iscode, inspect.isbuiltin, inspect.isroutine,
                     inspect.isabstract]

if sys.version_info < (2, 7):
    # On Python <= 2.6, json module is not C boosted, so try to use
    # simplejson module if available
    try:
        import simplejson as json
    except ImportError:
        import json
else:
    import json

def utcnow():
    """Overridable version of utils.utcnow."""
    if utcnow.override_time:
        try:
            return utcnow.override_time.pop(0)
        except AttributeError:
            return utcnow.override_time
    return datetime.datetime.utcnow()

def strtime(at=None, fmt=DEFAULT_DATETIME_FORMAT):
    """Returns formatted utcnow."""
    if not at:
        at = utcnow()
    return at.strftime(fmt)

def to_primitive(value, convert_instances=False, convert_datetime=True,
                 level=0, max_depth=3):
    """Convert a complex object into primitives.

    Handy for JSON serialization. We can optionally handle instances,
    but since this is a recursive function, we could have cyclical
    data structures.

    To handle cyclical data structures we could track the actual objects
    visited in a set, but not all objects are hashable. Instead we just
    track the depth of the object inspections and don't go too deep.

    Therefore, convert_instances=True is lossy ... be aware.

    """
    # handle obvious types first - order of basic types determined by running
    # full tests on nova project, resulting in the following counts:
    # 572754 <type 'NoneType'>
    # 460353 <type 'int'>
    # 379632 <type 'unicode'>
    # 274610 <type 'str'>
    # 199918 <type 'dict'>
    # 114200 <type 'datetime.datetime'>
    #  51817 <type 'bool'>
    #  26164 <type 'list'>
    #   6491 <type 'float'>
    #    283 <type 'tuple'>
    #     19 <type 'long'>
    if isinstance(value, _simple_types):
        return value

    if isinstance(value, datetime.datetime):
        if convert_datetime:
            return strtime(value)
        else:
            return value

    # value of itertools.count doesn't get caught by nasty_type_tests
    # and results in infinite loop when list(value) is called.
    if type(value) == itertools.count:
        return six.text_type(value)

    if level > max_depth:
        return '?'

    # The try block may not be necessary after the class check above,
    # but just in case ...
    try:
        recursive = functools.partial(to_primitive,
                                      convert_instances=convert_instances,
                                      convert_datetime=convert_datetime,
                                      level=level,
                                      max_depth=max_depth)
        if isinstance(value, dict):
            return dict((k, recursive(v)) for k, v in six.iteritems(value))
        elif isinstance(value, (list, tuple)):
            return [recursive(lv) for lv in value]

        # It's not clear why xmlrpclib created their own DateTime type, but
        # for our purposes, make it a datetime type which is explicitly
        # handled
        if isinstance(value, xmlrpclib.DateTime):
            value = datetime.datetime(*tuple(value.timetuple())[:6])

        if convert_datetime and isinstance(value, datetime.datetime):
            return strtime(value)
        elif hasattr(value, 'iteritems'):
            return recursive(dict(value.iteritems()), level=level + 1)
        elif hasattr(value, '__iter__'):
            return recursive(list(value))
        elif convert_instances and hasattr(value, '__dict__'):
            # Likely an instance of something. Watch for cycles.
            # Ignore class member vars.
            return recursive(value.__dict__, level=level + 1)
        else:
            if any(test(value) for test in _nasty_type_tests):
                return six.text_type(value)
            return value
    except TypeError:
        # Class objects are tricky since they may define something like
        # __iter__ defined but it isn't callable as list().
        return six.text_type(value)

def safe_decode(text, incoming=None, errors='strict'):
    """Decodes incoming text/bytes string using `incoming` if they're not
       already unicode.

    :param incoming: Text's current encoding
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a unicode `incoming` encoded
                representation of it.
    :raises TypeError: If text is not an instance of str
    """
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be decoded" % type(text))

    if isinstance(text, six.text_type):
        return text

    if not incoming:
        incoming = (sys.stdin.encoding or
                    sys.getdefaultencoding())

    try:
        return text.decode(incoming, errors)
    except UnicodeDecodeError:
        # Note(flaper87) If we get here, it means that
        # sys.stdin.encoding / sys.getdefaultencoding
        # didn't return a suitable encoding to decode
        # text. This happens mostly when global LANG
        # var is not set correctly and there's no
        # default encoding. In this case, most likely
        # python will use ASCII or ANSI encoders as
        # default encodings but they won't be capable
        # of decoding non-ASCII characters.
        #
        # Also, UTF-8 is being used since it's an ASCII
        # extension.
        return text.decode('utf-8', errors)

def dumps(value, default=to_primitive, **kwargs):
    return json.dumps(value, default=default, **kwargs)


def loads(s, encoding='utf-8'):
    return json.loads(safe_decode(s, encoding))

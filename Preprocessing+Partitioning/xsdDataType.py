# -*- coding: utf-8 -*-
"""
    Created on Mon Sep 2 10:15:32 2024

    Class that represents a XSD DataType parser object with its parsing methods.

    @author: drakopablo
"""
import re
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from functools import lru_cache

import isodate
import pandas as pd
from dateutil.parser import parse as date_parse

# TODO: improve "filter_best_datatype" function's filter.
class XSDDataType():
    """
        Class that represents a XSD data type parser.

        Notas:
            * Sin espacios en blanco (al principio o al final)
            * El separador numérico es el punto "."
            * El separador de fechas es el guión "-" (o "/" si no es estricto)
            * El separador de horas son los dos puntos ":"

        Full dictionary:
        xsd_type_dict = {
            # Booleans
                "xsd:boolean":  REGEX_XSD_BOOLEAN, # `boolean` represents the values of two-valued logic.
            # Numeric values
                "xsd:integer":  REGEX_XSD_INTEGER, # `integer` is ·derived· from decimal by fixing the value of ·fractionDigits· to be 0 and disallowing the trailing decimal point. This results in the standard mathematical concept of the integer numbers.  The ·value space· of integer is the infinite set {...,-2,-1,0,1,2,...}. The ·base type· of integer is decimal.
                "xsd:decimal":  REGEX_XSD_DECIMAL, # `decimal` represents a subset of the real numbers, which can be represented by decimal numerals. The ·value space· of decimal is the set of numbers that can be obtained by dividing an integer by a non-negative power of ten, i.e., expressible as i / 10n where i and n are integers and n ≥ 0. Precision is not reflected in this value space; the number 2.0 is not distinct from the number 2.00. The order relation on decimal is the order relation on real numbers, restricted to this subset.
                "xsd:float":    REGEX_XSD_FLOAT, # The `float` datatype is patterned after the IEEE single-precision 32-bit floating point datatype [IEEE 754-2008]. Its value space is a subset of the rational numbers. Floating point numbers are often used to approximate arbitrary real numbers.
                "xsd:double":   REGEX_XSD_DOUBLE, # The `double` datatype is patterned after the IEEE double-precision 64-bit floating point datatype [IEEE 754-2008]. Each floating point datatype has a value space that is a subset of the rational numbers.  Floating point numbers are often used to approximate arbitrary real numbers.
            # Dates, times, and durations. According to the Seven-property Model: https://www.w3.org/TR/xmlschema11-2/#theSevenPropertyModel
                "xsd:date": REGEX_XSD_DATE, # `date` represents top-open intervals of exactly one day in length on the timelines of dateTime, beginning on the beginning moment of each day, up to but not including the beginning moment of the next day). For non-timezoned values, the top-open intervals disjointly cover the non-timezoned timeline, one per day.  For timezoned values, the intervals begin at every minute and therefore overlap.
                "xsd:time": REGEX_XSD_TIME, # `time` represents instants of time that recur at the same point in each calendar day, or that occur in some arbitrary calendar day.
                "xsd:dateTime": REGEX_XSD_DATETIME, # `dateTime` represents instants of time, optionally marked with a particular time zone offset.  Values representing the same instant but having different time zone offsets are equal but not identical.
                "xsd:dateTimeStamp": REGEX_XSD_DATETIMESTAMP, # The `dateTimeStamp` datatype is ·derived· from dateTime by giving the value required to its explicitTimezone facet. The result is that all values of dateTimeStamp are required to have explicit time zone offsets and the datatype is totally ordered.
                "xsd:duration": REGEX_XSD_DURATION, # `duration` is a datatype that represents durations of time. The concept of duration being captured is drawn from those of [ISO 8601], specifically durations without fixed endpoints. For example, "15 days" (whose most common lexical representation in duration is "'P15D'") is a duration value; "15 days beginning 12 July 1995" and "15 days ending 12 July 1995" are not duration values. duration can provide addition and subtraction operations between duration values and between duration/dateTime value pairs, and can be the result of subtracting dateTime values. However, only addition to dateTime is required for XML Schema processing and is defined in the function ·dateTimePlusDuration·.
                "xsd:gYear": REGEX_XSD_GYEAR, # `gYear` represents Gregorian calendar years.
                "xsd:gMonth": REGEX_XSD_GMONTH, # `gMonth` represents whole (Gregorian) months within an arbitrary year—months that recur at the same point in each year. It might be used, for example, to say what month annual Thanksgiving celebrations fall in different countries (--11 in the United States, --10 in Canada, and possibly other months in other countries).
                "xsd:gDay": REGEX_XSD_GDAY, # `gDay` represents whole days within an arbitrary month—days that recur at the same point in each (Gregorian) month. This datatype is used to represent a specific day of the month. To indicate, for example, that an employee gets a paycheck on the 15th of each month. (Obviously, days beyond 28 cannot occur in all months; they are nonetheless permitted, up to 31.)
                "xsd:gYearMonth": REGEX_XSD_GYEARMONTH, # `gYearMonth` represents specific whole Gregorian months in specific Gregorian years.
                "xsd:gMonthDay": REGEX_XSD_GMONTHDAY, # `gMonthDay` represents whole calendar days that recur at the same point in each calendar year, or that occur in some arbitrary calendar year. (Obviously, days beyond 28 cannot occur in all Februaries; 29 is nonetheless permitted.)
            # Binaries
                "xsd:hexBinary": REGEX_XSD_HEXBINARY, # `hexBinary` represents arbitrary hex-encoded binary data.
                "xsd:base64Binary": REGEX_XSD_BASE64BINARY, # `base64Binary` represents arbitrary Base64-encoded binary data. For base64Binary data the entire binary stream is encoded using the Base64 Encoding defined in [RFC 3548], which is derived from the encoding described in [RFC 2045].
            # Text based
                "xsd:anyURI": REGEX_XSD_ANYURI, # `anyURI` represents an Internationalized Resource Identifier Reference (IRI). An anyURI value can be absolute or relative, and may have an optional fragment identifier (i.e., it may be an IRI Reference). This type should be used when the value fulfills the role of an IRI, as defined in [RFC 3987] or its successor(s) in the IETF Standards Track.
        }

        TODO:
            Regex verbose: https://docs.python.org/3/howto/regex.html#:~:text=For%20example%2C%20here%E2%80%99s%20a%20RE%20that%20uses%20re.VERBOSE%3B%20see%20how%20much%20easier%20it%20is%20to%20read%3F
    """
    DEFAULT_XSD_DATATYPES = {"xsd:boolean", "xsd:integer", "xsd:decimal", "xsd:float", "xsd:date", "xsd:time", "xsd:dateTime", "xsd:dateTimeStamp", "xsd:duration", "xsd:hexBinary"}
    ALL_XSD_DATATYPES = {"xsd:boolean", "xsd:integer", "xsd:decimal", "xsd:float", "xsd:double", "xsd:date", "xsd:time", "xsd:dateTime", "xsd:dateTimeStamp", "xsd:duration", "xsd:gYear", "xsd:gMonth", "xsd:gDay", "xsd:gYearMonth", "xsd:gMonthDay", "xsd:hexBinary", "xsd:base64Binary", "xsd:anyURI"}
    DEFAULT_CACHE_MAXSIZE = 1024 * 4 # 4096

    def __init__(self, filter_xsd_datatypes:list[str]=list(DEFAULT_XSD_DATATYPES),
                 use_any_uri:bool=True, use_permanent_iana_uri_scheme:bool=False,
                 use_lru_cache:bool=True, cache_maxsize:int|None=DEFAULT_CACHE_MAXSIZE):
        # Filter xsd datatypes' dictionary entries
        if use_any_uri:
            self.use_permanent_iana_uri_scheme = use_permanent_iana_uri_scheme
            self.filter_xsd_datatypes = filter_xsd_datatypes + ["xsd:anyURI"]
        else:
            self.filter_xsd_datatypes = filter_xsd_datatypes
        # Using LRU cache
        self._use_lru_cache = use_lru_cache
        self.set_cache_maxsize(cache_maxsize)

    @property
    def xsd_type_dict(self) -> dict:
        """
            Returns a dictionary with the Regex expressions.
            
            Constants for regex expressions: https://www.w3.org/TR/xmlschema11-2/#built-in-primitive-datatypes

            TODO: Check other date formats: https://en.wikipedia.org/wiki/List_of_date_formats_by_country
            TODO: Maybe separate this constants to another file
            TODO: Maybe add some flags to choose what types to check. (done in __init__)
        """
        #############
        ### REGEX ###
        #############

        # Booleans
        REGEX_XSD_BOOLEAN   = r"[Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee]|1|0"
        # Numeric values
        REGEX_SEP_NUMBER    = r"[.]"
        REGEX_XSD_INTEGER   = r"[+-]?[0-9]+"
        REGEX_XSD_DECIMAL   = r"[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)"
        REGEX_INFINITY      = r"[Ii][Nn][Ff]"
        REGEX_NAN           = r"[Nn][Aa][Nn]"
        REGEX_XSD_FLOAT     = r"[+-]?([0-9]+("+REGEX_SEP_NUMBER+r"[0-9]*)?|"+REGEX_SEP_NUMBER+r"[0-9]+)([Ee][+-]?[[0-9]]+)?|[+-]?"+REGEX_INFINITY+"|"+REGEX_NAN # TODO: strict: 32 bit
        REGEX_XSD_DOUBLE    = r"[+-]?([0-9]+("+REGEX_SEP_NUMBER+r"[0-9]*)?|"+REGEX_SEP_NUMBER+r"[0-9]+)([Ee][+-]?[[0-9]]+)?|[+-]?"+REGEX_INFINITY+"|"+REGEX_NAN # TODO: strict: 64 bit
        # Dates, times, and durations
        REGEX_SEP_DATE      = r"[-/]" # (!) default value: "-"
        REGEX_SEP_TIME      = r"[:]" # (!) default value: ":"
        REGEX_FRAG_YEAR     = r"([1-9][0-9]{3,}|0[0-9]{3})"
        REGEX_FRAG_MONTH    = r"(0[1-9]|1[0-2])"
        REGEX_FRAG_DAY      = r"(0[1-9]|[12][0-9]|3[01])"
        REGEX_FRAG_HOUR     = r"([01][0-9]|2[0-3])"
        REGEX_FRAG_MINUTE   = r"[0-5][0-9]"
        REGEX_FRAG_SECOND   = r"[0-5][0-9](\.[0-9]+)?" # TODO: stric: with microseconds
        REGEX_TIMEZONE_OFFSET = r"(Z|[+-]((0[0-9]|1[0-3]):[0-5][0-9]|14:00))"
        REGEX_XSD_GYEAR     = REGEX_FRAG_YEAR+REGEX_TIMEZONE_OFFSET+r"?" # "timezoneOffset" remains optional
        REGEX_XSD_GMONTH    = REGEX_FRAG_MONTH+REGEX_TIMEZONE_OFFSET+r"?" # "timezoneOffset" remains optional
        REGEX_XSD_GDAY      = REGEX_FRAG_DAY+REGEX_TIMEZONE_OFFSET+r"?" # "timezoneOffset" remains optional
        REGEX_XSD_GYEARMONTH= REGEX_FRAG_YEAR+r"-"+REGEX_FRAG_MONTH+REGEX_TIMEZONE_OFFSET+r"?" # "timezoneOffset" remains optional
        REGEX_XSD_GMONTHDAY = r"--"+REGEX_FRAG_MONTH+r"-"+REGEX_FRAG_DAY+REGEX_TIMEZONE_OFFSET+r"?" # "timezoneOffset" remains optional
        REGEX_XSD_DATE      = r"-?"+REGEX_FRAG_YEAR+REGEX_SEP_DATE+REGEX_FRAG_MONTH+REGEX_SEP_DATE+REGEX_FRAG_DAY+REGEX_TIMEZONE_OFFSET+r"?" # "timezoneOffset" remains optional
        REGEX_XSD_TIME      = r"("+REGEX_FRAG_HOUR+REGEX_SEP_TIME+REGEX_FRAG_MINUTE+REGEX_SEP_TIME+REGEX_FRAG_SECOND+r"|(24:00:00(\.0+)?))"+REGEX_TIMEZONE_OFFSET+r"?"  # "timezoneOffset" remains optional
        REGEX_XSD_DATETIME  = REGEX_XSD_DATE+r"T"+REGEX_XSD_TIME # strictly without "timezoneOffset"
        REGEX_XSD_DATETIMESTAMP = REGEX_XSD_DATETIME+REGEX_TIMEZONE_OFFSET
        REGEX_XSD_DURATION  = r"-?P[0-9]+Y?([0-9]+M)?([0-9]+D)?(T([0-9]+H)?([0-9]+M)?([0-9]+(\.[0-9]+)?S)?)?"
        # Binaries
        REGEX_XSD_HEXBINARY = r"([0-9a-fA-F]{2})+" # NOTE: due to this string can be empty, we force the "+" closure instead of "*"
        REGEX_XSD_BASE64BINARY  = r"(([A-Za-z0-9+/] ?){4})*(([A-Za-z0-9+/] ?){3}[A-Za-z0-9+/]|([A-Za-z0-9+/] ?){2}[AEIMQUYcgkosw048] ?=|[A-Za-z0-9+/] ?[AQgw] ?= ?=)"
            # Text based
            # https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml (Permanent ones only)
        REGEX_IANA_URI_SCHEME = r'([A-Za-z])[A-Za-z0-9+\-\.]*' if not self.use_permanent_iana_uri_scheme else r'(aaa|aaas|about|acap|acct|cap|cid|coap|coap[+]tcp|coap[+]ws|coaps|coaps[+]tcp|coaps[+]ws|crid|data|dav|dict|dns|dtn|example|file|ftp|geo|go|gopher|h323|http|https|iax|icap|im|imap|info|ipn|ipp|ipps|iris|iris.beep|iris.lwz|iris.xpc|iris.xpcs|jabber|ldap|leaptofrogans|mailto|mid|msrp|msrps|mt|mtqp|mupdate|news|nfs|ni|nih|nntp|opaquelocktoken|pkcs11|pop|pres|reload|rtsp|rtsps|rtspu|service|session|shttp (OBSOLETE)|sieve|sip|sips|sms|snmp|soap.beep|soap.beeps|stun|stuns|tag|tel|telnet|tftp|thismessage|tip|tn3270|turn|turns|tv|urn|vemmi|vnc|ws|wss|xcon|xcon-userid|xmlrpc.beep|xmlrpc.beeps|xmpp|z39.50r|z39.50s)'
            # valid URI: https://www.w3.org/2011/04/XMLSchema/TypeLibrary-IRI-RFC3987.xsd
        REGEX_XSD_ANYURI = r"(("+REGEX_IANA_URI_SCHEME+"):((//(((([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽!$&'()*+,;=:]|(%[0-9A-Fa-f][0-9A-Fa-f]))*@))?((\[((((([0-9A-Fa-f]{0,4}:)){6}(([0-9A-Fa-f]{0,4}:[0-9A-Fa-f]{0,4})|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))))|(::(([0-9A-Fa-f]{0,4}:)){5}(([0-9A-Fa-f]{0,4}:[0-9A-Fa-f]{0,4})|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))))|(([0-9A-Fa-f]{0,4})?::(([0-9A-Fa-f]{0,4}:)){4}(([0-9A-Fa-f]{0,4}:[0-9A-Fa-f]{0,4})|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))))|((((([0-9A-Fa-f]{0,4}:))?[0-9A-Fa-f]{0,4}))?::(([0-9A-Fa-f]{0,4}:)){3}(([0-9A-Fa-f]{0,4}:[0-9A-Fa-f]{0,4})|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))))|((((([0-9A-Fa-f]{0,4}:)){0,2}[0-9A-Fa-f]{0,4}))?::(([0-9A-Fa-f]{0,4}:)){2}(([0-9A-Fa-f]{0,4}:[0-9A-Fa-f]{0,4})|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))))|((((([0-9A-Fa-f]{0,4}:)){0,3}[0-9A-Fa-f]{0,4}))?::[0-9A-Fa-f]{0,4}:(([0-9A-Fa-f]{0,4}:[0-9A-Fa-f]{0,4})|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))))|((((([0-9A-Fa-f]{0,4}:)){0,4}[0-9A-Fa-f]{0,4}))?::(([0-9A-Fa-f]{0,4}:[0-9A-Fa-f]{0,4})|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))))|((((([0-9A-Fa-f]{0,4}:)){0,5}[0-9A-Fa-f]{0,4}))?::[0-9A-Fa-f]{0,4})|((((([0-9A-Fa-f]{0,4}:)){0,6}[0-9A-Fa-f]{0,4}))?::))|(v[0-9A-Fa-f]+\.[A-Za-z0-9\-\._~!$&'()*+,;=:]+))\])|(([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5]))\.([0-9]|([1-9][0-9])|(1([0-9]){2})|(2[0-4][0-9])|(25[0-5])))|(([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=]))*)((:[0-9]*))?)((/(([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=:@]))*))*)|(/(((([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=:@]))+((/(([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=:@]))*))*))?)|((([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=:@]))+((/(([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=:@]))*))*)|)((\?(([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=:@])|[-󰀀-󿿽􀀀-􏿽/?])*))?((#((([A-Za-z0-9\-\._~ -퟿豈-﷏ﷰ-￯𐀀-🿽𠀀-𯿽𰀀-𿿽񀀀-񏿽񐀀-񟿽񠀀-񯿽񰀀-񿿽򀀀-򏿽򐀀-򟿽򠀀-򯿽򰀀-򿿽󀀀-󏿽󐀀-󟿽󡀀-󯿽]|(%[0-9A-Fa-f][0-9A-Fa-f])|[!$&'()*+,;=:@])|/|\?))*))?)"
            # TODO: more...

        ############
        ### DICT ###
        ############

        # Return final dictionary
        xsd_type_dict = {
        # Booleans
            "xsd:boolean":  REGEX_XSD_BOOLEAN, # `boolean` represents the values of two-valued logic.
        # Numeric values
            "xsd:integer":  REGEX_XSD_INTEGER, # `integer` is ·derived· from decimal by fixing the value of ·fractionDigits· to be 0 and disallowing the trailing decimal point. This results in the standard mathematical concept of the integer numbers.  The ·value space· of integer is the infinite set {...,-2,-1,0,1,2,...}. The ·base type· of integer is decimal.
            "xsd:decimal":  REGEX_XSD_DECIMAL, # `decimal` represents a subset of the real numbers, which can be represented by decimal numerals. The ·value space· of decimal is the set of numbers that can be obtained by dividing an integer by a non-negative power of ten, i.e., expressible as i / 10n where i and n are integers and n ≥ 0. Precision is not reflected in this value space; the number 2.0 is not distinct from the number 2.00. The order relation on decimal is the order relation on real numbers, restricted to this subset.
            "xsd:float":    REGEX_XSD_FLOAT, # The `float` datatype is patterned after the IEEE single-precision 32-bit floating point datatype [IEEE 754-2008]. Its value space is a subset of the rational numbers. Floating point numbers are often used to approximate arbitrary real numbers.
            "xsd:double":   REGEX_XSD_DOUBLE, # The `double` datatype is patterned after the IEEE double-precision 64-bit floating point datatype [IEEE 754-2008]. Each floating point datatype has a value space that is a subset of the rational numbers.  Floating point numbers are often used to approximate arbitrary real numbers.
        # Dates, times, and durations. [According to the Seven-property Model: https://www.w3.org/TR/xmlschema11-2/#theSevenPropertyModel]
            "xsd:date":     REGEX_XSD_DATE, # `date` represents top-open intervals of exactly one day in length on the timelines of dateTime, beginning on the beginning moment of each day, up to but not including the beginning moment of the next day). For non-timezoned values, the top-open intervals disjointly cover the non-timezoned timeline, one per day.  For timezoned values, the intervals begin at every minute and therefore overlap.
            "xsd:time":     REGEX_XSD_TIME, # `time` represents instants of time that recur at the same point in each calendar day, or that occur in some arbitrary calendar day.
            "xsd:dateTime": REGEX_XSD_DATETIME, # `dateTime` represents instants of time, optionally marked with a particular time zone offset.  Values representing the same instant but having different time zone offsets are equal but not identical.
            "xsd:dateTimeStamp":REGEX_XSD_DATETIMESTAMP, # The `dateTimeStamp` datatype is ·derived· from dateTime by giving the value required to its explicitTimezone facet. The result is that all values of dateTimeStamp are required to have explicit time zone offsets and the datatype is totally ordered.
            "xsd:duration":     REGEX_XSD_DURATION, # `duration` is a datatype that represents durations of time. The concept of duration being captured is drawn from those of [ISO 8601], specifically durations without fixed endpoints. For example, "15 days" (whose most common lexical representation in duration is "'P15D'") is a duration value; "15 days beginning 12 July 1995" and "15 days ending 12 July 1995" are not duration values. duration can provide addition and subtraction operations between duration values and between duration/dateTime value pairs, and can be the result of subtracting dateTime values. However, only addition to dateTime is required for XML Schema processing and is defined in the function ·dateTimePlusDuration·.
            "xsd:gYear":    REGEX_XSD_GYEAR, # `gYear` represents Gregorian calendar years.
            "xsd:gMonth":   REGEX_XSD_GMONTH, # `gMonth` represents whole (Gregorian) months within an arbitrary year—months that recur at the same point in each year. It might be used, for example, to say what month annual Thanksgiving celebrations fall in different countries (--11 in the United States, --10 in Canada, and possibly other months in other countries).
            "xsd:gDay":     REGEX_XSD_GDAY, # `gDay` represents whole days within an arbitrary month—days that recur at the same point in each (Gregorian) month. This datatype is used to represent a specific day of the month. To indicate, for example, that an employee gets a paycheck on the 15th of each month. (Obviously, days beyond 28 cannot occur in all months; they are nonetheless permitted, up to 31.)
            "xsd:gYearMonth":   REGEX_XSD_GYEARMONTH, # `gYearMonth` represents specific whole Gregorian months in specific Gregorian years.
            "xsd:gMonthDay":    REGEX_XSD_GMONTHDAY, # `gMonthDay` represents whole calendar days that recur at the same point in each calendar year, or that occur in some arbitrary calendar year. (Obviously, days beyond 28 cannot occur in all Februaries; 29 is nonetheless permitted.)
        # Binaries
            "xsd:hexBinary": REGEX_XSD_HEXBINARY, # `hexBinary` represents arbitrary hex-encoded binary data.
            "xsd:base64Binary": REGEX_XSD_BASE64BINARY, # `base64Binary` represents arbitrary Base64-encoded binary data. For base64Binary data the entire binary stream is encoded using the Base64 Encoding defined in [RFC 3548], which is derived from the encoding described in [RFC 2045].
        # Text based
            "xsd:anyURI":   REGEX_XSD_ANYURI, # `anyURI` represents an Internationalized Resource Identifier Reference (IRI). An anyURI value can be absolute or relative, and may have an optional fragment identifier (i.e., it may be an IRI Reference). This type should be used when the value fulfills the role of an IRI, as defined in [RFC 3987] or its successor(s) in the IETF Standards Track.
        }

        # Return dictionary with filtered keys (it doesn't return errors)
        result_dict = {}
        result_keys = xsd_type_dict.keys()
        for key in self.filter_xsd_datatypes:
            if key in result_keys:
                result_dict[key] = xsd_type_dict[key]
        return result_dict

    def _initialize_cache(self):
        """
            Initializes the cached functions with the the current maxsize
        """
        # Internal cache instances
        self._cached_infer_xsd_type_native = lru_cache(maxsize=self._cache_maxsize)(self._infer_xsd_type_native)
        self._cached_infer_xsd_type_regex = lru_cache(maxsize=self._cache_maxsize)(self._infer_xsd_type_regex)

    def set_cache_maxsize(self, cache_maxsize:int|None):
        """
            Sets the lru cache maxsize.
        """
        if cache_maxsize is None:
            self._cache_maxsize = None
        else:
            self._cache_maxsize = abs(cache_maxsize) if abs(cache_maxsize) <= self.DEFAULT_CACHE_MAXSIZE else self.DEFAULT_CACHE_MAXSIZE
        if self._use_lru_cache:
            self._initialize_cache()
    
    def _infer_xsd_type_regex(self, x: str|None = None) -> str:
        """
            Infers the XSD data type.

            Args:
                x: element/string to parse.

            Returns:
                str with the inferred xsd type.
        """
        DEFAULT_XSD_TYPE = "xsd:string" # The string datatype represents character strings in XML.
        def re_exact_pattern(pattern):
            """
                Returns the exact regex expression. This is, '^expression$'
            """
            patterns = []
            if pattern.startswith("^"):
                if pattern.endswith("$"):
                    patterns = [pattern]
                else:
                    patterns = [pattern, "$"]
            elif pattern.endswith("$"):
                patterns = ["^", pattern]
            else:
                patterns = ["^", pattern, "$"]
            return "".join(patterns)

        if x is None:
            return "xsd:float" # (!) It could also be "NaN" or "infinity"
        for key, value in self.xsd_type_dict.items():
            # p = re.compile(re_exact_pattern(value)) # (!) Matches the exact pattern
            # m = p.match(x)
            p = re.compile(value) # TODO: If python version >= 3.4 # NOTE: It may raise [FutureWarning: Possible nested set at position X]
            m = p.fullmatch(x) # (!) Matches the exact pattern
            if m:
                #print("\t>>> Match found:", m.group(0))
                return key
        return DEFAULT_XSD_TYPE

    def _infer_xsd_type_native(self, x: str = None) -> str:
        """
            Infers the xsd type with native language supportted methods.

            Args:
                x: element/string to parse.

            Returns:
                str with the inferred xsd type.
        """
        # Helper functions for specific types
        def is_boolean(x: str) -> bool:
            return re.fullmatch(r"[Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee]|1|0", x) is not None #x in ["true", "false", "1", "0"]

        def is_integer(x: str) -> bool:
            #return re.fullmatch(r"[-+]?\d+", x) is not None
            try:
                int(x)
                return True
            except ValueError:
                try:
                    int(float(x))
                    return True
                except ValueError:
                    return False

        def is_float(x: str) -> bool:
            #return re.fullmatch(r"[-+]?\d+", x) is not None
            try:
                float(x)
                return True
            except:
                return False
            
        def is_decimal(x: str) -> bool:
            try:
                Decimal(x)
                return True
            except:
                return False

        def is_date(x: str) -> bool:
            # TODO: check non-standard formatting
            try:
                date_parse(x)
                return True
            except:
                return False

        def is_duration(x: str) -> bool:
            # TODO: check non-standard formatting
            try:
                isodate.parse_duration(x)
                return True
            except:
                return False

        def is_time(x: str) -> bool:
            # TODO: check non-standard formatting
            try:
                datetime.strptime(x, "%H:%M:%S")
                return True
            except:
                return False

        # Inference order based on specificity
        if x is None:
            return "xsd:float" # (!) It could also be "NaN" or "infinity"
        elif is_boolean(x):
            return "xsd:boolean"
        elif is_integer(x):
            return "xsd:integer"
        elif is_float(x):
            return "xsd:float" # (!) It could also be "NaN" or "infinity"
        elif is_decimal(x):
            return "xsd:decimal"
        elif is_duration(x):
            return "xsd:duration"
        elif is_time(x):
            return "xsd:time"
        elif is_date(x):
            return "xsd:dateTime"  # Could be further refined for xsd:date, xsd:gYear, etc.

        # Default fallback
        return "xsd:string"

    def _xsd_type_parser(self, x: str, strict_case:bool=True) -> str:
        """ 
            Returns the inferred xsd data type from the given string. It assumes the string is correctly transformed.

            Args:
                x: element/string to parse.
                strict_case: If true, it will apply strictly regex matching case to the elements, following the XML specifications.
                get_cache_info: If true, the cache information of the `lru_cache` will be returned.
                clear_cache: If true, the cache information of the `lru_cache` will be cleared.

            Returns:
                str with the inferred xsd type.
        """
        result = self._infer_xsd_type_native(x)
        # Check if 'strict_case' flag activated and default case found
        if strict_case:
            if result in ['xsd:string','xsd:decimal','xsd:float','xsd:double']:
                result = self._infer_xsd_type_regex(x)
        return result
    
    def xsd_type_parser(self, x: str, strict_case:bool=True) -> str:
        """
            Returns the inferred xsd data type from the given string.  It assumes the string is not transformed.

            Args:
                x: element/string to parse.
                strict_case: If true, it will apply strictly regex matching case to the elements, following the XML specifications.
                get_cache_info: If true, the cache information of the `lru_cache` will be returned.
                clear_cache: If true, the cache information of the `lru_cache` will be cleared.

            Returns:
                str with the inferred xsd type.
        """
        _x = str(x).upper().strip()
        return self._xsd_type_parser(_x, strict_case=strict_case)
    
    def _cached_xsd_type_parser(self, x: str, strict_case:bool=True, 
                         get_cache_info:bool=False, clear_cache:bool=False) -> str:
        """ 
            Returns the inferred xsd data type from the given string. It assumes the string is correctly transformed.

            Args:
                x: element/string to parse.
                strict_case: If true, it will apply strictly regex matching case to the elements, following the XML specifications.
                get_cache_info: If true, the cache information of the `lru_cache` will be returned.
                clear_cache: If true, the cache information of the `lru_cache` will be cleared.

            Returns:
                str with the inferred xsd type.
        """
        if clear_cache: #hasattr(self, '_cached_infer_xsd_type_native') and clear_cache:
            self._cached_infer_xsd_type_native.cache_clear()
            self._cached_infer_xsd_type_regex.cache_clear()
        elif get_cache_info:  #hasattr(self, '_cached_infer_xsd_type_native') and get_cache_info:
            result = "Cache info:\n" + \
                    "\tself._cached_infer_xsd_type_native.cache_info(): " + \
                        str(self._cached_infer_xsd_type_native.cache_info()) + \
                        "\n" + \
                    "\tself._cached_infer_xsd_type_regex.cache_info(): " + \
                        str(self._cached_infer_xsd_type_regex.cache_info())
            return result
        else:
            result = self._cached_infer_xsd_type_native(x)
            # Check if 'strict_case' flag activated and default case found
            if strict_case:
                if result in ['xsd:string','xsd:decimal','xsd:float','xsd:double']:
                    result = self._cached_infer_xsd_type_regex(x)
            return result
    
    def cached_xsd_type_parser(self, x: str, strict_case:bool=True, 
                        get_cache_info:bool=False, clear_cache:bool=False) -> str:
        """
            Returns the inferred xsd data type from the given string.  It assumes the string is not transformed.

            Args:
                x: element/string to parse.
                strict_case: If true, it will apply strictly regex matching case to the elements, following the XML specifications.
                get_cache_info: If true, the cache information of the `lru_cache` will be returned.
                clear_cache: If true, the cache information of the `lru_cache` will be cleared.

            Returns:
                str with the inferred xsd type.
        """
        _x = str(x).upper().strip()
        return self._cached_xsd_type_parser(_x, strict_case=strict_case, get_cache_info=get_cache_info, clear_cache=clear_cache)
    
    @staticmethod
    def filter_best_datatype(result_dict:pd.DataFrame, max_depth:int=1) -> dict:
        """
            Filters the best datatype results of the resulting dictionary.

            Args:
                result_dict: DataFrame from where to filter the results.
                max_depth: The maximum number of best results to return.
        """
        # TODO: It's not as easy as returning the "best" datatype. Some hierarchy may be considered.
        # For example, a string has more weight than an integer type. Apart from that, values equal to 0 must be deleted.
        # TODO: So check ordenation criteria here
        aux_dict = {k:dict(v) for k,v in result_dict.items()}
        keys_name = list(aux_dict.keys())
        #keys_datatype = [next(iter(s)) for s in list(aux_dict.values())] # First best result
        keys_datatype = [[j for i,j in enumerate(s) if i < max_depth] for s in list(aux_dict.values())] # Rank of "max_depth" best results
        result_dict = {keys_name[i]:keys_datatype[i] for i in range(0, len(keys_name))}

    def _cached_parse_df(self, df: pd.DataFrame, strict_case:bool=True,
                 vectorize_dataframe:bool=False, eafp_lbyl:bool=True,
                 ordered_datatypes:bool=True, sort_keys=False,
                 show_only_best_datatypes:bool=False, dynamic_cache_size:bool=False,
                 print_cache_info:bool=False, clear_cache:bool=False) -> dict:
        """
            Parses the given dataframe and returns a dictionary of a column with its possible xsd data types. With caching.

            Args:
                df: pd.DataFrame with the dataframe to parse.
                strict_case: If true, it will apply strictly regex matching case to the elements, following the XML specifications.
                vectorize_dataframe: If true, it will apply vectorization to the dataframe for the needed operations. If set, `eafp_lbyl` will be ignored.
                eafp_lbyl: If true, it will use the "Easier to Ask For Forgiveness Than Permission (EAFP)" policy, instead of "Look Before You Leap (LBYL)"
                ordered_datatypes: If true, it will apply ascending value ordering to the found datatypes. This is, the most representative will be found first.
                sort_keys: If true, as in json.dumps(), the keys of the dictionary will be sorted in ascending order.
                show_only_best_datatypes: If true, the resulting dictionary will be compacted to show only the best possible datatype match.
                dynamic_cache_size: If true, the cache maximum size will be updated according to the number of unique values in the current column.
                print_cache_info: If true, the cache information of the `lru_cache` will be printed.
                clear_cache: If true, the cache information of the `lru_cache` will be cleared.

            Returns:
                dict with the parsing results. 
                TODO: it's pending to do an statistical analysis of the resulting data.
                TODO: Python 3.11 has "zero-cost exceptions"
                TODO: It's implemented the option to dynamically set the maxsize of the cache. However, it's not used in vectorized data
        """
        result_dict = {}
        if not self._use_lru_cache:
            raise ValueError("`use_lru_cache` is not set. Thus, caching is disabled.")
        if vectorize_dataframe:
            # Apply vectorized operations to preprocess the data
            #df = df.applymap(lambda x: str(x).upper().strip())
            # Apply the xsd_type_parser function to each element in the DataFrame. Just in case, we transform it to string
            parsed_df = df.applymap(lambda x: self._cached_xsd_type_parser(str(x), strict_case=strict_case))
            # Count occurrences of each inferred type per column
            result_dict = parsed_df.apply(pd.Series.value_counts).fillna(0).astype(int).to_dict()
            result_dict = {k:{m:w for m,w in v.items() if w > 0} for k,v in result_dict.items()}
            # Show cache info
            if print_cache_info:
                print(self._cached_xsd_type_parser(None, get_cache_info=True))
        else:
            # We iterate over the columns of the dataframe
            for column_name, column_data in df.items():
                if dynamic_cache_size:
                    cache_maxsize = int(column_data.nunique())
                    self.set_cache_maxsize(cache_maxsize)
                for x in column_data:
                    # Apply the xsd_type_parser function to each element of the current column of the DataFrame. Just in case, we transform it to string
                    xsd_type = self._cached_xsd_type_parser(str(x), strict_case=strict_case)
                    if eafp_lbyl: # Easier to Ask For Forgiveness Than Permission (EAFP) or Look Before You Leap (LBYL)
                        try:
                            result_dict[column_name][xsd_type] += 1
                        except KeyError:
                            try:
                                result_dict[column_name] |= {xsd_type: 1}
                            except KeyError:
                                result_dict |= {column_name: {xsd_type: 1}}
                    else:
                        if column_name not in result_dict:
                            result_dict[column_name] = {}
                        if xsd_type not in result_dict[column_name]:
                            result_dict[column_name][xsd_type] = 0
                        result_dict[column_name][xsd_type] += 1
            # Show cache info
            if print_cache_info:
                print(self._cached_xsd_type_parser(None, get_cache_info=True))
        # We check if any flag is set
        if sort_keys:
            result_dict = OrderedDict(sorted(result_dict.items(), key=lambda t: t[0]))
        if ordered_datatypes:
            for k, v in result_dict.items():
                result_dict[k] = OrderedDict(sorted(v.items(), key=lambda t: t[1], reverse=True))
        if self._use_lru_cache and clear_cache:
            # self._cached_xsd_type_parser(None, clear_cache=True)
            self._cached_xsd_type_parser(None, clear_cache=True)
        if show_only_best_datatypes:
            result_dict = self.filter_best_datatype(result_dict)
        # Return the results' dictionary
        return result_dict

    def _parse_df(self, df: pd.DataFrame, strict_case:bool=True,
                 vectorize_dataframe:bool=False, eafp_lbyl:bool=True,
                 ordered_datatypes:bool=True, sort_keys=False,
                 show_only_best_datatypes:bool=False) -> dict:
        """
            Parses the given dataframe and returns a dictionary of a column with its possible xsd data types. Without caching.

            Args:
                df: pd.DataFrame with the dataframe to parse.
                strict_case: If true, it will apply strictly regex matching case to the elements, following the XML specifications.
                vectorize_dataframe: If true, it will apply vectorization to the dataframe for the needed operations. If set, `eafp_lbyl` will be ignored.
                eafp_lbyl: If true, it will use the "Easier to Ask For Forgiveness Than Permission (EAFP)" policy, instead of "Look Before You Leap (LBYL)"
                ordered_datatypes: If true, it will apply ascending value ordering to the found datatypes. This is, the most representative will be found first.
                sort_keys: If true, as in json.dumps(), the keys of the dictionary will be sorted in ascending order.
                show_only_best_datatypes: If true, the resulting dictionary will be compacted to show only the best possible datatype match.

            Returns:
                dict with the parsing results. 
                TODO: it's pending to do an statistical analysis of the resulting data.
                TODO: Python 3.11 has "zero-cost exceptions"
        """
        result_dict = {}
        if vectorize_dataframe:
            # Apply vectorized operations to preprocess the data
            #df = df.applymap(lambda x: str(x).upper().strip())
            # Apply the xsd_type_parser function to each element in the DataFrame. Just in case, we transform it to string
            parsed_df = df.applymap(lambda x: self._xsd_type_parser(str(x), strict_case=strict_case))
            # Count occurrences of each inferred type per column
            result_dict = parsed_df.apply(pd.Series.value_counts).fillna(0).astype(int).to_dict()
            result_dict = {k:{m:w for m,w in v.items() if w > 0} for k,v in result_dict.items()}
        else:
            # We iterate over the columns of the dataframe
            for column_name, column_data in df.items():
                for x in column_data:
                    # Apply the xsd_type_parser function to each element of the current column of the DataFrame. Just in case, we transform it to string
                    xsd_type = self.xsd_type_parser(str(x), strict_case=strict_case)
                    if eafp_lbyl: # Easier to Ask For Forgiveness Than Permission (EAFP) or Look Before You Leap (LBYL)
                        try:
                            result_dict[column_name][xsd_type] += 1
                        except KeyError:
                            try:
                                result_dict[column_name] |= {xsd_type: 1}
                            except KeyError:
                                result_dict |= {column_name: {xsd_type: 1}}
                    else:
                        if column_name not in result_dict:
                            result_dict[column_name] = {}
                        if xsd_type not in result_dict[column_name]:
                            result_dict[column_name][xsd_type] = 0
                        result_dict[column_name][xsd_type] += 1
        # We check if any flag is set
        if sort_keys:
            result_dict = OrderedDict(sorted(result_dict.items(), key=lambda t: t[0]))
        if ordered_datatypes:
            for k, v in result_dict.items():
                result_dict[k] = OrderedDict(sorted(v.items(), key=lambda t: t[1], reverse=True))
        if show_only_best_datatypes:
            result_dict = self.filter_best_datatype(result_dict)
        # Return the results' dictionary
        return result_dict

    def parse_df(self, df: pd.DataFrame, strict_case:bool=True,
                 vectorize_dataframe:bool=False, eafp_lbyl:bool=True,
                 ordered_datatypes:bool=True, sort_keys=False,
                 show_only_best_datatypes:bool=False, dynamic_cache_size:bool=False,
                 print_cache_info:bool=False, clear_cache:bool=False) -> dict:
        """
            Parses the given dataframe and returns a dictionary of a column with its possible xsd data types.

            Args:
                df: pd.DataFrame with the dataframe to parse.
                strict_case: If true, it will apply strictly regex matching case to the elements, following the XML specifications.
                vectorize_dataframe: If true, it will apply vectorization to the dataframe for the needed operations. If set, `eafp_lbyl` will be ignored.
                eafp_lbyl: If true, it will use the "Easier to Ask For Forgiveness Than Permission (EAFP)" policy, instead of "Look Before You Leap (LBYL)"
                ordered_datatypes: If true, it will apply ascending value ordering to the found datatypes. This is, the most representative will be found first.
                sort_keys: If true, as in json.dumps(), the keys of the dictionary will be sorted in ascending order.
                show_only_best_datatypes: If true, the resulting dictionary will be compacted to show only the best possible datatype match.
                dynamic_cache_size: If true, the cache maximum size will be updated according to the number of unique values in the current column.
                print_cache_info: If true, the cache information of the `lru_cache` will be printed.
                clear_cache: If true, the cache information of the `lru_cache` will be cleared.

            Returns:
                dict with the parsing results. 
                TODO: it's pending to do an statistical analysis of the resulting data.
                TODO: Python 3.11 has "zero-cost exceptions"
        """
        #result_dict = {}
        if self._use_lru_cache:
            ### With caching information
            return self._cached_parse_df(df,strict_case,vectorize_dataframe,eafp_lbyl,ordered_datatypes,sort_keys,show_only_best_datatypes,dynamic_cache_size,print_cache_info,clear_cache)
        else:
            ### Without caching information
            return self._parse_df(df,strict_case,vectorize_dataframe,eafp_lbyl,ordered_datatypes,sort_keys,show_only_best_datatypes)
        #return result_dict

### MAIN ###
def test_XSDDataType():
    from time import time
    # Examples
    result1 = {}
    result2 = {}
    result3 = {}
    result4 = {}
    result5 = {}
    result6 = {}
    time1 = 0
    time2 = 0
    time3 = 0
    time4 = 0
    time5 = 0
    time6 = 0

    samples = ["true", "2023-08-23", "12.34", "P1Y2M", "15:30:00", "123", "Hello World", "https://regexr.com/"]
    samples2 = ["https://regexr.com/", "https://zh.wikipedia.org/wiki/中国大陆报纸列表", "oeoe"]
    samples3 = samples2 + samples
    aux = pd.DataFrame({"samples3": samples3})

    cache_maxsize = None #1024 * 4
    xsdDT = XSDDataType(use_lru_cache=True, cache_maxsize=cache_maxsize)
    print(f"# Try 3: cache_maxsize=Dynamic or {cache_maxsize}")
    ###### RUNTIME ###
    ini = time()
    # aux = dataframe
    result1 = xsdDT.parse_df(aux, clear_cache=True, dynamic_cache_size=False)
    ###### RUNTIME ###
    time1 = time()-ini
    print("Result 1:",time1)

    ###### RUNTIME ###
    ini = time()
    # aux = dataframe
    result2 = xsdDT.parse_df(aux, eafp_lbyl=False, clear_cache=True, dynamic_cache_size=False)
    ###### RUNTIME ###
    time2 = time()-ini
    print("Result 2:",time2)

    ##### RUNTIME ###
    ini = time()
    # aux = dataframe
    result3 = xsdDT.parse_df(aux, vectorize_dataframe=True, clear_cache=True, dynamic_cache_size=False)
    ###### RUNTIME ###
    time3 = time()-ini
    print("Result 3:",time3)

    # ###### RUNTIME ###
    # ini = time()
    # # aux = dataframe
    # result4 = xsdDT.parse_df(aux, strict_case=False)
    # ###### RUNTIME ###
    # time4 = time()-ini
    # print("Result 4:",time4)

    # ###### RUNTIME ###
    # ini = time()
    # # aux = dataframe
    # result5 = xsdDT.parse_df(aux, eafp_lbyl=False, strict_case=False)
    # ###### RUNTIME ###
    # time5 = time()-ini
    # print("Result 5:",time5)
    
    # ###### RUNTIME ###
    # ini = time()
    # # aux = dataframe
    # result6 = xsdDT.parse_df(aux, vectorize_dataframe=True, strict_case=False)
    # ###### RUNTIME ###
    # time6 = time()-ini
    # print("Result 6:",time6)

    results = {
        "result1": result1,
        "result2": result2,
        "result3": result3,
        # "result4": result4,
        # "result5": result5,
        # "result6": result6,
    }

    print("Best Result Strict:", min(time1, time2, time3))
    # print("Best Result Not Strict:", min(time4, time5, time6))
    # print("Best Result Overall:", min(time1, time2, time3, time4, time5, time6))

    #print("Results:\n", json.dumps(results, sort_keys=False, indent=2))
    
    # keys_name = [{k:[m for m,_ in v.items()]} for k, v in results.items()]
    # keys_datatype = [[*x.values()] for x in [dict(v.items()) for _, v in results.items()]]

    # keys_name = flat_matrix([[["_".join([k,w]) for w in v] for k,v in dict_name.items()] for dict_name in keys_name],1)
    # keys_datatype = [next(iter(s)) for s in flat_matrix(keys_datatype, 1)]
    # resultss = {keys_name[i]:keys_datatype[i] for i in range(0, len(keys_name))}
    
    #print("Results:\n", json.dumps(resultss, sort_keys=False, indent=2))

    # result_dict = {k:dict(v) for k,v in result3.items()}
    # keys_name = list(result_dict.keys())
    # keys_datatype = [next(iter(s)) for s in list(result_dict.values())]
    # resultsss = {keys_name[i]:keys_datatype[i] for i in range(0, len(keys_name))}
    # print("Results:\n", json.dumps(resultsss, sort_keys=False, indent=2))

if __name__ == "__main__":
    test_XSDDataType()
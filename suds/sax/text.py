# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jeff Ortel ( jortel@redhat.com )

"""
Contains XML text classes.
"""

from suds import *
from suds.sax import *


class Text(unicode):
    """
    An XML text object used to represent text content.
    @ivar lang: The (optional) language flag.
    @type lang: bool
    @ivar escaped: The (optional) XML special character escaped flag.
    @type escaped: bool
    """
    __slots__ = ('_lang', '_escaped',)

    _EMPTY = None
    
    @classmethod
    def __valid(cls, *args):
        return ( len(args) and args[0] is not None )
    
    def __new__(cls, *args, **kwargs):
        v = args[0]
        if v:
            if kwargs:
                lang = kwargs.pop('lang', None)
                escaped = kwargs.pop('escaped', False)
                result = unicode.__new__(cls, *args, **kwargs)
                result._lang = lang
                result._escaped = escaped
                return result
            else:
                return unicode.__new__(cls, *args)
        else:
            return None if v is None else cls._EMPTY

    @property
    def lang(self):
        return getattr(self, "_lang", None)

    @property
    def escaped(self):
        return getattr(self, "_escaped", False)
    
    def escape(self):
        """
        Encode (escape) special XML characters.
        @return: The text with XML special characters escaped.
        @rtype: L{Text}
        """
        if not self.escaped:
            post = sax.encoder.encode(self)
            escaped = ( post != self )
            return Text(post, lang=self.lang, escaped=escaped)
        return self
    
    def unescape(self):
        """
        Decode (unescape) special XML characters.
        @return: The text with escaped XML special characters decoded.
        @rtype: L{Text}
        """
        if self.escaped:
            post = sax.encoder.decode(self)
            return Text(post, lang=self.lang)
        return self
    
    def trim(self):
        post = self.strip()
        return Text(post, lang=self.lang, escaped=self.escaped)
    
    def __add__(self, other):
        joined = u''.join((self, other))
        result = Text(joined, lang=self.lang, escaped=self.escaped)
        if isinstance(other, Text):
            result.escaped = ( self.escaped or other.escaped )
        return result
    
    def __repr__(self):
        s = [self]
        if self.lang is not None:
            s.append(' [%s]' % self.lang)
        if self.escaped:
            s.append(' <escaped>')
        return ''.join(s)
    
    def __getstate__(self):
        return {"lang": self.lang, "escaped": self.escaped}
    
    def __setstate__(self, state):
        self.lang = state["lang"]
        self.escaped = state["escaped"]

Text._EMPTY = unicode.__new__(Text)
    
    
class Raw(Text):
    """
    Raw text which is not XML escaped.
    This may include I{string} XML.
    """
    def escape(self):
        return self
    
    def unescape(self):
        return self
    
    def __add__(self, other):
        joined = u''.join((self, other))
        return Raw(joined, lang=self.lang)

"""Shared by RIPPS2's host tests: the patched tree's source as the tests before build 104 knew it.

Build 104 put RIPPS2's English through _t("...") (and N_("...") in tables). unwrap() gives the source with those
wrappers around literals taken off, so a check written against "COPY" still finds it; a compiled extract gets
TR_STUBS for the _t(...) calls left on names. test_ripps2_build104.py checks the wrapping itself.
"""
import re

_LIT = re.compile(r'\b(?:_t|N_)\(\s*((?:"(?:[^"\\\n]|\\.)*"\s*)+?)\s*\)')

TR_STUBS = '#define _t(s) (s)\n#define N_(s) (s)\n'


def unwrap(text):
    return _LIT.sub(lambda m: m.group(1), text)

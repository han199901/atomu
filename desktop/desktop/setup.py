#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup
from Cython.Build import cythonize

setup(name='atomudesktop',
        ext_modules=cythonize("*.py",
            compiler_directives={'language_level' : "3"})
)

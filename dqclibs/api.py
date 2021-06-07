import os
import sys
import ctypes
import ctypes.util
import numpy as np
from typing import Callable, Dict, Any

__all__ = ["CINT", "CGTO", "CPBC", "CSYMM"]

# libraries
_ext = "dylib" if sys.platform == "darwin" else "so"
_libcint_relpath = os.path.join("libs", f"libcint.{_ext}")
_libcgto_relpath = os.path.join("libs", f"libcgto.{_ext}")
_libcpbc_relpath = os.path.join("libs", f"libpbc.{_ext}")
# _libcvhf_relpath = os.path.join("libs", f"libcvhf.{_ext}")
_libcsymm_relpath = os.path.join("libs", f"libsymm.{_ext}")

_libs: Dict[str, Any] = {}

def _library_loader(name: str, relpath: str) -> Callable:
    curpath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(curpath, relpath))

    # load the library and cache the handler
    def fcn():
        if name not in _libs:
            try:
                _libs[name] = ctypes.cdll.LoadLibrary(path)
            except OSError as e:
                path2 = ctypes.util.find_library(name)
                if path2 is None:
                    raise e
                _libs[name] = ctypes.cdll.LoadLibrary(path2)
        return _libs[name]
    return fcn

CINT = _library_loader("cint", _libcint_relpath)
CGTO = _library_loader("cgto", _libcgto_relpath)
CPBC = _library_loader("cpbc", _libcpbc_relpath)
# CVHF = _library_loader("CVHF", _libcvhf_relpath)
CSYMM = _library_loader("symm", _libcsymm_relpath)

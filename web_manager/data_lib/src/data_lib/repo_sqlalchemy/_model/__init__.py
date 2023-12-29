# Import `ModelAssembler` class
from ._assembler import MappingAssembler

# Create package-global `ModelAssembler` instance
mapping_assembler = MappingAssembler()
"""Package-global `MappingAssembler` instance"""

# Invoke mapping units registration
from . import types
from . import mapping_units

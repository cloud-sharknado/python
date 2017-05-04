#!/usr/bin/python3
# Reading Nested and Variable-Sized Binary Structures

import struct

class StructField:
	'''
	Descriptor representing a simple structure field.
	'''
	def __init__(self, fmt, offset):
		self.fmt = fmt
		self.offset = offset

	def __get__(self, instance, cls):
		if instance is None:
			return self
		else:
			r = struct.unpack_from(self.fmt, instance._buffer, self.offset)
			return r[0] if len(r) == 1 else r

class NestedStruct:
	'''
	Descriptor representing a nested structure.
	'''
	def __init__(self, name, struct_type, offset):
		self.name = name
		self.struct_type = struct_type
		self.offset = offset

	def __get__(self, instance, cls):
		if instance is None:
			return self
		else:
			data = instance._buffer[self.offset:self.offset+self.struct_type.struct_size]
			result = self.struct_type(data)
			# Save resulting structure back on instance to avoid
			# further recomputation of this step
			setattr(instance, self.name, result)
			return result

class StructureMeta(type):
	'''
	Metaclass that automatically creates StructFiled descriptors
	'''

	def __init__(self, clsname, bases, clsdict):
		fields = getattr(self, '_fields_', [])
		byte_order = ''
		offset = 0
		for fmt, fieldname in fields:
			if isinstance(fmt, StructureMeta):
				setattr(self, fieldname, NestedStruct(fieldname, fmt, offset))
				offset += fmt.struct_size
			else:
				if fmt.startswith(('<', '>', '!', '@')):
					byte_order = fmt[0]
					fmt = fmt[1:]
				fmt = byte_order + fmt
				setattr(self, fieldname, StructField(fmt, offset))
				offset += struct.calcsize(fmt)
		setattr(self, 'struct_size', offset)

class Structure(metaclass=StructureMeta):
	def __init__(self, bytedata):
		self._buffer = bytedata

	@classmethod
	def from_file(cls, f):
		return cls(f.read(cls.struct_size))

class PolyHeader(Structure):
	_fields_ = [
		('<i', 'file_code'),
		('d', 'min_x'),
		('d', 'min_y'),
		('d', 'max_x'),
		('d', 'max_y'),
		('d', 'num_polys')
	]

class Point(Structure):
	_fields_ = [
		('<d', 'x'),
		('d', 'y')
	]

class PolyHeader(Structure):
	_fields_ = [
	('<i', 'file_code'),
	(Point, 'min'),
	(Point, 'max'),
	('i', 'num_polys')
	]
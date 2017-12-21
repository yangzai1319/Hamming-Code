"""
File:		hamming.py
Author:		Dominic Carrano (carrano.dominic@gmail.com)
Created:	December 18, 2017

Implementation of Hamming single error correction, double error detection
(SECDED) codes for bitstrings. Supports encoding of bit and bytearrays as
a bitarray, as well as error detection/correction of bitarrays to decode.
"""

import bitarray

BITS_PER_BYTE = 8

def encode(bits):
	pass

def decode(bits):
	pass

# there's other ways to implement this algorithm... TODO: try drafting out alternatives
# and comparing performance
def data_bits_covered(parity, lim):
	"""
	Yields the indices of all data bits covered by a specified parity bit in a bitstring
	of length lim. The indices are relative to just the data bitstring itself, not including
	parity bits.
	"""
	if not is_power_of_two(parity):
		raise ValueError("All hamming parity bits are indexed by powers of two.")

	data_index  = 1		# the data bit we're currently at (indexed starting at 1)
	total_index = 3 	# index for parity + data. start at 1-index of first data bit
						# within entire sequence, which is at 3 since first 2 bits are parity

	while data_index <= lim:
		curr_bit_is_data = not is_power_of_two(total_index)
		if curr_bit_is_data and (total_index % (parity << 1)) >= parity:	
			yield data_index - 1						# adjust output to be zero indexed
		data_index += curr_bit_is_data
		total_index += 1
	return None

def is_power_of_two(n):
	"""
	Returns true if the given non-negative integer n is a power of two.
	Algorithm credit: https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2
	"""
	return (not (n == 0)) and ((n & (n - 1)) == 0)

def bytes_to_bits(byte_stream):
	"""
	Converts the given bytearray byte_stream to a bitarray by converting 
	each successive byte into its appropriate binary data bits and appending 
	them to the bitarray.

	>>> from bitarray import bitarray
	>>> foo = bytearray(b'\x11\x23\x6C')
	>>> bytes_to_bits(foo)
	bitarray('000100010010001101101100')
	"""
	out = bitarray.bitarray()
	for byte in byte_stream:
		data = bin(byte)[2:].zfill(BITS_PER_BYTE)
		for bit in data:
			out.append(0 if bit == '0' else 1) # note that all bits go to 1 if we just append bit, since it's a non-null string
	return out

def bits_to_bytes(bits):
	"""
	Converts the given bitarray bits to a bytearray. 

	Assumes the last len(bits) - len(bits) / 8 * 8 bits are to 
	be interpreted as the least significant bits of the last byte 
	of data, e.g. 100 would map to the byte 00000100.

	>>> from bitarray import bitarray
	>>> foo = bitarray('100')
	>>> bits_to_bytes(foo)
	bytearray(b'\x04')
	>>> bar = bitarray('1010110011111111001100011000')
	>>> bits_to_bytes(bar)
	bytearray(b'\xAC\xFF\x31\x08')
	"""
	out = bytearray()
	for i in range(0, len(bits) // BITS_PER_BYTE * BITS_PER_BYTE, BITS_PER_BYTE):
		byte, k = 0, 0
		for bit in bits[i:i + BITS_PER_BYTE][::-1]:
			byte += bit * (1 << k)
			k += 1
		out.append(byte)

	# tail case
	if len(bits) % BITS_PER_BYTE:
		byte, k = 0, 0
		for bit in bits[int(len(bits) // BITS_PER_BYTE * BITS_PER_BYTE):][::-1]:
			byte += bit * (1 << k)
			k += 1
		out.append(byte)

	return out
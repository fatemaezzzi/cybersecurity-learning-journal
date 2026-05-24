# =============================================================================
#                     PYTHON struct MODULE — COMPLETE GUIDE
#             
#
#  What is this file?
#  Every single thing from the documentation is here, explained simply.
#  Read it top to bottom like a story. Run any section you want to test it.
# =============================================================================


# =============================================================================
# STEP 0 — IMPORT THE MODULE
# =============================================================================

import struct
# This is the only import you need.
# You can also do: from struct import * (imports everything directly)
# Then you don't need to type "struct." before every function.

from struct import pack, unpack, pack_into, unpack_from, iter_unpack, calcsize
# This lets you call pack() directly instead of struct.pack()


# =============================================================================
# STEP 1 — THE BIG PICTURE
# =============================================================================

# The struct module is a TRANSLATOR between two worlds:
#
#   PYTHON WORLD          ←——struct——→       BYTES WORLD
#   (integers, floats,                    (raw bytes like \x00\xff
#    strings, bools)                       that networks/files use)
#
# You PACK   → turn Python values into raw bytes  (to send/save)
# You UNPACK → turn raw bytes into Python values  (to read/receive)
#
# Example of raw bytes — they look like this:
example_bytes = b'\x03\xe8'
# Each \xNN is one byte. NN is a hex number (00 to ff = 0 to 255).
# This is how data looks when it travels over a network or sits in a file.


# =============================================================================
# STEP 2 — THE FORMAT STRING (THE RECIPE)
# =============================================================================

# Every struct function needs a FORMAT STRING.
# Think of it as a recipe that tells struct:
#   - which direction bytes go  (first character)
#   - what types of values      (the letters after)
#
# Format string looks like this:  '>ih'
#                                  ↑ ↑↑
#                    byte order ───┘ └┴── data type letters
#
# It's always a normal Python string like '>', '<', '>ih', '<5sf' etc.


# =============================================================================
# STEP 3 — BYTE ORDER (THE FIRST CHARACTER OF FORMAT STRING)
# =============================================================================

# Your computer stores multi-byte numbers in memory byte by byte.
# But which byte comes first? That depends on the CPU/system.
#
# Example: the number 1000 in hex is 0x000003E8
#          bytes are: 00, 00, 03, E8
#
# Big-endian    → most significant byte first  →  00 00 03 E8
# Little-endian → least significant byte first →  E8 03 00 00
#
# The first character of your format string controls this.
# Here are ALL the options:

# ------- '>' — Big-endian -------
# Most significant byte comes FIRST.
# Used in: networking (most network protocols use this)
# Result is IDENTICAL on every machine. Safe for cross-platform use.
result_big = struct.pack('>h', 1000)
print(result_big)    # b'\x03\xe8'   ← 03 comes first

# ------- '<' — Little-endian -------
# Least significant byte comes FIRST.
# Used in: Intel/AMD CPUs (most Windows/Linux PCs)
# Result is IDENTICAL on every machine. Safe for cross-platform use.
result_little = struct.pack('<h', 1000)
print(result_little)  # b'\xe8\x03'   ← e8 comes first

# ------- '!' — Network byte order -------
# This is EXACTLY the same as '>' (big-endian).
# Just a convenient alias. Use it when specifically working with networks.
# The '!' comes from IETF RFC 1700 (an official internet standard document).
result_network = struct.pack('!h', 1000)
print(result_network)  # b'\x03\xe8'   ← same as '>'

# ------- '@' — Native byte order (with native size & alignment) -------
# Uses YOUR computer's natural byte order AND your computer's natural sizes.
# The result may be DIFFERENT on different machines.
# Also adds invisible padding bytes automatically (explained later).
# Use ONLY when talking to C code on the SAME machine.
result_native = struct.pack('@h', 1000)
print(result_native)  # depends on your machine

# ------- '=' — Native byte order (with standard size, no alignment) -------
# Uses YOUR computer's natural byte order BUT fixed standard sizes.
# No automatic padding. Slightly more predictable than '@'.
# Still machine-dependent byte order though.
result_native_std = struct.pack('=h', 1000)
print(result_native_std)  # depends on your machine's byte order

# ------- No prefix at all — same as '@' -------
# If you don't write any prefix, Python assumes '@' (native).
result_no_prefix = struct.pack('h', 1000)  # same as '@h'
print(result_no_prefix)

# ── SIMPLE RULE FOR BEGINNERS ──────────────────────────────────────────────
# Just always use '>' or '<'. Forget '@', '=', '!' for now.
# Use '>' when dealing with networks.
# Use '<' when dealing with Windows files or Intel-specific formats.
# This keeps your code predictable on every machine.
# ────────────────────────────────────────────────────────────────────────────


# =============================================================================
# STEP 4 — FORMAT CHARACTERS (THE DATA TYPE LETTERS)
# =============================================================================

# After the byte-order character, you write letters that represent data types.
# Each letter tells struct: "the next value is THIS type."

# ── INTEGER TYPES ─────────────────────────────────────────────────────────

# 'b' — signed char — small integer — range: -128 to 127 — 1 byte
struct.pack('>b', 100)      # ✅ works
struct.pack('>b', -50)      # ✅ works
# struct.pack('>b', 200)    # ❌ error! 200 is too big for 'b'

# 'B' — unsigned char — small positive integer — range: 0 to 255 — 1 byte
struct.pack('>B', 200)      # ✅ works (200 fits in unsigned)
# struct.pack('>B', -1)     # ❌ error! no negatives in unsigned

# 'h' — short — medium integer — range: -32768 to 32767 — 2 bytes
struct.pack('>h', 1000)     # ✅ works
# struct.pack('>h', 99999)  # ❌ error! too big

# 'H' — unsigned short — range: 0 to 65535 — 2 bytes
struct.pack('>H', 60000)    # ✅ works

# 'i' — int — normal integer — range: about -2 billion to 2 billion — 4 bytes
struct.pack('>i', 1000000)  # ✅ works

# 'I' — unsigned int — range: 0 to about 4 billion — 4 bytes
struct.pack('>I', 3000000000)  # ✅ works

# 'l' — long — same range as 'i' in standard mode — 4 bytes
struct.pack('>l', 1000000)  # ✅ works

# 'L' — unsigned long — 4 bytes
struct.pack('>L', 3000000000)  # ✅ works

# 'q' — long long — very large integer — 8 bytes
# range: about -9 quintillion to 9 quintillion
struct.pack('>q', 9000000000000)  # ✅ works

# 'Q' — unsigned long long — 8 bytes — range: 0 to ~18 quintillion
struct.pack('>Q', 9000000000000)  # ✅ works

# 'n' — ssize_t — only available in NATIVE mode ('@') — size varies
# This is a C type for sizes (like array sizes). Only use with '@'.
struct.pack('@n', 100)      # ✅ native only

# 'N' — size_t — only available in NATIVE mode ('@') — size varies
struct.pack('@N', 100)      # ✅ native only

# ── FLOATING POINT TYPES ──────────────────────────────────────────────────

# 'e' — half precision float — 2 bytes — range: ~0.00006 to ~65504
# Not very precise. Rarely used. Added in Python 3.6.
struct.pack('>e', 3.14)     # ✅ but loses precision

# 'f' — float — single precision — 4 bytes — about 7 decimal digits of precision
struct.pack('>f', 3.14)     # ✅ common for floats

# 'd' — double — double precision — 8 bytes — about 15 decimal digits
struct.pack('>d', 3.141592653589793)  # ✅ very precise

# ── COMPLEX NUMBER TYPES (added in Python 3.14) ────────────────────────────

# 'F' — float complex — 8 bytes (real part as float + imaginary part as float)
struct.pack('>F', 3+4j)     # ✅ packs 3.0 and 4.0 each as 4-byte floats

# 'D' — double complex — 16 bytes (real as double + imaginary as double)
struct.pack('>D', 3+4j)     # ✅ packs 3.0 and 4.0 each as 8-byte doubles

# ── BOOLEAN TYPE ──────────────────────────────────────────────────────────

# '?' — bool — True or False — 1 byte
struct.pack('>?', True)     # b'\x01'
struct.pack('>?', False)    # b'\x00'

# When UNPACKING, any non-zero byte becomes True:
struct.unpack('>?', b'\x05')   # (True,)   ← 5 is non-zero so it's True
struct.unpack('>?', b'\x00')   # (False,)  ← 0 is False

# ── STRING/BYTES TYPES ────────────────────────────────────────────────────

# 'c' — single character — 1 byte — value must be a bytes object of length 1
struct.pack('>c', b'A')     # b'A'
struct.pack('>c', b'Z')     # b'Z'

# '4c' — four separate single characters
struct.pack('>4c', b'H', b'e', b'l', b'l')  # b'Hell'  ← 4 separate values

# 's' — byte string — IMPORTANT: the number means LENGTH, not repeat count!
# '5s' = one string of 5 bytes (not five separate strings)
struct.pack('>5s', b'hello')   # b'hello'   ← one value of 5 bytes

# If string is TOO SHORT → padded with \x00 (null bytes)
struct.pack('>8s', b'hello')   # b'hello\x00\x00\x00'  ← padded to 8 bytes

# If string is TOO LONG → truncated (extra bytes cut off)
struct.pack('>3s', b'hello')   # b'hel'  ← only first 3 bytes kept

# '0s' — empty string — special case
struct.pack('>0s', b'')        # b''

# 'p' — Pascal string — DIFFERENT from 's'
# First byte stores the LENGTH, then the actual string follows.
# The count includes the length byte itself.
# Example: '5p' with b'hi' → stores: [2, h, i, \x00, \x00]
#          first byte is 2 (length of 'hi'), then 'hi', then padding
struct.pack('>5p', b'hi')      # b'\x02hi\x00\x00'
#                                    ↑↑ length=2, then 'hi', then nulls

# Max string length Pascal can store is 255 (because length must fit in 1 byte)
# When unpacking 'p', the result is the actual string WITHOUT the length byte.

# ── PAD BYTE ─────────────────────────────────────────────────────────────

# 'x' — pad byte — inserts ONE \x00 byte — no Python value consumed/produced
struct.pack('>xh', 1000)    # b'\x00\x03\xe8'  ← 1 pad byte, then 1000
struct.pack('>2xh', 1000)   # b'\x00\x00\x03\xe8'  ← 2 pad bytes, then 1000
# 'x' is used in STANDARD mode to manually add padding where needed.

# ── POINTER TYPE ─────────────────────────────────────────────────────────

# 'P' — void pointer — only in NATIVE mode — size varies (4 or 8 bytes)
# Used when working with C pointers. Very advanced. Ignore for now.
struct.pack('@P', 0)        # native only, size depends on 64-bit vs 32-bit


# =============================================================================
# STEP 5 — REPEAT COUNTS (NUMBERS BEFORE LETTERS)
# =============================================================================

# Put a number before a letter to repeat it.
# '4h' means four shorts — same as 'hhhh'

struct.pack('>4h', 10, 20, 30, 40)
# same as struct.pack('>hhhh', 10, 20, 30, 40)
# result: b'\x00\x0a\x00\x14\x00\x1e\x00\x28'

# BUT for 's', the number means string LENGTH, not repeat:
struct.pack('>4s', b'ABCD')    # one 4-byte string ← NOT four strings
struct.pack('>4c', b'A', b'B', b'C', b'D')  # four 1-byte chars

# Whitespace between format characters is ignored (but NOT inside a count+letter)
struct.pack('> i h', 100, 50)    # spaces between types are fine
# struct.pack('> 4 h', ...)      # ❌ space inside '4h' is NOT allowed

# =============================================================================
# STEP 6 — ALL MODULE-LEVEL FUNCTIONS
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# struct.pack(format, v1, v2, ...)
# ─────────────────────────────────────────────────────────────────────────────
# Converts Python values → bytes object.
# Number of values must EXACTLY match what the format expects.

packed = struct.pack('>bhl', 1, 2, 3)
# '>bhl' expects exactly 3 values: one b, one h, one l
print(packed)   # b'\x01\x00\x02\x00\x00\x00\x03'

# Error example — too many or too few values:
# struct.pack('>bh', 1)         # ❌ too few values
# struct.pack('>bh', 1, 2, 3)   # ❌ too many values


# ─────────────────────────────────────────────────────────────────────────────
# struct.unpack(format, buffer)
# ─────────────────────────────────────────────────────────────────────────────
# Converts bytes → Python tuple.
# The buffer (bytes object) must be EXACTLY the right size for the format.
# Always returns a TUPLE, even if there's only one value inside.

data = b'\x01\x00\x02\x00\x00\x00\x03'
result = struct.unpack('>bhl', data)
print(result)    # (1, 2, 3)   ← always a tuple

# One value? Still a tuple:
result2 = struct.unpack('>h', b'\x03\xe8')
print(result2)   # (1000,)   ← note the comma — it's a tuple

# To get just the value, index it:
value = result2[0]
print(value)     # 1000

# Error — buffer size must exactly match:
# struct.unpack('>h', b'\x00')         # ❌ too few bytes
# struct.unpack('>h', b'\x00\x01\x02') # ❌ too many bytes


# ─────────────────────────────────────────────────────────────────────────────
# struct.pack_into(format, buffer, offset, v1, v2, ...)
# ─────────────────────────────────────────────────────────────────────────────
# Packs values DIRECTLY INTO an existing writable buffer (like a bytearray).
# Instead of creating a NEW bytes object, it writes into an existing one.
# 'offset' = where in the buffer to start writing (in bytes from the start).
#
# Why use this? Efficiency. No new bytes object created. Good for large buffers.

# Create a writable buffer of 10 bytes (all zeros)
buf = bytearray(10)
print(buf)   # bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

# Pack the integer 999 as a short, starting at position 4 in the buffer
struct.pack_into('>h', buf, 4, 999)
print(buf)   # bytearray(b'\x00\x00\x00\x00\x03\xe7\x00\x00\x00\x00')
#                                          ↑↑↑↑  positions 4 and 5 changed

# Pack another value at position 0
struct.pack_into('>h', buf, 0, 42)
print(buf)   # bytearray(b'\x00\x2a\x00\x00\x03\xe7\x00\x00\x00\x00')

# Note: offset is REQUIRED — you can't skip it
# Note: buffer must be a WRITABLE type (bytearray, not bytes)


# ─────────────────────────────────────────────────────────────────────────────
# struct.unpack_from(format, buffer, offset=0)
# ─────────────────────────────────────────────────────────────────────────────
# Unpacks from a buffer starting at a specific position.
# The buffer can be LARGER than what you're reading — no exact size needed.
# offset defaults to 0 (start of buffer) if you don't specify it.
#
# This is the PAIR to pack_into — you use them together.

data = b'\x00\x00\x00\x00\x03\xe7\x00\x00'
result = struct.unpack_from('>h', data, offset=4)
print(result)   # (999,)   ← read from position 4

result2 = struct.unpack_from('>h', data, offset=0)
print(result2)  # (0,)     ← read from position 0

# No offset needed if reading from the start:
result3 = struct.unpack_from('>h', data)
print(result3)  # (0,)     ← defaults to offset=0


# ─────────────────────────────────────────────────────────────────────────────
# struct.iter_unpack(format, buffer)
# ─────────────────────────────────────────────────────────────────────────────
# Reads the SAME format REPEATEDLY from a buffer until the buffer is empty.
# Returns an ITERATOR (like a generator — reads one chunk at a time).
#
# Use this when you have a buffer containing many repeated fixed-size records.
# Like: a list of scores, a list of coordinates, a list of sensor readings.
#
# IMPORTANT: buffer size must be a MULTIPLE of the format size.
# If calcsize('>h') = 2, then buffer must be 2, 4, 6, 8... bytes long.

# Example: reading three short integers from a buffer
data = struct.pack('>hhh', 10, 20, 30)   # 6 bytes total (3 × 2 bytes)
print(data)   # b'\x00\x0a\x00\x14\x00\x1e'

for chunk in struct.iter_unpack('>h', data):
    print(chunk)
# (10,)
# (20,)
# (30,)

# Another example: reading multiple (x, y) coordinate pairs
coords_data = struct.pack('>6h', 1, 2, 3, 4, 5, 6)
for x, y in struct.iter_unpack('>hh', coords_data):
    print(f"x={x}, y={y}")
# x=1, y=2
# x=3, y=4
# x=5, y=6

# Added in Python 3.4


# ─────────────────────────────────────────────────────────────────────────────
# struct.calcsize(format)
# ─────────────────────────────────────────────────────────────────────────────
# Tells you HOW MANY BYTES a format string will produce/consume.
# Very useful to check your math before using pack/unpack.

struct.calcsize('>bhl')   # 7  (b=1, h=2, l=4)
struct.calcsize('>i')     # 4
struct.calcsize('>10s')   # 10
struct.calcsize('>?')     # 1
struct.calcsize('>4h')    # 8  (4 shorts × 2 bytes each)

# In NATIVE mode, sizes can differ:
struct.calcsize('@i')     # probably 4, but depends on machine
struct.calcsize('@l')     # 4 on Windows, 8 on Linux 64-bit!

print(struct.calcsize('>bhl'))   # 7


# =============================================================================
# STEP 7 — THE struct.error EXCEPTION
# =============================================================================

# struct.error is raised when something goes wrong.
# Always happens when:
#   - Value is out of range for its format
#   - Buffer is wrong size for unpack
#   - Format string has mistakes

try:
    struct.pack('>h', 99999)   # 'h' max is 32767
except struct.error as e:
    print(f"Error: {e}")
    # Error: 'h' format requires -32768 <= number <= 32767

try:
    struct.pack('>b', 200)     # 'b' max is 127 (signed)
except struct.error as e:
    print(f"Error: {e}")

try:
    struct.unpack('>hh', b'\x00\x01')   # format needs 4 bytes, only 2 given
except struct.error as e:
    print(f"Error: {e}")

# Always use try/except when unpacking data from external sources
# (files, network) because you can't always trust the data is correct.


# =============================================================================
# STEP 8 — NATIVE MODE DEEP DIVE (@ and =)
# =============================================================================

# ─── What is "native"? ────────────────────────────────────────────────────
#
# Your computer's CPU has a natural preference for storing bytes.
# Intel/AMD (most PCs, laptops, phones) = little-endian (small byte first)
# IBM mainframes, some network hardware = big-endian (big byte first)
#
# NATIVE means: "Use whatever MY computer naturally does. Don't change it."
#
# The result may be DIFFERENT on different machines.
# That's why you should NEVER use native for network or file data.

# ─── @ vs = difference ──────────────────────────────────────────────────

# '@' — native byte order + NATIVE sizes + NATIVE alignment (with padding!)
#   - Sizes depend on C compiler (l might be 4 or 8 bytes)
#   - Adds invisible pad bytes automatically for memory alignment
#   - Use ONLY for C interop on the same machine

# '=' — native byte order + STANDARD sizes + NO alignment
#   - Sizes are fixed (same as >, <)
#   - No automatic padding
#   - Byte order still depends on your machine

# ─── What is "alignment"? ────────────────────────────────────────────────
#
# Your CPU likes data to start at specific positions in memory.
# Specifically, an N-byte type prefers to start at a position divisible by N.
#
# Example: a 4-byte int prefers to start at positions 0, 4, 8, 12... (÷4)
#          if it starts at position 1, 2, or 3, the CPU still works but slower.
#
# In NATIVE mode ('@'), struct automatically adds invisible "pad bytes"
# between fields to maintain proper alignment, just like a C compiler would.
#
# These pad bytes contain nothing — they're just spacers.

# Example of automatic padding in native mode:
# 'c' = 1 byte char, 'i' = 4 byte int
# You'd expect: 1 + 4 = 5 bytes total
# But native mode adds 3 pad bytes after 'c' so 'i' starts at position 4:

size_ci = struct.calcsize('@ci')   # probably 8 (not 5!)
size_ic = struct.calcsize('@ic')   # probably 5 (int first, no padding needed)
print(f"@ci size: {size_ci}")   # 8
print(f"@ic size: {size_ic}")   # 5

# Visually for '@ci':
# [char][pad][pad][pad][int ][int ][int ][int ]
#  pos0  pos1 pos2 pos3 pos4  pos5  pos6  pos7

# In standard mode (>, <), this NEVER happens:
size_std = struct.calcsize('>ci')  # always 5 (no padding)
print(f">ci size: {size_std}")   # 5

# ─── Zero-repeat format trick (for native mode alignment) ─────────────────
#
# Sometimes you want to manually align the END of your struct in native mode.
# Use a zero-repeat format like '0l' or '0i' at the end.
# '0l' adds zero longs but DOES pad to the alignment of a long.

struct.calcsize('@llh')      # 18 — end is not aligned
struct.calcsize('@llh0l')    # 24 — padded to long boundary at the end

# This trick only works in NATIVE mode.
# In standard mode, use 'x' bytes for manual padding instead.

# ─── Checking your system's byte order ───────────────────────────────────
import sys
print(sys.byteorder)   # 'little' on Intel/AMD, 'big' on some others


# =============================================================================
# STEP 9 — STANDARD MODE — FOR CROSS-PLATFORM USE
# =============================================================================

# When exchanging data between machines, programs, or over networks:
# → Use STANDARD mode (>, <, or !)
# → Sizes are FIXED and PREDICTABLE everywhere
# → NO automatic padding — you control every byte

# ─── Standard sizes (always the same, everywhere) ─────────────────────────
#   b, B = 1 byte
#   h, H = 2 bytes
#   i, I = 4 bytes
#   l, L = 4 bytes
#   q, Q = 8 bytes
#   e    = 2 bytes
#   f    = 4 bytes
#   d    = 8 bytes
#   F    = 8 bytes (complex with float components)
#   D    = 16 bytes (complex with double components)
#   ?    = 1 byte
#   c    = 1 byte
#   x    = 1 byte (pad)

# ─── Manual padding in standard mode with 'x' ─────────────────────────────
# Since standard mode never adds padding automatically,
# you add 'x' bytes yourself wherever you need gaps.

# Example: align a long long after a short (need 6 pad bytes in between)
struct.calcsize('<qh6xq')   # 24   (8 + 2 + 6 pad + 8 = 24)
packed = struct.pack('<qh6xq', 1, 2, 3)

# The '6x' inserts 6 null bytes — no Python value needed for them
# When unpacking, 'x' bytes are skipped (no value returned for them)
a, b_val, c = struct.unpack('<qh6xq', packed)
print(a, b_val, c)   # 1 2 3


# =============================================================================
# STEP 10 — NAMING YOUR UNPACKED VALUES
# =============================================================================

# unpack() always returns a raw tuple like (b'raymond  ', 4658, 264, 8)
# This is hard to read. Two ways to make it nicer:

# ─── Option 1: Unpack directly into named variables ──────────────────────

record = b'raymond   \x32\x12\x08\x01\x08'
name, serialnum, school, gradelevel = struct.unpack('<10sHHb', record)
print(name)         # b'raymond   '
print(serialnum)    # 4658
print(gradelevel)   # 8

# ─── Option 2: Use namedtuple (cleaner, recommended) ─────────────────────

from collections import namedtuple

# Define the structure — like a blueprint with field names
Student = namedtuple('Student', 'name serialnum school gradelevel')

# Create an instance by unpacking
student = Student._make(struct.unpack('<10sHHb', record))

# Now access by name instead of index!
print(student.name)        # b'raymond   '
print(student.serialnum)   # 4658
print(student.school)      # 264
print(student.gradelevel)  # 8

# This is MUCH better than result[0], result[1], result[2]...


# =============================================================================
# STEP 11 — SPECIAL NOTE: USING __index__() WITH INTEGERS
# =============================================================================

# When you pack an integer format (b, h, i, etc.),
# the value doesn't have to literally be an int.
# It just needs to have an __index__() method (which converts it to int).
#
# This means enums, numpy integers, and other int-like objects work too!

import enum

class Color(enum.IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3

struct.pack('>h', Color.RED)     # ✅ works — uses Color.RED.__index__()
struct.pack('>h', Color.GREEN)   # ✅ works

# This was added in Python 3.2


# =============================================================================
# STEP 12 — THE Struct CLASS (COMPILED, REUSABLE FORMAT)
# =============================================================================

# Every time you call struct.pack('>ih', ...), Python has to:
# 1. Read the format string '>ih'
# 2. Parse it (figure out byte order, types, sizes)
# 3. Then do the actual packing
#
# If you call it 10,000 times in a loop, step 1-2 happens 10,000 times.
# Wasteful! The Struct CLASS lets you do steps 1-2 ONCE and reuse the result.

# ─── Creating a Struct object ─────────────────────────────────────────────

s = struct.Struct('>ih')   # compile the format ONCE
# Now 's' knows everything about '>ih' — byte order, sizes, total size

# ─── Struct object methods ────────────────────────────────────────────────

# .pack() — same as struct.pack() but uses the compiled format
packed = s.pack(1000, 50)
print(packed)   # b'\x00\x00\x03\xe8\x00\x32'

# .unpack() — same as struct.unpack() — buffer size must equal s.size
unpacked = s.unpack(packed)
print(unpacked)   # (1000, 50)

# .pack_into() — same as struct.pack_into()
buf = bytearray(20)
s.pack_into(buf, 4, 1000, 50)   # write at position 4
print(buf)

# .unpack_from() — same as struct.unpack_from()
result = s.unpack_from(buf, 4)   # read from position 4
print(result)   # (1000, 50)

# .iter_unpack() — same as struct.iter_unpack()
data = s.pack(1, 2) + s.pack(3, 4) + s.pack(5, 6)
for chunk in s.iter_unpack(data):
    print(chunk)
# (1, 2)
# (3, 4)
# (5, 6)

# ─── Struct object attributes ─────────────────────────────────────────────

# .size — the byte size of this format (like calcsize())
print(s.size)     # 6  (i=4 bytes + h=2 bytes)

# .format — the original format string
print(s.format)   # '>ih'

# ─── repr() of Struct (changed in Python 3.13) ────────────────────────────
s2 = struct.Struct('i')
print(repr(s2))   # Struct('i')   ← clean output since Python 3.13

# ─── When to use Struct class vs module functions? ────────────────────────
#
# Use MODULE FUNCTIONS (struct.pack etc.) when:
#   - You're only packing/unpacking a format once or a few times
#   - Quick one-off conversions
#
# Use STRUCT CLASS when:
#   - You're using the same format in a LOOP (thousands of times)
#   - Performance matters
#   - You want to store the format as part of a class or object
#
# Note: Python DOES cache the last few format strings used with module
# functions, so the speed difference is small unless you're doing a LOT.


# =============================================================================
# STEP 13 — THE BUFFER PROTOCOL
# =============================================================================

# Many struct functions take a "buffer" argument.
# A "buffer" is any Python object that stores raw bytes and supports
# the "Buffer Protocol" — meaning struct can directly read/write its memory.
#
# Common buffer types:
#   bytes      — readable, NOT writable (immutable)
#   bytearray  — readable AND writable (mutable)
#   memoryview — a view into another buffer (no copying)
#
# Use bytes for READ operations (unpack, unpack_from, iter_unpack)
# Use bytearray for WRITE operations (pack_into)

# bytes example (read only):
data_bytes = b'\x00\x0a\x00\x14'
struct.unpack('>hh', data_bytes)   # ✅ works — reading

# bytearray example (read + write):
data_bytearray = bytearray(b'\x00\x00\x00\x00')
struct.pack_into('>h', data_bytearray, 0, 999)   # ✅ works — writing
struct.unpack_from('>h', data_bytearray, 0)       # ✅ works — reading

# memoryview example (efficient — no copying):
mv = memoryview(bytearray(10))
struct.pack_into('>h', mv, 2, 777)   # ✅ works — writes directly into memory


# =============================================================================
# STEP 14 — PRACTICAL EXAMPLES
# =============================================================================

# ─── Example 1: Packing different types together ──────────────────────────

age = 25
height = 175
weight = 70.5
name = b'Alice'
is_member = True

data = struct.pack('>Hhf5s?', age, height, weight, name, is_member)
print(data)
print(f"Size: {struct.calcsize('>Hhf5s?')} bytes")  # 14 bytes

# Unpack it back:
age2, height2, weight2, name2, member2 = struct.unpack('>Hhf5s?', data)
print(age2, height2, round(weight2, 1), name2, member2)
# 25 175 70.5 b'Alice' True


# ─── Example 2: Reading a binary file header (like image files) ───────────
#
# Many file formats store a header at the start with metadata.
# Example: a simple custom file header with:
#   - magic number (4 bytes) to identify the file type
#   - version (2 bytes)
#   - width (4 bytes)
#   - height (4 bytes)

import io   # lets us simulate a file in memory

# Writing a fake file header:
header_format = '>4sHII'
header_data = struct.pack(header_format,
    b'MYFT',   # magic number — our file type identifier
    1,          # version 1
    1920,       # width
    1080        # height
)

# Reading back:
magic, version, width, height = struct.unpack(header_format, header_data)
print(magic)    # b'MYFT'
print(version)  # 1
print(width)    # 1920
print(height)   # 1080


# ─── Example 3: Network packet ────────────────────────────────────────────
#
# Simulate building and parsing a network packet.
# Packet structure:
#   - Protocol version (1 byte, unsigned)
#   - Message type    (1 byte, unsigned)
#   - Payload length  (2 bytes, unsigned short)
#   - Sender ID       (4 bytes, unsigned int)
#   - Payload         (8 bytes, string)

PACKET_FORMAT = '>BBHi8s'
PacketTuple = namedtuple('Packet', 'version msg_type length sender_id payload')

def build_packet(version, msg_type, sender_id, payload):
    payload_bytes = payload.encode().ljust(8, b'\x00')[:8]
    return struct.pack(PACKET_FORMAT,
        version,
        msg_type,
        len(payload),
        sender_id,
        payload_bytes
    )

def parse_packet(raw):
    return PacketTuple._make(struct.unpack(PACKET_FORMAT, raw))

# Build a packet:
raw_packet = build_packet(1, 42, 9001, "hello")
print(raw_packet)

# Parse it:
pkt = parse_packet(raw_packet)
print(pkt.version)    # 1
print(pkt.msg_type)   # 42
print(pkt.sender_id)  # 9001
print(pkt.payload)    # b'hello\x00\x00\x00'


# ─── Example 4: iter_unpack for bulk data ─────────────────────────────────
#
# Imagine you receive a stream of sensor readings.
# Each reading = 1 short (temperature) + 1 short (humidity)
# You get 5 readings at once.

sensor_data = struct.pack('>10h',
    25, 60,   # reading 1: temp=25, humidity=60
    27, 55,   # reading 2
    22, 70,   # reading 3
    30, 45,   # reading 4
    24, 65    # reading 5
)

print("Sensor Readings:")
for i, (temp, humidity) in enumerate(struct.iter_unpack('>hh', sensor_data), 1):
    print(f"  Reading {i}: Temperature={temp}°C, Humidity={humidity}%")


# ─── Example 5: pack_into for building a buffer piece by piece ────────────
#
# Build a 20-byte data packet by writing different parts separately.

buf = bytearray(20)

struct.pack_into('>I', buf, 0, 0xDEADBEEF)   # magic at position 0
struct.pack_into('>H', buf, 4, 512)            # value at position 4
struct.pack_into('>8s', buf, 6, b'testdata')   # string at position 6
struct.pack_into('>I', buf, 14, 12345)          # number at position 14

print(buf)
# Verify by reading back:
magic = struct.unpack_from('>I', buf, 0)[0]
print(hex(magic))   # 0xdeadbeef


# =============================================================================
# STEP 15 — NATIVE MODE EXAMPLE (for comparison)
# =============================================================================

# Just to show what native looks like, and why it's unpredictable:

# Both use NATIVE byte order, but '@' adds alignment padding:
packed_at = struct.pack('@ci', b'#', 0x12131415)
packed_ic = struct.pack('@ic', 0x12131415, b'#')

print(packed_at)   # b'#\x00\x00\x00\x15\x14\x13\x12'  (on little-endian)
print(packed_ic)   # b'\x15\x14\x13\x12#'

print(struct.calcsize('@ci'))   # 8 (with 3 pad bytes)
print(struct.calcsize('@ic'))   # 5 (no padding needed)

# Padding example with zero-repeat trick:
# '@llh' = long + long + short = 8 + 8 + 2 = 18 bytes (not aligned at end)
# '@llh0l' adds padding at end to align to long boundary = 24 bytes
print(struct.calcsize('@llh'))    # 18
print(struct.calcsize('@llh0l'))  # 24


# =============================================================================
# STEP 16 — QUICK REFERENCE CHEAT SHEET
# =============================================================================

# ─── BYTE ORDER PREFIX ────────────────────────────────────────────────────
# '>'  big-endian, standard sizes, no padding    ← USE FOR NETWORKS
# '<'  little-endian, standard sizes, no padding ← USE FOR PC/WINDOWS FILES
# '!'  network = big-endian (same as '>')
# '@'  native byte order, native sizes, WITH auto-padding
# '='  native byte order, standard sizes, no padding
# (none)  same as '@'

# ─── FORMAT CHARACTERS ────────────────────────────────────────────────────
# x   pad byte (no value)              1 byte
# c   char (single byte string)        1 byte
# b   signed int                       1 byte   range: -128 to 127
# B   unsigned int                     1 byte   range: 0 to 255
# ?   bool                             1 byte
# h   signed short                     2 bytes  range: -32768 to 32767
# H   unsigned short                   2 bytes  range: 0 to 65535
# i   signed int                       4 bytes
# I   unsigned int                     4 bytes
# l   signed long                      4 bytes
# L   unsigned long                    4 bytes
# q   signed long long                 8 bytes
# Q   unsigned long long               8 bytes
# n   ssize_t (native only)            varies
# N   size_t (native only)             varies
# e   half-precision float             2 bytes
# f   float                            4 bytes
# d   double                           8 bytes
# F   float complex (Python 3.14+)     8 bytes
# D   double complex (Python 3.14+)    16 bytes
# s   byte string (Ns = N-byte string) N bytes
# p   Pascal string                    N bytes (first byte = length)
# P   void pointer (native only)       varies

# ─── FUNCTIONS ────────────────────────────────────────────────────────────
# struct.pack(fmt, v1, v2, ...)          → bytes
# struct.unpack(fmt, buffer)             → tuple
# struct.pack_into(fmt, buf, offset, ..) → None (writes into buf)
# struct.unpack_from(fmt, buf, offset)   → tuple
# struct.iter_unpack(fmt, buffer)        → iterator of tuples
# struct.calcsize(fmt)                   → int (byte size of format)

# ─── THE Struct CLASS ─────────────────────────────────────────────────────
# s = struct.Struct(fmt)    compile format once
# s.pack(v1, v2, ...)       same as struct.pack
# s.unpack(buffer)          same as struct.unpack
# s.pack_into(buf, off, ..) same as struct.pack_into
# s.unpack_from(buf, off)   same as struct.unpack_from
# s.iter_unpack(buffer)     same as struct.iter_unpack
# s.size                    byte size of this format
# s.format                  the format string

# ─── GOLDEN RULES ─────────────────────────────────────────────────────────
# 1. Always use '>' or '<' unless you have a specific reason not to
# 2. unpack() always returns a TUPLE (even for one value)
# 3. calcsize() tells you exactly how many bytes your format uses
# 4. For strings: the number means LENGTH not repeat ('5s' = one 5-byte string)
# 5. For everything else: the number means REPEAT ('5h' = five shorts)
# 6. Use Struct class when using the same format many times in a loop
# 7. Use namedtuple with unpack() to make field names readable
# 8. Use bytearray (not bytes) when you need a writable buffer
# 9. Native mode ('@') is for C interop on the SAME machine only
# 10. struct.error is raised for bad values, wrong sizes, bad formats

# =============================================================================
#                         END OF COMPLETE struct GUIDE
# =============================================================================
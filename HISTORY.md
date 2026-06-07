* 2021-01-04:
	* Provided a variety of additional processors
	* Provided full documentation of the module

* 2021-02-10:
	* Added empty __slots__ to DumpMixin to prevent classes derived from getting a __dict__

* 2021-02-17:
	* Improved _canCompactSequence()
	* Corrected type in dumper.py
	* Improved value type detection

* 2021-02-18:
	* Better formatting of byte sequences

* 2021-07-09:
	* Added: dumpToStr()

* 2022-08-14:
	* Added: Hex output of binary data

* 2023-03-11:
	* Added: Support for unprocessed (raw) output

* 2024-02-18:
	* Added: Shortening objects

* 2024-06-07:
	* Improved shortening
	* More testing
	* Fixed: Raw output

* 2024-08-03:
	* Refactoring

* 2024-10-20:
	* Added: pprint()

* 2024-10-25:
	* Removed: Unnecessary dependencies

* 2025-05-24:
	* Improved: Raw output

* 2025-06-19:
	* Added: NamedTupleDumpMixinMeta

* 2025-08-14:
	* Improved: RawValue now tolerates empty strings

* 2025-10-12:
	* Improved: Added "dumpToStrList()"

* 2025-11-13:
	* Refactoring
	* Improved: Dumping ordered dictionaries now supports the same processing specifiers as standard dictionaries

* 2026-01-03:
	* Added: Support for classes implementing collection.Mapping

* 2026-06-07:
	* Fixed: pprint() caching problem


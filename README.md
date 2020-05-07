# Ralf Explorer

> Ralf Brown's Interrupt List (aka RBIL, x86 Interrupt List, MS-DOS Interrupt List or INTER) is a comprehensive list of interrupts, calls, hooks, interfaces, data structures, CMOS settings, memory and port addresses, as well as processor opcodes and special function registers for x86 machines (including many clones) from the very start of the PC era in 1981 up to 2000, most of it still applying to PCs today.
- [Wikipedia](https://en.wikipedia.org/wiki/Ralf_Brown%27s_Interrupt_List)

### What is this?

This is a Django website for searching a list of interrupts compiled by Ralf Brown, all content contained on it was pulled from [here](https://www.cs.cmu.edu/~ralf/files.html). Ralf's interrupt list is one of the best available information wise, but it is a pain to traverse and even harder to use if you are looking for specific entries, so this website is an attempt to resolve those issues. The original 151.1K lines of interrupts were parsed into a JSON format and then fed into a database, the wrapper site simply provides tools for searching said database.

### What are its use cases?

The primary reason I was use the interrupt list to begin with was for operating system development, as bare metal CPU functionality is a large requirement even when just making small test systems. Another use that came to mind was for reverse engineering unknown interrupts, as the search provides simple functionality to do something such as 

```
vector:10 number:42h
```
or the shorter version
```
v:10 n:42h
```

in order to find the definition of an interrupt that loads `42h` into either the AX or AH register and interrupts with vector `10`.

### Where can I find more information

Most other questions specific to the site (such as search functionality and category lists) can be found on the website itself.

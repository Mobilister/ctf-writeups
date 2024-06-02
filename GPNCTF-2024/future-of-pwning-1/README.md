# Solve

Understand ForwardCom language... Not very intutive! 

There are a few example using libc.li functions. The libc functions are however very limited as you can see here:

https://github.com/ForwardCom/code-examples

https://github.com/ForwardCom/libraries/blob/8cbc6588f3fbd67eb149bb398535e285263f3bd8/README.md 

Get the libc.li library from the same repository 

```
wget https://github.com/ForwardCom/libraries/raw/8cbc6588f3fbd67eb149bb398535e285263f3bd8/libc.li
```

The location of the flag is known from the Dockerfile configuration "/flag" 

Create the binary to read the file and print its content   
- open file 
- fread to a buffer
- prinft from the buffer 

```
extern _printf:   function reguse=0xF,0          // write formatted string to stdout
extern _fopen:    function reguse=0xF,0          // open a file
extern _fread:    function reguse=0xF,0          // read from a file

const section read ip
filename:         int8 "/flag", 0                // filename to open
mode:             int8 "r", 0                    // mode to open file (read)
format:           int8 "%s\n", 0                 // format string for printf
failed: 	  int8 "failed\n", 0
const end

bss section datap uninitialized                  // uninitialized read/write data section
int8 buffer[256]                                 // buffer to read file content
bss end

code1 section execute                            // code section

__entry_point function public                    // skip startup code
_main function public

// Open the file
int64  r0 = address [filename]                   // address of filename
int64  r1 = address [mode]                       // mode to open file
call   _fopen                                    // open file, file pointer in r0

int64  r4 = r0                                   // save file pointer in r4

// Check if file is opened successfully
if (int64 r0 == 0) {
   int64  r0 = address([failed])                 // address of string
   int64  r1 = 10
   call   _printf                                // print string without linefeed
   return
}

int64  r0 = address([buffer])                    // buffer to read
int64  r1 = 128                                  // size of buffer
int64  r2 = 128                                   // file pointer
int64  r3 = r4
call _fread

// Prepare the parameters for printf
int64  r0 = address([buffer])                     // format string
int64  r1 = 10                                   // buffer content
call   _printf                                   // print the content of the buffer

_main end
code1 end

```

Build (build.sh): 
```
./forw -ass solve.asm
./forw -link solve.ex solve.ob libc.li
./forw -emu solve.ex
```

Upload using webpage! 

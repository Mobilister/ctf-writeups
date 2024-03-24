#!/bin/sh

./forw -ass solve.asm
./forw -link solve.ex solve.ob libc.li
./forw -emu solve.ex

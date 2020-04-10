# avr-disassemble
An disassembler script that uses avr-objdump to disassemble elf32 or ihex formats files for AVR microcontrollers.

Written in python language that converts registrar addresses to their familiar names as in the device datasheet.

This program is a python script, for its execution it is necessary to have python installed on the computer.
The version of python it is designed for is 3.7, or newer.
<https://www.python.org>
Python 3.7 is only compatible with Windows Vista or newer.

For a better reading of this script use a supported text editor for UTF-8 unicode encoding, otherwise the characters will look strange (notepad is a SUCKER!).

This program is functional in Windows, but needs modifications, because there are no interesting terminal tools for Windows
to send the outputs to files (CMD is a SUCKER!). But all is not lost, in Windows 10 there is WSL, to make life easier for anyone who wants to use Windows.

Required tool: avr-objdumb
This tool can be found with the following suppliers:

AVR Microchip tolchain:
<https://www.microchip.com/mplab/avr-support/avr-and-arm-toolchains-c-compilers>

Arduino IDE:
<https://www.arduino.cc/en/main/software>

Eclipse IDE:
<http://avr-eclipse.sourceforge.net/wiki/index.php/The_AVR_GCC_Toolchain>

WinAVR 20100110:
<http://winavr.sourceforge.net>

Or in AVR tolchains community distributions.

Debian or Ubuntu:
apt-get install gcc-avr binutils-avr libc-avr avrdude

Redhat or Fedora:
yum install avr-gcc avr-binutils avr-libc avrdude

Arch or Manjaro:
pacman -S avr-gcc avr-inutils avr-libc

The path to avr-objdumb can be changed in the variable "disassemble"


Currently supported AVR families are:

avr35:
“Classic” devices with 16 KiB up to 64 KiB of program memory
and with the MOVW instruction.
mcu = attiny167, attiny1634, atmega8u2, atmega16u2, atmega32u2, ata5505,
ata6617c, ata664251, at90usb82, at90usb162.

avr25:
“Classic” devices with up to 8 KiB of program memory
and with the MOVW instruction.
mcu = attiny13, attiny13a, attiny24, attiny24a, attiny25, attiny261,
attiny261a, attiny2313, attiny2313a, attiny43u, attiny44, attiny44a, attiny45,
attiny48, attiny441, attiny461, attiny461a, attiny4313, attiny84, attiny84a,
attiny85, attiny87, attiny88, attiny828, attiny841, attiny861, attiny861a,
ata5272, ata6616c, at86rf401.

avr5:
“Enhanced” devices with 16 KiB up to 64 KiB of program memory.
mcu = atmega16, atmega16a, atmega16hva, atmega16hva2, atmega16hvb,
atmega16hvbrevb, atmega16m1, atmega16u4, atmega161, atmega162, atmega163,
atmega164a, atmega164p, atmega164pa, atmega165, atmega165a, atmega165p,
atmega165pa, atmega168, atmega168a, atmega168p, atmega168pa, atmega168pb,
atmega169, atmega169a, atmega169p, atmega169pa, atmega32, atmega32a,
atmega32c1, atmega32hvb, atmega32hvbrevb, atmega32m1, atmega32u4, atmega32u6,
atmega323, atmega324a, atmega324p, atmega324pa, atmega325, atmega325a,
atmega325p, atmega325pa, atmega328, atmega328p, atmega328pb, atmega329,
atmega329a, atmega329p, atmega329pa, atmega3250, atmega3250a, atmega3250p,
atmega3250pa, atmega3290, atmega3290a, atmega3290p, atmega3290pa, atmega406,
atmega64, atmega64a, atmega64c1, atmega64hve, atmega64hve2, atmega64m1,
atmega64rfr2, atmega640, atmega644, atmega644a, atmega644p, atmega644pa,
atmega644rfr2, atmega645, atmega645a, atmega645p, atmega649, atmega649a,
atmega649p, atmega6450, atmega6450a, atmega6450p, atmega6490, atmega6490a,
atmega6490p, ata5795, ata5790, ata5790n, ata5791, ata6613c, ata6614q, ata5782,
ata5831, ata8210, ata8510, ata5702m322, at90pwm161, at90pwm216, at90pwm316,
at90can32, at90can64, at90scr100, at90usb646, at90usb647, at94k, m3000.

avr4:
“Enhanced” devices with up to 8 KiB of program memory.
mcu = atmega48, atmega48a, atmega48p, atmega48pa, atmega48pb, atmega8,
atmega8a, atmega8hva, atmega88, atmega88a, atmega88p, atmega88pa, atmega88pb,
atmega8515, atmega8535, ata6285, ata6286, ata6289, ata6612c, at90pwm1,
at90pwm2, at90pwm2b, at90pwm3, at90pwm3b, at90pwm81.

Other architectures do not yet have a special use register dictionary, coming soon ... in this summer
... maybe. However, feel free to write other dictionaries of registers and share they with us.

More support architectures for avr-objdump can be checked at:
<https://gcc.gnu.org/onlinedocs/gcc/AVR-Options.html>

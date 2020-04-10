#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

MIT License

Copyright (c) 2018-2020 Marcelo Henrique Moraes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Programa para disassemble de códigos C/C++ para microcontroladores AVR,
converte os endereços dos registradores de função especial em seus respectivos
nomes, compatíveis a função de cada registrador segundo o datasheet
dos dispositivos.

Este programa e um script python,
para sua execução é necessário ter o python instalado no computador.
A versão do python para qual ele foi projetado é 3.7, ou mais novo.
<https://www.python.org>
Python 3.7 é compatível apenas com Windows Vista ou mais novo.

Para melhor leitura deste script utilize um editor de texto com suporte
para codificação unicode UTF-8,
caso contrário os caracteres vão ficar estranhos (notepad is a SUCKER!).

Este programa é funcional em Windows, mas necessita de modificações,
pois não existem ferramentas interessantes de terminal para Windows
para enviar as saídas para arquivos (CMD is a SUCKER!).
Mas nem tudo está perdido, no Windows 10 existe o WSL,
para facilitar a vida de quem queira utilizar Windows.

Ferramenta necessária: avr-objdumb
Esta ferramenta pode ser encontrada com o seguintes fornecedores:

AVR tolchain Microchip:
<https://www.microchip.com/mplab/avr-support/avr-and-arm-toolchains-c-compilers>

Arduino IDE:
<https://www.arduino.cc/en/main/software>

Eclipse IDE:
<http://avr-eclipse.sourceforge.net/wiki/index.php/The_AVR_GCC_Toolchain>

WinAVR 20100110:
<http://winavr.sourceforge.net>

Ou em distribuicoes comunitarias do AVR tolchains

Debian ou Ubuntu:
apt-get install gcc-avr binutils-avr libc-avr avrdude

Redhat ou Fedora:
yum install avr-gcc avr-binutils avr-libc avrdude

Arch ou Manjaro:
pacman -S avr-gcc avr-inutils avr-libc

O caminho para avr-objdumb pode ser alterado na variável "disassemble"


No momento as famílias AVR suportadas são:

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

Outras arquiteturas ainda não possuem
dicionário de registradores de uso especial, coming soon... in this summer
... maybe.

Mais arquiteturas de suporte para o avr-objdump podem ser verificadas em:
<https://gcc.gnu.org/onlinedocs/gcc/AVR-Options.html>


"""

from __future__ import print_function
import subprocess
import sys
import re



'''
 Caminho para o programa avr-objdump
 descomente uma das linhas de acordo com o seu sistema
'''

disassembler = '/usr/bin/avr-objdump'  # linux, install AVR tolchain

'''
disassembler = '~/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino5\
/bin/avr-objdump'  # linux, Arduino IDE 1.8.12
'''

'''
disassembler = 'C:/WinAVR-20100110/bin/avr-objdump'  # Windows, winAVR20100110
'''


familias = {
    '''
     Dicionário de ISAs AVR suportadas.
     Veja lista completa suportada pelo avr-objdump em:
     <https://gcc.gnu.org/onlinedocs/gcc/AVR-Options.html>
    '''
    "at90s1200": "avr1",
    "attiny11": "avr1",
    "attiny12": "avr1",
    "attiny15": "avr1",
    "attiny28": "avr1",
    "at90s2313": "avr2",
    "at90s2323": "avr2",
    "at90s2333": "avr2",
    "at90s2343": "avr2",
    "attiny22": "avr2",
    "attiny26": "avr2",
    "at90s4414": "avr2",
    "at90s4433": "avr2",
    "at90s4434": "avr2",
    "at90s8515": "avr2",
    "at90c8534": "avr2",
    "at90s8535": "avr2",
    "at86rf401": "avr25",
    "ata6289": "avr25",
    "ata5272": "avr25",
    "ata6616c": "avr25",
    "attiny13": "avr25",
    "attiny13a": "avr25",
    "attiny2313": "avr25",
    "attiny2313a": "avr25",
    "attiny24": "avr25",
    "attiny24a": "avr25",
    "attiny25": "avr25",
    "attiny261": "avr25",
    "attiny261a": "avr25",
    "attiny4313": "avr25",
    "attiny43u": "avr25",
    "attiny44": "avr25",
    "attiny44a": "avr25",
    "attiny441": "avr25",
    "attiny45": "avr25",
    "attiny461": "avr25",
    "attiny461a": "avr25",
    "attiny48": "avr25",
    "attiny828": "avr25",
    "attiny84": "avr25",
    "attiny84a": "avr25",
    "attiny841": "avr25",
    "attiny85": "avr25",
    "attiny861": "avr25",
    "attiny861a": "avr25",
    "attiny87": "avr25",
    "attiny88": "avr25",
    "atmega603": "avr3",
    "at43usb355": "avr3",
    "atmega103": "avr31",
    "at43usb320": "avr31",
    "at90usb82": "avr35",
    "at90usb162": "avr35",
    "ata5505": "avr35",
    "ata6617c": "avr35",
    "ata664251": "avr35",
    "atmega8u2": "avr35",
    "atmega16u2": "avr35",
    "atmega32u2": "avr35",
    "attiny167": "avr35",
    "attiny1634": "avr35",
    "at76c711": "avr3",
    "ata6285": "avr4",
    "ata6286": "avr4",
    "ata6612c": "avr4",
    "atmega48": "avr4",
    "atmega48a": "avr4",
    "atmega48pa": "avr4",
    "atmega48p": "avr4",
    "atmega8": "avr4",
    "atmega8a": "avr4",
    "atmega8515": "avr4",
    "atmega8535": "avr4",
    "atmega88": "avr4",
    "atmega88a": "avr4",
    "atmega88p": "avr4",
    "atmega88pa": "avr4",
    "atmega8hva": "avr4",
    "at90pwm1": "avr4",
    "at90pwm2": "avr4",
    "at90pwm2b": "avr4",
    "at90pwm3": "avr4",
    "at90pwm3b": "avr4",
    "at90pwm81": "avr4",
    "at90can32": "avr5",
    "at90can64": "avr5",
    "at90pwm161": "avr5",
    "at90pwm216": "avr5",
    "at90pwm316": "avr5",
    "at90scr100": "avr5",
    "at90usb646": "avr5",
    "at90usb647": "avr5",
    "at94k": "avr5",
    "atmega16": "avr5",
    "ata5790": "avr5",
    "ata5702m322": "avr5",
    "ata5782": "avr5",
    "ata6613c": "avr5",
    "ata6614q": "avr5",
    "ata5790n": "avr5",
    "ata5795": "avr5",
    "ata5831": "avr5",
    "atmega161": "avr5",
    "atmega162": "avr5",
    "atmega163": "avr5",
    "atmega164a": "avr5",
    "atmega164p": "avr5",
    "atmega164pa": "avr5",
    "atmega165": "avr5",
    "atmega165a": "avr5",
    "atmega165p": "avr5",
    "atmega165pa": "avr5",
    "atmega168": "avr5",
    "atmega168a": "avr5",
    "atmega168p": "avr5",
    "atmega168pa": "avr5",
    "atmega169": "avr5",
    "atmega169a": "avr5",
    "atmega169p": "avr5",
    "atmega169pa": "avr5",
    "atmega16a": "avr5",
    "atmega16hva": "avr5",
    "atmega16hva2": "avr5",
    "atmega16hvb": "avr5",
    "atmega16hvbrevb": "avr5",
    "atmega16m1": "avr5",
    "atmega16u4": "avr5",
    "atmega32": "avr5",
    "atmega32a": "avr5",
    "atmega323": "avr5",
    "atmega324a": "avr5",
    "atmega324p": "avr5",
    "atmega324pa": "avr5",
    "atmega325": "avr5",
    "atmega325a": "avr5",
    "atmega325p": "avr5",
    "atmega325pa": "avr5",
    "atmega3250": "avr5",
    "atmega3250a": "avr5",
    "atmega3250p": "avr5",
    "atmega3250pa": "avr5",
    "atmega328": "avr5",
    "atmega328p": "avr5",
    "atmega329": "avr5",
    "atmega329a": "avr5",
    "atmega329p": "avr5",
    "atmega329pa": "avr5",
    "atmega3290": "avr5",
    "atmega3290a": "avr5",
    "atmega3290p": "avr5",
    "atmega3290pa": "avr5",
    "atmega32c1": "avr5",
    "atmega32hvb": "avr5",
    "atmega32hvbrevb": "avr5",
    "atmega32m1": "avr5",
    "atmega32u4": "avr5",
    "atmega32u6": "avr5",
    "atmega406": "avr5",
    "atmega64rfr2": "avr5",
    "atmega644rfr2": "avr5",
    "atmega64": "avr5",
    "atmega64a": "avr5",
    "atmega640": "avr5",
    "atmega644": "avr5",
    "atmega644a": "avr5",
    "atmega644p": "avr5",
    "atmega644pa": "avr5",
    "atmega645": "avr5",
    "atmega645a": "avr5",
    "atmega645p": "avr5",
    "atmega6450": "avr5",
    "atmega6450a": "avr5",
    "atmega6450p": "avr5",
    "atmega649": "avr5",
    "atmega649a": "avr5",
    "atmega6490": "avr5",
    "atmega6490a": "avr5",
    "atmega6490p": "avr5",
    "atmega649p": "avr5",
    "atmega64c1": "avr5",
    "atmega64hve": "avr5",
    "atmega64hve2": "avr5",
    "atmega64m1": "avr5",
    "m3000": "avr5",
    "at90can128": "avr51",
    "at90usb1286": "avr51",
    "at90usb1287": "avr51",
    "atmega128": "avr51",
    "atmega128a": "avr51",
    "atmega1280": "avr51",
    "atmega1281": "avr51",
    "atmega1284": "avr51",
    "atmega1284p": "avr51",
    "atmega128rfr2": "avr51",
    "atmega1284rfr2": "avr51",
    "atmega2560": "avr6",
    "atmega2561": "avr6",
    "atmega256rfr2": "avr6",
    "atmega2564rfr2": "avr6",
    "atxmega16a4": "avrxmega2",
    "atxmega16a4u": "avrxmega2",
    "atxmega16c4": "avrxmega2",
    "atxmega16d4": "avrxmega2",
    "atxmega32a4": "avrxmega2",
    "atxmega32a4u": "avrxmega2",
    "atxmega32c3": "avrxmega2",
    "atxmega32c4": "avrxmega2",
    "atxmega32d3": "avrxmega2",
    "atxmega32d4": "avrxmega2",
    "atxmega8e5": "avrxmega2",
    "atxmega16e5": "avrxmega2",
    "atxmega32e5": "avrxmega2",
    "atxmega64a3": "avrxmega4",
    "atxmega64a3u": "avrxmega4",
    "atxmega64a4u": "avrxmega4",
    "atxmega64b1": "avrxmega4",
    "atxmega64b3": "avrxmega4",
    "atxmega64c3": "avrxmega4",
    "atxmega64d3": "avrxmega4",
    "atxmega64d4": "avrxmega4",
    "atxmega64a1": "avrxmega5",
    "atxmega64a1u": "avrxmega5",
    "atxmega128a3": "avrxmega6",
    "atxmega128a3u": "avrxmega6",
    "atxmega128b1": "avrxmega6",
    "atxmega128b3": "avrxmega6",
    "atxmega128c3": "avrxmega6",
    "atxmega128d3": "avrxmega6",
    "atxmega128d4": "avrxmega6",
    "atxmega192a3": "avrxmega6",
    "atxmega192a3u": "avrxmega6",
    "atxmega192c3": "avrxmega6",
    "atxmega192d3": "avrxmega6",
    "atxmega256a3": "avrxmega6",
    "atxmega256a3u": "avrxmega6",
    "atxmega256a3b": "avrxmega6",
    "atxmega256a3bu": "avrxmega6",
    "atxmega256c3": "avrxmega6",
    "atxmega256d3": "avrxmega6",
    "atxmega384c3": "avrxmega6",
    "atxmega384d3": "avrxmega6",
    "atxmega128a1": "avrxmega7",
    "atxmega128a1u": "avrxmega7",
    "atxmega128a4u": "avrxmega7",
    "attiny4": "avrtiny10",
    "attiny5": "avrtiny10",
    "attiny9": "avrtiny10",
    "attiny10": "avrtiny10",
    "attiny20": "avrtiny10",
    "attiny40": "avrtiny10",
}

registradores = {
    '''
    Dicionário de rgistradores,
    suporte limitado aos mais encontrados no mercado...
    São muitos registradores, porque AVR é isso,
    muito mais periféricos do que eles deveriam ter.
    More coming soon... In this summer... Maybe...
    '''
    "avr35": {
        0x7F: "TWSCRA",
        0x7E: "TWSCRB",
        0x7D: "TWSSRA",
        0x7C: "TWSA",
        0x7B: "TWSAM",
        0x7A: "TWSD",
        0x79: "UCSR1A",
        0x78: "UCSR1B",
        0x77: "UCSR1C",
        0x76: "UCSR1D",
        0x75: "UBRR1H",
        0x74: "UBRR1L",
        0x73: "UDR1",
        0x72: "TCCR1A",
        0x71: "TCCR1B",
        0x70: "TCCR1C",
        0x6F: "TCNT1H",
        0x6E: "TCNT1L",
        0x6D: "OCR1AH",
        0x6C: "OCR1AL",
        0x6B: "OCR1BH",
        0x6A: "OCR1BL",
        0x69: "ICR1H",
        0x68: "ICR1L",
        0x67: "GTCCR",
        0x66: "OSCCAL1",
        0x65: "OSCTCAL0B",
        0x64: "OSCTCAL0A",
        0x63: "OSCCAL0",
        0x62: "DIDR2",
        0x61: "DIDR1",
        0x60: "DIDR0",
        0x3F: "SREG",
        0x3E: "SPH",
        0x3D: "SPL",
        0x3C: "GIMSK",
        0x3B: "GIFR",
        0x3A: "TIMSK",
        0x39: "TIFR",
        0x38: "QTCSR",
        0x37: "SPMCSR",
        0x36: "MCUCR",
        0x35: "MCUSR",
        0x34: "PRR",
        0x33: "CLKPR",
        0x32: "CLKSR",
        0x30: "WDTCSR",
        0x2F: "CCP",
        0x2E: "DWDR",
        0x2D: "USIBR",
        0x2C: "USIDR",
        0x2B: "USISR",
        0x2A: "USICR",
        0x29: "PCMSK2",
        0x28: "PCMSK1",
        0x27: "PCMSK0",
        0x26: "UCSR0A",
        0x25: "UCSR0B",
        0x24: "UCSR0C",
        0x23: "UCSR0D",
        0x22: "UBRR0H",
        0x21: "UBRR0L",
        0x20: "UDR0",
        0x1F: "EEARH",
        0x1E: "EEARL",
        0x1D: "EEDR",
        0x1C: "EECR",
        0x1B: "TCCR0A",
        0x1A: "TCCR0B",
        0x19: "TCNT0",
        0x18: "OCR0A",
        0x17: "OCR0B",
        0x16: "GPIOR2",
        0x15: "GPIOR1",
        0x14: "GPIOR0",
        0x13: "PORTCR",
        0x12: "PUEA",
        0x11: "PORTA",
        0x10: "DDRA",
        0x0F: "PINA",
        0x0E: "PUEB",
        0x0D: "PORTB",
        0x0C: "DDRB",
        0x0B: "PINB",
        0x0A: "PUEC",
        0x09: "PORTC",
        0x08: "DDRC",
        0x07: "PINC",
        0x06: "ACSRA",
        0x05: "ACSRB",
        0x04: "ADMUX",
        0x03: "ADCSRA",
        0x02: "ADCSRB",
        0x01: "ADCH",
        0x00: "ADCL",
    },
    "avr25": {
        0x3F: "SREG",
        0x3E: "SPH",
        0x3D: "SPL",
        0x3B: "GIMSK",
        0x3A: "GIFR",
        0x39: "TIMSK",
        0x38: "TIFR",
        0x37: "SPMCSR",
        0x35: "MCUCR",
        0x34: "MCUSR",
        0x33: "TCCR0B",
        0x32: "TCNT0",
        0x31: "OSCCAL",
        0x30: "TCCR1",
        0x2F: "TCNT1",
        0x2E: "OCR1A",
        0x2D: "OCR1C",
        0x2C: "GTCCR",
        0x2B: "OCR1B",
        0x2A: "TCCR0A",
        0x29: "OCR0A",
        0x28: "OCR0B",
        0x27: "PLLCSR",
        0x26: "CLKPR",
        0x25: "DT1A",
        0x24: "DT1B",
        0x23: "DTPS1",
        0x22: "DWDR",
        0x21: "WDTCR",
        0x20: "PRR",
        0x1F: "EEARH",
        0x1E: "EEARL",
        0x1D: "EEDR",
        0x1C: "EECR",
        0x18: "PORTB",
        0x17: "DDRB",
        0x16: "PINB",
        0x15: "PCMSK",
        0x14: "DIDR0",
        0x13: "GPIOR2",
        0x12: "GPIOR1",
        0x11: "GPIOR0",
        0x10: "USIBR",
        0x0F: "USIDR",
        0x0E: "USISR",
        0x0D: "USICR",
        0x08: "ACSR",
        0x07: "ADMUX",
        0x06: "ADCSRA",
        0x05: "ADCH",
        0x04: "ADCL",
        0x03: "ADCSRB",
    },
    "avr5": {
        0xFA: "CANMSG",
        0xF9: "CANSTMPH",
        0xF8: "CANSTMPL",
        0xF7: "CANIDM1",
        0xF6: "CANIDM2",
        0xF5: "CANIDM3",
        0xF4: "CANIDM4",
        0xF3: "CANIDT1",
        0xF2: "CANIDT2",
        0xF1: "CANIDT3",
        0xF0: "CANIDT4",
        0xEF: "CANCDMOB",
        0xEE: "CANSTMOB",
        0xED: "CANPAGE",
        0xEC: "CANHPMOB",
        0xEB: "CANREC",
        0xEA: "CANTEC",
        0xE9: "CANTTCH",
        0xE8: "CANTTCL",
        0xE7: "CANTIMH",
        0xE6: "CANTIML",
        0xE5: "CANTCON",
        0xE4: "CANBT3",
        0xE3: "CANBT2",
        0xE2: "CANBT1",
        0xE1: "CANSIT1",
        0xE0: "CANSIT2",
        0xDF: "CANIE1",
        0xDE: "CANIE2",
        0xDD: "CANEN1",
        0xDC: "CANEN2",
        0xDB: "CANGIE",
        0xDA: "CANGIT",
        0xD9: "CANGSTA",
        0xD8: "CANGCON",
        0xD2: "LINDAT",
        0xD1: "LINSEL",
        0xD0: "LINIDR",
        0xCF: "LINDLR",
        0xCE: "LINBRRH",
        0xCD: "LINBRRL",
        0xCC: "LINBTR",
        0xCB: "LINERR",
        0xCA: "LINENIR",
        0xC9: "LINSIR",
        0xC8: "LINCR",
        0xC6: "UDR0",
        0xC5: "UBRR0H",
        0xC4: "UBRR0L",
        0xC2: "UCSR0C",
        0xC1: "UCSR0B",
        0xC0: "UCSR0A",
        0xBD: "TWAMR",
        0xBC: "TWCR",
        0xBB: "TWDR",
        0xBA: "TWAR",
        0xB9: "TWSR",
        0xB8: "TWBR",
        0xB7: "PCTL",
        0xB5: "PCNF",
        0xB6: "ASSR",
        0xB4: "OCR2B",
        0xB3: "OCR2A",
        0xB2: "TCNT2",
        0xB1: "TCCR2B",
        0xB0: "TCCR2A",
        0xAF: "POCR2RAH",
        0xAE: "POCR2RAL",
        0xAD: "POCR2SAH",
        0xAC: "POCR2SAL",
        0xAB: "POCR1SBH",
        0xAA: "POCR1SBL",
        0xA9: "POCR1RAH",
        0xA8: "POCR1RAL",
        0xA7: "POCR1SAH",
        0xA6: "POCR1SAL",
        0xA5: "POCR0SBH",
        0xA4: "POCR0SBL",
        0xA3: "POCR0RAH",
        0xA2: "POCR0RAL",
        0xA1: "POCR0SAH",
        0xA0: "POCR0SAL",
        0x97: "AC3CON",
        0x96: "AC2CON",
        0x95: "AC1CON",
        0x94: "AC0CON",
        0x92: "DACH",
        0x91: "DACL",
        0x90: "DACON",
        0x8B: "OCR1BH",
        0x8A: "OCR1BL",
        0x89: "OCR1AH",
        0x88: "OCR1AL",
        0x87: "ICR1H",
        0x86: "ICR1L",
        0x85: "TCNT1H",
        0x84: "TCNT1L",
        0x82: "TCCR1C",
        0x81: "TCCR1B",
        0x80: "TCCR1A",
        0x7F: "DIDR1",
        0x7E: "DIDR0",
        0x7C: "ADMUX",
        0x7B: "ADCSRB",
        0x7A: "ADCSRA",
        0x79: "ADCH",
        0x78: "ADCL",
        0x77: "AMP2CSR",
        0x76: "AMP1CSR",
        0x75: "AMP0CSR",
        0x6F: "TIMSK1",
        0x6E: "TIMSK0",
        0x6D: "PCMSK3",
        0x6C: "PCMSK2",
        0x6B: "PCMSK1",
        0x6A: "PCMSK0",
        0x69: "EICRA",
        0x68: "PCICR",
        0x66: "OSCCAL",
        0x64: "PRR",
        0x61: "CLKPR",
        0x60: "WDTCSR",
        0x3F: "SREG",
        0x3E: "SPH",
        0x3D: "SPL",
        0x37: "SPMCSR",
        0x35: "MCUCR",
        0x34: "MCUSR",
        0x33: "SMCR",
        0x30: "ACSR",
        0x2E: "SPDR",
        0x2D: "SPSR",
        0x2C: "SPCR",
        0x29: "PLLCSR",
        0x28: "OCR0B",
        0x27: "OCR0A",
        0x26: "TCNT0",
        0x25: "TCCR0B",
        0x24: "TCCR0A",
        0x23: "GTCCR",
        0x22: "EEARH",
        0x21: "EEARL",
        0x20: "EEDR",
        0x1F: "EECR",
        0x1E: "GPIOR0",
        0x1D: "EIMSK",
        0x1C: "EIFR",
        0x1B: "PCIFR",
        0x1A: "GPIOR2",
        0x19: "GPIOR1",
        0x16: "TIFR1",
        0x15: "TIFR0",
        0x0E: "PORTE",
        0x0D: "DDRE",
        0x0C: "PINE",
        0x0B: "PORTD",
        0x0A: "DDRD",
        0x09: "PIND",
        0x08: "PORTC",
        0x07: "DDRC",
        0x06: "PINC",
        0x05: "PORTB",
        0x04: "DDRB",
        0x03: "PINB",
    },
    "avr4": {
        0x3F: "SREG",
        0x3E: "SPH",
        0x3D: "SPL",
        0x3B: "GICR",
        0x3A: "GIFR",
        0x39: "TIMSK",
        0x38: "TIFR",
        0x37: "SPMCR",
        0x36: "TWCR",
        0x35: "MCUCR",
        0x34: "MCUCSR",
        0x33: "TCCR0",
        0x32: "TCNT0",
        0x31: "OSCCAL",
        0x30: "SFIOR",
        0x2F: "TCCR1A",
        0x2E: "TCCR1B",
        0x2D: "TCNT1H",
        0x2C: "TCNT1L",
        0x2B: "OCR1AH",
        0x2A: "OCR1AL",
        0x29: "OCR1BH",
        0x28: "OCR1BL",
        0x27: "ICR1H",
        0x26: "ICR1L",
        0x25: "TCCR2",
        0x24: "TCNT2",
        0x23: "OCR2",
        0x22: "ASSR",
        0x21: "WDTCR",
        0x20: "UCSRC",
        0x1F: "EEARH",
        0x1E: "EEARL",
        0x1D: "EEDR",
        0x1C: "EECR",
        0x18: "PORTB",
        0x17: "DDRB",
        0x16: "PINB",
        0x15: "PORTC",
        0x14: "DDRC",
        0x13: "PINC",
        0x12: "PORTD",
        0x11: "DDRD",
        0x10: "PIND",
        0x0F: "SPDR",
        0x0E: "SPSR",
        0x0D: "SPCR",
        0x0C: "UDR",
        0x0B: "UCSRA",
        0x0A: "UCSRB",
        0x09: "UBRRL",
        0x08: "ACSR",
        0x07: "ADMUX",
        0x06: "ADCSRA",
        0x05: "ADCH",
        0x04: "DCL",
        0x03: "WDR",
        0x02: "TWAR",
        0x01: "TWSR",
        0x00: "TWBR",
    }
}

'''
 Verifica os opcodes (in|out|lds|sts|cbi|sbi|sbic|sbis)
 E os registradores de uso especifíco para determinar se é necessário
 substituir o endereço por nome.
'''
decode = [
    re.compile(r'\b(?P<opcode>in|lds)\s+\w+,\s+(?P<sfr>\w+)'),
    re.compile(r'\b(?P<opcode>out|[cs]bi|sts|sbi[cs])\s+(?P<sfr>\w+),\s+\w+'),
]


def report(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main(args):
    """ Argumentos: <nome do mcu> <arquivo formato elf> """
    try:
        mcu = args[1]
        familia = familias[mcu]
        comando = [disassembler, '-m', familia, '-d'] + args[2:]
        sfr_dic = registradores[familia]

    except IndexError:
        report('''{0}: Sem argumentos suficiente

Sintaxe: {0} <MCU> <arquivo.elf>
ou
         {0} <MCU> <seção> <arquivo.hex>

Exemplos:
  {0} atmega328p main.elf
  {0} atmega328p -j .sec1 main.hex
'''.format(args[0]))
        return 1

    # Para famílias desconhecidas ou lista de dicionário desconhecido
    # usa um dicionário vazio
    except KeyError:
        sfr_dic = []
        try:
            report("Dicionário de registradores para '{}'   \
                    ainda não está diponível...".format(familia))
        except UnboundLocalError:
            comando = [disassembler] + args[1:]
            report("MCU desconhecido: '{}'".format(mcu))

    objdump = subprocess.Popen(comando, stdout=subprocess.PIPE,
                               universal_newlines=True)
    
    try:

        # Passando saída de avr-objdum para o console
        for linha in iter(objdump.stdout.readline, ''):
            combina = decode[0].search(linha) or decode[1].search(linha)
            try:
                # Se aconteceu alguma igualdade entre o endereço acessado
                # e o dicionário de registradores.
                if combina:
                    # De acordo com o datasheet, os registradores de 0-0x3F,
                    # quando acessados com instruções (LDS & STS),
                    # recebem um offset +0x20 nos endereços
                    sfr = int(combina['sfr'], 0)
                    if combina['opcode'] in ['sts', 'lds'] and sfr < 0x60:
                        sfr -= 0x20

                    linha = ''.join([
                        linha[:combina.start(0)],
                        re.sub(combina['sfr'], sfr_dic[sfr], combina[0]),
                        linha[combina.end(0):]
                    ])

            # Se a instrução bater mas não os operandos,
            # significa que não tem lista de registradores suportado
            # ou que está sendo acessado um endereço da memória ram
            except IndexError:
                pass

            # Caso a lista de instrução não for encontrada
            # não precisa fazer nenhuma mudança.
            except KeyError:
                pass

            sys.stdout.write(linha)

        objdump.stdout.close()
        return objdump.wait()

    except BrokenPipeError:
        report(
            '''Deu ruim e nem sei o que aconteceu...
               Se vira!''')
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))


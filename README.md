# PacketParsing
Python/XML implementation for parsing (network) packets and displaying them

## Goals
The goal of this project is to build a core of bitstream parsers to allow for easily hacking together new packet format with XML.

## Tests
You can run the automatic test with

>  #!/bin/bash <br>
>  #virtualenv venv <br>
>  #./test.sh

if you have virtualenv installed.

## Usage
Custom packet descriptions can be supplied via XML. The basic structure of each element can be observed in the files in 
![the xml folder](https://github.com/HeroicKatora/PacketParsing/tree/master/src/xml),
for a deeper understanding documentation should be added soon, for now you have to rely on the xsd files
in the packages ![gpp.builtin](https://github.com/HeroicKatora/PacketParsing/tree/master/src/gpp/builtin) and
![gpp.standard](https://github.com/HeroicKatora/PacketParsing/tree/master/src/gpp/standard).

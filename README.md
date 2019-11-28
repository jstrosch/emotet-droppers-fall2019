# Deobfuscate Emotet Droppers - Fall 2019

Python2 script that deobfuscates and then decodes base64 string that contains PowerShell script and extracts the URLs used to download Emotet binaries. 

These Word documents originally started appearing when Emotet resumed operations in the Fall of 2019 as simple base64 encoded strings that contained PowerShell to download the Emotet binary. Later, the base64 strings were padded with a "key" that was replaced at run time. The key also began with a simple pattern but has become slightly more complex over time, to include splitting the key with the key so that it requires multiple rounds of replacement.

Sample documents are contained in the _samples_ folder, the password for the zip is _infected_.

## Sample Output

![alt text](https://github.com/jstrosch/emotet-droppers-fall2019/blob/master/sample-output.png "Sample Output")

## Subject to Change

As is likely no surprise, the padding/key will evolve over time requiring updates to this script.
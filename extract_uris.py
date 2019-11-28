#!/usr/bin/env python

__author__ = "Josh Stroschein"
__version__ = "0.0.1"
__maintainer__ = "Josh Stroschein"

import sys, os, re, base64, zlib, requests, optparse

# This needs to be more generous then the normal b64 character set due to obfuscation
regex_b64 = "(?:[A-Za-z0-9+/_]{4})*(?:[A-Za-z0-9+/_]{2}==|[A-Za-z0-9+/_]{3}=)?"
regex_uri = "https?:\/\/[a-zA-Z0-9\.\/\-]{5,}"
# Accounts for 0xAA11, AAA_, 199 style keys - this is, of course, likely to change
regex_key = "([1-9]{1}[0-9]{1,2}|0x[1-9a-f]{2,4}|[a-zA-Z0-9]{3}_{1})"

dl_urls = []

def setup_args():
    parser = optparse.OptionParser()

    parser.add_option('-d', '--directory',
    action="store", dest="directory",
    help="The folder that contains your Emotet Word docs", default=".")

    return parser.parse_args()

def extract_downloader_links(file_path):

    with open(file_path) as f:
        #greedy match on potential strings
        b64_strings = re.findall(regex_b64, f.read())

    for string in b64_strings:
        if len(string) > 500:
            #only search the beginning of the string, the padding/key is typically within the first few characters
            keys = re.findall(regex_key, string[:10])

            for key in keys:
                # Later docs padding the b64 string with multiple instances of the key, removing one instance would then reveal a second and so on
                string = string.replace(key,"").replace(key, "").replace(key, "")

                try:
                    #strings may not be properly padded and the forthcoming decode method will complain
                    pad = len(string) % 4

                    if pad > 0:
                        string = string + ("=" * pad)

                    #The output is actually UTF-16, found it easier to just remove the extra null-byte and then match for URIs
                    decoded = base64.b64decode(string).replace('\x00',"")

                    urls = re.findall(regex_uri, decoded)
                    
                    for url in urls:
                        if not url in dl_urls:
                            dl_urls.append(url)
                            print("[*] " + url.replace("http","hxxp"))

                except Exception as e:
                    print("[!] Failed to decode")


def main(argv):

    options, args = setup_args() 

    for file_name in os.listdir(options.directory):
        extract_downloader_links(file_name)

    print("[*] Found " + str(len(dl_urls)) + " unique URIs")
 
if __name__ == '__main__':
	main(sys.argv[1:])
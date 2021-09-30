import requests
from optparse import OptionParser
import time

# globals
urls = []
url_file = ""
magic_word = ""
headers = ""
header_dict = {}
time_delay = None


def urls_load():
    global url_file
    try:
        f = open(url_file, "r")
        urls = f.read().split('\n')
        print('Checking urls\n')
        for i in urls:
            url_call(i)
    except Exception as e:
        print("Exception : "+str(e))


def url_call(url):
    global urls, magic_word, header_dict, time_delay
    try:
        print('[=>]'+'\t'+url)
        pattern_match = magic_word

        response = requests.get(url, headers=header_dict)
        if pattern_match in response.text:
            urls.append(url)

        if time_delay is not None:
            time.sleep(time_delay)

    except Exception as e:
        print('Exception in get '+str(e))


def final_urls():
    print('\nReflected urls:\n')
    global urls
    for i in urls:
        print('\t'+i)


def parse_arguments():
    global url_file, magic_word, headers, time_delay
    usage = "Usage: header_reflect.py -f url_file -H headers_seperated_by_comma -m magic_word \n\tfor more try help -h"

    parser = OptionParser(
        usage=usage)

    # add options
    parser.add_option('-f', dest='url_file',
                      type='string',
                      help='specify the url file name',)
    parser.add_option('-m', dest='magic_word',
                      type='string',
                      help='specify the pattern for including in the header',)
    parser.add_option('-H', dest='headers',
                      type='string',
                      help='specify list of headers to check',)
    parser.add_option('-t', dest='time_delay',
                      type='float',
                      help='time_delay_between_each_request',)

    (options, args) = parser.parse_args()
    if (options.url_file == None):
        print(parser.usage)
        exit(0)
    else:
        url_file = options.url_file

    magic_word = options.magic_word if options.magic_word != None else "MaGiCwOrD"

    if options.time_delay is not None:
        time_delay = options.time_delay

    if (options.headers == None):
        print(parser.usage)
        exit(0)
    else:
        headers = options.headers


def seperate_headers():
    global headers, magic_word, header_dict

    space_striped = headers.rstrip()
    header_list = space_striped.split(',')

    for i in header_list:
        header_dict[i] = magic_word


class bcolors:
    OKBLUE = '\033[94m'   
    ENDC = '\033[0m'
    BOLD = '\033[1m'

if __name__ == "__main__":

    print(bcolors.OKBLUE + bcolors.BOLD +
              '\nHEADER REFLECT\n'+bcolors.ENDC+bcolors.ENDC)
    parse_arguments()
    seperate_headers()    
    urls_load()
    final_urls()

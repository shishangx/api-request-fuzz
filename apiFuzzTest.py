import argparse
import uncurl_lib
import requests
from pyjfuzz.lib import *
from argparse import Namespace
import json
import re
import sys, os
import time

from misc.parse_url import fuzz_url_path
from misc.utils import random_header


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='+',
                        help="input file")

    args = parser.parse_args()

    return args


def get_url_from_file(f):
    with open(f, 'r') as f:
        result = f.readlines(1)[0]

        if re.findall(r"-i", result):
            d_result = re.sub(r"-i", "", result)
            return d_result
        else:
            return result


def get_mutated_json(json_string):
    config = PJFConfiguration(Namespace(
        json=json.loads(json_string),
        level=6,
        strong_fuzz=True,
        nologo=True,
        debug=False,
        recheck_ports=False
    ))
    # init the object factory used to fuzz (see documentation)
    factory = PJFFactory(config)

    mutated_json = factory.fuzzed
    return mutated_json


def make_request(method, url, header, data):
    req = requests.request(method, url, data=data, headers=header)
    # return req.status_code
    return req

def test_main(filePathName, testRound, fileName):
    url = get_url_from_file(filePathName)
    context = uncurl_lib.parse_context(url)
    uncurl_url = context.url
    print "API URL: " + str(uncurl_url)

    uncurl_method = context.method
    print "API Method: " + str(uncurl_method)
    uncurl_data = context.data
    print "API body: " + str(uncurl_data)
    uncurl_header = context.headers
    # new_header = random_header(uncurl_header)
    # print "API Header1: " + str(new_header)
    
    for i in range(testRound):
        print "***** Test round: " + str(i) + " *****"
        try:
            # get or delete, fuzz url
            if uncurl_method == "get" or uncurl_method == "delete":

                # will someone put req boby with GET/DELETE method ?
                if uncurl_data is None:
                    fuzzed_json = uncurl_data
                else:
                    fuzzed_json = get_mutated_json(str(uncurl_data))

                new_url = fuzz_url_path(uncurl_url)
                try:
                    new_header = random_header(uncurl_header)
                except:
                    new_header = {""}
                    pass
                res = make_request(method=uncurl_method,
                                        url=new_url,
                                        header=new_header,
                                        data=fuzzed_json,
                                        )
                # print "status code:" + str(res_code) + "\tnew_url:" + \
                #     "\t" + new_url
                # print "*" * 100
                # print "response:" + str(res_code) + "\t"
                print "*" * 50
                print "count: " + str(i+1)
                print "new url:" + new_url
                print "header:" + str(new_header)
                print "status code:" + str(res.status_code)
                print "payload:" + str(fuzzed_json)
                print "response:" + res.content
                print "#" * 50
                logFile = open(os.path.join("logs",fileName), "a")
                logFile.write("count: " + str(i+1) + "\n"
                            "new url:" + new_url + "\n"
                            "header:" + str(new_header) + "\n"
                            "status code:" + str(res.status_code) + "\n"
                            "payload:" + str(fuzzed_json) + "\n"
                            "response:" + res.content  + "\n")
                logFile.close()

            # post or put, fuzz post body
            elif uncurl_method == "put" or uncurl_method == "post":
                fuzzed_json = get_mutated_json(str(uncurl_data))
                try:
                    new_header = random_header(uncurl_header)
                except:
                    new_header = {""}
                res = make_request(method=uncurl_method,
                                        url=uncurl_url,
                                        header=new_header,
                                        data=fuzzed_json,
                                        )
                print "*" * 50
                print "count: " + str(i+1)
                print "url:" + str(uncurl_url)
                print "method:" + str(uncurl_method)
                print "header:" + str(new_header)
                print "status code:" + str(res.status_code)
                print "payload:" + fuzzed_json
                print "response:" + res.content
                print "#" * 50
                logFile = open(os.path.join("logs",fileName), "a")
                logFile.write("count: " + str(i+1) + "\n"
                            "url:" + str(uncurl_url) + "\n"
                            "header:" + str(new_header) + "\n"
                            "status code:" + str(res.status_code) + "\n"
                            "payload:" + str(fuzzed_json) + "\n"
                            "response:" + res.content  + "\n")
                logFile.close()
            else:
                print "Wrong request method ! Only PUT/GET/POST/DELETE " \
                    "supported!"
        except:
            pass

if __name__ == '__main__':
    # clear files content from postman cUrl export 
    from misc.rawfiles_Clean import clean
    clean()
    print "***** wait clear data *****"
    time.sleep(5)
    print "***** test begin *****"
    args = arg_parser()
    testCount = sys.argv[2] # second cli input param, means test round number
    # args.file is a list of filenames, we need the first element!
    if args.file[0] == ".": 
        filePath_new = "input_files"
        fileList = os.listdir(filePath_new)
        for file in fileList:
            print "*****Testing API: " + file + " *****"
            test_main(os.path.join(filePath_new,file), int(testCount), file)
            
    else:
        test_main(args.file[0], int(testCount))

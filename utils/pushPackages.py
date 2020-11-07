from icinga2api.client import Client
import json
import glob
import os
import argparse
import time

#Temp until certs enabled
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def parse_args():
    parser = argparse.ArgumentParser(description="Icinga config publisher",)
    parser.add_argument(
        "--package", dest="package", help="package to update (default all)", nargs="+"
    )
    parser.add_argument(
        "--dir", dest="dir", help="directory in which configuration is", required=True
    )
    return parser.parse_args()

def uploadPackage(package):
    print("Uploading package for package "+package['name'])
    uploadResult = icinga.config.upload_package(package['name'], data)

    retry = 5
    done = 0
    while (retry > 0 and not done):
        print("Checking if stage passed ("+uploadResult['results'][0]['stage']+")")
        currentPackageList = icinga.config.list_packages()['results']

        for x in currentPackageList:
            if x['name'] == package['name']:
                print("Current stage "+uploadResult['results'][0]['stage'])
                if x['active-stage'] == uploadResult['results'][0]['stage']:
                    done = 1
                    print("Stage passed. Moving on.")
                break
        if done:
            break
        retry -= 1
        print("Checking again in 10 seconds")
        time.sleep(10)
    if done:
        return {"status" : 1, "stage" : uploadResult['results'][0]['stage']}
    else:
        return {"status" : 0, "stage" : uploadResult['results'][0]['stage']}

def removeOldStages(package, newStage):
    currentPackageList = icinga.config.list_packages()['results']
    for x in currentPackageList:
            if x['name'] == package['name']:
                for stage in x['stages']:
                    if stage != newStage:
                        tries = 3
                        for i in range(tries):
                            try:
                                print("Deleting stage " + stage)
                                fnret = icinga.config.remove_stage(package['name'], stage)
                            except KeyError as e:
                                if i < tries - 1: # i is zero indexed
                                    continue
                                else:
                                    raise
                            break    



with open('secrets/icinga-api.json') as f:
  data = json.load(f)

icinga = Client(data['baseUrl'], data['user'], data['password'])

args     = parse_args()
cur_dir  = os.path.abspath(args.dir)
packages = []

if args.package:
    for p in args.package:
        dirpath = os.path.join(cur_dir, p)
        if not os.path.isdir(dirpath):
            logging.error("%s is not a valid directory !" % (dirpath))
            sys.exit(1)
        packages.append({"name": p, "path": dirpath})
else:
    for dirname in sorted(os.listdir(cur_dir)):
        dirpath = os.path.join(cur_dir, dirname)
        if os.path.isdir(dirpath) and dirname not in [".git", "utils", ".gitsecret", "secrets"]:
            packages.append({"name": dirname, "path": dirpath})

print(packages)
for package in packages:
    print("Doing package "+ package['name'])
    os.chdir(package['path'])
    fileList = glob.glob("**/*conf", recursive=True)
    print(fileList)
    data = {}
    for filePath in fileList:
        with open(filePath, 'r') as f:
            data[filePath] = f.read()

    print(data)
    fnret = icinga.config.list_packages()
    for package in fnret['results']:
        if package['name'] == package['name']:
            exists = 1

    if not exists:
        fnret = icinga.config.create_package(package['name'])
        print(fnret)
    else:
        print("already exists")

    uploadRetry = 2
    uploadSuccess = 0
    lastStage = ""
    while (uploadRetry > 0 and not uploadSuccess):
        fnret = uploadPackage(package)
        uploadSuccess = fnret['status']
        lastStage     = fnret['stage']
        uploadRetry -= 1

    if not uploadSuccess:
        print("Failed to upload package", package['name'])
        fnret = icinga.config.get_package_error(package['name'], lastStage)
        print(fnret)

    removeOldStages(package, lastStage)




        

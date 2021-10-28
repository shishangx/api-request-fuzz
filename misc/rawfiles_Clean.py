import re
import os

def clean():
    filePath_raw = "input_files_raw"
    filePath_new = "input_files"
    fileList = os.listdir(filePath_raw)
    fileNum = 1
    print "***** cleaning ..... *****"
    for file in fileList:
        f_raw = open(os.path.join(filePath_raw,file))
        f_new = open(os.path.join(filePath_new,file), 'w')
        print str(fileNum) + " : "+ file
        for raw_content in f_raw.readlines():
            new_content = re.sub("--header", "-H", raw_content)
            new_content = re.sub("--data-raw", "-d", new_content)
            new_content = re.sub("--request", "-X", new_content)
            new_content = re.sub("--location", "", new_content)
            new_content = re.sub("\n", "", new_content)
            new_content = re.sub(r"\\", "", new_content)
            f_new.write(new_content)
        f_raw.close()
        f_new.close()
        fileNum = fileNum + 1

if __name__ == '__main__':
    clean()

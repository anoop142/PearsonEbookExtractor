#!/bin/python3
# copyright Anoop S
import os
import subprocess
import tarfile
import shutil
import sys
import argparse
import zlib
import re
from PyPDF2 import PdfFileReader
WHITE = '\033[m' 
GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
ver=2.0
print('Pearson ebook extractor ver',ver,' by Anoop')
default_dir=os.path.dirname(os.path.abspath(sys.argv[0]))+'/books'
tmp_dir=os.path.dirname(os.path.abspath(sys.argv[0]))+'/tmp/'
app_android_path="/data/data/com.pearson.android.pulse.elibrary/files/books/"
app_package_name='com.pearson.android.pulse.elibrary'


def start_adb_server():
    device = subprocess.Popen(['adb','devices'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    device  = device.stdout.read().decode().split()
    if device[-1] != "device":
        print("No devices / emulator found")
        sys.exit(1)


def root():
    tmp_book_path='/data/local/tmp/'
    downloaded_list_pc = [i for i in os.listdir(out_dir) if i.endswith(".pdf")]
    downloaded_list_device=subprocess.Popen(['adb','shell',"su -c ls",app_android_path],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    downloaded_list_device  = downloaded_list_device.stdout.read().decode().split()
    if not downloaded_list_device:
        print(RED+"No PDF found on android device!."+WHITE)
        sys.exit()
    files_to_pull=[i for i in downloaded_list_device if i not in downloaded_list_pc]
    if files_to_pull:
         for i in files_to_pull:
             subprocess.call(['adb','shell','su', '-c', 'cp',app_android_path+i,tmp_book_path ],)
             subprocess.call(['adb','shell','su', '-c', 'chown','shell.shell',tmp_book_path+i ],)
             subprocess.call(['adb','pull', tmp_book_path+i, out_dir],)
             subprocess.call(['adb','shell','su', '-c', 'rm',tmp_book_path+i ],)

        # rm corrupt pdf     
         if args.remove_corrupt:
             remove_corrupt_pdf(files_to_pull)
        # rename
         if not args.no_rename:
             rename_pdf(files_to_pull)
         print(GREEN+'Finished'+WHITE)
    else:
        print(YELLOW+"All files trying to extract already exist.!"+WHITE)

def noroot():
    os.makedirs(tmp_dir,exist_ok=True)
    subprocess.call(['adb','backup', '-f', tmp_dir+'books.ab', app_package_name],)
    decompress_zlib(tmp_dir+'books.ab',tmp_dir+'books.tar')
    f = tarfile.open(tmp_dir+"books.tar")
    f.extractall(path=tmp_dir)
    files = os.listdir(tmp_dir+'apps/'+app_package_name+'/f/books' )
    for i in files:
        f = tmp_dir+'apps/'+app_package_name+'/f/books/'+i
        shutil.move(f,out_dir+i)
    # clean
    shutil.rmtree(tmp_dir)
    # rm corrupt pdf
    pdf_list = get_pdf_list(out_dir)
    if  args.remove_corrupt:
        remove_corrupt_pdf(pdf_list)
    # rename
    if not args.no_rename:
        rename_pdf(pdf_list)
    print(GREEN+'Finished'+WHITE)
    


def decompress_zlib(in_file,out_file):
    with open(in_file,"rb") as f , open(out_file,"wb") as o:
        data = zlib.decompressobj()
        f.seek(24)
        buf = f.read(4096)
        while buf:
            o.write(data.decompress(buf))
            buf = f.read(4096)
        data.flush()

def get_pdf_list(path):
    files = os.listdir(path)
    pdf_files = [ i for i in files if i.endswith(".pdf")]
    return pdf_files

def rename_pdf(pdf_list):
    for i in pdf_list:
        try:
            pdf_file = out_dir+i
            with open(pdf_file, 'rb') as f:
                info = PdfFileReader(f).getDocumentInfo()
            author = info.author
            title = info.title
            if not author or not title:
                continue
            new_name = title+'-'+author
            new_name = re.sub("[^a-zA-Z0-9-]+", " ", new_name)
            if len(new_name) > 80:
                continue
            new_name = out_dir+new_name+".pdf"
            os.rename(pdf_file,new_name)
        except:
            continue

def remove_corrupt_pdf(pdf_list):
    for i in pdf_list:
        if not i.endswith("pdf"):
            continue
        try:
            PdfFileReader(out_dir+i, "rb")
        except:
            print_k_flag=1
            os.remove(out_dir+i)
            print(RED+i, 'is corrupted!. hence deleted'+WHITE)



# CLI
parser = argparse.ArgumentParser(
    description='Pearson Ebook extractor by Anoop. A script to extract ebooks downloaded by Pearson Android app.')
parser.add_argument(
    '--root',
    dest='root_mode',
    help='root method to extract pdf.',
    action='store_true')

parser.add_argument(
    '--no-rename',
    dest='no_rename',
    help='dont rename pdf using metadata.',
    action='store_true')

parser.add_argument(
    '-o',
    metavar='path',
    help='output dir',
    dest='out_dir',
    default=default_dir,
    action='store')

parser.add_argument(
    '--rm-corrupt',
    help='remove corrupt pdf files',
    dest='remove_corrupt',
    action='store_true')

# start
if __name__ == '__main__':
    args = parser.parse_args()
    out_dir = os.path.abspath(args.out_dir)+'/'
    os.makedirs(out_dir,exist_ok=True)
    start_adb_server()
    if args.root_mode:
        root()
    else:
        noroot()
    
        
        
        
    


        

        
        

    

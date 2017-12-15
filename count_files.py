#coding: utf-8
import os
dir_list = []
def count_files(path): 
    list_dir = os.listdir(path)
    for dir_name in list_dir:
        dir_path = os.path.join(path,dir_name)
        if os.path.isdir(dir_path):
            count_files(dir_path)
        dir_list.append(dir_name)
    for i in dir_list:
        print (i)
    print ('共有%s个文件'%len(dir_list))

if __name__ == '__main__':
    path = input('请输入路径：')
    if path == '':
        path = os.getcwd()
    count_files(path)

#!usr/bin/env python
# coding:utf-8

import os
import time
def backup_files():
    print ("默认Unix/Linux下，如果您是Windows系统请这样输入r'C:\Documents'")
    source_list = []
    while 1:
        source = input('请输入要备份的文件路径(可多次输入，输入为空进行下一步)：')
        if source == '':
            break
        source_list.append(source)
        
    targat_dir = input('输入要备份到哪：')

    today = targat_dir + time.strftime('%Y%m%d')
    now = time.strftime('%H%M%S')
    if not os.path.exists(today):
        os.mkdir(today)
        print ('创建文件夹：', today)

    comment = input('输入备份信息:')
    if len(comment) == 0:
        target = today + os.sep + now + '.zip'  # os.sep 是操作分隔符 /，不同系统不一样，可以自动检测系统添加
    else:
        target = today + os.sep + now + comment.replace(' ','_') + '.zip'

    zip_func="zip -qr %s %s" % (target, ''.join(source_list))

    if os.system(zip_func) == 0:
        print ('成功备份到==>', target)
    else :
        print ('备份失败！')
   
if __name__ == '__main__':
    backup_files()
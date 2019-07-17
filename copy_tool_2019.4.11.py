'''
最后修改时间:2019年4月11日
更新内容:
    1.增加图幅等级选项
    2.优化弹窗
    3.优化图幅文件遍历顺序

'''


import os,threading,shutil,re,pprint
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter.messagebox


def gui_copy_data():

    dir_txt1 = {}  # 声明一个匹配到图幅列表文件的全球影像的字典
    dir_txt2 = {}  # 声明一个匹配到图幅列表文件的影像注记的字典
    dir_txt3 = {}  # 声明一个匹配到图幅列表文件的导航底图的字典
    t_m_s = False
    def select_path():
        path_ = askopenfilename()
        path.set(path_)

    def get_dir():
        path_ = askdirectory()
        path1.set(path_)

    def change_color():  # 更改颜色
        if var.get() == 1:
            cb.config(text='全球影像', fg='red')
        else:
            cb.config(text='全球影像', fg='black')

    def change_color1():  # 更改颜色
        if var1.get() == 1:
            cb1.config(text='影像注记', fg='red')
        else:
            cb1.config(text='影像注记', fg='black')

    def change_color2():  # 更改颜色
        if var2.get() == 1:
            cb2.config(text='导航底图', fg='red')
        else:
            cb2.config(text='导航底图', fg='black')

    def make_dir():  # 建立目录结构

        if nt1.get() == '': # 如果entry1的值为空
            lb.insert(0, '<' + '= =' * 7 + '请选择目的盘符' + '= =' * 7 + '>')
        elif nt1.get().endswith('GTGEODATA') and len(nt1.get()) == 12 and os.path.isdir(r'{}\GTGEODATA\image\全球影像.tfiles'.format(nt1.get()[:2])):
            return lb.insert(0, '<' + '= =' * 8 + '目录已存在！' + '= =' * 8 + '>')
        else:
            l = ['image', 'dem', 'vector', '全球影像.tfiles', '影像注记.tfiles', '导航底图.tfiles']
            for i in range(65, 91):  # 循环取出所有大写字母和Entry取到的值做匹配
                vol = chr(i) + ':' + '/'
                try:
                    if nt1.get() == vol: # 如果entry中的值等于某个盘符，建立目录
                        first_dir = vol[:2] + '\\' + r'GTGEODATA'
                        os.mkdir(first_dir)
                        for i in l[:3]:
                            os.mkdir(first_dir + '\\' + i)
                            if i == 'image':
                                for value in l[3:6]:
                                    os.mkdir(first_dir + '\\' + i + '\\' + value)
                                    for j in range(10, 19):
                                        os.mkdir(first_dir + '\\' + i + '\\' + value + '\\' + str(j))
                        lb.insert(0, '<' + '= =' * 7 + '目录文件创建成功' + '= =' * 7 + '>')  # 将消息在ListBox内显示
                except:
                    lb.insert(0, '<' + '= =' * 5 + '目录已存在、目的盘符输入有误' + '= =' * 5 + '>')

    def copy_data():

        ''' 获取图幅列表文件，并将图幅列表文件的比例尺取出并在listbox上显示。'''
        if var.get() == 1 or var1.get() == 1 or var2.get() == 1:
            new_dir = nt.get().replace('/', '\\')
            # 将entry中获取到的地址中的’/‘，替换成’\\‘。
            file_list = []
            if new_dir.endswith('.txt'):
                try:
                    with open(new_dir, 'r')as f:
                        for line in f.readlines():
                            if line.strip('\n') == '比例尺 250000':
                                lb.insert(0, '25万图幅列表文件')
                            elif line.strip('\n') == '比例尺 1000000':
                                lb.insert(0, '100万图幅列表文件')
                            else:
                                file_list.append(line.strip('\n'))
                except:
                    lb.insert(0, '<' + '= =' * 6 + '图幅列表文件选择错误' + '= =' * 6 + '>')
                    return

                dic_1 = {}
                dic_2 = {}
                dic_3 = {}
                for i in range(65, 91):  # 遍历所有GTGEODATA文件夹
                    value = chr(i) + ':'
                    if os.path.isdir(value) and os.path.exists(value+r'\GTGEODATA'):
                        for root, dirs, files in os.walk(value + r'\GTGEODATA'):
                            for file in files:
                                if '全球影像' in root:
                                    dic_1.setdefault(file, root)
                                if '影像注记' in root:
                                    dic_2.setdefault(file, root)
                                if '导航底图' in root:
                                    dic_3.setdefault(file, root)


                if var.get() == 1:
                    dir_txt1.clear()
                    for k, v in dic_1.items():
                        result = re.findall(r'-(\d{1,2})', k)
                        if result == []:
                            continue
                        elif int(result[0]) >= int(nt2.get()) and int(result[0]) <= int(nt3.get()):  #  判断数据等级范围
                            for file_name in file_list:
                                if k.startswith('{}'.format(file_name)):
                                    dir_txt1.setdefault(k, v)
                                elif file_name[:5] == k[:5] and len(k) == 12:
                                    dir_txt1.setdefault(k, v)  # 把匹配到的全球影像图幅名（k），绝对路径（V）放入字典
                                elif 'world' in k:
                                    dir_txt1.setdefault(k, v)
                # 声明一个匹配到图幅列表文件的影像注记的字典
                if var1.get() == 1:
                    dir_txt2.clear()
                    for k, v in dic_2.items():
                        result = re.findall(r'-(\d{1,2})', k)
                        if result == []:
                            continue
                        elif int(result[0]) >= int(nt2.get()) and int(result[0]) <= int(nt3.get()):
                            for file_name in file_list:
                                if k.startswith('{}'.format(file_name)):
                                    dir_txt2.setdefault(k, v)  # 把匹配到的影像注记图幅名（k），绝对路径（V）放入字典
                                elif file_name[:5] == k[:5] and len(k) == 12:
                                    dir_txt2.setdefault(k, v)  # 把匹配到的影像注记图幅名（k），绝对路径（V）放入字典
                                elif 'world' in k:
                                    dir_txt2.setdefault(k, v)

                if var2.get() == 1:
                    dir_txt3.clear()
                    for k, v in dic_3.items():
                        result = re.findall(r'-(\d{1,2})', k)
                        if result == []:
                            continue
                        elif int(result[0]) >= int(nt2.get()) and int(result[0]) <= int(nt3.get()):
                            for file_name in file_list:
                                if k.startswith('{}'.format(file_name)):
                                    dir_txt3.setdefault(k, v)  # 把匹配到的影像注记图幅名（k），绝对路径（V）放入字典
                                elif file_name[:5] == k[:5] and len(k) == 12:
                                    dir_txt3.setdefault(k, v)  # 把匹配到的影像注记图幅名（k），绝对路径（V）放入字典
                                elif 'world' in k:
                                    dir_txt3.setdefault(k, v)

                # 获取全球影像文件大小
                dict_txt1_size = 0
                for key, v1 in dir_txt1.items():
                    dir_name = v1 + '\\' + key
                    dict_txt1_size += os.path.getsize(dir_name)

                # 获取影像注记文件大小
                dict_txt2_size = 0
                for key, v2 in dir_txt2.items():
                    dir_name = v2 + '\\' + key
                    dict_txt2_size += os.path.getsize(dir_name)

                # 获取导航底图文件大小
                dict_txt3_size = 0
                for key, v3 in dir_txt3.items():
                    dir_name = v3 + '\\' + key
                    dict_txt3_size += os.path.getsize(dir_name)
                nonlocal t_m_s
                t_m_s = tkinter.messagebox.askokcancel('确定拷贝？',  '匹配到全球影像: ' + str(len(dir_txt1)) + '幅' + '{' + '数据大小为: %.2f GB' % ((dict_txt1_size )/1024**3) + ' (' + str(dict_txt1_size) + ')'+'}' +'\n'
                                                        '匹配到影像注记: ' + str(len(dir_txt2)) + '幅' + '{' + '数据大小为: %.2f GB' % ((dict_txt2_size )/1024**3) + ' (' + str(dict_txt2_size) + ')'+'}'  + '\n'
                                                        '匹配到导航底图: ' + str(len(dir_txt3)) + '幅' +  '{' + '数据大小为: %.2f GB' % ((dict_txt3_size )/1024**3) + ' (' + str(dict_txt3_size) + ')'+'}'  
                                               )
            else:
                lb.insert(0, '<' + '= =' * 6 + '图幅列表文件选择错误' + '= =' * 6 + '>')

        else:
            lb.insert(0, '<' + '= =' * 8 + '请选择数据种类' + '= =' * 8 + '>')




    def copy_yingxiang():  #  拷贝全球影像数据
        if t_m_s == True:
            if nt1.get() != '' and  var.get() == 1:
                value = nt1.get().replace('/', '\\')
                for key, v in dir_txt1.items():  # 循环取出全球影像的绝对路径和文件名
                    dirs = v + '\\' + key  # 将字典中的KEY和value拼成绝对路径
                    dir_str = '\\GTGEODATA\\image\\全球影像.tfiles\\'
                    dir_str1 = '\\image\\全球影像.tfiles\\'
                    for i in [str(i) + '.tdb' for i in range(10, 19)]:
                        if key.endswith(i):
                            try:
                                if len(value) == 12:
                                    shutil.copy(dirs, value + dir_str1 + i[:2])
                                    lb.insert(0, '全球影像图幅 ' + key + '拷贝完成')
                                else:
                                    shutil.copy(dirs, value + dir_str + i[:2])
                                    lb.insert(0, '全球影像图幅 ' + key + '拷贝完成')
                            except:
                                lb.insert(0, '全球影像图幅 ' + key + '已存在')
                    if 'world' in key:
                        try:
                            if len(value) == 12:
                                shutil.copy(dirs, value + dir_str1)
                                lb.insert(0, '全球影像图幅 ' + key + '拷贝完成')
                            else:
                                print(key, '-->', v)
                                shutil.copy(dirs, value + dir_str)
                                lb.insert(0, '全球影像图幅 ' + key + '拷贝完成')
                        except:
                            lb.insert(0, '全球影像图幅 ' + key + '已存在')
                lb.insert(0, '<' + '= =' * 7 + '全球影像拷贝完成' + '= =' * 7 + '>')
            else:
                pass


    def copy_zhuji(): #  拷贝影像注记数据
        if t_m_s == True:
            if nt1.get() != '' and var1.get() == 1:
                value = nt1.get().replace('/', '\\')
                for key, v in dir_txt2.items():
                    dirs = v + '\\' + key  # 将字典中的KEY和value拼成绝对路径
                    dir_str = '\\GTGEODATA\\image\\影像注记.tfiles\\'
                    dir_str1 = '\\image\\影像注记.tfiles\\'
                    for i in [str(i) + '.tdb' for i in range(10, 19)]:
                        if key.endswith(i):
                            try:
                                if len(value) == 12:
                                    shutil.copy(dirs, value + dir_str1 + i[:2])
                                    lb.insert(0, '影像注记图幅 ' + key + '拷贝完成')
                                else:
                                    shutil.copy(dirs, value + dir_str + i[:2])
                                    lb.insert(0, '影像注记图幅 ' + key + '拷贝完成')
                            except:
                                lb.insert(0,'影像注记图幅 ' + key + '已存在')
                    if 'world' in key:
                        try:
                            if len(value) == 12:
                                shutil.copy(dirs, value + dir_str1)
                                lb.insert(0, '影像注记图幅 ' + key + '拷贝完成')
                            else:
                                print(key, '-->',v)
                                shutil.copy(dirs, value + dir_str)
                                lb.insert(0, '影像注记图幅 ' + key + '拷贝完成')
                        except:
                            lb.insert(0,'影像注记图幅 ' + key + '已存在')
            lb.insert(0, '<' + '= =' * 7 + '影像注记拷贝完成' + '= =' * 7 + '>')
        else:
            pass


    def copy_ditu():# 拷贝导航底图数据
        if t_m_s == True:
            if nt1.get() != '' and var2.get() == 1:
                value = nt1.get().replace('/', '\\')
                for key, v in dir_txt3.items():
                    dirs = v + '\\' + key  # 将字典中的KEY和value拼成绝对路径
                    dir_str = '\\GTGEODATA\\image\\导航底图.tfiles\\'
                    dir_str1 = '\\image\\导航底图.tfiles\\'
                    for i in [str(i) + '.tdb' for i in range(10, 19)]:
                        if key.endswith(i):
                            try:
                                if len(value) == 12:
                                    shutil.copy(dirs, value + dir_str1 + i[:2])
                                    lb.insert(0, '导航底图图幅 ' + key + '拷贝完成')
                                else:
                                    shutil.copy(dirs, value + dir_str + i[:2])
                                    lb.insert(0, '导航底图图幅 ' + key + '拷贝完成')
                            except:
                                lb.insert(0, '导航底图图幅 ' + key + '已存在')
                    if 'world' in key:
                        try:
                            if len(value) == 12:
                                shutil.copy(dirs, value + dir_str1)
                                lb.insert(0, '导航底图图幅 ' + key + '拷贝完成')
                            else:
                                print(key, '-->', v)
                                shutil.copy(dirs, value + dir_str)
                                lb.insert(0, '导航底图图幅 ' + key + '拷贝完成')
                        except:
                            lb.insert(0, '导航底图图幅 ' + key + '已存在')
                lb.insert(0, '<' + '= =' * 7 + '导航底图拷贝完成' + '= =' * 7 + '>')
            else:
                pass


    def threanding_test():
        copy_data()
        th = threading.Thread(target=copy_yingxiang)
        th.setDaemon(True)
        th.start()

        th1 = threading.Thread(target=copy_zhuji)
        th1.setDaemon(True)
        th1.start()

        th2 = threading.Thread(target=copy_ditu)
        th2.setDaemon(True)
        th2.start()


    window = Tk()

    window.title('DataTool')
    window.minsize(435, 360)

    Label(window, text='<--数据拷贝工具-->', fg='blue', font='隶书').grid(columnspan=3, rowspan=2)

    Label(window, text='选择图幅文件路径:', fg='blue').grid(row=3, sticky=E)

    Label(window, text='选择目的盘符:', fg='blue').grid(row=4, sticky=E)

    Label(window, text='选择数据等级:', fg='blue').grid(row=5, sticky=E)

    path = StringVar()
    nt = Entry(window, width=36, textvariable=path)
    nt.grid(row=3, column=1, sticky=W)

    path1 = StringVar()
    nt1 = Entry(window, width=36, textvariable=path1)
    nt1.grid(row=4, column=1, sticky=W)

    path2 = StringVar()
    nt2 = Entry(window, width=15, textvariable=path2)
    nt2.grid(row=5, column=1, sticky=W)
    nt2.insert(2, '0')

    path3 = StringVar()
    nt3 = Entry(window, width=15, textvariable=path3)
    nt3.grid(row=5, column=1, sticky=E)
    nt3.insert(2, '18')

    bu = Button(window, text='选择', command=select_path, bd=2)
    bu.grid(row=3, column=2)

    bu1 = Button(window, text='选择', command=get_dir, bd=2)
    bu1.grid(row=4, column=2)

    bu2 = Button(window, text='拷贝数据', width=30, bd=2, command=threanding_test)
    bu2.grid(row=8, columnspan=3, sticky=E)

    bu3 = Button(window, text='创建目录', width=30, command=make_dir, bd=2)
    bu3.grid(row=8, columnspan=3, sticky=W)

    var = IntVar()
    cb = Checkbutton(window, text='全球影像', command=change_color, variable=var)
    cb.grid(row=6, sticky=W)

    var1 = IntVar()
    cb1 = Checkbutton(window, text='影像注记', command=change_color1, variable=var1)
    cb1.grid(row=6, column=1)

    var2 = IntVar()
    cb2 = Checkbutton(window, text='导航底图', command=change_color2, variable=var2)
    cb2.grid(row=6, column=2, sticky=E)

    lb = Listbox(window, width=60, bd=3)
    lb.grid(row=7, columnspan=3)

    window.mainloop()


if __name__ == '__main__':
    gui_copy_data()


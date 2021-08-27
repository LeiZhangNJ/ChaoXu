import re
import math
import os
import shutil


def open_txt(file_name):
    """
    打开指定文件，并读取
    :param file_name:文件名
    :return:
    """
    with open(file_name, 'r+') as f:
        while True:
            line = f.readline()
            if not line:
                return
            yield line.strip()


def get_lenth(xyz1, xyz2):
    """
    计算距离
    :param xyz1: 空间坐标1
    :param xyz2: 空间坐标2
    :return:
    """
    return math.sqrt((float(xyz1[0])-float(xyz2[0]))**2+(float(xyz1[1])-float(xyz2[1]))**2+(float(xyz1[2])-float(xyz2[2]))**2)


def all_list(arr):
    """
    统计列表中某一个元素出现的次数
    :param arr:需要统计的list数组
    :return:
    """
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result


def all_path(dirname):
    """
    读取指定目录下的文件
    :param dirname: 父路径
    :return:
    """
    result = []  # 所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容

            if ext in filter:
                result.append(apath)

    return result


if __name__ == '__main__':
    # 设置过滤后的文件类型 当然可以设置多个类型
    filter = [".cif"]
    # 指定目标文件夹
    file_path_li = all_path("F:\数据挖掘")
    # 遍历文件
    for path in file_path_li:
        txt_url = path
        # 检测是否到达坐标行数
        flag = False
        # index 为0则为a，index为1则为b
        index = 0
        # 空间坐标集
        xyzli = []
        # ra集合
        rali = []
        # rb集合
        rbli = []
        for phone in open_txt(txt_url):
            # 这个是坐标行开始标记
            if phone == '_atom_site_fract_z':
                flag = True
                continue
            # 这个是文件结束标记
            elif phone == '#END':
                flag = False
            # 下面处理坐标
            if flag:
                li = phone.split(' ')
                # 正则过滤括号内容，并且封装
                xyz = [re.sub('\(.*?\)', '', li[2]), re.sub('\(.*?\)', '', li[3]), re.sub('\(.*?\)', '', li[4])]
                # 封装后追加到总的空间坐标系列表
                xyzli.append(xyz)
        # 处理总的空间坐标系列表
        for i in range(1, len(xyzli)):
            # 从第二位开始取，取当前和前一位
            xyz1 = xyzli[i - 1]
            xyz2 = xyzli[i]
            if index == 0:
                index = 1
                rali.append(get_lenth(xyz1, xyz2))
            else:
                index = 0
                rbli.append(get_lenth(xyz1, xyz2))
        # 计算出现的次数
        count_ra = all_list(rali)
        count_rb = all_list(rbli)
        # 开始最终的计算
        sum_ra = 0
        sum_rb = 0
        # 遍历key
        for i in count_ra.keys():
            sum_ra = sum_ra + (i/count_ra.get(i))
        for i in count_rb.keys():
            sum_rb = sum_ra + (i/count_rb.get(i))
        print(sum_ra-sum_rb)
        # 判断条件判断一下，然后进行文件写出
        if -0.04 < sum_ra-sum_rb < 0.04:
            shutil.copyfile(path, 'F:/数据保存/' + os.path.basename(path))



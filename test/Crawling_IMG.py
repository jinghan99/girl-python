'''
Created by swh on 2017.09.12

需要安装
pip install BeautifulSoup4

'''
#_*_coding:utf-8_*_
import requests
import re
from bs4 import BeautifulSoup
import threading
import os
import re


# 请求数据
def get_response(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    #  取出返回的资源
    response = requests.get(url=url,headers=headers).content
    return response
def get_content(html):
    # 通过 bs4 框架 进行解析， 这里用内置默认html,parser,也可以使用 lxml解析器，需要安装
    soup = BeautifulSoup(html,"html.parser")
    # 获取每块的数据
    cont = soup.select(".j-r-list-c")
    # 定义数组存放 名称 地址
    urlList=[]
    for item in cont:
        # 查找第一个 a 标签的内容 作为 保存mp4的文件名
        name = item.find('a').text
        # 查找图片连接所在的位置 通过 data-original 属性值取出
        pmUrl = item.select('.j-r-list-c-img')[0].find('img').get("data-original")
        # 以元组形式 添加到数组

        print("name :" +str(name))
        print("pmUrl :" +str(pmUrl))
        urlList.append((name,pmUrl))
    return urlList
def get_img_url(imgUrlList):
    '''
    判断当前脚本所在路径是否存在picture文件夹，这里用os模块，os.getcwd()获取当前文件的绝对路径
     使用os模块的该方法不用考虑所在系统是Mac还是windows
    '''
    filePath = os.path.join(os.getcwd(),'picture')
    if not os.path.exists(filePath):
        print("路径不存在")
        os.makedirs(filePath)
    # 遍历取出 img 地址 和图片
    for item in imgUrlList:
        # 判断路径是否存在 不存在下一个
        if item[1] == None:
            continue
        # 判断名称是否过长，如果超过30 则截取 因过长会报错
        namestr = item[0].strip() if len(item[0]) < 30 else item[0].strip()[:27] +'...'

        namestr = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", '', namestr)

        imgPath = os.path.join(filePath,(namestr+item[1][-4:]))


        print("imgPath: "+imgPath)

        '''
        通过多线程 方式下载图片 增加速度
        '''
        thr = threading.Thread(target=save_mp,args=(imgPath,item[1]))
        # 启动线程
        thr.start()
def save_mp(imgPath,url):
    # 保存文件

    # 获取二进制流数据
    response  = get_response(url)

    # 通过文件写入保存文件
    with open(imgPath,"wb") as fp:
        fp.write(response)


    '''
    ** 由于我们这里仅用于测试，所以我们之抓取一页
    ** 链接最后的数字表示抓取的数据页码，由于首页的1可以不写，也可以写上
    ** 为了大家更好的理解多页的表示，这里我们仅抓取一页，并且链接后面写有页码1
    '''
urlStr = 'http://www.budejie.com/pic'
html = get_response(urlStr)
ll = get_content(html)
get_img_url(ll)

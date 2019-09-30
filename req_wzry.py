#encoding:UTF-8
import requests
from bs4 import BeautifulSoup
import os

'''
    方案：
        先获取所有英雄信息，找到对应英雄的序号；然后统计英雄的皮肤数量；
        最后找到皮肤进行下载
'''
# 英雄序号url
hero_url = 'http://pvp.qq.com/web201605/js/herolist.json'
# 皮肤数量url前缀
# eg http://pvp.qq.com/web201605/herodetail/106.shtml
skin_num_url = 'http://pvp.qq.com/web201605/herodetail/'
# 皮肤url前缀
# eg http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/106/106-bigskin-6.jpg
skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'

class GetImg(object):
    '''爬取王者荣耀所有英雄皮肤'''
    # 类属性 存放皮肤地址和名称
    skin_property = {}
    def __init__(self):
        # 图片存储文件按夹
        self.floder_name = 'wzry_skin'
        # 英雄序号url
        self.hero_url = 'http://pvp.qq.com/web201605/js/herolist.json'
        # 皮肤数量url前缀
        # eg http://pvp.qq.com/web201605/herodetail/106.shtml
        self.skin_num_mode = 'http://pvp.qq.com/web201605/herodetail/{}.shtml'
        # 皮肤url前缀
        # eg http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/106/106-bigskin-6.jpg
        self.skin_mode = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
        
    @staticmethod
    def req(url):
        '''因为一直要去请求页面，所以写一个请求的静态方法'''
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    
    def get_hero(self):
        '''获取英雄编号'''
        print('开始获取英雄编号...')
        r = self.req(self.hero_url)
        hero_list = list(map(lambda x:x['ename'], r.json()))
        return hero_list
        
    def get_skin(self, list_num):
        '''构造皮肤字典'''
        print('准备下载...')
        for hero in list_num:
            tmp_url = self.skin_num_mode.format(hero)
            r = self.req(tmp_url)
            
            # 获取皮肤列表
            soup = BeautifulSoup(r.text, 'html.parser')
            # 皮肤数量在<div class="pic-pf">标签下边，这个标签有且只有一个， 所以用find去查找
            skin_str = soup.find(class_="pic-pf").ul['data-imgname']
            skin_list = list(skin_str.split('|'))
            
            # 构造皮肤地址
            skin_num  = len(skin_list)
            for num in range(skin_num):
                skin_name = skin_list[num]
                self.skin_url = self.skin_mode.format(hero, hero, num+1)
                # self.skin_property[skin_name] = self.skin_url   本来打算将图片信息存到字典中，发现运行速度太慢了
                self.download_img(skin_name, self.skin_url)
            # print(self.skin_property)
        print('下载完成...')
    def make_dir(self):
        '''创建存储文件夹'''
        if not os.path.exists(self.floder_name):
            os.mkdir(self.floder_name)
    
    def download_img(self, img_name, img_url):
        '''下载图片'''
        print('正在下载[%s]...' % img_name)
        r = self.req(img_url)
        file_path = os.path.join(self.floder_name, img_name + '.jpg')
        with open(file_path, 'wb') as fp:
            fp.write(r.content)
        fp.close()
        
if __name__ == '__main__':
    try:
        img = GetImg()
        img.make_dir()
        hero_num = img.get_hero()
        img.get_skin(hero_num)
    except Exception as e:
        print(e)

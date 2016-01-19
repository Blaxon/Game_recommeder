"""
爬取游戏图片的爬虫

作者：向航
2016-1-19
"""
import time
import sqlite3
import threading
import traceback
from urllib.request import urlopen


class PictureCrawler:
    """
    一个专门爬取图片的爬虫
    """

    urls = []

    def get_all_url(self):
        """
        获取所有图片的url
        :return: 以列表形式返回
        """
        con = sqlite3.connect('test.db')
        cu = con.cursor()

        cu.execute('select picture from GameInfo_table')
        results = cu.fetchall()

        cu.close()
        con.close()

        self.urls = list(set([_[0] for _ in results]))  # 去tuple去重，这里url有重复的

    def download(self, url):
        """
        下载图片
        :param url: 图片的链接
        :return: 返回执行结果
        """
        file_name = url.split('/')[-1]
        _dir = './GamePic/%s' % file_name

        try:
            con = urlopen(url)
            f = open(_dir, 'wb')
            content = con.read()
            f.write(content)
            f.close()
            con.close()
        except :
            traceback.print_exc()

        print('%s Picture saved.' % file_name)

    def minion(self, lock, thread_id):
        """
        实现多线程的下载函数
        """
        print('Thread %d started work.' % thread_id)
        while 1:
            time.sleep(0.5)
            lock.acquire()
            if len(self.urls) == 0:
                print('No more picture url find.Thread %d shutdown.' % thread_id)
                lock.release()
                return
            else:
                url = self.urls.pop()
            lock.release()

            self.download(url)

    def commander(self):
        """
        多线程下载图片控制函数
        :return:
        """
        lock = threading.Lock()
        thread_num = 10
        threads = []

        for _ in range(thread_num):
            t = threading.Thread(target=self.minion, args=(lock, _))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()


if __name__ == '__main__':
    def test1():
        """
        测试 get_all_url
        :return:
        """
        a = PictureCrawler()
        a.get_all_url()
        print(len(a.urls))
        print(a.urls[:4])

    def test2():
        """
        测试 download
        :return:
        """
        a = PictureCrawler()
        a.get_all_url()
        a.download(a.urls[0])

    def test3():
        """
        测试多线程
        :return:
        """
        a = PictureCrawler()
        a.get_all_url()
        a.urls = a.urls[:30]
        print(len(a.urls))
        a.commander()

    # test3()
    P = PictureCrawler()
    P.get_all_url()
    P.commander()
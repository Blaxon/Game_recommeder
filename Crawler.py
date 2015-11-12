"""
2015-11-10

这个是游戏爬虫

目标网页：http://www.doyo.cn/danji/list?p=
页数范围：1-566
游戏数目：11319

待解决问题：
1.不知道怎么爬取图片，爬链接？#已解决，爬取链接

作者：向航
"""
import socket
import traceback
from urllib import request
from bs4 import BeautifulSoup

TARGET_URL = 'http://www.doyo.cn'
# TARGET_URL = 'http://www.doyo.cn/danji/list?p='
PAGE_RANGE = 566


class Crawler:
    """
    a crawler
    """
    def link_parser(self, list_page_url):
        """
        given a game list page url,
        return a tuple : (game_name, game_url) # this is complete game url
        """
        fail = 0
        while fail < 10:
            try:
                page = request.urlopen(list_page_url, timeout=3).read()
                break
            except socket.timeout:
                fail += 1
                print('connection failed, try again... %d' % fail)

        _soup = BeautifulSoup(page, 'html.parser')
        _f = _soup.find('div', class_='list')
        _ret = [(item['title'], TARGET_URL+item['href'])for item in _f.find_all('a')]
        print('list page parse done.')
        return _ret

    def content_parser(self, game_url, game_dict):
        """
        given a game url and a game dict which include game name
        return nothing, modify game_dict inplace.
        game_dict = {'game_name': str,
                     '简单介绍':   str,
                     '类型':      str,
                     '语言':      str,
                     '画面':      str,
                     '题材':      str,
                     '厂商':      str,
                     '上市':      str,
                     '标签':      str,
                     '玩家投票':   str, # 分为好玩、一般、不好玩
                     ’评分':      float,
                     '游戏介绍':   str,
                     '游戏图片':   str}  # 游戏图片为url链接
        """
        fail = 0
        while fail < 10:
            try:
                page = request.urlopen(game_url, timeout=3).read()
                break
            except socket.timeout:
                fail += 1
                print('connection failed,try again... %d' % fail)

        _soup = BeautifulSoup(page, 'html.parser')
        game_info = _soup.find('div', id='game_info').text
        game_dict['简单介绍'] = _soup.find('div', class_='intro').text
        lines = game_info.split('\n')

        for each_line in lines[8:15]:
            _ = each_line.split('：')
            game_dict[_[0]] = _[1].strip()

        game_dict['玩家投票'] = [int(_) for _ in lines[21:24]]
        game_dict['评分'] = float(lines[26])
        game_dict['游戏介绍'] = _soup.find('div', id='game_introduction').text
        game_dict['游戏图片'] = _soup.find('div', id='game_info').img['src']
        print('content parse done.[%s]' % game_dict['game_name'])

    def run(self):
        """
        this is a game info generator which will collect all the game info from DOYO.
        this output need module to save it into excel or files like this.
        """
        for i in range(PAGE_RANGE):
            _url = TARGET_URL + '/danji/list?p=' + str(i)
            _links = self.link_parser(_url)
            for _link in _links:
                _game_dict = {'game_name': _link[0]}
                self.content_parser(_link[1], _game_dict)
                yield _game_dict

    def multi_run(self):
        """
        using multi-thread to collect
        also this is a generator.
        """
        import threading

        def multi_thread(links, dicts):
            while 1:
                lock.acquire()
                if len(links) == 0:
                    print('links empty exit thread.')
                    lock.release()
                    return
                else:
                    _link = links.pop()
                lock.release()

                _game_dict = {'game_name': _link[0]}
                self.content_parser(_link[1], _game_dict)

                lock.acquire()
                dicts.append(_game_dict)
                lock.release()

        lock = threading.Lock()
        thread_count = 20

        for i in range(PAGE_RANGE):
            _url = TARGET_URL + '/danji/list?p=' + str(i)
            _links = self.link_parser(_url)
            _dicts = []  # include many games info

            # import ipdb
            # ipdb.set_trace()
            threads = []

            for _ in range(thread_count):
                t = threading.Thread(target=multi_thread, args=(_links, _dicts))
                threads.append(t)

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            yield _dicts

if __name__ == '__main__':
    def test1():
        """
        test link parser
        """
        c = Crawler()
        for _ in range(10):
            ret = c.link_parser(TARGET_URL+'/danji/list?p='+str(_))
            print(ret)

    def test2():
        """
        test content parser
        """
        c = Crawler()
        links = c.link_parser(TARGET_URL+'/danji/list?p=1')
        for link in links:
            d = {'game_name': link[0]}
            c.content_parser(link[1], d)
            print(d)

    def test3():
        """
        test run function
        """
        c = Crawler()
        for item in c.run():
            print(item)

    def test4():
        """
        test multi thread run
        """
        c = Crawler()
        ret = next(c.multi_run())
        print(ret)

    test4()
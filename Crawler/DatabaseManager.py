"""
2015-11-10

这是数据存入数据库的模块，
以及未来数据库与服务器交互的模块。

作者：向航
"""
import sqlite3
import traceback


class DbManager:
    """
    store game info into database.
    """
    def __init__(self, database):
        """
        build database
        input database which is a str,means database name.
        """
        self.db_path = database
        con = sqlite3.connect(self.db_path)
        sql_create_table = 'create table if not exists GameInfo_table \
        (name text primary key, simple_intro text, \
        type text, language text, display text, theme test, company test, time text, \
        tag text, player_vote text, score float, introduction text, picture text)'
        con.execute(sql_create_table)
        con.close()
        print('database initial complete.')

    def open(self):
        self.con = sqlite3.connect(self.db_path)

    def close(self):
        self.con.close()

    def check_num(self):
        cu = self.con.cursor()
        cu.execute('select count(*) from GameInfo_table')
        print('total num: ', cu.fetchall()[0][0])

    def insert_result(self, game_info):
        cu = self.con.cursor()
        try:
            # import ipdb
            # ipdb.set_trace()
            cu.execute("insert into GameInfo_table values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (game_info['game_name'], game_info['简单介绍'], game_info['类型'],
                        game_info['语言'], game_info['画面'], game_info['题材'], game_info['厂商'],
                        game_info['上市'], game_info['标签'], str(game_info['玩家投票']), game_info['评分'],
                        game_info['游戏介绍'], game_info['游戏图片']))
            self.con.commit()
            print('Inserted %s' % game_info['game_name'])
        except sqlite3.IntegrityError:
            print('same game,skipped.')
        except :
            traceback.print_exc()
        cu.close()

    def multi_insert_results(self, game_infos):
        cu = self.con.cursor()
        try:
            for game_info in game_infos:
                try:
                    cu.execute("insert into GameInfo_table values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (game_info['game_name'], game_info['简单介绍'], game_info['类型'],
                                game_info['语言'], game_info['画面'], game_info['题材'], game_info['厂商'],
                                game_info['上市'], game_info['标签'], str(game_info['玩家投票']), game_info['评分'],
                                game_info['游戏介绍'], game_info['游戏图片']))
                except sqlite3.IntegrityError:
                    print('same game, skipped...')
                print('Inserted %s' % game_info['game_name'])
            self.con.commit()
        except:
            traceback.print_exc()
        cu.close()


if __name__ == '__main__':
    # Dbmanager inital test
    def test1():
        db = DbManager('test.db')

    # insert_result test
    def test2():
        import Crawler
        c = Crawler.Crawler()
        db = DbManager('test.db')
        db.open()
        for result in c.run():
            db.insert_result(result)
            db.check_num()

    # multi_insert_results test
    def test3():
        import Crawler
        c = Crawler.Crawler()
        db = DbManager('test.db')
        db.open()
        for results in c.multi_run():
            db.multi_insert_results(results)
            db.check_num()

    test3()
import re
from .utils import data_path


class ReplyDict(object):
    def __init__(self):
        self.reply = {'': '我在 众神傻逼', '哈哈哈': '本群禁止哈哈哈!'}
        self.read_reply_dict()

    def is_in_dict(self, keyword):
        return keyword in self.reply.keys()

    def get_reply_msg(self, keyword):
        return self.reply[keyword]

    def refresh_reply_dict(self, content):
        result = re.split('[:：]', content.replace('\n', ''))
        self.reply[result[0]] = result[1]
        self.save_reply_dict()

    def read_reply_dict(self):
        with open(data_path + 'reply.txt', 'r+') as reply_dict_file:
            for line in reply_dict_file.readlines():
                result = line.split('\t')
                if len(result) == 2:
                    self.reply[result[0]] = result[1][:-1]
        # for keyword in self.reply.keys():
        #     print("%s\t%s" % (keyword, self.reply[keyword]))

    def save_reply_dict(self):
        try:
            with open(data_path + 'reply.txt', 'w+') as reply_dict_file:
                for keyword in self.reply.keys():
                    if keyword != '':
                        reply_dict_file.writelines(keyword + '\t' + self.reply[keyword] + '\n')
        except UnicodeEncodeError as e:
            print(e)


if __name__ == "__main__":
    reply_dict = ReplyDict()
    reply_dict.is_in_dict('?')
    reply_dict.get_reply_msg('？')
    reply_dict.refresh_reply_dict('哈哈哈:本群禁止哈哈哈!')

import os
import datetime

from crack.crack_task import CrackTask

author_info = '''
+---------------------------------------------------+
| __          __  _      _____                _     |
| \ \        / / | |    / ____|              | |    |
|  \ \  /\  / /__| |__ | |     _ __ __ _  ___| | __ |
|   \ \/  \/ / _ \ '_ \| |    | '__/ _' |/ __| |/ / |
|    \  /\  /  __/ |_) | |____| | | (_| | (__|   <  |
|     \/  \/ \___|_.__/ \_____|_|  \__,_|\___|_|\_\ |
|                                                   |
|                 code by @yzddmr6                  |
|                  version: 2.2                     |
+---------------------------------------------------+
'''


def single_process_crack(url_list):
    all_num = len(url_list)
    cur_num = 1
    print("总任务数: " + str(all_num))
    for url in url_list:
        CrackTask().run(cur_num, url)
        cur_num += 1


if __name__ == '__main__':
    print(author_info)
    try:
        import conf.config
    except:
        print("加载配置文件失败！")
        exit(0)

    url_file_name = input('File or Url:\n')

    if '://' in url_file_name:
        CrackTask().run(1, url_file_name)
    else:
        url_list = []
        if os.path.exists(url_file_name):
            print(url_file_name, "exists!\n")
            with open(url_file_name, 'r', encoding="UTF-8") as url_file:
                for url in url_file.readlines():
                    url = url.strip()
                    if url.startswith('#') or url == '' or ('.edu.cn' in url) or ('.gov.cn' in url):
                        continue
                    url_list.append(url)
            start = datetime.datetime.now()
            single_process_crack(url_list)
            end = datetime.datetime.now()
            print(f'All processes done! Cost time: {str(end - start)}')
        else:
            print(url_file_name + " not exist!")
            exit(0)

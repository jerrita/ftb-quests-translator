import os

from concurrent.futures import ThreadPoolExecutor
from Translator import GoogleTranslator
# from Translator import BaiduTranslator
# from priv import apikey, appid

import ftb_snbt_lib as slib

base = './quests/chapters'
lang = 'zh'
out = 'out_chapters'
debug = True

client = GoogleTranslator()

trans_cache = {}


def translate(src):
    if src.strip() == '':
        return ''

    res = ''
    # res = client.translate(src, target=lang).translatedText
    if src in trans_cache:
        res = trans_cache[src]
    else:
        res = trans_cache[src] = client.translate(src, dst=lang)

    if debug:
        print(f'  {src[:30]} -> {res[:30]}')
    return slib.String(res)


def trans_title(ctx):
    ctx['title'] = translate(ctx['title'])
    return ctx


def trans_quests(ctx):
    res = []
    for quest in ctx['quests']:
        quest = trans_title(quest)
        work = []
        for desc in quest['description']:
            work.append(translate(desc))
        quest['description'] = slib.List(work)
        res.append(quest)
    ctx['quests'] = slib.List(res)
    return ctx


def work_file(file_path):
    if file_path.endswith('.snbt'):
        if os.path.isfile(os.path.join(out, file_path)):
            print('[Skip]', file_path)
            return file_path

        print('=>', file_path)
        ctx = slib.load(
            open(os.path.join(base, file_path), 'r', encoding='utf-8'))
        ctx = trans_title(ctx)
        ctx = trans_quests(ctx)
        slib.dump(ctx, open(os.path.join(out, file_path), 'w', encoding='utf-8'))
    return file_path


def main():
    files = os.listdir(base)
    print('Working dir:', base, '\nTranslating...')
    # shutil.rmtree(out)
    if not os.path.exists(out):
        os.mkdir(out)

    with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(work_file, files)
        for res in result:
            print('[Done]', res)
    print('All Done.')


if __name__ == '__main__':
    main()

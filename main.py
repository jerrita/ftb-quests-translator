import os
import re

from concurrent.futures import ThreadPoolExecutor

# from Translator import GoogleTranslator
from Translator import BaiduTranslator
# from priv import apikey, appid

base = './quests/chapters'
lang = 'zh'
out = 'out_chapters'
debug = True

# client = GoogleTranslator()
client = BaiduTranslator(appid, apikey)

trans_cache = {}


def translate(src: str):
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
    return res


def trans_title(ctx):
    titleRegex = r'title: ".*"'
    titleRegexStr = r'title: "(.+)"'
    titles = re.findall(titleRegex, ctx)
    for i in titles:
        src = re.match(titleRegexStr, i).group(1)
        dst = translate(src)
        ctx = ctx.replace(i, i.replace(src, dst))
    return ctx


def trans_desc(ctx):
    descRegex = r'description: \[(?:\s*)?(?:".*"(?:\s*)?)+\]'
    targets = re.findall(descRegex, ctx, )
    for desc in targets:
        desc_old = desc
        srcs = re.findall('"(.+)"', desc)
        for src in srcs:
            dst = translate(src)
            desc = desc.replace(src, dst)
        ctx = ctx.replace(desc_old, desc)
    return ctx


def work_file(file_path):
    if file_path.endswith('.snbt'):
        if os.path.isfile(os.path.join(out, file_path)):
            print('[Skip]', file_path)
            return file_path

        print('=>', file_path)
        ctx = open(os.path.join(base, file_path), 'r', encoding='utf-8').read()
        ctx = trans_title(ctx)
        ctx = trans_desc(ctx)
        fp = open(os.path.join(out, file_path), 'w', encoding='utf-8')
        fp.write(ctx)
        fp.close()
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

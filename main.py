import os
import asyncio

import ftb_snbt_lib as slib

from priv import base_url, api_key
from translator.openai import OpenAITranslator

base = './quests/chapters'
lang = 'zh-CN'
out = 'out_chapters'
dual_lang = False  # 是否启用双语
debug = True

modpack = slib.load(
    open('./quests/data.snbt', 'r', encoding='utf-8'))['title']
print('Modpack:', modpack)

client = OpenAITranslator(
    base_url=base_url,
    api_key=api_key,
    modpack=modpack
)

trans_cache = {}


async def translate(src):
    if src.strip() == '':
        return slib.String('')

    res = ''
    if src in trans_cache:
        res = trans_cache[src]
    else:
        res = trans_cache[src] = await client.translate(src, dst=lang)

    if debug:
        print(f'  {src[:30]} -> {res[:30]}')
    return slib.String(res)


async def trans_title(ctx):
    if 'title' in ctx:
        if dual_lang:
            ctx['title'] = ctx['title'] + ' / ' + await translate(ctx['title'])
        else:
            ctx['title'] = await translate(ctx['title'])
        ctx['title'] = slib.String(ctx['title'])
    return ctx


async def trans_quests(ctx):
    if 'quests' not in ctx:
        return ctx

    # 并发处理所有quest，但保持顺序
    async def process_quest(quest):
        quest = await trans_title(quest)
        if 'description' in quest:
            work = []
            # 并发翻译所有描述，但保持顺序
            translation_tasks = []
            for desc in quest['description']:
                if dual_lang:
                    work.append(desc)
                translation_tasks.append(translate(desc))

            # 等待所有翻译完成，保持顺序
            if translation_tasks:
                translations = await asyncio.gather(*translation_tasks)
                work.extend(translations)

            quest['description'] = slib.List(work)
        return quest

    # 并发处理所有quest，使用gather保持顺序
    tasks = [process_quest(quest) for quest in ctx['quests']]
    results = await asyncio.gather(*tasks)

    ctx['quests'] = slib.List(results)
    return ctx


async def work_file(file_path):
    if file_path.endswith('.snbt'):
        if os.path.isfile(os.path.join(out, file_path)):
            print('[Skip]', file_path)
            return file_path

        print('=>', file_path)
        ctx = slib.load(
            open(os.path.join(base, file_path), 'r', encoding='utf-8'))
        ctx = await trans_title(ctx)
        ctx = await trans_quests(ctx)
        slib.dump(ctx, open(os.path.join(out, file_path), 'w', encoding='utf-8'))
    return file_path


async def main():
    files = os.listdir(base)
    print('Working dir:', base, '\nTranslating...')
    # shutil.rmtree(out)
    if not os.path.exists(out):
        os.mkdir(out)

    try:
        # 直接并发处理所有文件，不限制并发数
        tasks = [work_file(file_path) for file_path in files]
        results = await asyncio.gather(*tasks)

        for res in results:
            print('[Done]', res)
    finally:
        # 确保关闭客户端连接
        await client.close()

    print('All Done.')


if __name__ == '__main__':
    asyncio.run(main())

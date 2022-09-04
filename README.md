# FTB Quests 一键翻译器

找汉化包要么对不上版本，要么服务端没汉化，索性整一个

## Feature

- 硬编码翻译写入，省时省力 (i18n 去他妈)
- 支持版本: 1.16+ ? (反正这个逻辑的都行)
- 你可以自己重写翻译逻辑 (比如换成 pygtrans，当前是百度)

## 使用教程

- 将你整合包的 quests 目录丢过来 (你也可以 ln)
- 新建 prv.py，填入你的翻译 API (有白嫖额度，但质量不咋样)
- python main.py
- (Optional) 备份原有 chapters
- mv out_chapters chapters
- mv chapters quests
- 将 quests 丢回去

## priv.py 格式

```python
appid, apikey = 'xxx', 'xxx'
```
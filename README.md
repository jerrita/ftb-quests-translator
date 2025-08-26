# FTB Quests 一键翻译器

找汉化包要么对不上版本，要么服务端没汉化，索性整一个

## Feature

- 硬编码翻译写入，省时省力 (i18n 去他妈)
- 支持版本: 1.16+ ? (反正这个逻辑的都行)
- 默认 Async OpenAI 翻译器，一个大型包可以 10S 翻译完
- 某格雷空岛包在 gpt-4o-mini 下大概用量为 $0.02

## 使用教程

- 将你整合包的 quests 目录丢过来 (你也可以 ln)
- 新建 priv.py，并在 main.py 配置你的 Translator
- python main.py
- (Optional) 备份原有 chapters
- mv out_chapters chapters
- mv chapters quests
- 将 quests 丢回去

## priv.py 格式

```python
# baidu
appid, apikey = 'xxx', 'xxx'

# openai
base_url = 'https://api.example.com/v1'
api_key = 'sk-1145141919810'
```


from translator import Translator
from openai import OpenAI


class OpenAITranslator(Translator):
    def __init__(self, base_url, api_key, model='gpt-4o-mini', modpack='Modpack'):
        """
        初始化 OpenAI 翻译器

        Args:
            base_url (str): OpenAI API 的基础 URL
            token (str): OpenAI API 令牌
            model (str): 使用的模型名称，默认为 'gpt-4o-mini'
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model
        self.modpack = modpack

    def set_modpack_name(self, modpack: str):
        self.modpack = modpack

    def translate(self, query: str, src='auto', dst='zh-CN') -> str:
        """
        使用 OpenAI 模型进行翻译

        Args:
            query (str): 要翻译的文本
            src (str): 源语言，默认为 'auto'
            dst (str): 目标语言，默认为 'zh-CN'

        Returns:
            str: 翻译后的文本
        """
        if query in ['I', 'i']:
            return query

        prompt = ' '.join([
            f"Please translate the following text to {dst}.",
            f"This text is from a minecraft FTB Quests' title/description, with modpack name `{self.modpack}`.",
            f"Handle the tag syntax of Minecraft carefully."
            f"Only return the translated text without any explanation:\n\n{query}"
        ])

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )

            # 检查响应类型并提取翻译结果
            if hasattr(response, 'choices') and len(response.choices) > 0:
                translation = response.choices[0].message.content.strip()
                return translation
            else:
                # 如果响应格式不正确，记录响应内容
                print(f"Unexpected response format: {response}")
                raise Exception(f"Unexpected response format: {type(response)}")

        except Exception as e:
            # 如果翻译失败，抛出异常或返回原文
            print(f"Translation error details: {e}")
            print(f"Query was: {query}")
            raise Exception(f"OpenAI translation failed: {str(e)}")


if __name__ == '__main__':
    # 示例用法
    # translator = OpenAITranslator('https://api.openai.com/v1', 'your-api-key')
    # result = translator.translate('Hello world!')
    # print(result)
    pass

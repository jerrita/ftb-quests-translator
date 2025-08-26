class Translator:
    async def translate(self, query: str, src='auto', dst='zh') -> str:
        raise NotImplementedError

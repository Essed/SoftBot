
class UserSettings:
    def __init__(self) -> None:
        self.__settings = dict()
        self.__categories = dict()

    async def set_keywords(self, user_id: int, key_words: list):
        self.__settings[user_id] = key_words

    async def user_keywords(self, user_id: int):
        if len(self.__settings.items()) > 0:
            return self.__settings[user_id]
        return []

    async def set_categories(self, user_id: int, categories: list):
        self.__categories[user_id] = categories

    async def user_categories(self, user_id: int):
        if len(self.__categories.items()) > 0:
            return self.__categories[user_id]
        return []

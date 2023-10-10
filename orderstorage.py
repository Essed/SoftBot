class OrderStorage:

    orders: str = ""
    orders_main: str = ""
    last_index: int = 0

    @staticmethod
    async def get_orders() -> str:
        return OrderStorage.orders

    @staticmethod
    async def get_last_index():
        return OrderStorage.last_index

    @staticmethod
    async def set_orders(text: str):
        OrderStorage.orders = text
    
    @staticmethod
    async def set_main_orders(text: str):
        OrderStorage.orders_main = text

    @staticmethod
    async def get_main_orders():
        return OrderStorage.orders_main

    @staticmethod
    async def set_index(index: int):
        OrderStorage.last_index = index
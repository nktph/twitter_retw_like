import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import keyboardmarkups as nav
from aiogram.contrib.fsm_storage.memory import MemoryStorage

try:
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token="6140832192:AAGXVzLxuBIKKGjU3QEOGx9a3A_omROHGpM")
    # Диспетчер
    dp = Dispatcher(bot, storage=MemoryStorage())


    class StateWorker(StatesGroup):
        work_accounts = State()
        add_account = State()
        delete_accounts = State()

        edit_proxy = State()

        set_delays = State()
        set_delay_tweet = State()
        set_delay_like_retw = State()

        set_tweet_quantity = State()

    # Хэндлер на команду /start
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await message.answer("Привет\nДержи меню", reply_markup=nav.mainMenu)

    # Выбор операции над аккаунтом
    @dp.message_handler(state=StateWorker.work_accounts)
    async def add_account(message: types.Message, state: FSMContext):
        if message.text == '📂 Добавить новый аккаунт':
            await message.answer("Аккаунты добавлены")
        elif message.text == '🗑 Очистить все аккаунты':
            await message.answer("Аккаунты удалены")

        await state.finish()

    # Добавление Аккаунтов
    @dp.message_handler(state=StateWorker.work_accounts)
    async def add_account(message: types.Message, state: FSMContext):
        await message.answer("Аккаунты добавлены")
        await state.finish()

    # Изменение прокси
    @dp.message_handler(state=StateWorker.edit_proxy)
    async def add_account(message: types.Message, state: FSMContext):
        await message.answer("Прокси изменён")
        await state.finish()

    # Изменение количества твитов
    @dp.message_handler(state=StateWorker.set_tweet_quantity)
    async def add_account(message: types.Message, state: FSMContext):
        await message.answer("Количество твитов задано")
        await state.finish()

    # Задание задержек
    @dp.message_handler(state=StateWorker.set_delays)
    async def add_account(message: types.Message, state: FSMContext):
        await message.answer("Задайте задержку между лайком и ретвитом")
        await state.set_state(StateWorker.set_delay_like_retw.state)

    # Задержка между лайком и ретвитом
    @dp.message_handler(state=StateWorker.set_delay_like_retw)
    async def add_account(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            await message.answer("Задержка между лайком и ретвитом установлена\nТеперь задайте задержу между твитами")
            await state.set_state(StateWorker.set_delay_tweet.state)

    # Задержка между лайком и ретвитом
    @dp.message_handler(state=StateWorker.set_delay_tweet)
    async def add_account(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            await message.answer("Задержка между твитами установлена")
            await state.finish()


    # Приёмник комманд
    @dp.callback_query_handler()
    async def menu(call: types.CallbackQuery):
        if call.data == "accounts":
            await call.message.answer("Работа с аккаунтами", reply_markup=nav.cookieMenu)
            await StateWorker.add_account.set()

        elif call.data == "launch":
            await call.message.answer("Запуск")

        elif call.data == "proxy":
            await call.message.answer("Смена прокси")
            await StateWorker.edit_proxy.set()

        elif call.data == "delays":
            await call.message.answer("Задержки")
            await StateWorker.set_delays.set()

        elif call.data == "quantity":
            await call.message.answer("Количество твитов")
            await StateWorker.set_tweet_quantity.set()

        elif call.data == '⬅️Главное меню':
            await call.message.answer('Главное меню', reply_markup=nav.mainMenu)

        elif call.data == '📂 Добавить новый аккаунт':
            await call.message.answer('Новый аккаунт', reply_markup=types.ReplyKeyboardRemove())
            # await CookieWorker.add_cookie.set()
        elif call.data == '🗑 Очистить все аккаунты':
            # await clear_cookies_all()
            await call.message.answer('Аккаунты удалены', reply_markup=nav.mainMenu)


    @dp.callback_query_handler(state='*')
    async def cancel(call: types.CallbackQuery, state: FSMContext):
        if call.data == 'back_menu':
            await state.finish()
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await call.message.answer('Отменено')


    # Запуск процесса поллинга новых апдейтов
    async def main():
        await dp.start_polling(bot)


    if __name__ == "__main__":
        asyncio.run(main())

except KeyboardInterrupt:
    print('Работа прервана вручную')


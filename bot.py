import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import keyboardmarkups as nav
import database as db
import main as main_script
from aiogram.contrib.fsm_storage.memory import MemoryStorage

try:
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token="ТВОЙ ТОКЕН БОТА")
    # Диспетчер
    dp = Dispatcher(bot, storage=MemoryStorage())


    class StateWorker(StatesGroup):
        work_accounts = State()

        add_account_login = State()
        add_account_mail = State()

        edit_proxy = State()

        set_delays = State()
        set_delay_tweet = State()
        set_delay_like_retw = State()

        set_tweet_quantity = State()

        get_account = State()
        post_count = State()

    # Хэндлер на команду /start
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await message.answer("Привет\nДержи меню", reply_markup=nav.mainMenu)

    # Добавление Аккаунтов
    @dp.message_handler(state=StateWorker.work_accounts)
    async def add_account(message: types.Message, state: FSMContext):
        await message.answer("Аккаунты добавлены")
        await state.finish()

    # Изменение прокси
    @dp.message_handler(state=StateWorker.edit_proxy)
    async def add_account(message: types.Message, state: FSMContext):
        if ':' in message.text and len(message.text) > 5:
            await message.answer("Прокси изменён")
            return await state.finish()

        await message.answer("Проверьте правильность прокси")

    # Изменение количества твитов
    @dp.message_handler(state=StateWorker.set_tweet_quantity)
    async def add_account(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            print(message.text)
            await message.answer("Количество твитов задано")
            return await state.finish()

        await message.answer('Введите число')

    @dp.message_handler(state=StateWorker.set_delay_like_retw)
    async def set_delay_like_retw(message: types.Message, state: FSMContext):
        if not message.text.isdigit():
            return await bot.send_message(message.chat.id, 'Введите число')
        print('like delay:',message.text)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id,"Успешно\nДержи меню", reply_markup=nav.mainMenu)
        await state.finish()


    @dp.message_handler(state=StateWorker.set_delay_tweet)
    async def set_delay_tweet(message: types.Message, state: FSMContext):
        if not message.text.isdigit():
            return await bot.send_message(message.chat.id, 'Введите число')
        print('Tweet delay:',message.text)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, "Успешно\nДержи меню", reply_markup=nav.mainMenu)
        await state.finish()


    @dp.message_handler(state=StateWorker.add_account_mail)
    async def add_account_mail(message: types.Message, state: FSMContext):
        if '@' in message.text and ':' in message.text:
            async with state.proxy() as data:
                print(f'[mail:password] {message.text}\n'
                      f'[login:password] {data["account"]}')
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.send_message(message.chat.id, "Успешно\nДержи меню", reply_markup=nav.mainMenu)
                db.Accounts.create(login=data['account'].split(':')[0],
                                   password = data['account'].split(':')[1],
                                   mail = message.text.split(':')[0],
                                   mail_password = message.text.split(':')[1])
                return await state.finish()

        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, "Убедитесь что ввели почту в верном формате почта:пароль")


    @dp.message_handler(state=StateWorker.get_account)
    async def get_account(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['url'] = message.text

        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.send_message(message.from_user.id, 'Теперь введите кол-во постов для накрутки')
        await StateWorker.post_count.set()

    @dp.message_handler(state=StateWorker.post_count)
    async def get_account(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if not message.text.isdigit():
                await message.answer('Вы ввели не число')
                await state.finish()

            await bot.delete_message(message.from_user.id, message.message_id)
            accounts = db.Accounts.select().dicts()
            if len(accounts) == 0:
                await bot.send_message(message.from_user.id, 'Сначала добавьте аккаунты')
                return await state.finish()

            tweets = 0
            likes = 0

            for i in accounts:
                res = main_script.start_account(int(message.text), i['login'], i['password'], i['mail'], i['mail_password'], data['url'])
                tweets += res[1]
                likes += res[0]

            await bot.send_message(message.from_user.id, f'Успешно накручено {tweets} ретвитов и {likes} лайков')

            await state.finish()


    @dp.message_handler(state=StateWorker.add_account_login)
    async def add_account_login(message: types.Message, state: FSMContext):
        if ':' in message.text:
            async with state.proxy() as data:
                data['account'] = message.text
            print(f'[login:password] {message.text}')
            await message.delete()
            await bot.send_message(message.chat.id, 'Теперь введи почту и пароль от нее в формате почта:пароль')
            return await StateWorker.add_account_mail.set()

        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, "Убедитесь что ввели данные от аккаунта в верном формате логин:пароль")

    # Приёмник комманд
    @dp.callback_query_handler(state='*')
    async def menu(call: types.CallbackQuery, state: FSMContext):
        if call.data == "accounts":
            await call.message.edit_text("Работа с аккаунтами", reply_markup=nav.cookieMenu)

        elif call.data == 'add_new_account':
            await call.message.edit_text('Введи логин и пароль от аккаунта в формате: логин:пароль')
            await StateWorker.add_account_login.set()

        elif call.data == "launch":
            await call.message.edit_text('Введите ссылку на аккаунт')
            await StateWorker.get_account.set()

        elif call.data == 'delay_likes':
            await call.message.edit_text(text='Введите задержку лайков и твитов')
            await StateWorker.set_delay_like_retw.set()

        elif call.data == 'delay_twites':
            await call.message.edit_text(text='Введите задержку лайков и твитов')
            await StateWorker.set_delay_tweet.set()

        elif call.data == "proxy":
            await call.message.answer("Введите новое прокси")
            await StateWorker.edit_proxy.set()

        elif call.data == "delays":
            await call.message.edit_text("Выбери задержку для редактирования", reply_markup=nav.delay_kb)

        elif call.data == "quantity":
            await call.message.answer("Количество твитов")
            await StateWorker.set_tweet_quantity.set()

        elif call.data == 'back_menu':
            await call.message.edit_text("Привет\nДержи меню", reply_markup=nav.mainMenu)
            await state.finish()

        elif call.data == 'delete_all_accounts':
            db.Accounts.delete().execute()
            await call.message.edit_text('Успешно', reply_markup=nav.mainMenu)

        elif call.data == 'accounts_list':
            temp_kb = types.InlineKeyboardMarkup()

            for i in db.Accounts.select().dicts():
                temp_kb.add(
                    types.InlineKeyboardButton(text=i['login'], callback_data=f'del_{i["login"]}')
                )
                print(i)

            temp_kb.add(nav.back_button)

            await call.message.edit_text('При нажатии на аккаунт он удаляется', reply_markup=temp_kb)

        elif 'del_' in call.data:
            login = call.data.replace('del_', '', 1)
            db.Accounts.delete().where(db.Accounts.login == login).execute()

            temp_kb = types.InlineKeyboardMarkup()

            for i in db.Accounts.select().dicts():
                temp_kb.add(
                    types.InlineKeyboardButton(text=i['login'], callback_data=f'del_{i["login"]}')
                )
                print(i)

            temp_kb.add(nav.back_button)

            await call.message.edit_reply_markup(reply_markup=temp_kb)

    # Запуск процесса поллинга новых апдейтов
    async def main():
        db.connect()
        await dp.start_polling(bot)


    if __name__ == "__main__":
        asyncio.run(main())

except KeyboardInterrupt:
    print('Работа прервана вручную')


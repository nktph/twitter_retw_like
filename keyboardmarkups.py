from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

back_menu = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена', callback_data='back_menu'))
back_button = InlineKeyboardButton(text='⬅  Назад', callback_data='back_menu')

btnMainMenu = KeyboardButton('⬅️Главное меню')
# --Main menu--
btnAccounts = InlineKeyboardButton(text='👤 Работа с аккаунтами', callback_data='accounts')
#btnProxy = InlineKeyboardButton(text='🗄 Изменить прокси', callback_data='proxy')
#btnTimings = InlineKeyboardButton(text='🕑 Установить задержки', callback_data='delays')
#btnQuantity = InlineKeyboardButton(text='📐 Установить количество твитов', callback_data='quantity')
btnBegin = InlineKeyboardButton(text='🤖 Запуск', callback_data='launch')
mainMenu = InlineKeyboardMarkup(row_width=1).add(btnAccounts, btnBegin)

# --Cookie--
btnAddCookies = InlineKeyboardButton('📂 Добавить новый аккаунт', callback_data='add_new_account')
btnDeleteCookies = InlineKeyboardButton('🗑 Очистить все аккаунты', callback_data='delete_all_accounts')
cookieMenu = InlineKeyboardMarkup(row_width=1).add(btnAddCookies, btnDeleteCookies).add(back_button)

# --Delay Panel--
btnlikeDelay = InlineKeyboardButton(text='Задержка между лайками и твитами', callback_data='delay_likes')
btntwitsDelay = InlineKeyboardButton(text='Задержка между твитами', callback_data='delay_twites')

delay_kb = InlineKeyboardMarkup(row_width=1).add(btnlikeDelay).add(btntwitsDelay).add(back_button)
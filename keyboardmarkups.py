from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

back_menu = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена', callback_data='back_menu'))

btnMainMenu = KeyboardButton('⬅️Главное меню')
# --Main menu--
btnAccounts = InlineKeyboardButton(text='👤 Работа с аккаунтами', callback_data='accounts')
btnProxy = InlineKeyboardButton(text='🗄 Изменить прокси', callback_data='proxy')
btnTimings = InlineKeyboardButton(text='🕑 Установить задержки', callback_data='delays')
btnQuantity = InlineKeyboardButton(text='📐 Установить количество твитов', callback_data='quantity')
btnBegin = InlineKeyboardButton(text='🤖 Запуск', callback_data='launch')
mainMenu = InlineKeyboardMarkup(row_width=2).add(btnAccounts, btnProxy, btnTimings, btnQuantity, btnBegin)

# --Cookie--
btnAddCookies = KeyboardButton('📂 Добавить новый аккаунт')
btnDeleteCookies = KeyboardButton('🗑 Очистить все аккаунты')
cookieMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAddCookies, btnDeleteCookies, btnMainMenu)

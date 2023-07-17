from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from loguru import logger
import config
from google_table import GoogleTable
from utils import get_command_number

logger.add(
    config.settings["LOG_FILE"],
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip",
)


class FreakTelegramBot(Bot):
    """Класс информационного бота для студии танцев."""
    def __init__(
        self,
        token:str,
        parse_mode:'aiogram.enums.ParseMode',
        google_table:GoogleTable=None,
    ) -> None:
        """Инициализирует класс.
        Args:
            tokens (str): Токен бота для доступа к Telegram API.
            parse_mode (ParseMode): id публичной страницы ВКонтакте от имени которой опрос.
            google_table (GoogleTable): Агрегат для работы с Google Sheet.
        Returns:- 
        """
        super().__init__(token, parse_mode=parse_mode)
        self._google_table: GoogleTable = google_table

bot: FreakTelegramBot = FreakTelegramBot(
    token=config.settings["TOKEN"],
    parse_mode=types.ParseMode.HTML,
    google_table=GoogleTable("creds.json", config.settings['DOC_URL'])
)
dp = Dispatcher(bot)


@dp.message_handler(filters.Regexp(regexp=r"(((А|а)бонемент)(\s)(\d+))"))
async def abonement_handler(message_from: types.Message) -> None:
    """Обработчик команды Абонемент."""
    user_id: str = str(message_from.from_id)
    command, number = get_command_number(message_from.md_text)
    
    values = bot._google_table.search_abonement(number)
    if values == -1:
        message = 'Такого абонемента не существует, либо его срок действия закончился 😰'
    else:
        end_date_value = values[0]
        balance_value = int(values[1])
        last_digit = balance_value % 10

        if last_digit == 1 and balance_value != 11:
            balance_value = f'{balance_value} занятие'
        elif last_digit in (2, 3, 4) and balance_value not in (12, 13, 14):
            balance_value = f'{balance_value} занятия'
        else:
            balance_value = f'{balance_value} занятий'
        message = f'🗓 Ваш абонемент заканчивается {end_date_value}\n💃 У Вас осталось {balance_value}'
    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@dp.message_handler(filters.Regexp(regexp=r"(((Б|б)от))"))
async def bot_commands_handler(message_from: types.Message) -> None:
    """Обработчик команды Бот."""
    user_id: str = str(message_from.from_id)

    message = (
        f"🤖 КОМАНДЫ ДЛЯ ЧАТ-БОТА: 🤖\n\n"
        f"❗ Бот ❗\n"
        f"-- все доступные команды чат-бота 📣\n\n"
        f"❗ Абонемент *** ❗\n"
        f"-- (*** - № абонемента) информация о Вашем абонементе (дата окончания и количество оставшихся занятий) 🔖\n\n"
        f"❗ Как добраться ❗\n"
        f"-- наш адрес, карта и инструкция, как нас найти 🗺\n\n"
        f"❗ Цены ❗\n"
        f"-- цены на занятия и программа лояльности 💰\n\n"
        f"❗ Расписание ❗\n"
        f"-- расписание занятий 📆\n\n"
        f"Если у Вас иной вопрос, то напишите и вам ответит администратор 👤 @melnikovvv"
    )
    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@dp.message_handler(filters.Regexp(regexp=r"(((Ц|ц)ены))"))
async def prices_handler(message_from: types.Message) -> None:
    """Обработчик команды Цены."""
    user_id: str = str(message_from.from_id)

    message = 'https://vk.com/wall-208780733_645'
    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@dp.message_handler(filters.Regexp(regexp=r"(((Р|р)асписание))"))
async def schedule_kids_handler(message_from: types.Message) -> None:
    """Обработчик команды Расписание."""
    user_id: str = str(message_from.from_id)
    
    message = "https://vk.com/wall-208780733_643"
    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return

@dp.message_handler(filters.Regexp(regexp=r"(((К|к)ак)(\s)(добраться))"))
async def how_to_get_handler(message_from: types.Message) -> None:
    """Обработчик команды Как добраться."""
    user_id: str = str(message_from.from_id)
    
    message = "https://vk.com/wall-208780733_279"
    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{send_error.message}: Trouble id: {user_id}")
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

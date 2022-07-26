import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from loguru import logger
from googlesheet_table import GoogleTable

logger.add(
    config.settings["LOG_FILE"],
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip",
)

class FreakTelegramBot(Bot):
    def __init__(
        self,
        token,
        parse_mode,
        google_table=None,
    ):
        super().__init__(token, parse_mode=parse_mode)
        self._google_table: GoogleTable = google_table

bot: FreakTelegramBot = FreakTelegramBot(
    token=config.settings["TOKEN"],
    parse_mode=types.ParseMode.HTML,
    google_table=GoogleTable("creds.json",
                             "https://docs.google.com/spreadsheets/d/111"),
)
dp = Dispatcher(bot)


@dp.message_handler(filters.Regexp(regexp=r"(((А|а)бонемент)(\s)(\d+))"))
async def abonement_handler(message_from: types.Message) -> None:
  user_id: str = str(message_from.from_id)
  text_msg: str = message_from.md_text.strip(" @#")
  command, number = text_msg.lower().split(' ')
  print(f"Вход: команда '{command}', опция '{number}'")

  values = bot._google_table.search_abonement(number)

  if values == -1:
    message = f'Такого абонемента не существует, либо его срок действия закончился 😰'
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
  user_id: str = str(message_from.from_id)
  text_msg: str = message_from.md_text.strip(" @#")
  command = text_msg.lower()
  print(f"Вход: команда '{command}'")

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
    f"❗ Расписание дети ❗\n"
    f"-- расписание детских занятий (от 5 до 13 лет) 📆\n\n"
    f"❗ Расписание взрослые ❗\n"
    f"-- расписание взрослых занятий (13+) 📆\n\n"
    f"Если у Вас иной вопрос, то напишите и вам ответит администратор 👤"
  )

  try:
      await message_from.reply(message)
  except Exception as send_error:
      logger.debug(f"{send_error.message}: Trouble id: {user_id}")
      return

@dp.message_handler(filters.Regexp(regexp=r"(((Ц|ц)ены))"))
async def prices_handler(message_from: types.Message) -> None:
  user_id: str = str(message_from.from_id)
  text_msg: str = message_from.md_text.strip(" @#")
  command = text_msg.lower()
  print(f"Вход: команда '{command}'")

  try:
      with open('res/price.jpg', 'rb') as photo:
        await bot.send_photo(user_id, photo)
  except Exception as send_error:
      logger.debug(f"{send_error.message}: Trouble id: {user_id}")
      return
    
@dp.message_handler(filters.Regexp(regexp=r"(((Р|р)асписание)(\s)(взрослые))"))
async def schedule_adults_handler(message_from: types.Message) -> None:
  user_id: str = str(message_from.from_id)
  text_msg: str = message_from.md_text.strip(" @#")
  command = text_msg.lower()
  print(f"Вход: команда '{command}'")

  try:
    with open('res/timetable.jpg', 'rb') as photo:
        await bot.send_photo(user_id, photo)
  except Exception as send_error:
    logger.debug(f"{send_error.message}: Trouble id: {user_id}")
    return
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

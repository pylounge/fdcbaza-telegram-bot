def get_command_number(message) -> tuple:
    """Очищает и парсит сообщение."""
    text_msg: str = message.strip(" @#")
    command, number = text_msg.lower().split(' ')
    return (command, number)

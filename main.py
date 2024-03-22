import requests
import json
import logging
import time

from bd.create_db import create_categories, create_cities, create_data
from bd.input_db import inp_into_data_pars
from config.config import Config, load_config
from parsers.yandexparser import YandexPars

# Иницилиализируем логер
logger = logging.getLogger(__name__)

# Площадка Город Сфера ТипКлиента Кол-воСтрок
# Кол-во отзывов от %
# Рейтинг от % до %

def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска приложения
    logger.info('Starting pars_app')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Создаем бд и нужные таблицы
    create_categories(config.db.database, config.db.db_user, config.db.db_password, config.db.db_host)
    create_cities(config.db.database, config.db.db_user, config.db.db_password, config.db.db_host)
    create_data(config.db.database, config.db.db_user, config.db.db_password, config.db.db_host)

    # Пример входных данных
    city = 'Видное'
    category = 'Аптеки'
    # парсер яндекс карт
    inp_into_data_pars(YandexPars(city, category), config.db.database, config.db.db_user, config.db.db_password, config.db.db_host)




if __name__ == '__main__':
    main()
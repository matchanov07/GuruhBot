from aiogram import Dispatcher

from loader import dp
from .is_admin import AdminFilter
from .private import IsPrivate
from .groups import IsGroup


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)
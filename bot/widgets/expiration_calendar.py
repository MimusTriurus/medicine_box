from abc import ABC
from calendar import monthcalendar
from datetime import date
from time import mktime
from typing import List, Callable, Union, Awaitable, TypedDict

from aiogram.types import InlineKeyboardButton, CallbackQuery

from aiogram_dialog.context.events import ChatEvent
from aiogram_dialog.manager.protocols import DialogManager, ManagedDialogProto
from aiogram_dialog.widgets.kbd import Keyboard, ManagedCalendarAdapter
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor, \
    ensure_event_processor

from constants import EN, LANG, START_DATA
from localization.localization_keys import localizers, ID_TXT_SELECT_YEAR, ID_TXT_YEAR, en
from localization.string_builder import make_month_title

OnDateSelected = Callable[[ChatEvent, "ManagedCalendarAdapter", DialogManager, date], Awaitable]

# Constants for managing widget rendering scope
SCOPE_DAYS = "SCOPE_DAYS"
SCOPE_MONTHS = "SCOPE_MONTHS"
SCOPE_YEARS = "SCOPE_YEARS"

# Constants for scrolling months
MONTH_NEXT = "+"
MONTH_PREV = "-"

# Constants for prefixing month and year values
PREFIX_MONTH = "MONTH"
PREFIX_YEAR = "YEAR"

MONTHS_NUMBERS = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]


class CalendarData(TypedDict):
    current_scope: str
    current_offset: str


class ExpirationCalendar(Keyboard, ABC):
    def __init__(
            self,
            id: str,
            on_click: Union[OnDateSelected, WidgetEventProcessor, None] = None,
            when: Union[str, Callable] = None
    ):
        super().__init__(id, when)
        self.on_click = ensure_event_processor(on_click)
        self.current_lang = EN

    async def _render_keyboard(
            self,
            data,
            manager: DialogManager
    ) -> List[List[InlineKeyboardButton]]:
        offset = self.get_offset(manager)
        self.current_lang = data[START_DATA][LANG] if data[START_DATA] else EN
        current_scope = self.get_scope(manager)

        if current_scope == SCOPE_YEARS:
            return self.years_kbd(offset)
        elif current_scope == SCOPE_MONTHS:
            return self.months_kbd(offset)

    async def _process_item_callback(
            self, c: CallbackQuery,
            data: str,
            dialog: ManagedDialogProto,
            manager: DialogManager,
    ) -> bool:
        current_offset = self.get_offset(manager)

        if data in [SCOPE_MONTHS, SCOPE_YEARS]:
            self.set_scope(data, manager)

        elif data.startswith(PREFIX_YEAR):
            data = int(data[len(PREFIX_YEAR):])
            new_offset = date(data, 1, 1)
            self.set_scope(SCOPE_MONTHS, manager)
            self.set_offset(new_offset, manager)

        elif data.startswith(PREFIX_MONTH):
            data = int(data[len(PREFIX_MONTH):])
            new_offset = date(current_offset.year, data, 1)
            self.set_offset(new_offset, manager)
            await self.on_click.process_event(
                c, self.managed(manager), manager,
                new_offset,
            )
        return True

    def years_kbd(self, offset) -> List[List[InlineKeyboardButton]]:
        years = []
        for n in range(offset.year, offset.year + 6, 3):
            year_row = []
            for year in range(n, n + 3):
                year_row.append(InlineKeyboardButton(
                    text=str(year),
                    callback_data=self._item_callback_data(
                        f"{localizers.get(self.current_lang, en).gettext(PREFIX_YEAR)}{year}"
                    )
                ))
            years.append(year_row)
        # return years
        return [
            [
                InlineKeyboardButton(
                    text=localizers.get(self.current_lang, en).gettext(ID_TXT_SELECT_YEAR),
                    callback_data=self._item_callback_data(SCOPE_MONTHS),
                ),
            ],
            *years
        ]

    def months_kbd(self, offset) -> List[List[InlineKeyboardButton]]:
        header_year = offset.strftime(f"{localizers.get(self.current_lang, en).gettext(ID_TXT_YEAR)} %Y")
        months = []
        for n in MONTHS_NUMBERS:
            season = []
            for month in n:
                month_text = make_month_title(month, self.current_lang)
                season.append(InlineKeyboardButton(
                    text=month_text,
                    callback_data=self._item_callback_data(f"{PREFIX_MONTH}{month}"))
                )
            months.append(season)
        return [
            [
                InlineKeyboardButton(
                    text=header_year,
                    callback_data=self._item_callback_data(SCOPE_YEARS),
                ),
            ],
            *months
        ]

    def days_kbd(self, offset) -> List[List[InlineKeyboardButton]]:
        header_week = offset.strftime("%B %Y")
        weekheader = [
            InlineKeyboardButton(text=dayname, callback_data=" ")
            for dayname in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ]
        days = []
        for week in monthcalendar(offset.year, offset.month):
            week_row = []
            for day in week:
                if day == 0:
                    week_row.append(InlineKeyboardButton(
                        text=" ",
                        callback_data=" ",
                    ))
                else:
                    raw_date = int(mktime(date(offset.year, offset.month, day).timetuple()))
                    week_row.append(InlineKeyboardButton(
                        text=str(day),
                        callback_data=self._item_callback_data(raw_date),
                    ))
            days.append(week_row)
        return [
            [
                InlineKeyboardButton(
                    text=header_week,
                    callback_data=self._item_callback_data(SCOPE_MONTHS),
                ),
            ],
            weekheader,
            *days,
            [
                InlineKeyboardButton(
                    text="Prev month",
                    callback_data=self._item_callback_data(MONTH_PREV),
                ),
                InlineKeyboardButton(
                    text="Zoom out",
                    callback_data=self._item_callback_data(SCOPE_MONTHS),
                ),
                InlineKeyboardButton(
                    text="Next month",
                    callback_data=self._item_callback_data(MONTH_NEXT),
                ),
            ],
        ]

    def get_scope(self, manager: DialogManager) -> str:
        calendar_data: CalendarData = self.get_widget_data(manager, {})
        current_scope = calendar_data.get("current_scope")
        return current_scope or SCOPE_YEARS

    def get_offset(self, manager: DialogManager) -> date:
        calendar_data: CalendarData = self.get_widget_data(manager, {})
        current_offset = calendar_data.get("current_offset")
        if current_offset is None:
            return date.today()
        return date.fromisoformat(current_offset)

    def set_offset(self, new_offset: date, manager: DialogManager) -> None:
        data = self.get_widget_data(manager, {})
        data["current_offset"] = new_offset.isoformat()

    def set_scope(self, new_scope: str, manager: DialogManager) -> None:
        data = self.get_widget_data(manager, {})
        data["current_scope"] = new_scope

    def managed(self, manager: DialogManager):
        return ManagedCalendarAdapter(self, manager)

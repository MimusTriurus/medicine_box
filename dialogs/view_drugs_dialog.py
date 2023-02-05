from aiogram_dialog import Dialog, Window

from constants import TABLE_HEIGHT
from localization.string_builder import make_actual_drugs_table_title, \
    make_del_actual_drugs_table_title, make_expired_drugs_table_title
from states.state_drugs import FSMViewDrugs, FSMDelDrugs, FSMExpiredDrugs
from widgets.drugs_table import DrugsTable
from widgets.localized_text import LocalizedText

view_actual_drugs_table = DrugsTable(*[], id='view_actual_drugs_table', width=1, height=TABLE_HEIGHT)
del_actual_drugs_table = DrugsTable(*[], id='del_actual_drugs_table', width=1, height=TABLE_HEIGHT)

expired_drugs_table = DrugsTable(*[], id='view_expired_drugs_table', width=1, height=TABLE_HEIGHT)


view_actual_drugs_dialog = Dialog(
    Window(
        LocalizedText(make_actual_drugs_table_title),
        view_actual_drugs_table,
        state=FSMViewDrugs.drugs
    )
)


del_actual_drugs_dialog = Dialog(
    Window(
        LocalizedText(make_del_actual_drugs_table_title),
        del_actual_drugs_table,
        state=FSMDelDrugs.drugs
    )
)


view_expired_drugs_dialog = Dialog(
    Window(
        LocalizedText(make_expired_drugs_table_title),
        expired_drugs_table,
        state=FSMExpiredDrugs.drugs
    )
)

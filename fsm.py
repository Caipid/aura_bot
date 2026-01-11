from aiogram.fsm.state import State, StatesGroup


class FSM_state(StatesGroup):
    fill_university = State()  # Состояние ожидания ввода возраста
    fill_group = State()  # Состояние ожидания выбора пола
    change_university = State()
    change_group = State()
    custom_data = State()
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


add_workout_bt = KeyboardButton("Add workout")
del_workout_bt = KeyboardButton("Delete workout")
#set_notif_bt = KeyboardButton("Set notification")
#stop_notif_bt = KeyboardButton("Stop notification")
see_workouts_bt = KeyboardButton("See my workouts")
main_markup = ReplyKeyboardMarkup(resize_keyboard = True).row(add_workout_bt, del_workout_bt).add(see_workouts_bt)

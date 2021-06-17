import logging
import config
#import keyboards as kb
import aiohttp
import asyncio
import json

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, Command
from states.add_work import AddWorkout


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=config.TOKEN)


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI am a bot that will help you monitor your workouts.")
    user = (message.from_user.id, message.from_user.username)
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://localhost:8000/add_user/", json = user) as response:

            print("Status:", response.status)

            html = await response.text()
            print(html)
            await message.answer(html)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):

	await message.answer("/start - start bot.\n/help - get help with bot commands.")


@dp.message_handler(Text(equals = ["Add workout"]), state = None)
async def add_workout(message: types.Message):
    await message.answer("Enter workout name")

    await AddWorkout.Q1.set()


@dp.message_handler(state=AddWorkout.Q1)
async def answer_q1(message: types.Message, state:FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)

    await message.answer("Enter workout date")
    await AddWorkout.next()


@dp.message_handler(state=AddWorkout.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2 = answer)

    await message.answer("Enter workout time")
    await AddWorkout.next()


@dp.message_handler(state=AddWorkout.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3 = answer)

    await message.answer("Enter all exercises and number of repetitions comma separated (Like 'exercise' - 'number',)")
    await AddWorkout.next()


@dp.message_handler(state=AddWorkout.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    answer = message.text
    exercises_dict = dict(i.split('-') for i in answer.split(','))
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = data.get("answer3")
    work = {'workout':{
    'name':answer1,
    'date':answer2,
    'time':answer3,
    'user':str(message.from_user.id)
    }, 'exercises':
    exercises_dict,}
    print (work)
    async with aiohttp.ClientSession() as session:
        wname = 'asd'
        async with session.post(f"http://localhost:8000/add_workout/", json = work) as response:

            print("Status:", response.status)

            html = await response.text()
            print(html)
            await message.answer(html)
    await state.finish()


@dp.message_handler(Text(equals = ["Delete workout"]))
async def echo(message: types.Message):

    await message.answer("Choose workout")


@dp.message_handler(Text(equals = ["See my workouts"]))
async def echo(message: types.Message):

    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8000/see_workouts/?u_id={message.from_user.id}") as response:

            print("Status:", response.status)

            html = await response.text()
            html = json.loads(html)
            for w in html:
                my_string = ''
                my_string += w['workout']['name']+ '\n' + w['workout']['date'] + '\n' + w['workout']['time'] + '\n'
                for ex in w['exercises']:
                    my_string += ex['name'] + ' - ' + ex['number'] + '\n'
                await message.answer(my_string)


@dp.message_handler()
async def echo(message: types.Message):

    await message.answer("Sorry, I don't understand you")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
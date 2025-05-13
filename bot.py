import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

answers = {1: '43', 2: ['0,25', '0.25'], 3: '155', 4: ['5.2', '5,2'], 5: '120', 6: ['0.9409', '0,9409']}
wrong_answers = []


async def start(update, context):
    await update.message.reply_text(
        "Привет. Вы проходите опрос по математике.\n"
        "Ответом может быть целое число или десятичная дробь.\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "1. Решите уравнение: 6х - 19 = 5х +24")

    return 1


async def first_response(update, context):
    if update.message.text.strip() == answers[1]:
        context.user_data["points"] = 1
    else:
        context.user_data["points"] = 0
        wrong_answers.append(1)
    await update.message.reply_text(
        "2. Игральную кость бросают дважды. Найдите вероятность того,\n"
        "что сумма двух выпавших чисел равна 6 или 9.")
    return 2


async def second_response(update, context):
    if update.message.text in answers[2]:
        context.user_data["points"] += 1
    else:
        wrong_answers.append(2)
    await update.message.reply_text(
        "3. Камень бросают в глубокое ущелье. При этом в первую секунду он пролетает 11 метров,\n"
        "а в каждую следующую секунду на 10 метров больше,\n"
        " чем в предыдущую, до тех пор, пока не достигнет дна ущелья.\n"
        "Сколько метров пролетит камень за первые пять секунд?")
    return 3


async def third_response(update, context):
    if update.message.text == answers[3]:
        context.user_data["points"] += 1
    else:
        wrong_answers.append(3)
    await update.message.reply_text(
        f"4. Решите уравнение: 2,7х + 18 = 44 - 2,3х")
    return 4


async def fourth_response(update, context):
    if update.message.text in answers[4]:
        context.user_data["points"] += 1
    else:
        wrong_answers.append(4)
    await update.message.reply_text(
        "5. Одна из сторон параллелограмма равна 12, а опущенная на нее\n"
        "высота равна 10. Найдите площадь параллелограмма.")
    return 5


async def fifth_response(update, context):
    if update.message.text == answers[5]:
        context.user_data["points"] += 1
    else:
        wrong_answers.append(5)
    await update.message.reply_text(
        "6. Фирма «Вспышка» изготавливает фонарики. Вероятность того, что случайно\n"
        "выбранный фонарик из партии бракованный, равна 0,03. Какова вероятность\n"
        "того, что два случайно выбранных из одной партии фонарика окажутся\n"
        "небракованными?")
    return 6


async def six_response(update, context):
    if update.message.text in answers[6]:
        context.user_data["points"] += 1
    else:
        wrong_answers.append(6)
    text = f"Количество правильных ответов: {context.user_data['points']}\n"
    if wrong_answers:
        text += f"Номера вопросов, ответы на которые вы дали" \
                f" неправильно: {', '.join([str(x) for x in wrong_answers])}"
    else:
        text += f"Все верно, вы молодец!"
    await update.message.reply_text(text, "Чтобы пройти опрос заново, отправьте команду /start.")
    context.user_data.clear()
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token('8047098949:AAGn39cJQf3EgCxz22Ekmjeco9tNYoLOv-E').build()

    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, fifth_response)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, six_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()

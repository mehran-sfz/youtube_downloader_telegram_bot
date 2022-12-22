import telegram
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler
import logging, os, shutil
from telegram import ReplyKeyboardRemove

# find port of server 
PORT = int(os.environ.get('PORT',5000))
token = ''

# show log of each part of code
logging.basicConfig(filename='bin\log\log.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

START_CO, GET_WORD, GET_NUMBER, GET_URL = range(1, 5)

def start(update,context):
    user = update.message.from_user
    user_data = context.user_data

    remake_folder(str(user.id))

    user_data['number_of_photo'] = 0
    user_data['id_account'] = user.username

    text = 'تگ اکانت خود را وارد کنید برای مثال: UPV988V2'
    update.message.reply_text(text, reply_markup = markup.markup_back)
    logger.info(' user %s start to entery a account %s' , user.username , update.message.text)
    return(TAG)

def tag(update,context):
    user = update.message.from_user
    user_data = context.user_data
    tag_account = update.message.text
    if tag_account == 'بازگشت' :
        with open('bin/stickers/AnimatedSticker.tgs', 'rb') as file:
            update.message.reply_sticker(file, reply_markup = markup.markup_welcome)
            return(START_CO)

    # remove # on tag the stupid user forgot to remove that
    tag_account = tag_account.replace('#','')
    tag_account = tag_account.replace(' ','')
    tag_account= tag_account.strip()
    category = 'tag_account'

    check = supercell_api.Get_user_info_clashofclans(tag_account)
    if check.get('reason') == 'notFound':   
        text = 'این تگ اکانت معتبر نمیباشد لطفا تگ درست اکانت را وارد کنید.'
        update.message.reply_text(text, reply_markup = markup.markup_back)
        return(TAG)

    elif check.get('reason') == 'accessDenied.invalidIp':
        text = f'توکن کلش آف کلنز از کار افتاده'
        bot.send_message(chat_id = tokens.channel_id, text = text)
        text = 'مشکلی در ارتباط با سرور سوپرسل پیش آمده است لطفا مدتی بعد دوباره اقدام به ثبت آگهی کنید'
        update.message.reply_text(text, reply_markup = markup.markup_welcome)
        return(START_CO)
    logger.info(' tag of %s account is %s' , user.username , update.message.text)
    user_data[category] = tag_account

    reply_sentens ='''🔶 تصاویر اکانت خود را وارد کنید و بعد بر روی گزینه "⬅️ رفتن به مرحله بعدی کلیک کنید.. \n\n🔴 توجه داشته باشید افزودن حداقل 4 تصویر الزامی میباشد 🔴'''

    update.message.reply_text(reply_sentens, reply_markup = markup.markup_photo)
    return(PHOTO)






def stop_conversation(update,context):
    user = update.message.from_user
    logger.info('User %s end the convertations ', user.username)
    update.message.reply_text('برای شروع دوباره روی /start کلیک کن' , reply_markup = ReplyKeyboardRemove())

    return(ConversationHandler.END)

def cancle(update,context):
    user = update.message.from_user
    logger.info('User %s cancled the convertations ', user.username)
    update.message.reply_text('بدرود امیدوارم باز هم به ربات ما سر بزنی.' , reply_markup = ReplyKeyboardRemove())

    return(ConversationHandler.END)

def timeout(update, context):
    user = update.message.from_user
    try:
        shutil.rmtree(str(user.id))
    except:
        print('chat is all new ')

    update.message.reply_text('به دلیل تکمیل نکردن و استفاده نکردن از ربات به مدت طولانی چت بسته شد. برای شروع دوباره روی /start کلیک کنید.',reply_markup = ReplyKeyboardRemove())

def error(update,context):
    logger.warning('Update %s coused error %s ',update,context.error)
    print(update,context.error)















# info of bot and chanal
bot = telegram.Bot(token=token)

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # ---------------------------------------------->>>> User Bot Handler
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],


        states = states,

        fallbacks = [CommandHandler('cancle', start), CommandHandler('start', start), MessageHandler(Filters.regex('^exit$'), start_fun.stop_conversation),
                    MessageHandler(Filters.regex('^🏠 home$'), start_fun.start_co)],

        conversation_timeout = 10000, 
    )


    dp.add_handler(conv_handler)

    dp.add_error_handler(start_fun.error)

    print('trying to connect to telegram api ...')

    updater.start_polling()
    

    # updater.start_webhook(listen='0.0.0.0',port=PORT,url_path=TOKEN)
    # updater.bot.set_webhook('https://clashbazar.com/' + TOKEN )

    print('connected to telegram api : 200 ')

    updater.idle()



def remake_folder(folder_name):

    folder_name = f'users/{folder_name}'        

    if os.path.exists(folder_name):
        for filename in os.listdir(folder_name):
            file_path = os.path.join(folder_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    else:
        os.mkdir(folder_name)



if __name__ == '__main__':

    same = [CommandHandler('cancle', cancle), MessageHandler(Filters.regex('^exit$'), stop_conversation), MessageHandler(Filters.regex('^🏠 home$'), start)]


    states = {
            START_CO : [CommandHandler('start', start),
                        MessageHandler(Filters.regex('^🛡 ثبت آگهی Clash of Clans$'), start_to_get_info_coc),
                        MessageHandler(Filters.regex('^⚔️ ثبت آگهی Clash Royale$'), start_to_get_info_cr),
                        ],

            START_0 : [CommandHandler('start', start),
                        MessageHandler(Filters.regex('^🟢 ورود$'), start_login),
                        MessageHandler(Filters.regex('^🟡 ثبت نام$'), signin),
                        ],

            GET_PHONE_NUMBER : same + [CommandHandler('start', start), MessageHandler(Filters.text , get_phone_number)],

    print(len(states))



    main()


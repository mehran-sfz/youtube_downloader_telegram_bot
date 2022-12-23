import telegram
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler
import os, shutil
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from youtube import *

# find port of server 
PORT = int(os.environ.get('PORT',5000))
token = ''

START_CO, GET_WORD, GET_NUMBER,GET_CHANNEL_URL, GET_URL, CONFIRMATION = range(1, 7)

reply_keyboeard_start = [['Download entire channel'],['Download with searching word'], ['Download one video'], ['exit']]
markup_start = ReplyKeyboardMarkup(reply_keyboeard_start,resize_keyboard=True, one_time_keyboard=True)

reply_keyboeard_back = [['back', '🏠 home', 'exit']]
markup_back = ReplyKeyboardMarkup(reply_keyboeard_back,resize_keyboard=True, one_time_keyboard=True)

reply_keyboeard_confirmation = [['I confirm'], ['🏠 home', 'exit']]
markup_confirmation = ReplyKeyboardMarkup(reply_keyboeard_confirmation,resize_keyboard=True, one_time_keyboard=True)



def start(update,context):
    update.message.reply_text('Choose between options : ', reply_markup = markup_start)
    return(START_CO)

def start_co(update, context):
    user = update.message.from_user
    text = update.message.text

    remake_folder(str(user.id))

    if text == 'Download entire channel':
        update.message.reply_text('Enter URL of one video on channel you want to download all of that videos.', reply_markup = markup_back)
        return(GET_CHANNEL_URL)

    elif text == 'Download with searching word':
        update.message.reply_text('Enter word you want to search.', reply_markup = markup_back)
        return(GET_WORD)

    elif text == 'Download one video':
        update.message.reply_text('Enter link of that video.', reply_markup = markup_back)
        return(GET_URL)

def get_channel_url(update,context):
    user_data = context.user_data
    text = update.message.text

    if text == 'back':
        update.message.reply_text('Choose ...', reply_markup = markup_start)
        return(START_CO)

    id = find_channel_id(text)
    if id :
        list_of_urls = get_videos_from_channel(id)
        if list_of_urls:
            user_data['list_of_urls'] = list_of_urls
            update.message.reply_text(f'there is {len(list_of_urls)} videos on this channel', reply_markup = markup_start)
            return(CONFIRMATION)

def get_word_for_search(update, context):
    user_data = context.user_data
    text = update.message.text

    if text == 'back':
        update.message.reply_text('Choose ...', reply_markup = markup_start)
        return(START_CO)
    
    user_data['search_word'] = text
    update.message.reply_text('How many videos you wanna download ?', reply_markup = markup_back)
    return(GET_NUMBER)

def get_number_of_videos(update, context):
    user_data = context.user_data
    number = update.message.text

    if number == 'back':
        update.message.reply_text('Enter word you want to search.', reply_markup = markup_back)
        return(GET_WORD)
    
    try:
        number = int(number)
    except:
        update.message.reply_text('Wrong input', reply_markup = markup_back)
        return(GET_NUMBER) 

    list_of_urls = find_videos_with_search(user_data['search_word'], number)
    if list_of_urls:
        user_data['list_of_urls'] = list_of_urls
    
    text = f'''
    Search word : {user_data['search_word']}
    Number of videos : {number}
    If it is ok pleas confirm.'''
    update.message.reply_text(text, reply_markup = markup_confirmation)
    return(CONFIRMATION)

def one_video_download(update, context):
    user_data = context.user_data
    user = update.message.from_user
    text = update.message.text
    url = text.strip()

    if text == 'back':
        update.message.reply_text('Choose ...', reply_markup = markup_start)
        return(START_CO)

    try:
        status = Download(url, user.id)
        print(status)
        if status:
            update.message.reply_video(video = status, reply_markup = markup_start)
            os.chmod(f"rm {status}")
            return(START_CO)
        else:
            update.message.reply_text(f"could not download the video {url}", reply_markup = markup_start)
            return(START_CO)
    except:
        update.message.reply_text(f"could not download {url}", reply_markup = markup_start)
        return(START_CO)
        

def confirmation(update, context):
    user_data = context.user_data
    user = update.message.from_user
    text = update.message.text

    if text != 'I confirm':
        update.message.reply_text('Choose ...', reply_markup = markup_start)
        return(START_CO)

    for url in user_data['list_of_urls']:
        try:
            status = Download(url['url'], user.id)
            if status:
                update.message.reply_video(video = status, caption = url['title'])
                os.chmod(f"rm {status}")
            else:
                update.message.reply_text(f"could not download the video {url['url']}")
                continue
        except:
            update.message.reply_text(f"could not download {url['url']}", reply_markup = ReplyKeyboardRemove())
            continue

    update.message.reply_text('finish proces', reply_markup = markup_start)
    return(START_CO)


def stop_conversation(update,context):
    update.message.reply_text('goodbye' , reply_markup = ReplyKeyboardRemove())
    return(ConversationHandler.END)

def cancle(update,context):
    update.message.reply_text('bye' , reply_markup = ReplyKeyboardRemove())
    return(ConversationHandler.END)

def timeout(update, context):
    user = update.message.from_user
    try:
        remake_folder(str(user.id))
    except:
        pass

    update.message.reply_text('the time is out.',reply_markup = ReplyKeyboardRemove())

def error(update,context):
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

        fallbacks = [CommandHandler('cancle', start), CommandHandler('start', start), MessageHandler(Filters.regex('^exit$'), stop_conversation),
                    MessageHandler(Filters.regex('^🏠 home$'), start_co)],

        conversation_timeout = 50000, 
    )


    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    print('trying to connect to telegram api ...')

    updater.start_polling()
    

    # updater.start_webhook(listen='0.0.0.0',port=PORT,url_path=TOKEN)
    # updater.bot.set_webhook('https://clashbazar.com/' + TOKEN )

    print('connected to telegram api : 200 ')

    updater.idle()



def remake_folder(folder_name):

    folder_name = f'Downloads/{folder_name}'        

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
                        MessageHandler(Filters.regex('^Download entire channel$'), start_co),
                        MessageHandler(Filters.regex('^Download with searching word$'), start_co),
                        MessageHandler(Filters.regex('^Download one video$'), start_co),
                        ],
            
            GET_WORD : same + [CommandHandler('start', start), MessageHandler(Filters.text , get_word_for_search)],

            GET_NUMBER : same + [CommandHandler('start', start), MessageHandler(Filters.text , get_number_of_videos)],

            GET_CHANNEL_URL : same + [CommandHandler('start', start), MessageHandler(Filters.text , get_channel_url)],

            GET_URL : same + [CommandHandler('start', start), MessageHandler(Filters.text , one_video_download)],

            CONFIRMATION : [CommandHandler('start', start), MessageHandler(Filters.regex('^I confirm$'), confirmation)],

            

    }

    main()
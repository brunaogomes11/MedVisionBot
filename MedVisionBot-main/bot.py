import telebot
import requests
import datetime
import pytz
import tensorflow as tf


BOT_TOKEN = '7226074783:AAHTIgmSos0eqKFDU5DYF2MEiYGa_rTQmMs'

classes_index = {
    'BrainTumorClassifier': [1, 'Ressonância Magnética do Cérebro'],
    'ChestXRayClassifier': [3, 'Raio-X do Pulmão'],
    'KneeMRIClassifier': [4, 'Ressonância Magnética do Joelho'],
    'KneeXRayClassifier': [5, 'Raio-X do Joelho'],
    'EyeClassifier': [7, 'Oftalmoscopia'],
    'UniversalClassifier': [8, 'Classificador Universal']
}

bot = telebot.TeleBot(BOT_TOKEN)

# Carregar os modelos treinados
model_paths = {
    'BrainTumorClassifier': 'models/BrainTumorClassifier/best.pth',
    'ChestXRayClassifier': 'models/ChestXRayClassifier/checkpoint.pth',
    'KneeXRayClassifier': 'models/KneeMRIClassifier/rmibest.h5',
    'EyeClassifier': 'models/EyeClassifier/best.pth',
    'UniversalClassifier': 'models/UniversalClassifier/proto_5.pth.tar'
}

loaded_models = {}

for classifier, model_path in model_paths.items():
    loaded_models[classifier] = tf.keras.models.load_model(model_path)

@bot.message_handler(commands=['caption'])
def caption(message):
    user_id = message.chat.id
    
    msg1 = 'Em caso de erros do classificador geral você pode reenviar a imagem com uma legenda escrito o tipo correto da imagem.'
    msg2 = '''
- BrainTumorClassifier
- ChestXRayClassifier
- KneeMRIClassifier
- KneeXRayClassifier
- EyeClassifier
- UniversalClassifier
    '''
    bot.send_message(user_id, msg1)
    bot.send_message(user_id, msg2)

def classify_image(image, classifier):
    # Aqui você faria a classificação da imagem usando o modelo correspondente
    # Substitua este bloco de código pela lógica de classificação com o modelo carregado
    pass

@bot.message_handler(content_types=['photo'])
def classifierImage(message):
    existCaption = True if message.caption is not None else False

    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        caption = message.caption

        if caption:
            caption = caption.replace(' ', '').strip()
            isCaptionValid = caption in classes_index.keys()

            if not isCaptionValid:
                caption_error_msg = f'A legenda {caption} não é válida. Consulte /caption e digite corretamente.'
                bot.reply_to(message, caption_error_msg)
                return
            
            classifier = caption
        else:
            # Se não houver legenda, usar o classificador universal
            classifier = 'UniversalClassifier'

        classification_result = classify_image(downloaded_file, classifier)

        # Aqui você processaria o resultado da classificação e retornaria a mensagem correspondente
        # Substitua este bloco de código pela lógica de processamento do resultado da classificação

    except Exception as e:
        print(str(e))
        bot.reply_to(message, 'Foi detectada uma imagem não médica ou que não é suportada pelo sistema.\nEnvie uma imagem válida') 


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    msg1 = f"Olá, {message.from_user.first_name} seja bem-vindo ao MedVision!\n" 
    msg2 = "Para fazer diagnósticos basta enviar sua imagem.\n"
    msg3 = "Em caso de dúvidas digite: /help\n"
        
    bot.send_message(user_id, msg1)
    bot.send_message(user_id, msg2)
    bot.send_message(user_id, msg3)
    

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.chat.id

    comandos = 'Comandos\n' + \
               '/info - Mostra informações sobre o projeto\n'  + \
               '/team - Mostra meios de contato à equipe\n' + \
               '/types - Mostra os tipos de imagens suportadas\n' + \
               '/cg - Mostra informações sobre o classificador geral\n' + \
               '/caption - Ajusta erros do classificador geral'
    
    bot.send_message(user_id, comandos)


@bot.message_handler(commands=['cg'])
def cg(message):
    user_id = message.chat.id

    msg_title = 'Classificador Geral'
    msg = 'O classificador geral é usado antes de passar a imagem'
    # Adicione aqui a descrição sobre o classificador geral

    bot.send_message(user_id, msg_title)
    bot.send_message(user_id, msg)


@bot.message_handler
def handle_message(message):
    bot.reply_to(message, "Comando não reconhecido. Digite /help para ver os comandos disponíveis.")


bot.polling()

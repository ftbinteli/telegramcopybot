from src.check_message import *
from src.logger import *
from src.command_handler import *
from src.help_message import help_message
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime
from logging import info, error
import os

info("Bot is starting...")
print("Starting...")

try:
    telethon_client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    telethon_client.start()
    info("Telethon client connection have been set successfully.")
except Exception as e:
    print(f"ERROR - {e}")
    error(f"Telethon client connection error. Error: {e}")
    exit(1)

try:
    bot_client_telethon = TelegramClient("bot", APP_ID, API_HASH)
    bot_client_telethon.start(bot_token=TELEGRAM_BOT_TOKEN)
    info("Telethon bot client connection have been set successfully.")
except Exception as e:
    print(f"ERROR - {e}")
    error(f"Telethon bot client connection error. Error: {e}")
    exit(1)


@telethon_client.on(events.NewMessage(outgoing=outgoing, incoming=True, chats=FROM))
async def sender_bH(event):
    # Define globals
    global FROM
    global TO
    global SEPARATE_CHANNELS
    global outgoing
    global BLACKLIST_WORDS
    global CHANGE_FOR
    global THROW_IF_MESSAGE_CONSIST_WORDS
    global FORWARD_IF_MESSAGE_CONSIST_WORDS
    global THROW_IF_MESSAGE_CONSIST_URL
    global DELETE_URL_FROM_MESSAGE

    sender = await event.get_sender()
    sender_id = sender.id
    userMessage = str(event.message.message)
    userMessage = checkMgs(
        userMessage, THROW_IF_MESSAGE_CONSIST_URL, DELETE_URL_FROM_MESSAGE)

    # Log variables
    message_id = event.message.id
    message_date = event.message.date
    message_source_id = sender_id

    info(m(message_id=message_id, message_date=str(message_date), message_source_id=message_source_id,
         is_message_forwarded=False, log_message="Message Captured.", message_forward_date="N/A", message_target_id="N/A"))

    if userMessage != "THROW_THIS_MESSAGE":
        event.message.message = userMessage

        for i in range(len(TO)):
            if SEPARATE_CHANNELS:
                sendTo = find_index_of_channel(sender_id, FROM)

                try:
                    await telethon_client.send_message(entity=TO[sendTo], message=event.message)
                    info(m(message_id=message_id, message_date=str(message_date), message_source_id=message_source_id, is_message_forwarded=True,
                         log_message="Message forwarded", message_forward_date=str(datetime.utcnow()), message_target_id=TO[sendTo]))
                except Exception as e:
                    error(m(message_id=message_id, message_date=str(message_date), message_source_id=message_source_id,
                          is_message_forwarded=False, log_message=str(e), message_forward_date="N/A", message_target_id=TO[sendTo]))
                    # print(e)

                break
            else:
                try:
                    await telethon_client.send_message(entity=TO[i], message=event.message)
                    info(m(message_id=message_id, message_date=str(message_date), message_source_id=message_source_id, is_message_forwarded=True,
                         log_message="Message forwarded", message_forward_date=str(datetime.utcnow()), message_target_id=TO[i]))
                except Exception as e:
                    error(m(message_id=message_id, message_date=str(message_date), message_source_id=message_source_id,
                          is_message_forwarded=False, log_message=str(e), message_forward_date="N/A", message_target_id=TO[i]))
                    # print(e)
    else:
        info(m(message_id=message_id, message_date=str(message_date), message_source_id=message_source_id, is_message_forwarded=False,
             log_message="Message is not forwarded. content of the message is blacklisted.", message_forward_date="N/A", message_target_id="N/A"))
        # print("Message thrown.")


@telethon_client.on(events.NewMessage(pattern=r"\/", chats=BOT_CHAT_ID, incoming=False))
async def handler(event):
    # Define globals
    global FROM
    global TO
    global SEPARATE_CHANNELS
    global outgoing
    global BLACKLIST_WORDS
    global CHANGE_FOR
    global THROW_IF_MESSAGE_CONSIST_WORDS
    global FORWARD_IF_MESSAGE_CONSIST_WORDS
    global THROW_IF_MESSAGE_CONSIST_URL
    global DELETE_URL_FROM_MESSAGE

    userMessage = str(event.message.message)
    userId = event.sender_id
    message_id = event.message.id
    message_date = event.message.date

    msg_to_send = ""

    info(m(bot_interaction=True, message_id=message_id, message_date=str(
        message_date), command_sent=userMessage, log_message="Message Captured."))

    # Handle start and help command
    if userMessage == "/start" or userMessage == "/help":
        try:
            await bot_client_telethon.send_message(userId, help_message.source_control())
            await bot_client_telethon.send_message(userId, help_message.message_control())
            info(m(bot_interaction=True, message_id=message_id, message_date=str(
                message_date), command_sent=userMessage, log_message="Help message sent to user."))
            userMessage = ""
        except Exception as e:
            error(m(bot_interaction=True, command_sent=userMessage,
                  log_message=f"Help message could not sent to user. Error: {e}"))

    # Handle view_source_channels
    elif userMessage == "/view_source_channels":
        viewChannels = "Source channels/chats/groups are:" + \
            display_entries(FROM)

        msg_to_send = viewChannels

    # Handle add_source_channel
    elif userMessage.startswith("/add_source_channel"):
        userCommand = find_command(userMessage, 20)
        spaceInStr = space_pos(userMessage, 19)

        if spaceInStr == None or userCommand == None:
            msg_to_send = "Please send the command to bot in the following format\n\n/add_source_channel CHAT_ID_OF_NEW_SOURCE"
        else:
            if userCommand.find(".") == -1 and userCommand.find(",") == -1 and userCommand.isdigit():
                if int(userCommand) in FROM:
                    msg_to_send = f"Source {userCommand} is already in your source list."
                else:
                    try:
                        FROM.append(int(userCommand))
                        info(m(log_message="Source list updated."))
                    except Exception as e:
                        error(
                            m(log_message=f"Source list couldnt updated. Error: {e}"))

                    msg_to_send = f"New source {userCommand} is added into your source list.\n\nYour new source list is:\n{display_entries(FROM)}"

                    if SEPARATE_CHANNELS:
                        SEPARATE_CHANNELS = False
                        msg_to_send += "\n\nYour seperate_channels setting is changed to 0. If you need this feature please set it for 1 again with /seperate_channels command."
            else:
                msg_to_send = "Please be sure that you are trying to add Chat ID into source list. Chat ID is is not the username. Please add one source in one message."

    # Handle delete_source_channel
    elif userMessage.startswith("/delete_source_channel"):
        userCommand = find_command(userMessage, 23)
        spaceInStr = space_pos(userMessage, 22)

        if spaceInStr == None or userCommand == None:
            viewChannels = "Source channels/chats/groups are:" +\
                display_entries(FROM) +\
                "\n\nIf you would like to delete any of the source channels, please send the command to bot in the following format\n\n/delete_source_channel CHAT_ID_TO_DELETE"
            msg_to_send = viewChannels
        else:
            if userCommand.find(".") == -1 and userCommand.find(",") == -1 and userCommand.isdigit():
                if int(userCommand) in FROM:
                    try:
                        FROM.remove(int(userCommand))
                        info(m(log_message="Source list updated."))
                    except Exception as e:
                        error(
                            m(log_message=f"Source list couldnt updated. Error: {e}"))

                    msg_to_send = f"Source {userCommand} is deleted from your source list.\n\nYour new source list is:\n{display_entries(FROM)}"

                    if SEPARATE_CHANNELS == True:
                        SEPARATE_CHANNELS = False
                        msg_to_send += "\n\nYour seperate_channels setting is changed to 0. If you need this feature please set it for 1 again with /seperate_channels command."
                else:
                    msg_to_send = f"Source {userCommand} can not be found in your source list."
            else:
                msg_to_send = "Please be sure that you are trying to delete Chat ID from the source list. Chat ID is is not the username. Please delete one source in one message."

    # Handle view_target_channels
    elif userMessage == "/view_target_channels":
        viewChannels = "Target channels/chats/groups are:" + \
            display_entries(TO)

        msg_to_send = viewChannels

    # Handle add_target_channel
    elif userMessage.startswith("/add_target_channel"):
        userCommand = find_command(userMessage, 20)
        spaceInStr = space_pos(userMessage, 19)

        if spaceInStr == None or userCommand == None:
            msg_to_send = "Please send the command to bot in the following format\n\n/add_target_channel CHAT_ID_OF_NEW_TARGET"
        else:
            if userCommand.find(".") == -1 and userCommand.find(",") == -1 and userCommand.isdigit():
                if int(userCommand) in TO:
                    msg_to_send = f"Source {userCommand} is already in your target list."
                else:
                    try:
                        TO.append(int(userCommand))
                        info(m(log_message="Target list updated."))
                    except Exception as e:
                        error(
                            m(log_message=f"Source list couldnt updated. Error: {e}"))

                    msg_to_send = f"New target {userCommand} is added into your target list.\n\nYour new target list is:\n{display_entries(TO)}"

                    if SEPARATE_CHANNELS == True:
                        SEPARATE_CHANNELS = False
                        msg_to_send += "\n\nYour seperate_channels setting is changed to 0. If you need this feature please set it for 1 again with /seperate_channels command."
            else:
                msg_to_send = "Please be sure that you are trying to add Chat ID into target list. Chat ID is is not the username. Please add one target in one message."

    # Handle delete_target_channel
    elif userMessage.startswith("/delete_target_channel"):
        userCommand = find_command(userMessage, 23)
        spaceInStr = space_pos(userMessage, 22)

        if spaceInStr == None or userCommand == None:
            viewChannels = "Target channels/chats/groups are:" +\
                display_entries(TO) +\
                "\n\nIf you would like to delete any of the target channels, please send the command to bot in the following format\n\n/delete_target_channel CHAT_ID_TO_DELETE"

            msg_to_send = viewChannels
        else:
            if userCommand.find(".") == -1 and userCommand.find(",") == -1 and userCommand.isdigit():
                if int(userCommand) in TO:
                    try:
                        TO.remove(int(userCommand))
                        info(m(log_message="Target list updated."))
                    except Exception as e:
                        error(
                            m(log_message=f"Source list couldnt updated. Error: {e}"))

                    msg_to_send = f"Target {userCommand} is deleted from your target list.\n\nYour new target list is:\n{display_entries(TO)}"

                    if SEPARATE_CHANNELS == True:
                        SEPARATE_CHANNELS = False
                        msg_to_send += "\n\nYour seperate_channels setting is changed to 0. If you need this feature please set it for 1 again with /seperate_channels command."
                else:
                    msg_to_send = f'Target {userCommand} can not be found in your target list.'
            else:
                msg_to_send = "Please be sure that you are trying to delete Chat ID from the target list. Chat ID is is not the username. Please delete one source in one message."

    # Handle seperate_channels
    elif userMessage.startswith("/seperate_channels"):
        userCommand = find_command(userMessage, 19)
        spaceInStr = space_pos(userMessage, 18)

        if spaceInStr == None or userCommand == None:
            seperate_channels_info = f"Current value of seperate_channels is: {SEPARATE_CHANNELS}\n" +\
                "\nIf you would like to forward messages respectively (1st source to 1st target, 2nd source to 2nd target, 3rd source to 3rd target ...) set this value to 1.\n" + \
                "\nIf you would like to forward from all source channels to all target channels set this value to 0.\n" +\
                "\nIMPORTANT NOTE: In order to use this function you should have the same number of source and target channels. " +\
                "If you dont have the same number of source and target channels this value will automatically be set for 0.\n" +\
                "\nSource channels/chats/groups are:" + display_entries(FROM) +\
                "\n\nTarget channels/chats/groups are:" + display_entries(TO) +\
                "\n\nIf you would like to change this setting, please send the command to bot in the following format\n\n/seperate_channels VALUE"

            msg_to_send = seperate_channels_info

        else:
            if userCommand == "1" and len(FROM) == len(TO):
                SEPARATE_CHANNELS = True
                info(m(log_message="SEPARATE_CHANNELS updated."))
                msg_to_send = "seperate_channels is set to 1."
            elif userCommand == "1" and len(FROM) != len(TO):
                SEPARATE_CHANNELS = False
                info(m(log_message="SEPARATE_CHANNELS could not updated."))
                msg_to_send = "seperate_channels could not set to 1, number of sources and targets are not the same. Current value of seperate_channels is: 0."
            elif userCommand == "0":
                SEPARATE_CHANNELS = False
                info(m(log_message="SEPARATE_CHANNELS updated."))
                msg_to_send = "seperate_channels is set to 0"
            else:
                msg_to_send = "Unknown command."

    # Handle forward_from_your_channel
    elif userMessage.startswith("/forward_from_your_channel"):
        userCommand = find_command(userMessage, 27)
        spaceInStr = space_pos(userMessage, 26)

        if spaceInStr == None or userCommand == None:
            forward_from_your_channel_info = f"Current value of seperate_channels is: {outgoing}\n" +\
                "\nIf any of the source channels/groups are yours, you should set this value to 1.\n" +\
                "\nIf you dont forward from your own channel this can be set for 0.\n" +\
                "\nIf you would like to change this setting, please send the command to bot in the following format\n\n/forward_from_your_channel VALUE"
            msg_to_send = forward_from_your_channel_info
        else:
            if userCommand == "1":
                outgoing = 1
                info(m(log_message="forward_from_your_channel updated."))
                msg_to_send = "forward_from_your_channel is set to 1."
            elif userCommand == "0":
                outgoing = 0
                info(m(log_message="forward_from_your_channel updated."))
                msg_to_send = "forward_from_your_channel is set to 0."
            else:
                msg_to_send = "Unknown command."

    # Handle view_blacklist_words
    elif userMessage == "/view_blacklist_words":
        msg_to_send = "Blacklist words are:" + \
            display_entries(BLACKLIST_WORDS)

    # Handle add_blacklist_words
    elif userMessage.startswith("/add_blacklist_word"):
        userCommand = find_command(userMessage, 20)
        spaceInStr = space_pos(userMessage, 19)

        if spaceInStr == None or userCommand == None:
            msg_to_send = "Please send the command to bot in the following format\n\n/add_blacklist_word WORD_TO_BLACKLIST"
        else:
            if userCommand in BLACKLIST_WORDS:
                msg_to_send = f'{userCommand} is already in your blacklist list.'
            else:
                try:
                    BLACKLIST_WORDS.append(userCommand)
                    info(m(log_message="blacklist list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"Blacklist list couldnt updated. Error: {e}"))

                msg_to_send = f"New word {userCommand} is added into your blacklist list.\n\nYour new blacklist list is:\n{display_entries(BLACKLIST_WORDS)}"

    # Handle delete_blacklist_words
    elif userMessage.startswith("/delete_blacklist_word"):
        userCommand = find_command(userMessage, 23)
        spaceInStr = space_pos(userMessage, 22)

        if spaceInStr == None or userCommand == None:
            blacklist_words_list = "Blacklist words are:" +\
                display_entries(BLACKLIST_WORDS) +\
                "\n\nIf you would like to delete any of the blacklist word, please send the command to bot in the following format\n\n/delete_blacklist_word WORD_TO_REMOVE_FROM_BLACKLIST"
            msg_to_send = blacklist_words_list
        else:
            if userCommand in BLACKLIST_WORDS:
                try:
                    BLACKLIST_WORDS.remove(userCommand)
                    info(m(log_message="blacklist list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"Blacklist list couldnt updated. Error: {e}"))

                msg_to_send = f"{userCommand} is deleted from your blacklist list.\n\nYour new blacklist list is:\n{display_entries(BLACKLIST_WORDS)}"

            else:
                msg_to_send = f'{userCommand} can not be found in your blacklist list.'

    # Handle view_change_for
    elif userMessage == "/view_change_for":
        msg_to_send = "Blacklist words will be changed for:" + \
            display_entries(CHANGE_FOR)

    # Handle add_change_for
    elif userMessage.startswith("/add_change_for"):
        userCommand = find_command(userMessage, 16)
        spaceInStr = space_pos(userMessage, 15)

        if spaceInStr == None or userCommand == None:
            msg_to_send = 'Please send the command to bot in the following format\n\n/add_change_for WORD_TO_CHANGE_FOR'
        else:
            if userCommand in CHANGE_FOR:
                msg_to_send = f'{userCommand} is already in your change for list.'
            else:
                try:
                    CHANGE_FOR.append(userCommand)
                    info(m(log_message="CHANGE_FOR list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"CHANGE_FOR list couldnt updated. Error: {e}"))

                msg_to_send = f"New word {userCommand} is added into your change for list.\n\nYour new change for list is:\n{display_entries(CHANGE_FOR)}"

    # Handle delete_change_for
    elif userMessage.startswith("/delete_change_for"):
        userCommand = find_command(userMessage, 19)
        spaceInStr = space_pos(userMessage, 18)

        if spaceInStr == None or userCommand == None:
            change_for_words_list = "Change for words are:" +\
                display_entries(CHANGE_FOR) +\
                "\n\nIf you would like to delete any of the change for words, please send the command to bot in the following format\n\n/delete_change_for WORDS_TO_REMOVE_FROM_CHANGE_FOR"
            msg_to_send = change_for_words_list
        else:
            if userCommand in CHANGE_FOR:
                try:
                    CHANGE_FOR.remove(userCommand)
                    info(m(log_message="CHANGE_FOR list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"CHANGE_FOR list couldnt updated. Error: {e}"))

                msg_to_send = f"{userCommand} is deleted from your change for list.\n\nYour new change for list is:\n{display_entries(CHANGE_FOR)}"

            else:
                msg_to_send = f'{userCommand} can not be found in your change for list.'

    # Handle view_throw_if_message_consist_words
    elif userMessage == "/view_throw_if_message_consist_words":
        msg_to_send = "The message will not be forwarded if the message has following words:" + \
            display_entries(THROW_IF_MESSAGE_CONSIST_WORDS)

    # Handle add_throw_if_message_consist_words
    elif userMessage.startswith("/add_throw_if_message_consist_words"):
        userCommand = find_command(userMessage, 36)
        spaceInStr = space_pos(userMessage, 35)

        if spaceInStr == None or userCommand == None:
            msg_to_send = "Please send the command to bot in the following format\n\n/add_throw_if_message_consist_words WORD_TO_THROW_LIST"
        else:
            if userCommand in THROW_IF_MESSAGE_CONSIST_WORDS:
                msg_to_send = f'{userCommand} is already in your throw list.'
            else:
                try:
                    THROW_IF_MESSAGE_CONSIST_WORDS.append(userCommand)
                    info(m(log_message="THROW_IF_MESSAGE_CONSIST_WORDS list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"THROW_IF_MESSAGE_CONSIST_WORDS list couldnt updated. Error: {e}"))

                msg_to_send = f"New word {userCommand} is added into your throwlist.\n\nYour new throw list is:\n{display_entries(THROW_IF_MESSAGE_CONSIST_WORDS)}"

    # Handle delete_throw_if_message_consist_words
    elif userMessage.startswith("/delete_throw_if_message_consist_words"):
        userCommand = find_command(userMessage, 38)
        spaceInStr = space_pos(userMessage, 37)

        if spaceInStr == None or userCommand == None:
            throw_list_words_list = "Change for words are:" +\
                display_entries(THROW_IF_MESSAGE_CONSIST_WORDS) +\
                "\n\nIf you would like to delete any of the throw words, please send the command to bot in the following format\n\n/delete_throw_if_message_consist_words WORD_TO_REMOVE_FROM_THROW_LIST"
            msg_to_send = throw_if_message_consist_url_info
        else:
            if userCommand in THROW_IF_MESSAGE_CONSIST_WORDS:
                try:
                    THROW_IF_MESSAGE_CONSIST_WORDS.remove(userCommand)
                    info(m(log_message="THROW_IF_MESSAGE_CONSIST_WORDS list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"THROW_IF_MESSAGE_CONSIST_WORDS list couldnt updated. Error: {e}"))

                msg_to_send = f"{userCommand} is deleted from your throw list.\n\nYour new throw list is:\n{display_entries(THROW_IF_MESSAGE_CONSIST_WORDS)}"

            else:
                msg_to_send = f'{userCommand} can not be found in your throw list.'

    # Handle view_whitelist_words
    elif userMessage == "/view_whitelist_words":
        msg_to_send = "The message will be forwarded if the message has following words:" + \
            display_entries(FORWARD_IF_MESSAGE_CONSIST_WORDS)

    # Handle add_whitelist_words
    elif userMessage.startswith("/add_whitelist_words"):
        userCommand = find_command(userMessage, 21)
        spaceInStr = space_pos(userMessage, 20)

        if spaceInStr == None or userCommand == None:
            msg_to_send = "Please send the command to bot in the following format\n\n/add_whitelist_words WORD_TO_WHITELIST"
        else:
            if userCommand in FORWARD_IF_MESSAGE_CONSIST_WORDS:
                msg_to_send = f'{userCommand} is already in your whitelist list.'
            else:
                try:
                    FORWARD_IF_MESSAGE_CONSIST_WORDS.append(userCommand)
                    info(m(log_message="FORWARD_IF_MESSAGE_CONSIST_WORDS list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"FORWARD_IF_MESSAGE_CONSIST_WORDS list couldnt updated. Error: {e}"))

                msg_to_send = f"New word {userCommand} is added into your whitelist.\n\nYour new whitelist is:\n{display_entries(FORWARD_IF_MESSAGE_CONSIST_WORDS)}"

    # Handle delete_whitelist_words
    elif userMessage.startswith("/delete_whitelist_words"):
        userCommand = find_command(userMessage, 24)
        spaceInStr = space_pos(userMessage, 23)

        if spaceInStr == None or userCommand == None:
            whitelist_list = "Whitelist words are:" +\
                display_entries(FORWARD_IF_MESSAGE_CONSIST_WORDS) +\
                "\n\nIf you would like to delete any of the whitelist words, please send the command to bot in the following format\n\n/delete_whitelist_words WORD_TO_REMOVE_FROM_WHITELIST"
            msg_to_send = whitelist_list
        else:
            if userCommand in FORWARD_IF_MESSAGE_CONSIST_WORDS:
                try:
                    FORWARD_IF_MESSAGE_CONSIST_WORDS.remove(userCommand)
                    info(m(log_message="FORWARD_IF_MESSAGE_CONSIST_WORDS list updated."))
                except Exception as e:
                    error(
                        m(log_message=f"FORWARD_IF_MESSAGE_CONSIST_WORDS list couldnt updated. Error: {e}"))

                msg_to_send = f"{userCommand} is deleted from your whitelist list.\n\nYour new whitelist list is:\n{display_entries(FORWARD_IF_MESSAGE_CONSIST_WORDS)}"

            else:
                msg_to_send = f'{userCommand} can not be found in your whitelist list.'

    # Handle throw_if_message_consist_url
    elif userMessage.startswith("/throw_if_message_consist_url"):
        userCommand = find_command(userMessage, 30)
        spaceInStr = space_pos(userMessage, 29)

        if spaceInStr == None or userCommand == None:
            throw_if_message_consist_url_info = f"Current value of throw_if_message_consist_url is: {THROW_IF_MESSAGE_CONSIST_URL}\n" +\
                "\nIf you dont want to forward messages which consust any URL from any of the source channels/groups, you should set this value to 1.\n" +\
                "\nIf this is not needed, this value can be set for 0.\n" +\
                "\nIf you would like to change this setting, please send the command to bot in the following format\n\n/throw_if_message_consist_url VALUE"
            msg_to_send = throw_if_message_consist_url_info
        else:
            if userCommand == "1":
                THROW_IF_MESSAGE_CONSIST_URL = True
                info(m(log_message="THROW_IF_MESSAGE_CONSIST_URL updated."))
                msg_to_send = "throw_if_message_consist_url is set to 1."
            elif userCommand == "0":
                THROW_IF_MESSAGE_CONSIST_URL = False
                msg_to_send = "throw_if_message_consist_url is set to 0."
                info(m(log_message="THROW_IF_MESSAGE_CONSIST_URL updated."))
            else:
                msg_to_send = "Unknown command."

    # Handle delete_url_from_message
    elif userMessage.startswith("/delete_url_from_message"):
        userCommand = find_command(userMessage, 25)
        spaceInStr = space_pos(userMessage, 24)

        if spaceInStr == None or userCommand == None:
            delete_url_from_message_info = f"Current value of delete_url_from_message is: {DELETE_URL_FROM_MESSAGE}\n" +\
                "\nIf you would like to delete URLs from messages before forwarding which consust any URL from any of the source channels/groups, you should set this value to 1.\n" +\
                "\nIf this is not needed, this value can be set for 0.\n" +\
                "\nIf you would like to change this setting, please send the command to bot in the following format\n\n/delete_url_from_message VALUE"
            msg_to_send = delete_url_from_message_info
        else:
            if userCommand == "1":
                DELETE_URL_FROM_MESSAGE = True
                info(m(log_message="DELETE_URL_FROM_MESSAGE updated."))
                msg_to_send = "delete_url_from_message is set to 1."
            elif userCommand == "0":
                DELETE_URL_FROM_MESSAGE = True
                info(m(log_message="DELETE_URL_FROM_MESSAGE updated."))
                msg_to_send = "delete_url_from_message is set to 0."
            else:
                msg_to_send = "Unknown command."

    # handle download_log
    elif userMessage.startswith("/download_log"):
        list_of_files = os.listdir('log')
        for file in list_of_files:
            try:
                await bot_client_telethon.send_file(userId, f"log/{file}")
                info(m(bot_interaction=True, message_id=message_id, message_date=str(
                    message_date), command_sent=userMessage, log_message="Log file downloaded."))
            except Exception as e:
                error(m(bot_interaction=True, command_sent=userMessage,
                      log_message=f"Error: {e}"))

        userMessage = ""

    # Handle save settings
    elif userMessage.startswith("/save_settings"):
        with open(".env", "w") as f:
            f.write(f"APP_ID={APP_ID}\n")
            f.write(f"API_HASH={API_HASH}\n")
            f.write(f"SESSION={SESSION}\n")
            f.write(f"TELEGRAM_BOT_TOKEN={TELEGRAM_BOT_TOKEN}\n")
            f.write(f"BOT_CHAT_ID={BOT_CHAT_ID}\n")
            f.write(f"FROM_CHANNEL={';'.join(str(i) for i in FROM)}\n")
            f.write(f"TO_CHANNEL={';'.join(str(i) for i in TO)}\n")
            f.write(f"SEPARATE_CHANNELS={SEPARATE_CHANNELS}\n")
            f.write(f"FORWARD_FROM_YOUR_OWN_CHANNELS={outgoing}\n")
            f.write(
                f"BLACKLIST_WORDS={';'.join(str(i) for i in BLACKLIST_WORDS)}\n")
            f.write(f"CHANGE_FOR={';'.join(str(i) for i in CHANGE_FOR)}\n")
            f.write(
                f"THROW_IF_MESSAGE_CONSIST_WORDS={THROW_IF_MESSAGE_CONSIST_URL}\n")
            f.write(
                f"FORWARD_IF_MESSAGE_CONSIST_WORDS={';'.join(str(i) for i in FORWARD_IF_MESSAGE_CONSIST_WORDS)}\n")
            f.write(
                f"THROW_IF_MESSAGE_CONSIST_URL={THROW_IF_MESSAGE_CONSIST_URL}\n")
            f.write(f"DELETE_URL_FROM_MESSAGE={DELETE_URL_FROM_MESSAGE}\n")

        msg_to_send = "Settings saved into .env file."

    # Handle other messages
    else:
        msg_to_send = "Unknown Command."

    if (userMessage != "/start" or userMessage != "/help" or userMessage.startswith("/download_log") == False) and userMessage != "":
        print(userMessage)
        print("here")
        try:
            await bot_client_telethon.send_message(userId, msg_to_send)
            info(m(bot_interaction=True, message_id=message_id, message_date=str(
                message_date), command_sent=userMessage, log_message=msg_to_send))
        except Exception as e:
            error(m(bot_interaction=True, command_sent=userMessage,
                  log_message=f"Error: {e}"))

print("Bot started.")
info("Bot started.")
telethon_client.run_until_disconnected()

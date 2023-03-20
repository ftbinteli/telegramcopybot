class help_message():
    def source_control():
        source_control_msg = """
--------------------
/view_source_channels - Display the list of source Chat IDs where the messages forwarding from.
--------------------
/add_source_channel - Add new source channel/group/chat to your source list. 

/add_source_channel CHAT_ID_OF_NEW_SOURCE
--------------------
/delete_source_channel - Remove source channel/group/chat from your source list. 

/delete_source_channel CHAT_ID_TO_DELETE
--------------------
/view_target_channels - Display the list of target Chat IDs where the messages forwarding to.
--------------------
/add_target_channel - Add new target channel/group/chat to your target list. 

/add_target_channel CHAT_ID_OF_NEW_TARGET
--------------------
/delete_target_channel - Remove target channel/group/chat from your target list. 

/delete_target_channel CHAT_ID_TO_REMOVE
--------------------
/seperate_channels - If you would like to forward messages respectively (1st source to 1st target, 2nd source to 2nd target, 3rd source to 3rd target ...) set this value to 1. If you would like to forward from all source channels to all target channels set this value to 0.

IMPORTANT NOTE: In order to use this function you should have the same number of source and target channels.
If you dont have the same number of source and target channels this value will automatically be set for 0

/seperate_channels VALUE
--------------------
/forward_from_your_channel - If any of the source channels/groups are yours, you should set this value to 1. If you dont forward from your own channel this can be set for 0.

/forward_from_your_channel VALUE
--------------------
"""

        return source_control_msg
    
    def message_control():
        message_control_msg = """
--------------------
/view_blacklist_words - Display the blacklist words you are using. Blacklist words will be deleted and/or changed as your CHANGE_FOR settings.
--------------------
/add_blacklist_word - Add new blacklist word to your blacklist list. 

/add_blacklist_word WORD_TO_BLACKLIST
--------------------
/delete_blacklist_word - Remowe blacklist word from your blacklist list. 

/delete_blacklist_word WORD_TO_REMOVE_FROM_BLACKLIST
--------------------
/view_change_for - Display the change for words you are using. Blacklist words will be deleted and/or changed as your CHANGE_FOR settings.

There are 3 ways to use CHANGE_FOR
    i.    If CHANGE_FOR list will be empty, bot will delete all the BLACKLIST_WORDS from the message and forward.
    ii.   If you will enter one variable for CHANGE_FOR, bot will change all the BLACKLIST_WORDS from the messages as CHANGE_FOR and forward.
    iii.  If you will enter CHANGE_FOR for each BLACKLIST_WORDS, bot will change all the BLACKLIST_WORDS respectively with the CHANGE_FOR from the message and forward. (If you will not enter CHANGE_FOR for each BLACKLIST_WORDS, bot will just delete the BLACKLIST_WORDS.)
--------------------
/add_change_for - Add new change for word to your change for list. 

/add_change_for WORD_TO_CHANGE_FOR
--------------------
/delete_change_for - Remowe change for word from your change for list. 

/delete_change_for WORDS_TO_REMOVE_FROM_CHANGE_FOR
--------------------
/view_throw_if_message_consist_words - Display the list of the word(s) in the throw message list. If the message has any of those words the message will not be forwarded.
--------------------
/add_throw_if_message_consist_words - Add new word to your throw list. 

/add_throw_if_message_consist_words WORD_TO_THROW_LIST
--------------------
/delete_throw_if_message_consist_words - Remove word from your throw list. 

/delete_throw_if_message_consist_words WORD_TO_REMOVE_FROM_THROW_LIST
--------------------
/view_whitelist_words - Display the list of the word(s) in the whitelist list. If the message has any of those words, the message will be forwarded. If the message will not have any of the whitelist words, message will not be forwarded.
--------------------
/add_whitelist_words - Add new word to your whitelist list. 

/add_whitelist_words WORD_TO_WHITELIST
--------------------
/delete_whitelist_words - Remowe word from your whitelist list. 

/delete_whitelist_words WORD_TO_REMOVE_FROM_WHITELIST
--------------------
/throw_if_message_consist_url - If you dont want to forward messages which consist any URL from any of the source channels/groups, you should set this value to 1. If this is not needed, this value can be set for 0. 

/throw_if_message_consist_url VALUE
--------------------
/delete_url_from_message - If you would like to delete URLs from messages before forwarding which consust any URL from any of the source channels/groups, you should set this value to 1. If this is not needed, this value can be set for 0. 

/delete_url_from_message VALUE
--------------------
"""
        return message_control_msg
def find_command(command_message, command_start_index):
    try:
        msg = command_message[command_start_index:]
    except Exception as e:
        msg = None

    return msg


def space_pos(command_message, space_pos):
    try:
        spaceInStr = command_message[space_pos]
    except:
        spaceInStr = None

    return spaceInStr


def display_entries(entry_to_list):
    entries = ""

    if len(entry_to_list) > 0:
        for i in range(len(entry_to_list)):
            entries += f"\n{i+1}: {entry_to_list[i]}"

        return entries
    else:
        return "\nNot Found"

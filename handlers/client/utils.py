import yaml
import os
from datetime import datetime
from loguru import logger


def read_from_file_db(filename):
    file_path = f"file_database/{filename}.yaml"

    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            yaml.dump({}, file)

    with open(file_path, "r") as f:
        file_data = yaml.safe_load(f)
    return file_data


def write_to_file_db(filename, data):
    file_path = f"file_database/{filename}.yaml"
    with open(file_path, "w", encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)


def get_users_dict():
    with open("file_database/users.yaml", "r") as f:
        users = yaml.safe_load(f)
    return users


def get_author_name(author_username):
    users = get_users_dict()
    for name, username in users.items():
        if username == author_username:
            return name
    return None


# def add_to_give(author, user_data, users, summary_data):
#     amount = round(user_data['amount'] / len(user_data['people']), 2)
#     for user_name in user_data['people']:
#         user_username = users.get(user_name)  # TODO Can be None?
#         if user_username == author:
#             continue
#         summary_data[user_username][author] -= amount
#
#         current_amount = summary_data.get(user_username, 0)
#         summary_data[user_username] = current_amount + amount
#     return summary_data
#
#
# def add_to_take(author, user_data, summary_data):
#     amount = round(user_data['amount'] / len(user_data['people']), 2)
#     current_amount = summary_data.get(author, 0)
#     summary_data[author] = current_amount - amount
#     return summary_data


def save_transaction_to_db(author, user_data):
    users = get_users_dict()
    amount = round(user_data['amount'] / len(user_data['people']), 2)
    for current_name in user_data['people']:
        current_username = users[current_name]  # TODO can be error
        summary_data = read_from_file_db("summary")
        if current_username == author:
            continue

        author_dict = summary_data.get(author, {})
        username_amount = author_dict.get(current_username, 0) + amount
        author_dict[current_username] = username_amount
        summary_data[author] = author_dict

        username_dict = summary_data.get(current_username, {})
        author_amount = username_dict.get(author, 0) - amount
        username_dict[author] = author_amount
        summary_data[current_username] = username_dict

        write_to_file_db("summary", summary_data)
        logger.info("Save data to personal state")


def save_history_db(author, user_data):
    history_data = read_from_file_db("history")

    keys = list(history_data.keys())
    for k in keys:
        if (datetime.now() - k).days > 30:
            del history_data[k]

    history_data[datetime.now()] = {
        "author": author,
        "people": user_data['people'],
        "amount": user_data['amount'],
        "comment": user_data['comment']
    }
    write_to_file_db("history", history_data)
    logger.info("Save data to history")

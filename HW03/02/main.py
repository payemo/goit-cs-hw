import json
import os
from pymongo import MongoClient, errors
from bson import ObjectId

# Підключення до MongoDB
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'root'
MONGO_PASSWORD = 'example'

try:
    client = MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/")
    db = client["cats_db"]
    cats_collection = db["cats"]
except errors.ConnectionFailure as e:
    print(f"Помилка підключення до MongoDB: {e}")
    exit(1)

# Отримання шляху до файлу
curr_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(curr_dir, 'cats_data.json')

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Файл '{file_path}' не знайдено.")


# Завантаження даних із файлу
def load_data_from_file(file_path):
    """
    Завантажує дані про котів із JSON-файлу.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                if '_id' in item:
                    item['_id'] = ObjectId(item['_id'])
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Помилка завантаження даних із файлу: {e}")
        return []


# Ініціалізація колекції
def initialize_cats_collection(file_path):
    """
    Очищає колекцію та ініціалізує її даними з файлу.
    """
    try:
        cats_collection.delete_many({})
        print("Колекцію очищено.")

        data = load_data_from_file(file_path)
        if data:
            result = cats_collection.insert_many(data)
            print(f"Вставлено документів: {len(result.inserted_ids)}")
        else:
            print("Файл даних порожній або не містить записів.")
    except errors.PyMongoError as e:
        print(f"Помилка ініціалізації колекції: {e}")


# Виведення всіх котів
def show_all_cats():
    """
    Виводить усі записи про котів із бази даних.
    """
    try:
        print("Список всіх котів у базі даних:")
        for cat in cats_collection.find():
            print(f"- ID: {cat['_id']}")
            print(f"  Ім'я: {cat['name']}")
            print(f"  Вік: {cat['age']}")
            print(f"  Характеристики: {', '.join(cat['features'])}")
            print("-" * 40)
    except errors.PyMongoError as e:
        print(f"Помилка виведення даних: {e}")


# Знайти кота за ім'ям
def find_cat_by_name():
    """
    Шукає та виводить інформацію про кота за його ім'ям.
    """
    name = input("Введіть ім'я кота для пошуку: ").strip()
    try:
        cat = cats_collection.find_one({'name': name})
        if cat:
            print("Інформація про кота:")
            print(f"- ID: {cat['_id']}")
            print(f"  Ім'я: {cat['name']}")
            print(f"  Вік: {cat['age']}")
            print(f"  Характеристики: {', '.join(cat['features'])}")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений у базі даних.")
    except errors.PyMongoError as e:
        print(f"Помилка пошуку даних: {e}")


# Оновлення віку кота
def update_cat_age():
    """
    Оновлює вік кота за його ім'ям.
    """
    name = input("Введіть ім'я кота, чий вік потрібно оновити: ").strip()
    new_age = input("Введіть новий вік: ").strip()

    if not new_age.isdigit():
        print("Вік повинен бути числом. Спробуйте ще раз.")
        return

    new_age = int(new_age)
    try:
        result = cats_collection.update_one({'name': name}, {'$set': {'age': new_age}})
        if result.matched_count > 0:
            print(f"Вік кота '{name}' успішно оновлено до {new_age}.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений у базі даних.")
    except errors.PyMongoError as e:
        print(f"Помилка оновлення даних: {e}")


# Додавання характеристики
def add_cat_feature():
    """
    Додає нову характеристику до списку `features` кота.
    """
    name = input("Введіть ім'я кота, до якого потрібно додати характеристику: ").strip()
    new_feature = input("Введіть нову характеристику: ").strip()

    try:
        result = cats_collection.update_one({'name': name}, {'$addToSet': {'features': new_feature}})
        if result.matched_count > 0:
            if result.modified_count > 0:
                print(f"Характеристика '{new_feature}' успішно додана до кота '{name}'.")
            else:
                print(f"Характеристика '{new_feature}' вже існує у списку для кота '{name}'.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений у базі даних.")
    except errors.PyMongoError as e:
        print(f"Помилка оновлення характеристик: {e}")


# Видалення запису за ім'ям
def delete_cat_by_name():
    """
    Видаляє запис про кота за його ім'ям.
    """
    name = input("Введіть ім'я кота для видалення: ").strip()
    try:
        result = cats_collection.delete_one({'name': name})
        if result.deleted_count > 0:
            print(f"Запис про тварину '{name}' успішно видалено.")
        else:
            print(f"Запис про тварину з ім'ям '{name}' не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка видалення: {e}")


# Видалення всіх записів
def delete_all_cats():
    """
    Видаляє всі записи з колекції після підтвердження користувача.
    """
    confirmation = input("Ви дійсно хочете видалити всі записи? (так/ні): ").strip().lower()
    if confirmation == 'так':
        try:
            result = cats_collection.delete_many({})
            print(f"Усі записи успішно видалено. Видалено документів: {result.deleted_count}")
        except errors.PyMongoError as e:
            print(f"Помилка видалення записів: {e}")
    else:
        print("Видалення скасовано.")


# Основна функція
def main():
    """
    Основна функція програми.
    """
    initialize_cats_collection(file_path)

    while True:
        print("\nМеню:")
        print("1. Показати всіх котів")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота")
        print("4. Додати характеристику до кота")
        print("5. Видалити запис за ім'ям тварини")
        print("6. Видалити усі записи")
        print("7. Вийти")

        choice = input("Виберіть опцію (1/2/3/4/5/6/7): ").strip()

        if choice == '1':
            show_all_cats()
        elif choice == '2':
            find_cat_by_name()
        elif choice == '3':
            update_cat_age()
        elif choice == '4':
            add_cat_feature()
        elif choice == '5':
            delete_cat_by_name()
        elif choice == '6':
            delete_all_cats()
        elif choice == '7':
            print('Вихід.')
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == '__main__':
    main()

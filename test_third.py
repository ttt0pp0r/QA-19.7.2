# from api import PetFriends
# from settings import valid_email, valid_password
#
# pf = PetFriends()
#
# def test_api_key_for_valid_user(email=valid_email, password=valid_password):
#     status, result = pf.get_api_key(email, password)
#     assert status == 200
#     assert 'key' in result
#
# def test_get_all_pets_with_valid_key(filter=''):
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     status, result = pf.get_list_of_pets(auth_key, filter)
#     assert status == 200
#     assert len(result['pets']) > 0

from api import PetFriends
from settings import valid_email, valid_password, not_valid_password, not_valid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='кулема', animal_type='курник',
                                     age='3', pet_photo='images/dogg1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/dogg1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

"""
_______________________________________________________________________________________________________________________________________________
"""

"""Задание 19.7.2"""

def test_check_work_logining_with_not_valid_key(email = not_valid_email, password = not_valid_password):
    """1.Проверяем возможность входа на сайт с неверным паролем и логином"""
    status, result= pf.get_api_key(email, password)
    if status == 403:
        assert status == 403
        assert 'key' not in result

def test_check_work_logining_with_not_email(email = not_valid_email, password = valid_password):
    """2.Проверяем возможность входа на сайт с ошибкой в email"""
    status, result= pf.get_api_key(email, password)
    if status == 403:
        assert status == 403
        assert 'key' not in result

def test_check_work_logining_with_not_valid_pass(email = valid_email, password = not_valid_password):
    """3.Проверяем возможность входа на сайт с ошибкой в пароле"""
    status, result= pf.get_api_key(email, password)
    if status == 403:
        assert status == 403
        assert 'key' not in result

def test_add_new_pet_without_name(name=' ', animal_type='собакевич', age='2', pet_photo='images/dogg1.jpg'):
    """4.Проверяем возможность добавления питомца без имени"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)


    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_age(name='бублик', animal_type='пес', age=' ', pet_photo='images/dogg1.jpg'):
    """5.Проверяем возможность добавления питомца без возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)


    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_incorrect_name(name='25@475ЮdW!%', animal_type='', age='3', pet_photo='images/dogg2.jpg'):
    """6.Проверяем возможность добавления питомца с неккоректным указанием имени"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)


    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_info(name=' ', animal_type=' ', age=' ', pet_photo='images/dogg2.jpg'):
    """7.Проверяем возможность добавления питомца только с фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)


    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_all_info(name=' ', animal_type=' ', age=' '):
    """8.Проверяем возможность добавления питомца без указания всей информации"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_incorrect_age(name='Гоги', animal_type='Собакевич', age='-%6g200FDe', pet_photo='images/dogg1.jpg'):
    """9.Проверяем возможность добавления питомца с неккоректным указанием возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_without_incorrect_type(name='Рубенчик', animal_type='$122!246%', age='7', pet_photo='images/dogg1.jpg'):
    """10.Проверяем возможность добавления питомца с некоректным видом животного"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
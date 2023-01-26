# Публикация комиксов

Программа, которая высылает в группу ВК рандомный комикс xkcd.

### Как установить (Пошаговая инструкция)

1. Создайте группу в ВК
2. Создайте приложение ВК (тут > https://vk.com/apps?act=manage)
3. Получите Client ID (https://vk.com/apps?act=manage > Редактировать > Настройки)
4. Получите Access Token используя Client ID (https://oauth.vk.com/authorize?client_id=*ВАШ_CLIENT_ID*&scope=photos,groups,wall&response_type=token)
5. Получите ID вашей группы (здесь > https://regvk.com/id/)
6. Установите зависимости командой
   ```
   pip install -r requirements.txt
   ```
7. Для начала надо создать .env файл в директории программы и поместить туда Access Token и ID группы.

    ```
    ACCESS_TOKEN=*ВАШ ACCESS TOKEN*
    GROUP_ID=*ID ВАШЕЙ ГРУППЫ*
    ```

8. Для запуска скрипта используйте команду 
   ```
   python vk.py
   ```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
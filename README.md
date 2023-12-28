
# Домашнее задание к лекции «Работа с PostgreSQL из Python»
Создайте программу для управления клиентами на Python.

Требуется хранить персональную информацию о клиентах:

* имя,
* фамилия,
* email,
* телефон.

Схема представлена на рисунке ![Database.drawio.png](Database.drawio.png)

Пароль от PostgreSQL вставляем в файл [password.ini](password.ini)

***В функции create_db имеются команды по удалению и созданию таблиц.
При первом запуске необходимо "закоментировать" команды по удалению таблиц.
Иначе будет ошибка, так как таблицы еще не созданы т удалять нечего.***

Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона, например, он не захотел его оставлять.

Вам необходимо разработать структуру БД для хранения информации и несколько функций на Python для управления данными.

1. Функция, создающая структуру БД (таблицы).
2. Функция, позволяющая добавить нового клиента.
3. Функция, позволяющая добавить телефон для существующего клиента.
4. Функция, позволяющая изменить данные о клиенте.
5. Функция, позволяющая удалить телефон для существующего клиента.
6. Функция, позволяющая удалить существующего клиента.
7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
8. Функции выше являются обязательными, но это не значит, что должны быть только они. 
При необходимости можете создавать дополнительные функции и классы.

Также предоставьте код, демонстрирующий работу всех написанных функций.

Результатом работы будет .py файл.

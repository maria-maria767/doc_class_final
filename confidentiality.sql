--
-- Файл сгенерирован с помощью SQLiteStudio v3.2.1 в Ср янв 21 18:07:55 2026
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: access_types
CREATE TABLE access_types (id_access_type INTEGER PRIMARY KEY AUTOINCREMENT, name_access_right VARCHAR (50), description_rights VARCHAR (120));
INSERT INTO access_types (id_access_type, name_access_right, description_rights) VALUES (1, 'Базовый', 'Доступ к общим документам');
INSERT INTO access_types (id_access_type, name_access_right, description_rights) VALUES (2, 'Повышенный', 'Доступ к внутеренним документам');
INSERT INTO access_types (id_access_type, name_access_right, description_rights) VALUES (3, 'Служебный', 'Доступ к документам ограниченного доступа');
INSERT INTO access_types (id_access_type, name_access_right, description_rights) VALUES (4, 'Специальный', 'Доступ к конфиденциальной информации');

-- Таблица: assignment_rights
CREATE TABLE assignment_rights (id_assignment_rights INTEGER PRIMARY KEY AUTOINCREMENT, date_assignment DATE, id_role INTEGER REFERENCES role_users (id_role), id_access_type INTEGER REFERENCES access_types (id_access_type), id_document INTEGER REFERENCES documents (id_document));
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (1, '12.12.2025', 1, 4, 1);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (2, '15.12.2025', 2, 3, 2);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (3, '12.01.2026', 4, 3, 3);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (4, '12.12.2025', 3, 4, 1);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (5, '12.12.2025', 4, 3, 1);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (6, '12.01.2026', 3, 3, 4);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (7, '12.01.2026', 4, 2, 4);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (8, '12.01.2026', 5, 4, 4);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (9, '12.01.2026', 2, 2, 5);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (10, '12.01.2026', 4, 3, 5);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (11, '12.01.2026', 5, 4, 6);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (12, '12.01.2026', 5, 4, 7);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (13, '15.01.2026', 3, 2, 8);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (14, '15.01.2026', 3, 2, 9);
INSERT INTO assignment_rights (id_assignment_rights, date_assignment, id_role, id_access_type, id_document) VALUES (15, '15.01.2026', 3, 2, 10);

-- Таблица: category_documents
CREATE TABLE category_documents (id_category_document INTEGER PRIMARY KEY AUTOINCREMENT, category_document);
INSERT INTO category_documents (id_category_document, category_document) VALUES (1, 'Конфиденциальный');
INSERT INTO category_documents (id_category_document, category_document) VALUES (2, 'Внутренний');
INSERT INTO category_documents (id_category_document, category_document) VALUES (3, 'Публичный');
INSERT INTO category_documents (id_category_document, category_document) VALUES (4, 'Ограниченного доступа');

-- Таблица: correspondents
CREATE TABLE correspondents (id_correspondent INTEGER PRIMARY KEY AUTOINCREMENT, name_correspondent VARCHAR (50), id_type_correspondent INTEGER REFERENCES type_correspondents (id_type_correspondent));
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (1, 'Министерство науки и высшего образования РФ', 1);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (2, 'Министерство просвещения Российской Федерации', 1);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (3, 'ООО "Иваново"', 2);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (4, 'ООО "Куратово"', 2);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (5, 'Вузопедия', 3);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (6, 'Университет "Синергия"', 6);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (7, 'Журнал "Экономика и управление"', 4);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (8, 'Журнал "Российский экономический журнал"', 4);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (9, 'Институт экономики РАН', 4);
INSERT INTO correspondents (id_correspondent, name_correspondent, id_type_correspondent) VALUES (10, 'Внутренние подразделения', 6);

-- Таблица: departments
CREATE TABLE departments (id_department INTEGER PRIMARY KEY AUTOINCREMENT, name_department VARCHAR (150), submission VARCHAR (150));
INSERT INTO departments (id_department, name_department, submission) VALUES (1, 'Методический отдел программ высшего образования', 'Департамент учебно-методической работы');
INSERT INTO departments (id_department, name_department, submission) VALUES (2, 'Методический отдел программ СПО', 'Департамент учебно-методической работы');
INSERT INTO departments (id_department, name_department, submission) VALUES (3, 'Учебный отдел программ ВО и СПО', 'Департамент учебно-методической работы');
INSERT INTO departments (id_department, name_department, submission) VALUES (4, 'Научно-иследовательский отдел и аспирантура', 'Научно-исследовательский центр');
INSERT INTO departments (id_department, name_department, submission) VALUES (5, 'Клиентский отдел', 'Управление по организации приема');
INSERT INTO departments (id_department, name_department, submission) VALUES (6, 'Отдел по приему на обучение', 'Управление по организации приема');
INSERT INTO departments (id_department, name_department, submission) VALUES (7, 'Отедл разработки ПО', 'Департамент информационных технологий');
INSERT INTO departments (id_department, name_department, submission) VALUES (8, 'ИТ-служба технической поддержки', 'Департамент информационных технологий');
INSERT INTO departments (id_department, name_department, submission) VALUES (9, 'Отдел информационной безопасности', 'Департамент информационных технологий');
INSERT INTO departments (id_department, name_department, submission) VALUES (10, 'Бухгалтерия', 'Управление по экономике и финасам');
INSERT INTO departments (id_department, name_department, submission) VALUES (11, 'Отдел труда и заработной платы', 'Управление по экономике и финасам');
INSERT INTO departments (id_department, name_department, submission) VALUES (12, 'Планово-экономический отдел', 'Управление по экономике и финасам');

-- Таблица: documents
CREATE TABLE documents (id_document INTEGER PRIMARY KEY AUTOINCREMENT, name_document VARCHAR (50), text_document VARCHAR (150), size_document INTEGER, link_document VARCHAR (150), id_category_document INTEGER REFERENCES category_documents (id_category_document), id_correspondent INTEGER REFERENCES correspondents (id_correspondent));
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (1, 'Приказ о присвоении ученых званий от 25.12.2025 № 1241/нк', 'Приказ о присвоении ученых званий профессора и доцента и выдаче аттестатов о присвоении ученых званий профессора и доцента от 25.12.2025 № 1241/нк', 128, 'Приказ о присвоении ученых 25.12.2025 № 1241/нк.docx', 3, 1);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (2, 'Приказ Министерства просвещения Российской Федерации от 03.12.2025 № 897', '"Об утверждении Порядка проведения антикоррупционной экспертизы нормативных правовых актов Министерства просвещения Российской Федерации и проектов нормативных правовых актов, разработанных Министерством просвещения Российской Федерации"
(Зарегистрирован 14.01.2026 № 84934)', 312, 'Приказ Министерства просвещения Российской Федерации от 03.12.2025 № 897.docx', 3, 2);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (3, 'Рецензия на аттестационное дело № 123', 'Рецензия на аттестационное дело № 123', NULL, 'Рецензия на аттестационное дело № 123.docx', 4, 6);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (4, 'Инструкция по ТБ 1', 'Перечень инструкций по охране труда. 1 ИОТ № 1', 216, 'Инструкция по ТБ 1.docx', 2, 10);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (5, 'Инструкция по ИБ 1', 'Инструкция с правилами ИБ для сотрудников
(служебная)', 312, 'Инструкция по ИБ 1.docx', 4, 10);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (6, 'Приказ о приеме № 23', 'Приказ о переводе студентов из Синергия на третий курс', 126, 'Приказ о приеме № 23.docx', 4, 6);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (7, 'Приказ о приеме № 24', 'Приказ о переводе студентов из Синергия на второй курс', 128, 'Приказ о приеме № 24.docx', 4, 6);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (8, 'Предложение о сотрудничестве', 'Предложение о сотрудничестве', 128, 'Предложение о сотрудничестве.docx', 4, 6);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (9, 'Инструкция по ТБ 2', 'Перечень инструкций по охране труда. 1 ИОТ № 2', 112, 'Инструкция по ТБ 2.docx', 3, 10);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (10, 'Инструкция по ИБ 2', 'Инструкция с правилами ИБ для сотрудников
(общая)', 112, 'Инструкция по ИБ 2.docx', 3, 10);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (11, 'Смета по ремонту №123', 'Сводные данные по организации ремонта в корпусе 4 на 2025 г', 256, 'Смета по ремонту №123.docx', 1, 3);
INSERT INTO documents (id_document, name_document, text_document, size_document, link_document, id_category_document, id_correspondent) VALUES (13, 'Смета по ремонту №124', 'Сводные данные по организации ремонта в корпусе 5 на 2025 г', 256, 'Смета по ремонту №124.docx', 1, 4);

-- Таблица: employees
CREATE TABLE employees (id_employee INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR (50), login VARCHAR (20), password VARCHAR (20), id_department INTEGER REFERENCES departments (id_department), email VARCHAR (20), id_position INTEGER REFERENCES positions (id_position), id_role INTEGER REFERENCES role_users (id_role));
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (1, 'Корытов Владимир Петрович', 'korutov', '123', 1, 'korutov@belzavod.ru', 1, 2);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (2, 'Забеев Евгений Владимирович', 'zabeev', '12', 2, 'zabeev@belzavod.ru', 1, 3);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (3, 'Готов Игорь Иванович', 'gotov', '12', 3, 'gotov@belzavod.ru', 3, 3);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (4, 'Зотов Александр Алексеевич', 'zotov', '12', 4, 'zotov@belzavod.ru', 4, 4);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (5, 'Хабеев Алексей Алексеевич', 'habeev', '111', 5, 'habarov@belzavod.ru', 5, 4);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (7, 'Занин Константин Петрович', 'zanin', '1', 6, 'zanin@belzavod.ru', 6, 3);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (8, 'Суворов Андрей Констатинович', 'suvorov', '3', 7, 'suvorov@belzavod.ru', 10, 4);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (9, 'Маратов Евгений Евгенивич', 'muratov', '3', 8, 'maraov@belzavod.ru', 9, 5);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (10, 'Куратов Владимир Владимирович', 'kuratov', '123', 9, 'kuratov@belzavod.ru', 9, 5);
INSERT INTO employees (id_employee, name, login, password, id_department, email, id_position, id_role) VALUES (11, 'Жуков Владимир Владимирович', 'dzukov', '1234', 10, 'dzukov@belzavod.ru', 2, 5);

-- Таблица: positions
CREATE TABLE positions (id_position INTEGER PRIMARY KEY AUTOINCREMENT, position VARCHAR (30));
INSERT INTO positions (id_position, position) VALUES (1, 'Методист');
INSERT INTO positions (id_position, position) VALUES (2, 'Бухгалтер');
INSERT INTO positions (id_position, position) VALUES (3, 'Менеджер по работе со студентами');
INSERT INTO positions (id_position, position) VALUES (4, 'Заведующий аспирантурой');
INSERT INTO positions (id_position, position) VALUES (5, 'Специалист по работе с абитуриентами');
INSERT INTO positions (id_position, position) VALUES (6, 'Старший специалист по работе с абитуриентами');
INSERT INTO positions (id_position, position) VALUES (7, 'Начальник участка');
INSERT INTO positions (id_position, position) VALUES (8, 'Главный бухгалтер');
INSERT INTO positions (id_position, position) VALUES (9, 'Инженер-программист');
INSERT INTO positions (id_position, position) VALUES (10, 'Системный администратор');
INSERT INTO positions (id_position, position) VALUES (11, 'Помощник системного администратора');
INSERT INTO positions (id_position, position) VALUES (12, 'Помощник ректора по проеектной работе');
INSERT INTO positions (id_position, position) VALUES (13, 'Руководитель организационно-правового направления');
INSERT INTO positions (id_position, position) VALUES (14, 'Расчетчик');

-- Таблица: role_users
CREATE TABLE role_users (id_role INTEGER PRIMARY KEY AUTOINCREMENT, name_role VARCHAR (20), description_role VARCHAR (120));
INSERT INTO role_users (id_role, name_role, description_role) VALUES (1, 'Владелец информации', 'Определяет категории');
INSERT INTO role_users (id_role, name_role, description_role) VALUES (2, 'Уполномоченный руководитель', 'Допускают к документу, назначают исполнителей');
INSERT INTO role_users (id_role, name_role, description_role) VALUES (3, 'Исполнитель', 'Работают с документом');
INSERT INTO role_users (id_role, name_role, description_role) VALUES (4, 'Ограниченный доступ (чтение)', 'Имеют права на просмотр документа');
INSERT INTO role_users (id_role, name_role, description_role) VALUES (5, 'Ограниченный доступ (копирование, печать)', 'Права на копирование и печать документа');

-- Таблица: type_correspondents
CREATE TABLE type_correspondents (id_type_correspondent INTEGER PRIMARY KEY AUTOINCREMENT, type_correspondent VARCHAR (50));
INSERT INTO type_correspondents (id_type_correspondent, type_correspondent) VALUES (1, 'Государственные органы');
INSERT INTO type_correspondents (id_type_correspondent, type_correspondent) VALUES (2, 'Поставщики ТМЦ и услуг');
INSERT INTO type_correspondents (id_type_correspondent, type_correspondent) VALUES (3, 'Медиа и средства массовой информации');
INSERT INTO type_correspondents (id_type_correspondent, type_correspondent) VALUES (4, 'Партнеры по научной деятельности');
INSERT INTO type_correspondents (id_type_correspondent, type_correspondent) VALUES (5, 'Поставщики услуг');
INSERT INTO type_correspondents (id_type_correspondent, type_correspondent) VALUES (6, 'Партнеры по учебной деятельности');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

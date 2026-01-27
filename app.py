import sqlite3
#from keras.models import load_model
#import tensorflow as tf
from flask import Flask, render_template, redirect, request, flash, request, send_from_directory
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
import pprint
# from docx import Document

app = Flask(__name__)
#===Глобальные переменные
USER_NAME = '111'   # логин пользователя
USER_RIGHTS = 3     # права пользователя


app.config['SECRET_KEY'] = b'my)secret)key'
UPLOAD_FOLDER = 'requests'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#===Получение соединения с БД
def get_db_connection():
    conn = sqlite3.connect('confidentiality.db')
    conn.row_factory = sqlite3.Row
    return conn

#===Стартовая страница
@app.route('/')
def index():
    global USER_RIGHTS
    USER_RIGHTS = 3
    return redirect("/auth")


# ===Авторизация пользователей в системе
@app.route('/auth', methods=('GET', 'POST'))
def auth():
    if request.method == 'POST':
        global USER_NAME
        global USER_RIGHTS
        try:
            login_employee = str(request.form['selected_login'])
            USER_NAME = login_employee
            if login_employee == 'korutov':
                USER_RIGHTS = 1
            else:
                USER_RIGHTS = 2
            password_employee = str(request.form['password_employee'])
        except ValueError:
            flash('Введены некорректные значения')
        conn = get_db_connection()
        item = conn.execute("""SELECT * FROM employees
                            WHERE (employees.login = ?)and(employees.password = ?)
             """, (login_employee, password_employee)).fetchall()
        conn.close()
        if len(item) == 0:
            flash('Введен неправильный логин и(или) пароль пользователя! Повторите ввод')
            return redirect(f'/auth')
        else:
            return redirect(f'/correspondents')

    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM employees
        """).fetchall()
    conn.close()
    return render_template('auth.html', logins=pos)


def replace_text(paragraph, key, value):
    """ Работа docx - заполнение параграфов """

    if key in paragraph.text:
        paragraph.text = paragraph.text.replace(key, value)


def replace_text_in_tables(table, key, value):
    """ Работа docx - заполнение таблиц """

    for row in table.rows:
        for cell in row.cells:
            if key in cell.text:
                cell.text = cell.text.replace(key, value)







###############
###############
############### Сотрудники университета
###############
###############

@app.route('/employees')
#===Получение данных из таблицы 'Сотрудники'
def employees():
    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM employees, departments, positions, role_users
                WHERE (employees.id_department = departments.id_department)AND(employees.id_position = positions.id_position)AND
                (employees.id_role = role_users.id_role)
            """).fetchall()
    conn.close()
    return render_template('employees.html', employees=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Получение одного сотрудника из БД
def get_employee(item_id):
    conn = get_db_connection()
    item = conn.execute("""SELECT employees.id_employee, employees.name, employees.login, employees.password,
                                  employees.id_department, departments.name_department,
                                  employees.email, employees.id_position, positions.position,
                                  employees.id_role, role_users.name_role 
                           FROM employees, departments, positions, role_users
                           WHERE (employees.id_employee = ?)AND(employees.id_department=departments.id_department)AND
                           (employees.id_position=positions.id_position)AND(employees.id_role=role_users.id_role)
                        """, (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


#===Вывод карточки о сотруднике
@app.route('/employees/<int:id_employee>')
def employee(id_employee):
    pos = get_employee(id_employee)
    return render_template('employee.html', employee=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Добавление нового сотрудника
@app.route('/new_employee', methods=('GET', 'POST'))
def new_employee():

    if request.method == 'POST':
        # добавление нового сотрудника в БД после заполнения формы
        try:
            name = request.form['name']
            login = request.form['login']
            password = request.form['password']
            id_department = request.form['selected_id_department']
            email = request.form['email']
            id_position = request.form['selected_id_position']
            id_role = request.form['selected_id_role']

            base_flag = 1
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name and login and password and id_department and email and id_position and id_role):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO 'employees' ('name', 'login', 'password', 'id_department', 'email', id_position, id_role)  VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, login, password, id_department, email, id_position, id_role))
                conn.commit()
                conn.close()
                return redirect('/employees')

    # отрисовка формы
    conn = get_db_connection()
    posd = conn.execute("""SELECT * FROM departments""").fetchall()
    posp = conn.execute("""SELECT * FROM positions""").fetchall()
    posr = conn.execute("""SELECT * FROM role_users""").fetchall()
    conn.close()
    return render_template('new_employee.html', departments=posd, positions=posp, roles=posr, user_name=USER_NAME, user_rights=USER_RIGHTS)


@app.route('/employee/<int:id_employee>/del', methods=('GET', 'POST'))
#===Удаление сотрудника
def del_employee(id_employee):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id_employee = ?", (id_employee,))
        conn.commit()
        conn.close()
        return redirect('/employees')

    # отрисовка формы
    pos = get_employee(id_employee)
    return render_template('del_employee.html', employee=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/employee/<int:id_employee>/update', methods=('GET', 'POST'))
#===Редактирование сотрудника
def edit_employee(id_employee):
    base_flag = 1
    if request.method == 'POST':
        try:
            name = request.form['name']
            login = request.form['login']
            password = request.form['password']
            id_department = request.form['selected_id_department']
            email = request.form['email']
            id_position = request.form['selected_id_position']
            id_role = request.form['selected_id_role']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name and login and password and id_department and email and id_position and id_role):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE 'employees' set 'name'=?, 'login'=?, 'password'=?, 'id_department'=?,'email'=?,'id_position'=?, 'id_role'=?  WHERE id_employee = ?",
                    (name, login, password, id_department, email, id_position, id_role, id_employee))
                conn.commit()
                conn.close()
                return redirect('/employees')
    # отрисовка формы
    pos = get_employee(id_employee)
    conn = get_db_connection()
    posd = conn.execute("""SELECT * FROM departments""").fetchall()
    posp = conn.execute("""SELECT * FROM positions""").fetchall()
    posr = conn.execute("""SELECT * FROM role_users""").fetchall()
    conn.close()
    #for pp in pos:
    #    tt=pp.birthday

    return render_template('edit_employee.html', employee=pos, departments=posd, positions=posp, roles=posr, user_name=USER_NAME, user_rights=USER_RIGHTS)

###############
###############
############### Подразделения университета
###############
###############

@app.route('/departments')

#===Получение данных из таблицы 'Подразделения'
def departments():

    conn = get_db_connection()
    pos = conn.execute("""SELECT  * FROM departments
            """).fetchall()
    conn.close()
    return render_template('departments.html', departments=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Получение одного подразделения из БД
def get_department(item_id):

    conn = get_db_connection()
    item = conn.execute("""SELECT DISTINCT * FROM departments
                WHERE departments.id_department= ?
                        """, (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


@app.route('/departments/<int:id_department>')
#===Вывод карточки о подразделении
def department(id_department):

    pos = get_department(id_department)
    return render_template('department.html', department=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/new_department', methods=('GET', 'POST'))
#===Добавление нового подразделения
def new_department():

    base_flag = 1
    if request.method == 'POST':
        # добавление нового подразделения в БД после заполнения формы
        try:
            name_department = request.form['name_department']
            submission = request.form['submission']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_department and submission):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO 'departments' ('name_department', 'submission')  VALUES (?, ?)",
                    (name_department, submission))
                conn.commit()
                conn.close()
                return redirect('/departments')

    # отрисовка формы
    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM departments""").fetchall()
    conn.close()
    return render_template('new_department.html', departments=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/department/<int:id_department>/del', methods=('GET', 'POST'))
#===Удаление подразделения
def del_department(id_department):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM departments WHERE id_department = ?", (id_department,))
        conn.commit()
        conn.close()
        return redirect('/departments')

    # отрисовка формы
    pos = get_department(id_department)
    return render_template('del_department.html', department=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/department/<int:id_department>/update', methods=('GET', 'POST'))
#===Редактирование подразделения
def edit_department(id_department):
    base_flag = 1
    if request.method == 'POST':
        try:
            name_department = request.form['name_department']
            submission = request.form['submission']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_department and submission):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE 'departments' set 'name_department'=?, 'submission'=? WHERE id_department = ?",
                    (name_department, submission, id_department))
                conn.commit()
                conn.close()
                return redirect('/departments')
    # отрисовка формы
    pos = get_department(id_department)
    return render_template('edit_department.html', department=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)


###############
###############
############### Роли пользователей
###############
###############

@app.route('/role_users')

#===Получение данных из таблицы 'Роли пользователей'
def role_users():

    conn = get_db_connection()
    pos = conn.execute("""SELECT  * FROM role_users
            """).fetchall()
    conn.close()
    return render_template('role_users.html', role_users=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Получение одной роли пользователей из БД
def get_role_user(item_id):

    conn = get_db_connection()
    item = conn.execute("""SELECT DISTINCT * FROM role_users
                WHERE role_users.id_role= ?
                        """, (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


@app.route('/role_users/<int:id_role>')
#===Вывод карточки о роли пользователей
def role_user(id_role):

    pos = get_role_user(id_role)
    return render_template('role_user.html', role_user=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/new_role_user', methods=('GET', 'POST'))
#===Добавление новой роли пользователей
def new_role_user():

    base_flag = 1
    if request.method == 'POST':
        # добавление новой роли пользователей в БД после заполнения формы
        try:
            name_role = request.form['name_role']
            description_role = request.form['description_role']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_role and description_role):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO 'role_users' ('name_role', 'description_role')  VALUES (?, ?)",
                    (name_role, description_role))
                conn.commit()
                conn.close()
                return redirect('/role_users')

    # отрисовка формы
    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM role_users""").fetchall()
    conn.close()
    return render_template('new_role_user.html', role_users=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/role_user/<int:id_role>/del', methods=('GET', 'POST'))
#===Удаление роли пользователей
def del_role_user(id_role):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM role_users WHERE id_role = ?", (id_role,))
        conn.commit()
        conn.close()
        return redirect('/role_users')

    # отрисовка формы
    pos = get_role_user(id_role)
    return render_template('del_role_user.html', role_user=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/role_user/<int:id_role>/update', methods=('GET', 'POST'))
#===Редактирование роли пользователей
def edit_role_user(id_role):
    base_flag = 1
    if request.method == 'POST':
        try:
            name_role = request.form['name_role']
            description_role = request.form['description_role']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_role and description_role):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE 'role_users' set 'name_role'=?, 'description_role'=? WHERE id_role = ?",
                    (name_role, description_role, id_role))
                conn.commit()
                conn.close()
                return redirect('/role_users')
    # отрисовка формы
    pos = get_role_user(id_role)
    return render_template('edit_role_user.html', role_user=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

###############
###############
############### Типы прав
###############
###############

@app.route('/access_types')

#===Получение данных из таблицы 'Типы прав'
def access_types():

    conn = get_db_connection()
    pos = conn.execute("""SELECT  * FROM access_types
            """).fetchall()
    conn.close()
    return render_template('access_types.html', access_types=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Получение одного типа прав из БД
def get_access_type(item_id):

    conn = get_db_connection()
    item = conn.execute("""SELECT DISTINCT * FROM access_types
                WHERE access_types.id_access_type= ?
                        """, (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


@app.route('/access_types/<int:id_access_type>')
#===Вывод карточки о типе прав
def access_type(id_access_type):

    pos = get_access_type(id_access_type)
    return render_template('access_type.html', access_type=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/new_access_type', methods=('GET', 'POST'))
#===Добавление нового типа прав
def new_access_type():

    base_flag = 1
    if request.method == 'POST':
        # добавление нового типа прав в БД после заполнения формы
        try:
            name_access_right = request.form['name_access_right']
            description_rights = request.form['description_rights']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_access_right and description_rights):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO 'access_types' ('name_access_right', 'description_rights')  VALUES (?, ?)",
                    (name_access_right, description_rights))
                conn.commit()
                conn.close()
                return redirect('/access_types')

    # отрисовка формы
    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM access_types""").fetchall()
    conn.close()
    return render_template('new_access_type.html', access_types=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/access_type/<int:id_access_type>/del', methods=('GET', 'POST'))
#===Удаление типа прав
def del_access_type(id_access_type):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM access_types WHERE id_access_type = ?", (id_access_type,))
        conn.commit()
        conn.close()
        return redirect('/access_types')

    # отрисовка формы
    pos = get_access_type(id_access_type)
    return render_template('del_access_type.html', access_type=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/access_type/<int:id_access_type>/update', methods=('GET', 'POST'))
#===Редактирование типа прав
def edit_access_type(id_access_type):
    base_flag = 1
    if request.method == 'POST':
        try:
            name_access_right = request.form['name_access_right']
            description_rights = request.form['description_rights']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_access_right and description_rights):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE 'access_types' set 'name_access_right'=?, 'description_rights'=? WHERE id_access_type = ?",
                    (name_access_right, description_rights, id_access_type))
                conn.commit()
                conn.close()
                return redirect('/access_types')
    # отрисовка формы
    pos = get_access_type(id_access_type)
    return render_template('edit_access_type.html', access_type=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

###############
###############
############### Корреспонденты
###############
###############

@app.route('/correspondents')
#===Получение данных из таблицы 'Корреспонденты'
def correspondents():
    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM correspondents, type_correspondents
                WHERE (correspondents.id_type_correspondent = type_correspondents.id_type_correspondent)
            """).fetchall()
    conn.close()
    return render_template('correspondents.html', correspondents=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Получение одного корреспондента из БД
def get_correspondent(item_id):
    conn = get_db_connection()
    item = conn.execute("""SELECT correspondents.id_correspondent, correspondents.name_correspondent,
                                  correspondents.id_type_correspondent, type_correspondents.type_correspondent                                   
                           FROM correspondents, type_correspondents
                           WHERE (correspondents.id_correspondent = ?)AND(correspondents.id_type_correspondent=type_correspondents.id_type_correspondent)
                        """, (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


#===Вывод карточки о корреспонденте
@app.route('/correspondents/<int:id_correspondent>')
def correspondent(id_correspondent):
    pos = get_correspondent(id_correspondent)
    return render_template('correspondent.html', correspondent=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Добавление нового корреспондента
@app.route('/new_correspondent', methods=('GET', 'POST'))
def new_correspondent():

    if request.method == 'POST':
        # добавление нового корреспондента в БД после заполнения формы
        try:
            name_correspondent = request.form['name_correspondent']
            id_type_correspondent = request.form['selected_id_type_correspondent']

            base_flag = 1
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_correspondent and  id_type_correspondent):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO 'correspondents' ('name_correspondent', 'id_type_correspondent')  VALUES (?, ?)",
                    (name_correspondent, id_type_correspondent))
                conn.commit()
                conn.close()
                return redirect('/correspondents')

    # отрисовка формы
    conn = get_db_connection()
    post = conn.execute("""SELECT * FROM type_correspondents""").fetchall()
    conn.close()
    return render_template('new_correspondent.html', type_correspondents=post, user_name=USER_NAME, user_rights=USER_RIGHTS)


@app.route('/correspondent/<int:id_correspondent>/del', methods=('GET', 'POST'))
#===Удаление корреспондента
def del_correspondent(id_correspondent):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM correspondents WHERE id_correspondent = ?", (id_correspondent,))
        conn.commit()
        conn.close()
        return redirect('/correspondents')

    # отрисовка формы
    pos = get_correspondent(id_correspondent)
    return render_template('del_correspondent.html', correspondent=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/correspondent/<int:id_correspondent>/update', methods=('GET', 'POST'))
#===Редактирование корреспондента
def edit_correspondent(id_correspondent):
    base_flag = 1
    if request.method == 'POST':
        try:
            name_correspondent = request.form['name_correspondent']
            id_type_correspondent = request.form['selected_id_type_correspondent']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_correspondent and id_type_correspondent):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE 'correspondents' set 'name_correspondent'=?, 'id_type_correspondent'=?  WHERE id_correspondent = ?",
                    (name_correspondent, id_type_correspondent, id_correspondent))
                conn.commit()
                conn.close()
                return redirect('/correspondents')
    # отрисовка формы
    pos = get_correspondent(id_correspondent)
    conn = get_db_connection()
    post = conn.execute("""SELECT * FROM type_correspondents""").fetchall()
    conn.close()
    #for pp in pos:
    #    tt=pp.birthday

    return render_template('edit_correspondent.html', correspondent=pos, type_correspondents=post, user_name=USER_NAME, user_rights=USER_RIGHTS)




###############
###############
############### Документы
###############
###############

@app.route('/documents')
#===Получение данных из таблицы 'Документы'
def documents():
    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM documents, category_documents, correspondents
                WHERE (documents.id_category_document = category_documents.id_category_document)AND
                (documents.id_correspondent = correspondents.id_correspondent)
            """).fetchall()
    conn.close()
    return render_template('documents.html', documents=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Получение одного документа из БД
def get_document(item_id):
    conn = get_db_connection()
    item = conn.execute("""SELECT documents.id_document, documents.name_document, documents.text_document, documents.size_document,
                                  documents.link_document,                                  
                                  documents.id_category_document, category_documents.category_document,
                                  documents.id_correspondent, correspondents.name_correspondent                                   
                           FROM documents, category_documents, correspondents
                           WHERE (documents.id_document = ?)AND(documents.id_category_document=category_documents.id_category_document)AND
                                 (documents.id_correspondent=correspondents.id_correspondent)
                        """, (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


#===Вывод карточки о документе
@app.route('/documents/<int:id_document>')
def document(id_document):
    pos = get_document(id_document)
    return render_template('document.html', document=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Добавление нового документа
@app.route('/new_document', methods=('GET', 'POST'))
def new_document():

    if request.method == 'POST':
        # добавление нового документа в БД после заполнения формы
        try:
            name_document = request.form['name_document']
            #===разбор загруженного файла
            if 'text_document' in request.files:
                file = request.files['text_document']
                if file.filename != '':
                    # Получение имени файла
                    filename = secure_filename(file.filename)
                    # Чтение файла
                    SizeOfFile = request.content_length
                    TextOfFile = file.read().decode('utf-8')
            text_document = TextOfFile
            size_document = SizeOfFile
            link_document = filename
            id_category_document = request.form['selected_id_category_document']
            id_correspondent = request.form['selected_id_correspondent']

            base_flag = 1
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_document and text_document and size_document and link_document):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO 'documents' ('name_document', 'text_document', 'size_document', 'link_document', 'id_category_document', 'id_correspondent')  VALUES (?, ?, ?, ?, ?, ?)",
                    (name_document, text_document, size_document, link_document, id_category_document, id_correspondent))
                conn.commit()
                conn.close()
                return redirect('/documents')

    # отрисовка формы
    conn = get_db_connection()
    postcd = conn.execute("""SELECT * FROM category_documents""").fetchall()
    postc = conn.execute("""SELECT * FROM correspondents""").fetchall()
    conn.close()
    return render_template('new_document.html', category_documents=postcd, correspondents=postc, user_name=USER_NAME, user_rights=USER_RIGHTS)


@app.route('/document/<int:id_document>/del', methods=('GET', 'POST'))
#===Удаление документа
def del_document(id_document):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE id_document = ?", (id_document,))
        conn.commit()
        conn.close()
        return redirect('/documents')

    # отрисовка формы
    pos = get_document(id_document)
    tt=pos['link_document']
    return render_template('del_document.html', document=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/document/<int:id_document>/check', methods=('GET', 'POST'))
#===Изменение категории документа
def check_document(id_document):
    if request.method == 'POST':
        global model
        #model = load_model('workmodel.h5')
        # Required for model to work
        global graph
        #graph = tf.get_default_graph()

        doc = get_document(id_document)
        name_document = doc['name_document']
        text_document = doc['text_document']
        size_document = doc['size_document']
        link_document = doc['link_document']
        id_correspondent = doc['id_correspondent']
        try:
            with open('output.txt', 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = "Файл не найден"
        id_category_document = int(content)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE 'documents' set 'name_document'=?, 'text_document'=?, 'size_document'=?, 'link_document'=?, 'id_category_document'=?,'id_correspondent'=?  WHERE id_document = ?",
            (name_document, text_document, size_document, link_document, id_category_document, id_correspondent,
             id_document))
        conn.commit()
        conn.close()
        return redirect('/documents')

    # отрисовка формы
    pos = get_document(id_document)
    tt=pos['link_document']
    return render_template('check_document.html', document=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)



@app.route('/document/<int:id_document>/update', methods=('GET', 'POST'))
#===Редактирование локумента
def edit_document(id_document):
    base_flag = 1
    if request.method == 'POST':
        try:
            name_document = request.form['name_document']
            text_document = request.form['text_document']
            size_document = request.form['size_document']
            link_document = request.form['link_document']
            id_category_document = request.form['selected_id_category_document']
            id_correspondent = request.form['selected_id_correspondent']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (name_document and text_document and size_document and link_document):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE 'documents' set 'name_document'=?, 'text_document'=?, 'size_document'=?, 'link_document'=?, 'id_category_document'=?,'id_correspondent'=?  WHERE id_document = ?",
                    (name_document, text_document, size_document, link_document, id_category_document, id_correspondent, id_document))
                conn.commit()
                conn.close()
                return redirect('/documents')
    # отрисовка формы
    pos = get_document(id_document)
    conn = get_db_connection()
    poscd = conn.execute("""SELECT * FROM category_documents""").fetchall()
    posc = conn.execute("""SELECT * FROM correspondents""").fetchall()
    conn.close()

    return render_template('edit_document.html', document=pos, category_documents=poscd, correspondents=posc, user_name=USER_NAME, user_rights=USER_RIGHTS)



###############
###############
############### Назначение прав доступа
###############
###############

@app.route('/assignment_rights')
#===Получение данных из таблицы 'Назначение прав доступа'
def assignment_rights():
    conn = get_db_connection()
    pos = conn.execute("""SELECT * FROM assignment_rights, role_users, access_types, documents
                WHERE (assignment_rights.id_role = role_users.id_role)AND(assignment_rights.id_access_type = access_types.id_access_type)AND
                      (assignment_rights.id_document=documents.id_document)
            """).fetchall()
    conn.close()
    return render_template('assignment_rights.html', assignment_rights=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Получение одного назначения прав доступа из БД
def get_assignment_right(item_id):
    conn = get_db_connection()
    item = conn.execute("""SELECT assignment_rights.id_assignment_rights, assignment_rights.date_assignment,
                                  assignment_rights.id_role, role_users.name_role,
                                  assignment_rights.id_access_type, access_types.name_access_right,
                                  assignment_rights.id_document, documents.name_document 
                           FROM assignment_rights, role_users, access_types, documents
                           WHERE (assignment_rights.id_assignment_rights = ?)AND
                                 (assignment_rights.id_role=role_users.id_role)AND
                                 (assignment_rights.id_access_type=access_types.id_access_type)AND
                                 (assignment_rights.id_document=documents.id_document)
                        """, (item_id,)).fetchone()
    conn.close()
    if item is None:
        abort(404)
    return item


#===Вывод карточки о назначении прав
@app.route('/assignment_rights/<int:id_assignment_rights>')
def assignment_right(id_assignment_rights):
    pos = get_assignment_right(id_assignment_rights)
    return render_template('assignment_right.html', assignment_right=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

#===Добавление нового назначения прав
@app.route('/new_assignment_right', methods=('GET', 'POST'))
def new_assignment_right():

    if request.method == 'POST':
        # добавление нового назначения прав в БД после заполнения формы
        try:
            date_assignment = request.form['date_assignment']
            id_role = request.form['selected_id_role']
            id_access_type = request.form['selected_id_access_type']
            id_document = request.form['selected_id_document']

            base_flag = 1
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (date_assignment):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO 'assignment_rights' ('date_assignment', 'id_role', 'id_access_type', 'id_document')  VALUES (?, ?, ?, ?)",
                    (date_assignment, id_role, id_access_type, id_document))
                conn.commit()
                conn.close()
                return redirect('/assignment_rights')

    # отрисовка формы
    conn = get_db_connection()
    posru = conn.execute("""SELECT * FROM role_users""").fetchall()
    posat = conn.execute("""SELECT * FROM access_types""").fetchall()
    posd = conn.execute("""SELECT * FROM documents""").fetchall()
    conn.close()
    return render_template('new_assignment_right.html', role_users=posru, access_types=posat, documents=posd, user_name=USER_NAME, user_rights=USER_RIGHTS)


@app.route('/assignment_right/<int:id_assignment_rights>/del', methods=('GET', 'POST'))
#===Удаление назначения прав
def del_assignment_right(id_assignment_rights):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assignment_rights WHERE id_assignment_rights = ?", (id_assignment_rights,))
        conn.commit()
        conn.close()
        return redirect('/assignment_rights')

    # отрисовка формы
    pos = get_assignment_right(id_assignment_rights)
    return render_template('del_assignment_right.html', assignment_right=pos, user_name=USER_NAME, user_rights=USER_RIGHTS)

@app.route('/assignment_right/<int:id_assignment_rights>/update', methods=('GET', 'POST'))
#===Редактирование назначения прав
def edit_assignment_right(id_assignment_rights):
    base_flag = 1
    if request.method == 'POST':
        try:
            date_assignment = request.form['date_assignment']
            id_role = request.form['selected_id_role']
            id_access_type = request.form['selected_id_access_type']
            id_document = request.form['selected_id_document']
        except ValueError:
            flash('Некорректные значения')
            base_flag = 0
        if not base_flag > 0:
            flash('Не все поля заполнены')
        else:
            if not (date_assignment):
                flash('Не все поля заполнены')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE 'assignment_rights' set 'date_assignment'=?, 'id_role'=?, 'id_access_type'=?, 'id_document'=?  WHERE id_assignment_rights = ?",
                    (date_assignment, id_role, id_access_type, id_document, id_assignment_rights))
                conn.commit()
                conn.close()
                return redirect('/assignment_rights')
    # отрисовка формы
    pos = get_assignment_right(id_assignment_rights)
    conn = get_db_connection()
    posru = conn.execute("""SELECT * FROM role_users""").fetchall()
    posat = conn.execute("""SELECT * FROM access_types""").fetchall()
    posd = conn.execute("""SELECT * FROM documents""").fetchall()
    conn.close()

    return render_template('edit_assignment_right.html', assignment_right=pos, role_users=posru, access_types=posat, documents=posd, user_name=USER_NAME, user_rights=USER_RIGHTS)



#
# =========Выдача сообщения об отсутствии страницы (404)
#

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
import numpy as np
import pandas as pd

def generate_dataframe(seed=42):

    np.random.seed(seed)

    data = pd.DataFrame({
        'Возраст': np.random.randint(18, 65, size=1000),
        'Зарплата': np.random.randint(30000, 150000, size=1000),
        'Стаж': np.random.randint(1, 30, size=1000),
        'Город': np.random.choice(['Москва', 'СПб', 'Новосибирск', 'Екатеринбург',
                                'Нижний Новгород', 'Казань', 'Омск', 'Самара',
                                'Красноярск', 'Волгоград'], size=1000),
        'Пол': np.random.choice(['Муж.', 'Жен.'], size=1000),
        'Образование': np.random.choice(['Высшее', 'Среднее специальное', 'Среднее общее']),
        'Профессия': np.random.choice(['Инженер', 'Разработчик', 'Менеджер', 'Аналитик',
                                        'Дизайнер', 'Ведущий специалист', 'Техник'],
                                    size=1000),
        'Компания': np.random.choice(['Газпром', 'Роснефть', 'Сбербанк', 'Яндекс', 'Mail.ru Group',
                                    'Yandex.Cloud', 'SberDevices', 'Nornickel', 'Alrosa', 'Lukoil'],
                                    size=1000),
        'Отрасль': np.random.choice(['Энергетика', 'Финансы', 'Технологии', 'Натуральные ресурсы',
                                'Образование', 'Бизнес-сервисы', 'Искусственный интеллект',
                                'Цифровые технологии', 'Инновационные продукты', 'Транспорт'],
                                size=1000),
        'Уровень удовлетворенности': np.random.uniform(1, 10, size=1000),
        'Количество проектов': np.random.randint(1, 50, size=1000),
        'Стаж в текущей компании': np.random.randint(1, 15, size=1000),
        'Премиальные': np.random.uniform(50000, 200000, size=1000),
        'Бонусы': np.random.uniform(10000, 50000, size=1000),
        'Оценка работы': np.random.uniform(1, 10, size=1000),
        'Дата начала работы': pd.date_range(start='2020-01-01', periods=1000).astype(str),
        'Дата окончания контракта': pd.date_range(start='2020-01-01', periods=1000, freq='M').astype(str)
    })

    # Добавляем пропуски
    for col in data.keys():
        mask = np.random.choice([True, False], size=(len(data), 1), p=[0.3, 0.7])
        data[col] = np.where(mask.flatten(), np.nan, data[col])

    # Добавляем выбросы
    for col in ['Зарплата', 'Стаж', 'Количество проектов']:
        data[col] += np.random.normal(0, 500, size=len(data)).clip(min=-1000, max=1000)

    df = pd.DataFrame(data)

    return df
# print("\nСтатистические характеристики:")
# print(df.describe())

# Проверяем количество пропущенных значений
# print("\nКоличество пропущенных значений:")
# print(df.isnull().sum())

def transform_generated_to_sql(df):

    sql = """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        salary INTEGER,
        experience INTEGER,
        city VARCHAR(255),
        gender VARCHAR(255),
        education VARCHAR(255),
        profession VARCHAR(255),
        company VARCHAR(255),
        industry VARCHAR(255),
        satisfaction_level FLOAT,
        projects INTEGER,
        experience_in_company INTEGER,
        premium FLOAT,  
        bonuses FLOAT,
        rating FLOAT,
        start_date DATE,
        end_date DATE
    );
    """

    for i in range(len(df)):
        sql += f"""
        INSERT INTO employees (age, salary
        , experience
        , city
        , gender
        , education
        , profession
        , company
        , industry
        , satisfaction_level
        , projects
        , experience_in_company
        , premium
        , bonuses
        , rating
        , start_date
        , end_date)
        VALUES ({df.iloc[i]['Возраст']}, {df.iloc[i]['Зарплата']}
        , {df.iloc[i]['Стаж']}
        , '{df.iloc[i]['Город']}'
        , '{df.iloc[i]['Пол']}'
        , '{df.iloc[i]['Образование']}'
        , '{df.iloc[i]['Профессия']}'
        , '{df.iloc[i]['Компания']}'
        , '{df.iloc[i]['Отрасль']}'
        , {df.iloc[i]['Уровень удовлетворенности']}
        , {df.iloc[i]['Количество проектов']}
        , {df.iloc[i]['Стаж в текущей компании']}
        , {df.iloc[i]['Премиальные']}
        , {df.iloc[i]['Бонусы']}
        , {df.iloc[i]['Оценка работы']}
        , '{df.iloc[i]['Дата начала работы']}'
        , '{df.iloc[i]['Дата окончания контракта']}');
        """

    return sql.replace('nan', 'NULL')



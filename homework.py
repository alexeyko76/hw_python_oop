import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        sum = 0.0
        for record in self.records:
            if record.date == today:
                sum += record.amount
        return sum

    def get_week_stats(self):
        print('[get_week_stats called]')
        for record in self.records:
            print(f'{record.date}')
        today = dt.date.today()
        sum = 0.0
        delta = dt.timedelta(days=7)
        for record in self.records:
            if (record.date <= today) and (today - record.date <= delta):
                sum += record.amount
        return sum


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if (date is None):
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_spent = self.get_today_stats()

        if calories_spent < self.limit:
            calories_remained = self.limit - calories_spent
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained:.0f} кКал')

        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        rate = 1.0
        currency_name = ''
        if currency == 'usd':
            rate = self.USD_RATE
            currency_name = 'USD'
        elif currency == 'eur':
            rate = self.EURO_RATE
            currency_name = 'Euro'
        elif currency == 'rub':
            rate = 1.0
            currency_name = 'руб'
        else:
            return 'Error: Wrong currency'

        cash_spent = self.get_today_stats()

        if cash_spent < self.limit:
            cash_remained = (self.limit - cash_spent) / rate
            return (f'На сегодня осталось {cash_remained:.2f} '
                    f'{currency_name}')

        if cash_spent == self.limit:
            return 'Денег нет, держись'

        cash_remained = (cash_spent - self.limit) / rate
        return (f'Денег нет, держись: твой долг - {cash_remained:.2f} '
                f'{currency_name}')


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=3000, comment='бар в Танин др',
                                  date='08.11.2019'))
print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься: На сегодня осталось 555 руб

# для CaloriesCalculator
calories_calculator = CaloriesCalculator(2000)
calories_calculator.add_record(Record(amount=1186,
                                      comment='Кусок тортика. И ещё один.',
                                      date='24.02.2019'))
calories_calculator.add_record(Record(amount=84, comment='Йогурт.',
                                      date='23.02.2019'))
calories_calculator.add_record(Record(amount=1140, comment='Баночка чипсов.',
                                      date='24.02.2019'))
calories_calculator.add_record(Record(amount=1110, comment='Шоколад.'))
print(calories_calculator.get_calories_remained())

cash_calculator1 = CashCalculator(1000)
cash_calculator1.add_record(Record(amount=700, comment='бар в Танин др'))
print(cash_calculator1.get_today_cash_remained('eur'))

from queue import Queue
from random import randint
from threading import Thread
from time import sleep

class Table:
    def __init__(self, number):
        self.number = number # номер стола
        self.guest = None # имя госта за столом

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name # имя гостя

    def run(self):
        sleep(randint(3, 10))

class Cafe:
    def __init__(self, *tables: Table):
        self.tables = tables
        self.queue = Queue()

    def guest_arrival(self, *guests: Guest):
        for guest in guests:
            guest_in_queue = True
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(а) за стол номер {table.number}')
                    guest_in_queue = False
                    break
            if guest_in_queue:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')
    def discuss_guests(self):
        while not self.queue.empty(): # цикл запущен пока очеред не пуста
            for table in self.tables:
                if table.guest is None: # проверка на свободность столика
                    table.guest = self.queue.get() # посадка за столик гостя
                    print(f'{table.guest.name} вышел(-а) из очереди '
                          f'и сел(-а) за стол номер {table.number}')
                    table.guest.start()
                else:
                    if not table.guest.is_alive():
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None

if __name__ == '__main__':
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]
    # Имена гостей
    guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
                    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya',
                    'Alexandra']
    # Создание гостей
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами
    cafe = Cafe(*tables)
    # Приём гостей
    cafe.guest_arrival(*guests)
    # Обслуживание гостей
    cafe.discuss_guests()
    Kirill = Guest('Kirill')
    Karina = Guest('Karina')

    cafe.guest_arrival(Karina, Kirill)
    cafe.discuss_guests()


# Dushnila
_Программа для построения профиля Лоуренца, Гауса и Фойта._
_Реализованна на языке программирования Python_
## Описание файлов:
- "CO2 absorption coefficient, cm-1.csv"
> Файл с набором данных симуляции 
- "dushnila.py"
> Основной код программы 
- "README.md"
> Файл описания проекта 
- "ToDoList.md"
> Лист с задачами по проекту 
## Описание dushnila.py:
### Используемые библиотеки:
- ' numpy '
> Библиотека для работы с векторами и матрицами 
- ' pylab '
> Библиотека для отрисовки основного окна программы и выводимых графиков 
- ' hapi '
> Hitran API, в будущем планируется отказаться от использования 
- ' pandas '
> Библиотека для подключения scv файла 
- ' matplotlib.widgets ' 
> Библиотека используется для импорта класса Slider 
### Основные функции:
- ' first_y '
> Отображаемая фукнция профиля Лоуренца 
-  'second_y '
> Отображаемая фукнция профиля Гауса 
- ' third_y '
> Отображаемая фукнция профиля Фойта 
- ' get_param '
> Библиотека для подключения scv файла 
- ' updateGraph ' 
> Функция для обновления графика 
- ' onChangeValue '
> Обработчик события изменения значений слайдеров 
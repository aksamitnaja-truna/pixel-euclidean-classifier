from table import CriteriaPoint
import csv
import os


class PointsCSVHandler:
    @staticmethod
    def read_points(filename):

        points = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Проверяем наличие необходимых колонок
                required_columns = ['group', 'X', 'Y']
                if not all(column in reader.fieldnames for column in required_columns):
                    raise ValueError(f"Файл должен содержать колонки: {required_columns}")

                for row_num, row in enumerate(reader, start=2):
                    try:
                        group = row['group'].strip()
                        x = int(row['X'])
                        y = int(row['Y'])

                        # Если есть колонка index, используем её, иначе используем номер строки
                        index = int(row['index']) if 'index' in row and row['index'].strip() else row_num - 1

                        point = CriteriaPoint([x, y], group)
                        points.append(point)

                    except (ValueError, KeyError) as e:
                        print(f"Ошибка в строке {row_num}: {e}")
                        continue

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка при чтении файла: {e}")

        # print(f"Успешно загружено {len(points)} точек из {filename}")
        return points

    @staticmethod
    def update_points(filename, points, include_index=True):

        try:
            # Создаем папку если её нет
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Записываем заголовок
                if include_index:
                    writer.writerow(('index', 'group', 'X', 'Y'))
                else:
                    writer.writerow(('group', 'X', 'Y'))

                # Записываем точки с индексами
                for index, point in enumerate(points, start=1):
                    if isinstance(point, CriteriaPoint):
                        # CriteriaPoint объект
                        if include_index:
                            writer.writerow([
                                index,
                                point.group_name if point.group_name else '',
                                point.criteria[0],
                                point.criteria[1]
                            ])
                        else:
                            writer.writerow([
                                point.group_name if point.group_name else '',
                                point.criteria[0],
                                point.criteria[1]
                            ])
                    elif isinstance(point, (tuple, list)) and len(point) == 3:
                        # Кортеж (group, x, y)
                        group, x, y = point
                        if include_index:
                            writer.writerow((index, group, x, y))
                        else:
                            writer.writerow((group, x, y))
                    else:
                        print(f"Предупреждение: неподдерживаемый формат точки: {point}")
                        continue

            index_info = "с индексами" if include_index else "без индексов"
            # print(f"Успешно сохранено {len(points)} точек {index_info} в {filename}")
            return True

        except Exception as e:
            print(f"Ошибка при сохранении файла {filename}: {e}")
            return False

    @staticmethod
    def backup(n):
        """
        Оставляет в файле только первые N точек, остальные удаляются

        Args:
            filename (str): путь к CSV файлу
            n (int): количество точек для сохранения
            include_index (bool): включать ли колонку с индексами

        Returns:
            bool: True если успешно, False если ошибка
        """
        filename = 'data/data1/points.csv'
        include_index = True
        try:
            # Читаем все точки из файла
            points = PointsCSVHandler.read_points(filename)

            # Проверяем, что n не превышает количество точек
            if n > len(points):
                print(f"Предупреждение: запрошено {n} точек, но в файле только {len(points)}")
                n = len(points)

            # Берем только первые N точек
            first_n_points = points[:n]

            # Сохраняем обратно в файл
            return PointsCSVHandler.update_points(filename, first_n_points, include_index)

        except FileNotFoundError:
            print(f"Ошибка: файл {filename} не найден")
            return False
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")
            return False



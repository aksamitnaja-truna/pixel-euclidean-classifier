import matplotlib.pyplot as plt
import numpy as np
import os


class PointPlotter:
    def __init__(self, file_path):
        self.file_path = file_path
        # Создаем папку если её нет
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def plot_points_with_radius_groups(self, points, radius, c_point,  title="Точки с радиусом по группам"):
        """
        График с точками, окрашенными в цвета своих групп и радиусом вокруг последней точки

        Args:
            points: список объектов CriteriaPoint
            radius: радиус для группировки
            title: заголовок графика
        """
        plt.figure(figsize=(10, 8))

        # Извлекаем координаты
        x_coords = [p.criteria[0] for p in points]
        y_coords = [p.criteria[1] for p in points]

        # Центр окружности - последняя точка в списке
        center_point = points[-1]
        center_x, center_y = center_point.criteria

        # Создаем цветовую карту для существующих групп
        unique_groups = list(set([p.group_name for p in points if p.group_name]))
        color_map = {
            'red': 'red',
            'green': 'green',
            'blue': 'blue',
            'yellow': 'yellow',
            'purple': 'purple',
            'orange': 'orange',
            'brown': 'brown',
            'pink': 'pink',
            'gray': 'gray',
            'cyan': 'cyan'
        }

        # Если группа не найдена в color_map, используем цвет по умолчанию
        point_colors = []
        for point in points:
            group_color = color_map.get(point.group_name, 'black')
            point_colors.append(group_color)

        # Рисуем все точки с цветами их групп (кроме центральной)
        regular_points = [p for p in points if p != center_point]
        if regular_points:
            x_regular = [p.criteria[0] for p in regular_points]
            y_regular = [p.criteria[1] for p in regular_points]
            colors_regular = [color_map.get(p.group_name, 'black') for p in regular_points]
            plt.scatter(x_regular, y_regular, c=colors_regular, s=80, alpha=0.7,
                        edgecolors='black', linewidth=0.5)

        # Центральная точка в цвете своей группы, но большего размера
        center_color = color_map.get(center_point.group_name, 'black')
        plt.scatter(center_x, center_y, c=center_color, s=300, marker='o',
                    edgecolors='black', linewidth=3, zorder=10, label=f'Центр ({center_point.group_name})')

        # Рисуем круг радиуса вокруг центральной точки (только контур)
        circle = plt.Circle((center_x, center_y), radius, color='black', fill=False,
                            linestyle='--', linewidth=2, label=f'Радиус R={radius}')
        plt.gca().add_patch(circle)

        # Рисуем отрезок от c_point до центра, если c_point задан
        if c_point is not None:
            c_x, c_y = c_point.criteria
            color = c_point.get_group_name()
            plt.plot([c_x, center_x], [c_y, center_y],
                     color=color, linewidth=3, linestyle='-',
                     marker='o', markersize=8,
                     label='Минимальное расстояние', zorder=5)

        # Рисуем круг радиуса вокруг центральной точки (только контур)
        circle = plt.Circle((center_x, center_y), radius, color='black', fill=False,
                            linestyle='--', linewidth=2, label=f'Радиус R={radius}')
        plt.gca().add_patch(circle)

        # Подписываем точки только названием группы
        for i, point in enumerate(points):
            if point.group_name:
                # Для центральной точки делаем подпись особой
                if point == center_point:
                    plt.annotate(f"{point.group_name}\n(центр)",
                                 (point.criteria[0], point.criteria[1]),
                                 xytext=(10, 10), textcoords='offset points',
                                 fontsize=9, fontweight='bold',
                                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
                else:
                    plt.annotate(point.group_name,
                                 (point.criteria[0], point.criteria[1]),
                                 xytext=(5, 5), textcoords='offset points',
                                 fontsize=8, fontweight='bold')

        # Настройки графика
        plt.xlabel('Ends (X координата)')
        plt.ylabel('Nodes (Y координата)')
        plt.title(title)
        plt.grid(True, alpha=0.3)

        # Легенда только для существующих групп и радиуса
        from matplotlib.patches import Patch
        legend_elements = []

        # Добавляем группы в легенду
        for group in unique_groups:
            color = color_map.get(group, 'black')
            legend_elements.append(
                Patch(facecolor=color, alpha=0.7, label=group)
            )

        # Добавляем радиус (только контур)
        legend_elements.append(
            Patch(facecolor='white', edgecolor='black', linestyle='--',
                  linewidth=2, label=f'Радиус R={radius}')
        )

        plt.legend(handles=legend_elements, loc='upper right')

        # Устанавливаем масштаб чтобы были видны все точки и радиус
        all_x = x_coords + [center_x - radius, center_x + radius]
        all_y = y_coords + [center_y - radius, center_y + radius]

        margin = max(radius * 0.2, 1)  # Минимальный запас
        plt.xlim(min(all_x) - margin, max(all_x) + margin)
        plt.ylim(min(all_y) - margin, max(all_y) + margin)
        plt.axis('equal')

        # Сохраняем график
        plt.tight_layout()
        plt.savefig(self.file_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"График с радиусом по группам сохранен: {self.file_path}")

        # Возвращаем информацию о точках в радиусе
        points_in_radius = []
        for point in points:
            x, y = point.criteria
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if distance <= radius:
                points_in_radius.append(point)

        group_count = {
            "points_in_radius": len(points_in_radius),
            "total_points": len(points),
            "center_point": center_point
        }
        return group_count
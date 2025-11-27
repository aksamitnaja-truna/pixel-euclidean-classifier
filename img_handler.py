import os
import shutil
import cv2
from table import CriteriaPoint

class ImageHandler:

    @staticmethod
    def __img_to_criteria_point(img_path):
        if os.path.basename(img_path).find('_') == -1:
            group = None
        else:
            group = os.path.basename(img_path).split('_')[0]

        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)


        return CriteriaPoint(image.flatten(), group)


    @staticmethod
    def read_folder(folder_path):
        c_points = []
        all_items = os.listdir(folder_path)
        for img_name in all_items:
            img_path = os.path.join(folder_path, img_name)
            c_points.append(ImageHandler.__img_to_criteria_point(img_path))

        return c_points

    @staticmethod
    def read_file(img_path):
        return ImageHandler.__img_to_criteria_point(img_path)

    @staticmethod
    def img_name(group_name):
        return f'{group_name}_{len(os.listdir("./data/data2/source_images")) + 1}.png'

    @staticmethod
    def add_img_to_source(img_path, group_name):
        img_name = os.path.basename(img_path)
        new_img_name = ImageHandler.img_name(group_name)
        target_dir = './data/data2/source_images'
        new_full_path = os.path.join(target_dir, new_img_name)
        shutil.move(img_path, new_full_path)

    @staticmethod
    def backup():
        backup_dir = './data/data2/back_up'
        data2_dir = './data/data2'

        # Удаляем существующие папки (если есть)
        source_images_path = os.path.join(data2_dir, 'source_images')
        test_images_path = os.path.join(data2_dir, 'test_images')

        if os.path.exists(source_images_path):
            shutil.rmtree(source_images_path)
        if os.path.exists(test_images_path):
            shutil.rmtree(test_images_path)

        # Копируем из бэкапа
        shutil.copytree(
            os.path.join(backup_dir, 'source_images'),
            source_images_path
        )
        shutil.copytree(
            os.path.join(backup_dir, 'test_images'),
            test_images_path
        )

        print("Папки успешно восстановлены из бэкапа")
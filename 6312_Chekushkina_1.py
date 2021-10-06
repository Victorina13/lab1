import os
import zipfile
import hashlib
import requests
import re
import csv
# Задание 1
directory_to_extract_to = 'E:\\ARCH'
os.mkdir(directory_to_extract_to)
arch_file = zipfile.ZipFile('E:\\tiff-4.2.0_lab1.zip')
arch_file.extractall(directory_to_extract_to)
arch_file.close()

'''Задание №2.1
Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to.
#Сохранить полученный список в txt_files'''
txt_files = []
for root, dirs, files in os.walk(directory_to_extract_to):
    for i in files:
        if '.txt' in i:
            txt_files.append(os.path.join(root, i))
print("Список файлов с расширением txt: ")
for i in txt_files:
    print(i)
'''Задание №2.2. 
Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.'''
result = " "
for file in txt_files:
    tar_file = open(file, "rb")
    tmp = tar_file.read()
    result = hashlib.md5(tmp).hexdigest()
    tar_file.close()
print("Значения хэша найденных файлов: ")
print(result)

# Задание №3. Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''
target_file_data = ''
for root, dirs, files in os.walk(directory_to_extract_to):
    for i in files:
        file = open(os.path.join(root, i), "rb").read()
        file_data = hashlib.md5(file).hexdigest()
        if target_hash == file_data:
            target_file = root
            target_file_data = file
print("Путь к исходному файлу: ")
print(target_file)
print("Содержимое искомого файла: ")
print(target_file_data)
# Задание №4
r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы
counter = 0
headers = " "
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
# Извлечение заголовков таблицы
for line in lines:
    if counter == 0:
        headers = re.sub(r'\<[^>]*\>', " ", line)
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
    tmp = re.sub(r'\<[^>]*\>', ";", line)
    tmp = re.sub(r'\xa0', '', tmp)
    tmp = re.sub(r'[*]', '', tmp)
    tmp = re.sub(r'^\W+', '', tmp)
    tmp = re.sub(r'\(.*?\)', '', tmp)
    tmp = re.sub('_', '-1', tmp)
    tmp = re.sub(';+', ';', tmp)
    tmp = re.sub(';', "|", tmp)
    tmp = re.sub(r'\|+$', '', tmp)
    tmp_split = re.split(r'\|', tmp)
    if tmp_split != headers:
        country_name = tmp_split[0]
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)
    counter += 1
# Задание №5
# Запись данных из полученного словаря в файл
output = open('data.csv', 'w')
file_w = csv.writer(output, delimiter=";")
file_w.writerow(headers)
for key in result_dct.keys():
    file_w.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
output.close()
# Задание №6
#Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)
target_country = input("Введите название страны: ")
print(result_dct[target_country])
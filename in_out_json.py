import json

def writing_json(data_list, name):
   # Записываем в json
   try:
      with open(name, 'a', encoding="utf-8") as file:
         json.dump(data_list, file, indent=4, ensure_ascii=False)
      return 'Ок'
   except:
      print('Не удалось записать файл!')
      return None

def read_json(name):
   try:
      with open(name, 'r', encoding="utf-8") as file:
         text = json.load(file)
      return text
   except:
      print('Не удалось прочитать файл!')
      return None
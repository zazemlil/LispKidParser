from pywinauto import Application
from sys import argv
import re
import time

def close_error_window():
    error_titles = [
        "Lispkidpr"
    ]
    
    for title in error_titles:
        try:
            app = Application(backend="uia").connect(title_re=f".*{title}.*")
            error_window = app.window(title_re=f".*{title}.*")
            error_window.close()
            return
            
        except Exception as e:
            continue
    return

def execute_getResult_and_close(app_path, input_text):
    app = Application(backend="uia").start(app_path)

    main_window = app.window(title="Form1")
    
    all_edits = main_window.descendants(control_type="Edit")
    all_buttons = main_window.descendants(control_type="Button")

    edit9 = all_edits[8]
    edit8 = all_edits[7]
    edit7 = all_edits[6]
    
    execute_button = None

    for button in all_buttons:
        if button.window_text() == "Выполнить":
            execute_button = button
    
    edit9.set_text("")  
    edit9.set_text(input_text) 
    
    execute_button.click()
    
    # ждем пока завершится выполнение кода
    while edit8.get_value() == "" and edit7.get_value() == "":
        time.sleep(0.2)
    
    close_error_window()

    result = edit8.get_value()
    if result == "":
        result = edit7.get_value()

    main_window.close()

    return result


def read_blocks_by_dot_whitespace(file_path):
    """
    Чтение блоков по точке с последующим пробельным символом
    (пробел, табуляция, перенос строки)
    """
    blocks = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Обрабатываем случай, когда файл заканчивается точкой
        if content.strip().endswith('.'):
            content = content[:-1]
        
        # pattern: точка + один или более пробельных символов
        pattern = r'\.\s+'
        raw_blocks = re.split(pattern, content)
        
        for raw_block in raw_blocks:
            # Очищаем строки блока от лишних пробелов и переносов
            clean_block = ' '.join(raw_block.split()).strip()
            if clean_block:
                blocks.append(clean_block)
    return blocks


if __name__ == "__main__":
    if len(argv)==3:
        app_path = argv[1]
        code_path = argv[2]
    elif len(argv)==2:
        app_path = "LispKidPr.exe"
        code_path = argv[1]
    else:
        raise Exception("Неверное число аргументов.")
    
    try:
        blocks = read_blocks_by_dot_whitespace(code_path)
        for block in blocks:
            print(f">>> {execute_getResult_and_close(app_path=app_path, input_text=block)}")
    except Exception as e:
        print(f"Ошибка: {e}")
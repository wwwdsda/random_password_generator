from random import *
import json
from string import *
import tkinter as tk
from tkinter import messagebox
import pyperclip

#비밀번호 문자들 저장

special_characters = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', 
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
]

lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
                     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
                     'y', 'z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

password = ""
copy_buttons = []

#파일을 열어서 데이터 변수에 저장

with open('password.json', 'r', encoding='utf-8') as file:
        data = json.load(file)


#화면에 정보들 표시

def display():
    password_window.delete(1.0, tk.END) 
    
    global data

    site_names = list(data.keys())


    for button in copy_buttons:
        button.pack_forget()  # 기존 copy_button 제거
    
    # 새로운 copy_button 리스트 초기화
    copy_buttons.clear()

    for site_name in site_names:
        for site in data[site_name]:
            site_data = "{0}\n사이트 주소: {1}\n사이트 아이디: {2}\n사이트 비밀번호: {3}".format(
                site_name,site["link"],site["id"],site["password"]
                )
            password_window.insert(tk.END, site_data+"\n\n")  
            copy_button = tk.Button(window, text="비밀번호 복사", command=lambda password=site["password"]: copy_to_clipboard(password))
            copy_button.pack(pady=5)
            copy_buttons.append(copy_button)


#버튼을 누르면 비밀번호가 복사됨
def copy_to_clipboard(password):
        pyperclip.copy(password)
        messagebox.showinfo("성공!",f"비밀번호 '{password}'가 클립보드에 복사되었습니다.")


# 비밀번호 옵션 설정
def check_option():

    options_window = tk.Toplevel(window)  
    options_window.title("비밀번호 생성 옵션")
    
    tk.Label(options_window, text="비밀번호를 생성할 때 포함할 옵션을 선택하세요.").pack(pady=10)

    var1 = tk.BooleanVar()
    var2 = tk.BooleanVar()
    var3 = tk.BooleanVar()

    tk.Label(options_window, text="비밀번호 길이를 입력하세요:").pack(pady=5)
    entry_length = tk.Entry(options_window)
    entry_length.pack(pady=5)
    

    tk.Checkbutton(options_window, text="대문자 포함", variable=var1).pack()
    tk.Checkbutton(options_window, text="숫자 포함", variable=var2).pack()
    tk.Checkbutton(options_window, text="특수기호 포함", variable=var3).pack()

    #save에서 비동기처리 떄문에 password가 바뀔떄까지 기다리기 위함
    def on_confirm():
        generate_password(entry_length.get(), var1.get(), var2.get(), var3.get())
        options_window.destroy()

    confirm_button = tk.Button(options_window, text="확인", command=on_confirm)
    confirm_button.pack(pady=20)

    # options_window가 닫힐 때까지 기다림
    window.wait_window(options_window)


#실제로 비밀번호를 만드는 기능
def generate_password(entry_length, password_upper = False,password_num = False, password_special = False):

    #문자들을 불러옴
    global special_characters
    global lowercase_letters
    global numbers 
    global password
    global length
    
    length = int(entry_length)

    password = ""

    options = ["l"]
    if password_num ==True:
        options.append("n")
    if password_special ==True:
        options.append("s")
    if password_upper == True:
        options.append("u")

    
    for i in range(length+1):
        random_p = sample(options,1)[0]
        if random_p == 'n':
            password += sample(numbers,1)[0]
        if random_p == 's':
            password += sample(special_characters,1)[0]
        if random_p == 'l':
            password += sample(lowercase_letters,1)[0]
        if random_p == 'u':
            password += sample(lowercase_letters,1)[0].upper()
        
    messagebox.showinfo("새로운 비밀번호",f"비밀번호 '{password}'가 생성되었습니다.")

#정보들을 입력함
def generate():
    options_window2 = tk.Toplevel(window)  
    options_window2.title("새로운 사이트 정보")

    tk.Label(options_window2, text="저장할 사이트의 링크를 알려주세요. ").pack(pady=5)
    enter_site_link = tk.Entry(options_window2)
    enter_site_link.pack(pady=5)
    tk.Label(options_window2, text="저장할 사이트의 이름을 알려주세요. ").pack(pady=5)
    enter_site_name = tk.Entry(options_window2)
    enter_site_name.pack(pady=5)
    tk.Label(options_window2, text="사용할 아이디를 알려주세요. ").pack(pady=5)
    enter_site_id = tk.Entry(options_window2)
    enter_site_id.pack(pady=5)

    confirm_button = tk.Button(options_window2, text="확인", command=lambda: 
                               (duplicate_check(enter_site_name.get(),enter_site_id.get(),enter_site_link.get()),options_window2.destroy()))
    confirm_button.pack(pady=20)

    


#사이트 이름과 아이디가 중복인지 확인
def duplicate_check(enter_site_name,enter_site_id,enter_site_link):
    global data
    site_names = list(data.keys())

    if enter_site_name in site_names:
        for site in data[enter_site_name]:
            if site["id"] == enter_site_id:

                options_window3 = tk.Toplevel(window)  
                options_window3.title("비밀번호 변경 옵션")
    
                tk.Label(options_window3, text="이미 동일한 사이트에 같은 아이디가 등록되어 있습니다.").pack(pady=10)

                change = tk.BooleanVar()
                tk.Checkbutton(options_window3, text="비밀번호를 바꾸시겠습니까? ", variable=change).pack()

                confirm_button = tk.Button(options_window3, text="확인", command=lambda: 
                               (duplicate_decision(change.get(),site["password"],enter_site_name,enter_site_id,enter_site_link),options_window3.destroy()))
                confirm_button.pack(pady=20)

                
    else:
        save(enter_site_name,enter_site_id,enter_site_link)
        
def duplicate_decision(decision,password2,enter_site_name,enter_site_id,enter_site_link):
    global data
    if decision == True:
        for site in data[enter_site_name]:
            if site["id"] == enter_site_id:
                data[enter_site_name].remove(site)
                break
        save(enter_site_name,enter_site_id,enter_site_link)
    else:
        messagebox.showinfo("기존 비밀번호","등록된 비밀번호는 {0} 입니다.".format(password2))

def save(enter_site_name,enter_site_id,enter_site_link):
    global data
    global password
    global length

    check_option()
        

    new_site = {"link":enter_site_link,
                "id" : enter_site_id,
                "password" : password}
    if enter_site_name in data:
        data[enter_site_name].append(new_site)
    else:
        data[enter_site_name] = [new_site]
    
    with open('password.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    display()


window = tk.Tk()
window.title("password generator")


password_window = tk.Text(window, height=30, width=100)
password_window.pack(pady=20)

start_button = tk.Button(window, text="비밀번호 생성", command=generate)
start_button.pack(pady=20)


display()

window.mainloop()
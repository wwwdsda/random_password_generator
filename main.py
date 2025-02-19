from random import *
import json
from string import *

#사이트 정보 저장은 사이트이름(사용자 설정), 사이트 링크, 아이디, 비밀번호
#사이트 아이디 비밀번호를 입력받는 기능
#비밀번호의 조건을 확인하는 기능을 추가 (대문자, 길이, 숫자, 특수기호)
#이 조건에 맞는 비밀번호를 생성
#아이디를 저장할 수 있는 기능을 추가
#전에 사용했던 아이디를 똑같이 사용할 지 묻는 기능을 추가
#전에 사용했던 비밀번호를 바꿀지 묻는 기능을 추가
#비밀번호와 아이디를 파일에 추가
#전에 저장했던 사이트가 처음 목록에서 뜨고 그걸 누르면 비밀번호가 복사되는 기능


special_characters = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', 
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'
]

lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
                     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
                     'y', 'z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def check():
    with open('password.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    site_names = list(data.keys())
    print("사이트 이름들:", ", ".join(site_names)) 
    

    want_name = input("어떤 사이트의 아이디와 비밀번호를 확인하고 싶으십니까? ")
    if want_name in site_names:
        for index, site in enumerate(data[want_name]):
            print("\n{0} id{3} : {1}\n{0} 비밀번호{3} : {2}".format(want_name, site["id"], site["password"],index + 1) )
    else:
        print("그 사이트는 저장되어있지 않습니다.")


def generate_password():
    global special_characters
    global lowercase_letters
    global numbers 

    length = input("비밀번호의 길이를 설정하세요: ")
    password_upper = input("대문자를 포함합니까? (Y/N) ")
    password_num = input("숫자를 포함합니까? (Y/N) ")
    password_special = input("특수기호를 포함합니까? (Y/N) ")

    options = ["l"]
    if password_num =="Y":
        options.append("n")
    if password_special =="Y":
        options.append("s")
    if password_upper == "Y":
        options.append("u")

    password = ""
    
    for i in range(int(length)+1):
        random_p = sample(options,1)[0]
        if random_p == 'n':
            password += sample(numbers,1)[0]
        if random_p == 's':
            password += sample(special_characters,1)[0]
        if random_p == 'l':
            password += sample(lowercase_letters,1)[0]
        if random_p == 'u':
            password += sample(lowercase_letters,1)[0].upper()
        
    print("새로운 비밀번호는 {0} 입니다.".format(password))
    return password


def generate():
    with open('password.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    enter_site_link = input("저장할 사이트의 링크를 알려주세요. ")
    enter_site_name = input("저장할 사이트의 이름을 알려주세요. ")
    enter_site_id = input("사용할 아이디를 알려주세요. ")

    site_names = list(data.keys())

    if enter_site_name in site_names:
        for site in data[enter_site_name]:
            if site["id"] == enter_site_id:
                choice = input("이미 동일한 사이트에 같은 아이디가 등록되어 있습니다. 비밀번호를 바꾸시겠습니까? (Y/N) ")
                if choice == 'Y':
                    site["password"] = generate_password()

                else:
                    print("등록된 비밀번호는 {0} 입니다.".format(site["password"]))
    else:
        site_password = generate_password()
        new_site = {"link":enter_site_link,
                    "id" : enter_site_id,
                    "password" : site_password}
        if enter_site_name in data:
            data[enter_site_name].append(new_site)
        else:
            data[enter_site_name] = [new_site]

    with open('password.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
            
            


print("어떤 기능을 사용하시겠습니까?")
option = int(input("1. 비밀번호 확인, 2. 비밀번호 생성 "))


if option == 1:
    check()
    
if option == 2:
    generate()
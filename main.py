from random import *
import json

#사이트 정보 저장은 사이트이름(사용자 설정), 사이트 링크, 아이디, 비밀번호
#사이트 아이디 비밀번호를 입력받는 기능
#비밀번호의 조건을 확인하는 기능을 추가 (대문자, 길이, 숫자, 특수기호)
#이 조건에 맞는 비밀번호를 생성
#아이디를 저장할 수 있는 기능을 추가
#전에 사용했던 아이디를 똑같이 사용할 지 묻는 기능을 추가
#전에 사용했던 비밀번호를 바꿀지 묻는 기능을 추가
#비밀번호와 아이디를 파일에 추가
#전에 저장했던 사이트가 처음 목록에서 뜨고 그걸 누르면 비밀번호가 복사되는 기능

site_details = {
    "사이트1": [
        {
            "link": "http://site1.com",
            "id": "아이디1",
            "password": "패스워드1"
        },
        {
            "link": "http://site1.com",
            "id": "아이디1-1",
            "password": "패스워드1"
        }
    ],
    "사이트2": [
        {
            "link": "http://site2.com",
            "id": "아이디2",
            "password": "패스워드2"
        }
    ]
}



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




# def generate():
#     with open('password.json', 'w', encoding='utf-8') as file:
#         data = json.load(file)
#         enter_site_name = input("저장할 사이트의 이름을 알려주세요. ")
#         enter_site_link = input("저장할 사이트의 링크를 알려주세요. ")
#         enter_site_id = input("사용할 아이디를 알려주세요. ")
        
        
#     #json.dump(data, file, ensure_ascii=False, indent=4)


print("어떤 기능을 사용하시겠습니까?")
option = int(input("1. 비밀번호 확인, 2. 비밀번호 생성 "))


if option == 1:
    check()
    
# if option == 2:
#     generate()
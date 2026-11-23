def show_menu():
    print("=" * 40)
    print("        나만의 퀴즈 게임")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def get_menu_choice():
    while True:
        text = input("선택: ").strip()

        if text == "":
            print("[안내] 아무것도 입력하지 않았습니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("[안내] 숫자만 입력할 수 있습니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        if number < 1 or number > 5:
            print("[안내] 1-5 사이의 숫자를 입력하세요.")
            continue

        return number


def main():
    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 1:
            print("퀴즈 풀기는 아직 준비 중입니다.")
        elif choice == 2:
            print("퀴즈 추가는 아직 준비 중입니다.")
        elif choice == 3:
            print("퀴즈 목록은 아직 준비 중입니다.")
        elif choice == 4:
            print("점수 확인은 아직 준비 중입니다.")
        elif choice == 5:
            print("프로그램을 종료합니다. 안녕히 가세요!")
            break


main()
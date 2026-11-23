class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, number):
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer


def create_default_quizzes():
    return [
        Quiz(
            "소의 위는 몇 개의 방(구획)으로 이루어져 있을까요?",
            ["1개", "2개", "3개", "4개"],
            4,
        ),
        Quiz(
            "소가 삼킨 먹이를 다시 입으로 올려 되새김질하는 것을 무엇이라고 할까요?",
            ["반추", "발효", "배설", "호흡"],
            1,
        ),
        Quiz(
            "돼지고기 부위 중 삼겹살은 어느 부위일까요?",
            ["등", "배", "다리", "목"],
            2,
        ),
        Quiz(
            "소고기 육질 등급 중 가장 높은 등급은 무엇일까요?",
            ["1등급", "1+등급", "1++등급", "3등급"],
            3,
        ),
        Quiz(
            "돼지의 임신 기간은 약 며칠일까요?",
            ["약 30일", "약 114일", "약 200일", "약 285일"],
            2,
        ),
    ]


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


def ask_number(prompt, min_value, max_value):
    while True:
        text = input(prompt).strip()

        if text == "":
            print(f"[안내] 아무것도 입력하지 않았습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"[안내] 숫자만 입력할 수 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        if number < min_value or number > max_value:
            print(f"[안내] {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number


def play_quiz(quizzes):
    if len(quizzes) == 0:
        print("[안내] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return None

    total = len(quizzes)
    correct = 0
    print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

    for number, quiz in enumerate(quizzes, start=1):
        quiz.show(number)
        user_answer = ask_number("정답 입력: ", 1, 4)
        if quiz.is_correct(user_answer):
            print("정답입니다!")
            correct += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    score = correct * 100 // total
    print("=" * 40)
    print(f"결과: {total}문제 중 {correct}문제 정답! ({score}점)")
    print("=" * 40)
    return score


def main():
    quizzes = create_default_quizzes()

    while True:
        show_menu()
        choice = ask_number("선택: ", 1, 5)

        if choice == 1:
            play_quiz(quizzes)
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
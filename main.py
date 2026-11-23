import json

STATE_FILE = "state.json"


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

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }


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


def ask_text(prompt):
    while True:
        text = input(prompt).strip()

        if text == "":
            print("[안내] 아무것도 입력하지 않았습니다. 내용을 입력하세요.")
            continue

        return text


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load_state()

    def load_state(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes = []
            for item in data["quizzes"]:
                choices = item["choices"]
                answer = item["answer"]
                if len(choices) != 4 or answer not in (1, 2, 3, 4):
                    raise ValueError("퀴즈 형식이 올바르지 않습니다.")
                quizzes.append(Quiz(item["question"], choices, answer))

            best_score = data["best_score"]
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")
        except FileNotFoundError:
            self.quizzes = create_default_quizzes()
            self.best_score = None
            print("[안내] 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return
        except (OSError, ValueError, KeyError, TypeError):
            self.quizzes = create_default_quizzes()
            self.best_score = None
            print("[안내] 저장 파일이 손상되어 기본 퀴즈로 초기화합니다.")
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        if best_score is None:
            score_text = "없음"
        else:
            score_text = f"{best_score}점"
        print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고 점수 {score_text})")

    def save_state(self):
        quiz_list = []
        for quiz in self.quizzes:
            quiz_list.append(quiz.to_dict())

        data = {
            "quizzes": quiz_list,
            "best_score": self.best_score,
        }

        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("[안내] 파일을 저장하지 못했습니다.")
            return False

        return True

    def show_menu(self):
        print("=" * 40)
        print("        나만의 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("[안내] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
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

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
            self.save_state()

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")
        question = ask_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = ask_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = ask_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if len(self.quizzes) == 0:
            print("[안내] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def show_best_score(self):
        if self.best_score is None:
            print("[안내] 아직 퀴즈를 풀지 않았습니다.")
            return

        print(f"\n최고 점수: {self.best_score}점")

    def run(self):
        while True:
            self.show_menu()
            choice = ask_number("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.save_state()
                print("프로그램을 종료합니다. 안녕히 가세요!")
                break


def main():
    game = QuizGame()
    game.run()


main()
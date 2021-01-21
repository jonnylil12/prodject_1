import random


class Random_game:


    @staticmethod
    def main():

        print(f"Welcome to the random number game\n{'-' * 30}")

        rounds = 1
        points = 0

        while True:

            print(f"\n\n\t\t\tRound: {rounds}\n{'-' * 30}")

            num_1 = random.randint(1,20)
            num_2 = random.randint(1,20)
            choice = random.randrange(0,4)

            if choice == 0:
                sign , correct_ans = '+' , num_1 + num_2

            elif choice == 1:
                sign , correct_ans = '-' , num_1 - num_2

            elif choice == 2:
                sign ,correct_ans = '/' , float(format(num_1 / num_2 , '.2f'))

            else:
                sign, correct_ans = '*', num_1 * num_2

            user_answer = float(input(f'What is {num_1} {choice} {num_2} ?\n:'))

            if user_answer == correct_ans:
                print(f'That is the correct answer. Points = {(points := points + 1)}')

            else:
                print(f'That is the wrong answer the correct answer is {correct_ans}')

            rounds += 1

# random_game().main()



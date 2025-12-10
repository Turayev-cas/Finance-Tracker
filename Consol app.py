


while True:
    window.mainloop()
    print("\n" * 50)
    print("Текущий баланс: " , balance , " рублей")
    print("Что делаем?")
    print("1- Добавить доход")
    print("2- Добавить расход")
    print("3- Показать историю")
    print("0- Выход")

    choice = input("Твой выбор: ")
    if choice == "1":
        print("Сколько получил?")
        money = input("$")
        balance = balance + float(money)
        history.append(f"Доход: +{money} руб")
        save_data()
        print("успешно добавлено!")
        input("\n Нажми enter епт")


    elif choice == "2":
        print("Сколько потратил?")
        money = input("$")
        balance = balance - float(money)
        history.append(f"Расход: -{money} рублей")
        save_data()
        print('Успешно вычтено!')
        input("\n Нажми enter епт")


    elif choice == "3":
        print("\n Хистори ")
        for operation in history:
            print(operation)
        input("\n Нажми enter епт")



    elif choice == "0":
        print("пока пока попка")

        break

    else:
        print("ошибка")





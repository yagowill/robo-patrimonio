from src.receber import receber

strategy = input("Escolha o que receber:\n1) Tudo\n2) DIME\n: ")
match strategy:
    case 1:
        receber(True, "TUDO")
    case 2:
        receber(True, "DIME")
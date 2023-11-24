from src.receber import receber

strategy = input("Escolha o que receber:\n1) Tudo\n2) DIME\n: ")
if strategy == '1':
    receber("TUDO")
elif strategy == '2':
    receber("DIME")
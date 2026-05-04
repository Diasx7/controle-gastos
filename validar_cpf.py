# função que verifica se um CPF é válido matematicamente
def validar_cpf(cpf):
    # remove pontos e traço
    cpf = cpf.replace(".", "").replace("-", "")

    # cpf tem que ter 11 números
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    # cpf com todos os números iguais é inválido (ex: 111.111.111-11)
    if len(set(cpf)) == 1:
        return False

    # valida o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    primeiro_digito = (soma * 10 % 11) % 10
    if primeiro_digito != int(cpf[9]):
        return False

    # valida o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    segundo_digito = (soma * 10 % 11) % 10
    if segundo_digito != int(cpf[10]):
        return False

    return True
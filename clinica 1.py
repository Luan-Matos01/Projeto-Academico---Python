"""
Nome Completo: Luan Lira de Matos
Matricula: 202502535481
Tema: Sistema de Cadastro de Clínica (Pacientes e Consultas)
Turma: ADS - 3009
 
Sistema de Cadastro de Clínica - Gerenciamento de Pacientes e Consultas
"""


import json # Biblioteca para manipulação de arquivos JSON
from datetime import datetime # Biblioteca para manipulação de datas e horas

"""
Listas globais para armazenar dados
"""
pacientes = []
consultas = []
proximo_id_paciente = 1
proximo_id_consulta = 1


def menu():
    """
    Printa as opções do menu e retorna a escolha do usuário com os espaços em branco removidos: strip().
    
    """
    print("\n" + "="*50)
    print("   SISTEMA DE CADASTRO DE CLÍNICA")
    print("="*50)
    print("1 - Cadastrar Paciente")
    print("2 - Listar Pacientes")
    print("3 - Buscar Paciente")
    print("4 - Atualizar Paciente")
    print("5 - Remover Paciente")
    print("6 - Cadastrar Consulta")
    print("7 - Listar Consultas")
    print("8 - Buscar Consulta")
    print("9 - Remover Consulta")
    print("10 - Estatísticas")
    print("11 - Salvar arquivo")
    print("12 - Carregar arquivo")
    print("0 - Sair")
    print("="*50)
    opcao = input("Escolha uma opção: ").strip()
    return opcao


def validar_nome(nome):
    """
    Valida se o nome não está vazio e contém apenas letras e espaços.
    
    Args:
        nome (str): Nome a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
   
    if not nome or nome.isspace(): # Verifica se o nome tem somente espaços em branco ou está vazio
        return False
    # Permite letras, espaços e acentos
    return all(c.isalpha() or c.isspace() for c in nome) # Retorna true se todos caracteres do nome for letra ou espaço


def validar_idade(idade_str):
    """
    Valida se a idade é um número inteiro positivo.
    
    Args:
        idade_str (str): Idade em formato string
        
    Returns:
        tuple: (bool, int) - (válido, idade convertida)
    """
    try:
        idade = int(idade_str)
        if idade > 0 and idade < 150:
            return True, idade
        return False, 0
    except ValueError: # except ValueError caso usuario digite texto no lugar de numeros
        return False, 0


def validar_telefone(telefone):
    """
    Valida se o telefone não está vazio.
    
    Args:
        telefone (str): Telefone a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
    return bool(telefone and not telefone.isspace()) 


def validar_data(data_str):
    """
    Valida se a data está no formato DD/MM/AAAA.
    
    Args:
        data_str (str): Data em formato string
        
    Returns:
        bool: True se válido, False caso contrário
    """
    try:
        datetime.strptime(data_str, "%d/%m/%Y") #Conversão de texto para data
        return True
    except ValueError:
        return False


def cadastrar_paciente():
    """
    Cadastra um novo paciente no sistema com validações.
    Solicita nome, idade, telefone e endereço.
    Atribui um ID único automaticamente.
    """
    global proximo_id_paciente
    
    print("\n--- CADASTRAR NOVO PACIENTE ---")
    
    # Validação do nome
    nome = input("Nome completo: ").strip()
    if not validar_nome(nome):
        print("Erro: Nome inválido. Digite apenas letras e espaços.")
        return
    
    # Validação da idade
    idade_str = input("Idade: ").strip()
    valido, idade = validar_idade(idade_str)
    if not valido:
        print("Erro: Idade inválida. Digite um número entre 1 e 149.")
        return
    
    # Validação do telefone
    telefone = input("Telefone (com DDD): ").strip()
    if not validar_telefone(telefone):
        print("Erro: Telefone não pode estar vazio.")
        return
    
    # Validação do endereço
    endereco = input("Endereço: ").strip()
    if not endereco or endereco.isspace():
        print("Erro: Endereço não pode estar vazio.")
        return
    
    # Criar dicionário do paciente
    paciente = {
        "id": proximo_id_paciente,
        "nome": nome.title(), # .title() para deixar a primeira letra de cada palavra maiúscula
        "idade": idade,
        "telefone": telefone,
        "endereco": endereco
    }
    
    pacientes.append(paciente) # Adiciona o paciente na lista de pacientes
    proximo_id_paciente += 1
    
    print(f"Paciente cadastrado com sucesso! ID: {paciente['id']}")

def listar_pacientes():
    """
    Lista todos os pacientes cadastrados de forma ordenada por nome.
    Exibe ID, nome, idade, telefone e endereço de cada paciente.
    """
    if not pacientes:
        print("\nNenhum paciente cadastrado.")
        return
    
    print("\n--- LISTA DE PACIENTES ---")
    # Sorted = Ordenar por nome | Key = define como vai ser ordenado | Lambda = função anônima |
    # Lower = converter para minúsculo
    pacientes_ordenados = sorted(pacientes, key=lambda p: p["nome"].lower())
    
    for paciente in pacientes_ordenados:
        print(f"\nID: {paciente['id']}")
        print(f"Nome: {paciente['nome']}")
        print(f"Idade: {paciente['idade']} anos")
        print(f"Telefone: {paciente['telefone']}")
        print(f"Endereço: {paciente['endereco']}")
        print("-" * 40)


def buscar_paciente():
    """
    Busca pacientes por nome (busca parcial, case-insensitive).
    Exibe todos os pacientes que contenham o termo buscado no nome.
    """
    if not pacientes:
        print("\nNenhum paciente cadastrado.")
        return
    
    termo = input("\nDigite o nome ou parte do nome: ").strip().lower()
    
    resultados = [p for p in pacientes if termo in p["nome"].lower()]
    
    if not resultados:
        print(f"Nenhum paciente encontrado com '{termo}'.")
        return
    
    print(f"\n--- RESULTADOS DA BUSCA ({len(resultados)} encontrado(s)) ---")
    for paciente in resultados:
        print(f"\nID: {paciente['id']}")
        print(f"Nome: {paciente['nome']}")
        print(f"Idade: {paciente['idade']} anos")
        print(f"Telefone: {paciente['telefone']}")
        print(f"Endereço: {paciente['endereco']}")
        print("-" * 40)


def atualizar_paciente():
    """
    Atualiza os dados de um paciente existente.
    Permite atualizar nome, idade, telefone e endereço.
    """
    if not pacientes:
        print("\nNenhum paciente cadastrado.")
        return
    
    try:
        id_paciente = int(input("\nDigite o ID do paciente: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return
    
    # Buscar paciente pelo ID
    paciente = None
    for p in pacientes:
        if p["id"] == id_paciente:
            paciente = p
            break
    
    if not paciente:
        print(f"Paciente com ID {id_paciente} não encontrado.")
        return
    
    print(f"\nPaciente encontrado: {paciente['nome']}")
    print("Deixe em branco para manter o valor atual.")
    
    # Atualizar nome
    novo_nome = input(f"Novo nome [{paciente['nome']}]: ").strip()
    if novo_nome:
        if validar_nome(novo_nome):
            paciente["nome"] = novo_nome.title()
        else:
            print("Nome inválido, mantendo valor anterior.")
    
    # Atualizar idade
    nova_idade = input(f"Nova idade [{paciente['idade']}]: ").strip()
    if nova_idade:
        valido, idade = validar_idade(nova_idade)
        if valido:
            paciente["idade"] = idade
        else:
            print("Idade inválida, mantendo valor anterior.")
    
    # Atualizar telefone
    novo_telefone = input(f"Novo telefone [{paciente['telefone']}]: ").strip()
    if novo_telefone:
        if validar_telefone(novo_telefone):
            paciente["telefone"] = novo_telefone
        else:
            print("Telefone inválido, mantendo valor anterior.")
    
    # Atualizar endereço
    novo_endereco = input(f"Novo endereço [{paciente['endereco']}]: ").strip()
    if novo_endereco:
        paciente["endereco"] = novo_endereco
    
    print("Paciente atualizado com sucesso!")


def remover_paciente():
    """
    Remove um paciente do sistema pelo ID.
    Solicita confirmação antes de remover.
    """
    if not pacientes:
        print("\nNenhum paciente cadastrado.")
        return
    
    try:
        id_paciente = int(input("\nDigite o ID do paciente a remover: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return
    
    # Buscar e remover paciente
    for i, p in enumerate(pacientes):
        if p["id"] == id_paciente:
            print(f"\nPaciente encontrado: {p['nome']}")
            confirmacao = input("Confirma a remoção? (s/n): ").strip().lower()
            
            if confirmacao == 's':
                pacientes.pop(i) # Remove o paciente da lista
                print("Paciente removido com sucesso!")
            else:
                print("Remoção cancelada.")
            return
    
    print(f"Paciente com ID {id_paciente} não encontrado.")


def cadastrar_consulta():
    """
    Cadastra uma nova consulta vinculada a um paciente.
    Solicita ID do paciente, data, hora e especialidade.
    """
    global proximo_id_consulta 
    
    if not pacientes:
        print("\nÉ necessário cadastrar pacientes antes de agendar consultas.")
        return
    
    print("\n--- CADASTRAR NOVA CONSULTA ---")
    
    # Validar ID do paciente
    try:
        id_paciente = int(input("ID do paciente: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return
    
    # Verificar se paciente existe
    paciente_existe = any(p["id"] == id_paciente for p in pacientes)
    if not paciente_existe:
        print(f"Paciente com ID {id_paciente} não encontrado.")
        return
    
    # Validar data
    data = input("Data da consulta (DD/MM/AAAA): ").strip()
    if not validar_data(data):
        print("Erro: Data inválida. Use o formato DD/MM/AAAA.")
        return
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y").date()
    except ValueError:
        print("Erro: Data inválida. Use o formato DD/MM/AAAA.")
        return
    # Não permite datas anteriores à data atual
    if data_obj < datetime.now().date():
        print("Erro: A data da consulta não pode ser anterior à data de hoje.")
        return
    
     # Validar hora
    hora = input("Hora da consulta (HH:MM): ").strip()
    try:
        if not ":" in hora or len(hora.split(":")) != 2:
            print("Erro: Hora inválida. Use o formato HH:MM.")
            return
            
        horas, minutos = hora.split(":")
        if not (horas.isdigit() and minutos.isdigit() and len(minutos) == 2 and len(horas) == 2):
            print("Erro: Hora inválida. Use o formato HH:MM (exemplo: 09:30, 14:45)")
            return
            
        hora_obj = datetime.strptime(hora, "%H:%M").time()
        
        # Valida se hora está entre 00:00 e 23:59
        if not (0 <= int(horas) <= 23 and 0 <= int(minutos) <= 59):
            print("Erro: Hora inválida. Use valores entre 00:00 e 23:59")
            return
            
    except ValueError:
        print("Erro: Hora inválida. Use o formato HH:MM (exemplo: 09:30, 14:45)")
        return
    
    # Se a consulta for para hoje, não permite hora anterior ou igual à hora atual
    if data_obj == datetime.now().date() and hora_obj <= datetime.now().time():
        print("Erro: A hora da consulta deve ser posterior ao horário atual.")
        return

    # Especialidade
    especialidade = input("Especialidade: ").strip()
    if not especialidade or especialidade.isspace():
        print("Erro: Especialidade não pode estar vazia.")
        return
    
    # Verificar se já existe consulta dessa especialidade nesse horário
    # Não precisa global consultas, pois só lê a lista
    for consulta in consultas:
        if consulta["data"] == data and consulta["hora"] == hora and consulta["especialidade"].lower() == especialidade.lower():
            print("Erro: Já existe uma consulta dessa especialidade agendada para este horário.")
            return

    # Criar dicionário da consulta
    consulta = {
        "id": proximo_id_consulta,
        "id_paciente": id_paciente,
        "data": data,
        "hora": hora,
        "especialidade": especialidade.title()
    }
    
    consultas.append(consulta)
    proximo_id_consulta += 1
    
    print(f"Consulta agendada com sucesso! ID: {consulta['id']}")


def listar_consultas():
    """
    Lista todas as consultas cadastradas ordenadas por data.
    Exibe ID, paciente, data, hora e especialidade.
    """
    if not consultas:
        print("\nNenhuma consulta cadastrada.")
        return
    
    print("\n--- LISTA DE CONSULTAS ---")
    
    for consulta in consultas:
        # Buscar nome do paciente
        paciente = next((p for p in pacientes if p["id"] == consulta["id_paciente"]), None)
        nome_paciente = paciente["nome"] if paciente else "Paciente não encontrado"
        
        print(f"\nID Consulta: {consulta['id']}")
        print(f"Paciente: {nome_paciente} (ID: {consulta['id_paciente']})")
        print(f"Data: {consulta['data']}")
        print(f"Hora: {consulta['hora']}")
        print(f"Especialidade: {consulta['especialidade']}")
        print("-" * 40)


def buscar_consulta():
    """
    Busca consultas por ID do paciente ou especialidade.
    """
    if not consultas:
        print("\nNenhuma consulta cadastrada.")
        return
    
    print("\n--- BUSCAR CONSULTA ---")
    print("1 - Buscar por ID do paciente")
    print("2 - Buscar por especialidade")
    opcao = input("Escolha: ").strip()
    
    resultados = []
    
    if opcao == "1":
        try:
            id_paciente = int(input("Digite o ID do paciente: ").strip())
            resultados = [c for c in consultas if c["id_paciente"] == id_paciente]
        except ValueError:
            print("Erro: ID inválido.")
            return
    elif opcao == "2":
        termo = input("Digite a especialidade: ").strip().lower()
        resultados = [c for c in consultas if termo in c["especialidade"].lower()]
    else:
        print("Opção inválida.")
        return
    
    if not resultados:
        print("Nenhuma consulta encontrada.")
        return
    
    print(f"\n--- RESULTADOS ({len(resultados)} encontrada(s)) ---")
    for consulta in resultados:
        paciente = next((p for p in pacientes if p["id"] == consulta["id_paciente"]), None)
        nome_paciente = paciente["nome"] if paciente else "Paciente não encontrado"
        
        print(f"\nID Consulta: {consulta['id']}")
        print(f"Paciente: {nome_paciente}")
        print(f"Data: {consulta['data']}")
        print(f"Hora: {consulta['hora']}")
        print(f"Especialidade: {consulta['especialidade']}")
        print("-" * 40)


def remover_consulta():
    """
    Remove uma consulta do sistema pelo ID.
    Solicita confirmação antes de remover.
    """
    if not consultas:
        print("\nNenhuma consulta cadastrada.")
        return
    
    try:
        id_consulta = int(input("\nDigite o ID da consulta a remover: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return
    
    # Não precisa global consultas, pois só lê e remove itens da lista
    for i, c in enumerate(consultas):
        if c["id"] == id_consulta:
            print(f"\nConsulta encontrada:")
            print(f"Data: {c['data']} - Hora: {c['hora']}")
            print(f"Especialidade: {c['especialidade']}")
            
            confirmacao = input("Confirma a remoção? (s/n): ").strip().lower()
            
            if confirmacao == 's':
                consultas.pop(i)
                print("Consulta removida com sucesso!")
            else:
                print("Remoção cancelada.")
            return
    
    print(f"Consulta com ID {id_consulta} não encontrada.")


def estatisticas():
    """
    Exibe estatísticas do sistema:
    - Total de pacientes e consultas
    - Média de idade dos pacientes
    - Paciente mais jovem e mais velho
    - Especialidade mais procurada
    """
    print("\n" + "="*50)

    print("="*50)
    
    # Estatísticas de pacientes
    total_pacientes = len(pacientes)
    print(f"\nTotal de pacientes: {total_pacientes}")
    
    if total_pacientes > 0:
        idades = [p["idade"] for p in pacientes]
        media_idade = sum(idades) / len(idades) # Cálculo da média das idades onde sum soma todas idades e len conta quantas idades tem
        idade_min = min(idades)
        idade_max = max(idades)
        
        print(f"Média de idade: {media_idade:.1f} anos") # :.1f = formatação para 1 casa decimal
        print(f"Paciente mais jovem: {idade_min} anos")
        print(f"Paciente mais velho: {idade_max} anos")
    
    # Estatísticas de consultas
    total_consultas = len(consultas)
    print(f"\nTotal de consultas: {total_consultas}")
    
    if total_consultas > 0:
        especialidades = [c["especialidade"] for c in consultas]
        especialidade_mais_comum = max(set(especialidades), key=especialidades.count) # max = maior valor | set = conjunto de valores únicos | key = função para contar ocorrências
        contagem = especialidades.count(especialidade_mais_comum) # Conta quantas vezes a especialidade mais comum aparece
        
        print(f"Especialidade mais procurada: {especialidade_mais_comum} ({contagem} consultas)")
    
    print("="*50)


def salvar_arquivo():
    """
    Salva os dados de pacientes e consultas em arquivo JSON.
    """
    try:
        dados = {
            "pacientes": pacientes,
            "consultas": consultas,
            "proximo_id_paciente": proximo_id_paciente,
            "proximo_id_consulta": proximo_id_consulta
        }
        
        with open("clinica_dados.json", "w", encoding="utf-8") as arquivo: # encoding="utf-8" para suportar caracteres especiais
            json.dump(dados, arquivo, ensure_ascii=False, indent=2) # ensure_ascii=False para suportar caracteres especiais, indent=2 para formatar o JSON
        
        print("Dados salvos com sucesso em 'clinica_dados.json'!")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")


def carregar_arquivo():
    global pacientes, consultas, proximo_id_paciente, proximo_id_consulta

    try:
        with open("clinica_dados.json", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if not conteudo:
                print("Arquivo 'clinica_dados.json' vazio. Iniciando com dados vazios.")
                pacientes = []
                consultas = []
                proximo_id_paciente = 1
                proximo_id_consulta = 1
                return

            dados = json.loads(conteudo)

        pacientes = dados.get("pacientes", [])
        consultas = dados.get("consultas", [])
        proximo_id_paciente = dados.get("proximo_id_paciente", 1)
        proximo_id_consulta = dados.get("proximo_id_consulta", 1)

        print(f"Dados carregados com sucesso!")
        print(f"Pacientes: {len(pacientes)}")
        print(f"Consultas: {len(consultas)}")
    except json.JSONDecodeError:
        print("Arquivo 'clinica_dados.json' inválido ou corrompido. Usando dados vazios.")
        pacientes = []
        consultas = []
        proximo_id_paciente = 1
        proximo_id_consulta = 1
    except FileNotFoundError: # Caso o arquivo não exista
        print("Arquivo 'clinica_dados.json' não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")


def main():
    """
    Função principal que controla o fluxo do programa.
    Exibe o menu e executa as opções escolhidas pelo usuário.
    """
    print("\nBem-vindo ao Sistema de Cadastro de Clínica!")
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            cadastrar_paciente()
        elif opcao == "2":
            listar_pacientes()
        elif opcao == "3":
            buscar_paciente()
        elif opcao == "4":
            atualizar_paciente()
        elif opcao == "5":
            remover_paciente()
        elif opcao == "6":
            cadastrar_consulta()
        elif opcao == "7":
            listar_consultas()
        elif opcao == "8":
            buscar_consulta()
        elif opcao == "9":
            remover_consulta()
        elif opcao == "10":
            estatisticas()
        elif opcao == "11":
            salvar_arquivo()
        elif opcao == "12":
            carregar_arquivo()
        elif opcao == "0":
            print("\nEncerrando o sistema...")
            print("Obrigado por usar o Sistema de Cadastro de Clínica!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
        
        input("\nPressione ENTER para continuar...")


# Execução do programa
if __name__ == "__main__":
    main()
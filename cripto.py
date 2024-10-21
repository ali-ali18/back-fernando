import json

#Fernando Wellington Cardoso, Alisson Camargo Santos

class GerenciadorAlunos:
    def __init__(self, arquivo):
        
        self.arquivo = arquivo #Define o nome do arquivo Json
        self.alunos = self.carregar_alunos() # Carrega alunos do arquivo 
        

    def carregar_alunos(self):
        #Tenta abrir o arquivo e carregar os alunos
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            #Retorna um dicionário vazio se não existir
            return {}

    def adicionar_aluno(self, matricula, nome, nivel, idade, boletim):
        # Verifica se a matrícula não está vazia e se o aluno já existe
        print(f' está adicionando {self.arquivo}')
        if matricula == '':
            print("Erro: Matrícula não pode estar vazia.")
            return
        if matricula in self.alunos:
            print(f"Erro: Aluno com matrícula {matricula} já existe.")
            return
         # Verifica se as notas são válidas
        for diciplina, notas in boletim.items():
            for nota in notas:
                if nota < 0:
                    print("Erro: Nota negativa não é permitida.")
                    return
        # Adiciona o aluno e salva no arquivo
        self.alunos[matricula] = {
            'nome_completo': nome,
            'nivel': nivel,
            'idade': idade,
            'boletim': boletim,
        }
        self.salvar_alunos()

    def salvar_alunos(self):
         # Salva os dados dos alunos no arquivo JSON
        print(f'está salvando {self.arquivo}')
        with open(self.arquivo, 'w', encoding="utf-8") as f:
            json.dump(self.alunos,  f, ensure_ascii=False)

    def alterar_nota(self, matricula, disciplina, nova_nota, avaliacao_index):
        # Altera a nota de uma disciplina específica para um aluno
        if matricula in self.alunos:
            if disciplina in self.alunos[matricula]["boletim"]:
                if 0 <= avaliacao_index < len(self.alunos[matricula]["boletim"][disciplina]):
                    self.alunos[matricula]["boletim"][disciplina][avaliacao_index] = nova_nota
                    print(f"Nota de {disciplina} alterada com sucesso para {nova_nota}!")
                else:
                    print(f"Erro: Índice da avaliação inválido. Escolha um número entre 0 e {len(self.alunos[matricula]['boletim'][disciplina]) - 1}.")
            else:
                print(f"Erro: Disciplina {disciplina} não encontrada no boletim do aluno.")
        else:
            print(f"Erro: Matrícula {matricula} não encontrada.")

    def media_aluno(self, matricula, disciplina, limite):
        # Calcula a média das notas de um aluno em uma disciplina específica
        if matricula not in self.alunos:
            return f"Erro: Matrícula {matricula} não encontrada."

        notas = self.alunos[matricula]['boletim'].get(disciplina, [])

        if len(notas) == 0:
            return f"Erro: Não há notas para a disciplina {disciplina}."

        # Verifica se há nota negativa
        for nota in notas:
            if nota < 0:
                return "Erro: Nota negativa não é permitida."

        media = sum(notas) / len(notas)
        # Retorna a situação do aluno com base na média
        if media >= limite:
            return f"Média em {disciplina}: {media} - Aprovado"
        else:
            return f"Média em {disciplina}: {media} - Reprovado"


    def deletar_aluno(self, matricula):
        # Deleta um aluno pelo número de matrícula
        if matricula in self.alunos:
            del self.alunos[matricula]
            self.salvar_alunos()
            print(f"Aluno com matrícula {matricula} foi deletado com sucesso.")
        else:
            print(f"Erro: Matrícula {matricula} não encontrada.")

    def criar_item_vazio(self):
        # Cria um registro de aluno vazio
        aluno_vazio = {
        'nome_completo': '',
        'nivel': '',
        'idade': 0,
        'boletim': {
            'Matemática': [],
            'Português': [],
            'Ciências': [],
            'História': [],
            'Geografia': []
        }
    }
        return aluno_vazio

    def exibir_todos(self):
        if not self.alunos:
            print("Nenhum aluno cadastrado.")
        else:
            for matricula, dados in self.alunos.items():
                print(f"\nMatrícula: {matricula}")
                print(f"Nome: {dados['nome_completo']}")
                print(f"Nível: {dados['nivel']}")
                print(f"Idade: {dados['idade']}")
                print("Boletim:")
                for disciplina, notas in dados['boletim'].items():
                    print(f"  {disciplina}: {notas}")


class Menu:
    def __init__(self):
        self.gerenciador = GerenciadorAlunos("aluno.json")
        self.opcoes = {
            '1': self.solicitar_dados_aluno,
            '2': self.solicitar_alteracao_nota,
            '3': self.solicitar_media_aluno,
            '4': self.solicitar_deletar_aluno,
            '5': self.gerenciador.exibir_todos,
            '6': self.criar_item_vazio,  # Corrigido para chamar o método que salva o aluno vazio
            '7': self.sair
        }

    def mostrar_menu(self):
        while True:
            print("\nMenu:")
            print("1. Adicionar Aluno")
            print("2. Alterar Nota")
            print("3. Calcular Média do Aluno")
            print("4. Deletar Aluno")
            print("5. Exibir Todos os Alunos")
            print("6. Criar Item Vazio")
            print("7. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao in self.opcoes:
                self.opcoes[opcao]()  # Chama a função associada à opção
            else:
                print("Opção inválida. Tente novamente.")

    def solicitar_dados_aluno(self):
        matricula = input("Digite a matrícula do aluno: ")
        nome = input("Digite o nome do aluno: ")
        nivel = input("Digite o nível do aluno: ")
        idade = int(input("Digite a idade do aluno: "))

        boletim = {}
        for disciplina in ['Matemática', 'Português', 'Ciências', 'História', 'Geografia']:
            notas = input(f"Digite as notas para {disciplina} (separadas por vírgula): ")
            boletim[disciplina] = [float(nota) for nota in notas.split(",")]

        self.gerenciador.adicionar_aluno(matricula, nome, nivel, idade, boletim)

    def solicitar_alteracao_nota(self):
        matricula = input("Digite a matrícula do aluno: ").strip()
        disciplina = input("Digite a disciplina: ").strip()

        if matricula not in self.gerenciador.alunos:
            print("Erro: Matrícula não encontrada.")
            return

        if disciplina not in self.gerenciador.alunos[matricula]["boletim"]:
            print(f"Erro: Disciplina {disciplina} não encontrada no boletim.")
            return

        notas = self.gerenciador.alunos[matricula]["boletim"][disciplina]
        print(f"Notas atuais em {disciplina}: {notas}")

        try:
            avaliacao_index = int(input(f"Digite o índice da avaliação que deseja alterar (0 a {len(notas) - 1}): "))
            nova_nota = float(input("Digite a nova nota: "))
            if nova_nota < 0:
                print("Erro: Nota negativa não é permitida.")
                return
            self.gerenciador.alterar_nota(matricula, disciplina, nova_nota, avaliacao_index)
        except ValueError:
            print("Erro: O índice deve ser um número inteiro.")
            return

    def solicitar_media_aluno(self):
        matricula = input("Digite a matrícula do aluno: ")
        disciplina = input("Digite a disciplina: ")
        nota_minima = float(input("Digite a nota mínima para aprovação: "))

        resultado = self.gerenciador.media_aluno(matricula, disciplina, nota_minima)
        print(resultado)

    def solicitar_deletar_aluno(self):
        matricula = input("Digite a matrícula do aluno que deseja deletar: ").strip()
        self.gerenciador.deletar_aluno(matricula)

    def criar_item_vazio(self):
        aluno_vazio = self.gerenciador.criar_item_vazio()
        # Adiciona o aluno vazio na lista de alunos
        matricula = input("Digite a matrícula do aluno vazio: ")
        self.gerenciador.alunos[matricula] = aluno_vazio
        self.gerenciador.salvar_alunos()  # Salva no arquivo
        print(f"Aluno vazio com matrícula {matricula} criado e salvo com sucesso.")

    def sair(self):
        print("Saindo do programa.")
        exit()  # Adiciona o comando para sair do programa


if __name__ == "__main__":
    menu = Menu()
    menu.mostrar_menu()








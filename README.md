# projeto-arquitetura-de-TI

Integrantes do Grupo 

Leonardo Da Silva Adami
Guilherme Lacerda Araújo Da Silva 
Adriano Bruno Pacheco 

# Explicação do Projeto 

Análise do Funcionamento do Script gerenciador_chaves.py

Este documento detalha a estrutura e a lógica do script Python gerenciador_chaves.py, criado para gerenciar a ocupação de quartos de um hotel.

1. Visão Geral e Estrutura
O script é construído em torno de uma classe chamada HotelKeyManager. O uso de uma classe é uma prática de Programação Orientada a Objetos (POO) que ajuda a organizar o código de forma lógica. A classe agrupa os dados (o estado dos quartos) e as operações (check-in, check-out) em uma única entidade.

Os componentes principais do script são:

A Classe HotelKeyManager: Contém toda a lógica de negócio para gerenciar o hotel.

A Função main_menu: Responsável pela interface com o usuário no terminal.

O Bloco if __name__ == "__main__": É o ponto de partida que executa o programa.

2. Persistência de Dados: O Arquivo hotel_data.json
Para que o estado do hotel (quais quartos estão ocupados, etc.) não seja perdido toda vez que o programa fecha, as informações são salvas em um arquivo chamado hotel_data.json.

Formato JSON: JSON (JavaScript Object Notation) foi escolhido por ser um formato de texto leve e de fácil leitura tanto para humanos quanto para máquinas. Python tem bibliotecas nativas (json) que tornam muito simples a tarefa de ler e escrever nesse formato.

Estrutura do JSON: O arquivo tem dois elementos principais:

"rooms": Um objeto (dicionário em Python) onde cada chave é o número do quarto. O valor associado a cada chave contém os detalhes do quarto: status, guest_name e check_in_time.

"history": Uma lista que armazena um registro de cada check-out, guardando os detalhes da estadia.

3. Detalhamento das Funções (Métodos da Classe)
__init__(self, total_rooms=20)
Este é o construtor da classe. É executado automaticamente quando um novo objeto HotelKeyManager é criado.

Ele define o número total de quartos e chama o método _load_data() para carregar as informações do hotel_data.json ou criar um novo arquivo caso ele não exista.

_load_data(self)
Verifica se o arquivo hotel_data.json existe.

Se não existe: Ele cria uma estrutura de dados padrão (um dicionário Python) com todos os quartos definidos como "available" (disponíveis) e salva essa estrutura no novo arquivo.

Se existe: Ele abre o arquivo, lê o conteúdo JSON e o carrega para a memória (no atributo self.data).

_save_data(self, data_to_save)
Um método auxiliar e muito importante. Sua única função é receber os dados do hotel e escrevê-los no arquivo hotel_data.json. É chamado sempre que uma alteração importante é feita (check-in ou check-out).

check_in(self, room_number, guest_name)
Recebe o número do quarto e o nome do hóspede.

Validação: Verifica se o quarto existe e se já não está ocupado. Se alguma dessas condições for verdadeira, exibe uma mensagem de erro.

Atualização: Se o quarto estiver disponível, ele atualiza o status para "occupied", armazena o nome do hóspede e registra a data e hora do check-in usando datetime.now().isoformat().

Persistência: Chama _save_data() para salvar as alterações no arquivo.

check_out(self, room_number)
Recebe o número do quarto.

Validação: Verifica se o quarto existe e se ele está realmente ocupado.

Registro no Histórico: Antes de limpar os dados do quarto, ele cria um registro da estadia (quarto, hóspede, horários) e o adiciona à lista "history".

Limpeza: Reseta o status do quarto para "available" e apaga o nome do hóspede e o horário de check-in.

Persistência: Chama _save_data() para salvar o novo estado do hotel.

display_status(self)
Responsável por exibir a tabela com o estado de todos os quartos.

Ele percorre os dados em self.data["rooms"], formatando cada linha para que a saída fique alinhada e fácil de ler no terminal.

Para quartos ocupados, ele formata a data de check-in para um formato mais amigável (dd/mm/aaaa HH:MM).

4. Interface e Execução
main_menu(manager)
Funciona como o "motor" da interface do usuário.

Usa um loop infinito (while True) para manter o menu sempre ativo até que o usuário escolha a opção "Sair".

A cada ciclo, ele imprime as opções, captura a entrada do usuário e, com base na escolha, chama o método apropriado do objeto manager (que é uma instância da classe HotelKeyManager).

if __name__ == "__main__"
Este é um bloco padrão em Python que indica o ponto de início da execução do script.

O código dentro deste if só é executado quando o arquivo é chamado diretamente (e não quando é importado por outro script).

Ele primeiro cria a instância da classe (hotel_manager = HotelKeyManager()) e depois passa essa instância para a função main_menu() para iniciar a interação com o usuário.

----

# Automação com GitHub Actions e Docker Hub

Uma parte crucial de projetos modernos é a automação. Este projeto utiliza o GitHub Actions para automatizar a criação e publicação da imagem Docker no Docker Hub, um processo conhecido como CI/CD (Integração Contínua / Entrega Contínua).

Como Funciona o Fluxo de Automação:
Gatilho (Trigger): O processo é iniciado automaticamente sempre que uma nova alteração é enviada (push) para o repositório principal (main branch) no GitHub.

Configuração do Ambiente: O GitHub Actions inicializa um ambiente virtual (um "runner"). Este ambiente faz o checkout (download) da versão mais recente do código do repositório.

Login Seguro no Docker Hub: O workflow se autentica de forma segura no Docker Hub. As credenciais (usuário e token de acesso) não são escritas diretamente no código, mas sim armazenadas como "Secrets" nas configurações do repositório do GitHub. Isso garante que as senhas não fiquem expostas.

Build e Push da Imagem: Utilizando o Dockerfile presente no projeto, o GitHub Actions executa os seguintes passos:

Build: Ele constrói a imagem Docker, seguindo as instruções do Dockerfile (copiando o script, definindo o ambiente, etc.).

Push: Após a construção bem-sucedida, a nova imagem é enviada (push) para o seu repositório no Docker Hub. A imagem é geralmente marcada com uma tag, como latest ou um número de versão, para fácil identificação.

Vantagens dessa Automação:
Consistência: Garante que toda imagem publicada seja gerada exatamente da mesma forma, eliminando erros manuais.

Agilidade: Desenvolvedores podem focar em escrever código. Assim que a alteração é enviada, o processo de publicação é automático.

Confiabilidade: A versão mais recente do código está sempre disponível como uma imagem Docker pronta para ser executada em qualquer lugar.

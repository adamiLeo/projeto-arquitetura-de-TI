# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

# Define o nome do arquivo que armazenará os dados
DATA_FILE = "hotel_data.json"

class HotelKeyManager:
    """
    Gerencia as operações de check-in, check-out e status dos quartos de um hotel.
    Os dados são persistidos em um arquivo JSON.
    """

    def __init__(self, total_rooms=20):
        """
        Inicializa o gerenciador. Carrega os dados existentes ou cria um novo
        arquivo de dados se ele não existir.
        """
        self.total_rooms = total_rooms
        self.data = self._load_data()

    def _load_data(self):
        """
        Carrega os dados do arquivo JSON. Se o arquivo não existir,
        cria uma estrutura de dados padrão para todos os quartos.
        """
        if not os.path.exists(DATA_FILE):
            print(f"Arquivo '{DATA_FILE}' não encontrado. Criando um novo com {self.total_rooms} quartos.")
            # Estrutura inicial dos dados
            initial_data = {
                "rooms": {},
                "history": []
            }
            for i in range(1, self.total_rooms + 1):
                initial_data["rooms"][str(i)] = {
                    "status": "available",
                    "guest_name": None,
                    "check_in_time": None
                }
            self._save_data(initial_data)
            return initial_data
        
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao ler o arquivo de dados: {e}. O programa será encerrado.")
            exit(1) # Encerra se não conseguir ler o arquivo

    def _save_data(self, data_to_save):
        """Salva o dicionário de dados atual no arquivo JSON."""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar os dados: {e}")

    def check_in(self, room_number, guest_name):
        """
        Realiza o check-in de um hóspede em um quarto específico.
        """
        room_str = str(room_number)
        if room_str not in self.data["rooms"]:
            print(f"Erro: O quarto {room_number} não existe.")
            return

        room = self.data["rooms"][room_str]
        if room["status"] == "occupied":
            print(f"Erro: O quarto {room_number} já está ocupado por {room['guest_name']}.")
            return

        room["status"] = "occupied"
        room["guest_name"] = guest_name
        room["check_in_time"] = datetime.now().isoformat() # Formato padrão ISO 8601
        
        self._save_data(self.data)
        print(f"\nCheck-in realizado com sucesso! Hóspede '{guest_name}' alocado no quarto {room_number}.")

    def check_out(self, room_number):
        """
        Realiza o check-out de um quarto, tornando-o disponível.
        """
        room_str = str(room_number)
        if room_str not in self.data["rooms"]:
            print(f"Erro: O quarto {room_number} não existe.")
            return

        room = self.data["rooms"][room_str]
        if room["status"] == "available":
            print(f"Erro: O quarto {room_number} já está disponível.")
            return

        # Registra a estadia no histórico
        log_entry = {
            "room_number": room_number,
            "guest_name": room["guest_name"],
            "check_in_time": room["check_in_time"],
            "check_out_time": datetime.now().isoformat()
        }
        self.data["history"].append(log_entry)

        # Reseta o status do quarto
        room["status"] = "available"
        room["guest_name"] = None
        room["check_in_time"] = None

        self._save_data(self.data)
        print(f"\nCheck-out do quarto {room_number} realizado com sucesso.")

    def display_status(self):
        """
        Exibe o status atual de todos os quartos de forma organizada.
        """
        print("\n--- Status Atual dos Quartos ---")
        print("-" * 70)
        print(f"{'Quarto':<10} | {'Status':<15} | {'Hóspede':<25} | {'Check-in':<20}")
        print("-" * 70)

        # Ordena os quartos numericamente para exibição
        sorted_rooms = sorted(self.data["rooms"].items(), key=lambda item: int(item[0]))

        for room_num, details in sorted_rooms:
            guest = details['guest_name'] or 'N/A'
            check_in = details['check_in_time'] or 'N/A'
            if check_in != 'N/A':
                 # Formata a data para melhor leitura
                 check_in_dt = datetime.fromisoformat(check_in)
                 check_in = check_in_dt.strftime('%d/%m/%Y %H:%M')

            print(f"{room_num:<10} | {details['status'].capitalize():<15} | {guest:<25} | {check_in:<20}")
        
        print("-" * 70)


def main_menu(manager):
    """
    Exibe o menu principal e processa a entrada do usuário.
    """
    while True:
        print("\n--- Hotel Key Master - Menu Principal ---")
        print("1. Ver Status dos Quartos")
        print("2. Realizar Check-in")
        print("3. Realizar Check-out")
        print("4. sair")
        
        choice = input("Escolha uma opção: ")

        if choice == '1':
            manager.display_status()
        elif choice == '2':
            try:
                room = int(input("Digite o número do quarto para check-in: "))
                guest = input("Digite o nome do hóspede: ")
                if not guest: # Validação simples
                    print("Nome do hóspede não pode ser vazio.")
                    continue
                manager.check_in(room, guest)
            except ValueError:
                print("Entrada inválida. O número do quarto deve ser um inteiro.")
        elif choice == '3':
            try:
                room = int(input("Digite o número do quarto para check-out: "))
                manager.check_out(room)
            except ValueError:
                print("Entrada inválida. O número do quarto deve ser um inteiro.")
        elif choice == '4':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    hotel_manager = HotelKeyManager(total_rooms=20)
    main_menu(hotel_manager)

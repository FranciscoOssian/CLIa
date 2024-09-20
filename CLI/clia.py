import argparse
from commands import execute_command, help_command, chat_command

def main():
    parser = argparse.ArgumentParser(description="Clia - Your AI-Powered Terminal Assistant")
    subparsers = parser.add_subparsers(dest='command', help='Subcomandos disponíveis')

    # Subcomando "help"
    parser_help = subparsers.add_parser('help', help='Exibe informações de ajuda.')

    # Subcomando "execute"
    parser_execute = subparsers.add_parser('execute', help='Executa um comando arbitrário.')
    parser_execute.add_argument('command_to_execute', nargs='+', help='Comando a ser executado (com argumentos).')

    # Subcomando "chat"
    parser_chat = subparsers.add_parser('chat', help='Inicia uma conversa com o chatbot.')

    args = parser.parse_args()

    if args.command == "help":
        help_command()
    elif args.command == "execute":
        command_str = " ".join(args.command_to_execute)  # Junta os elementos da lista em uma string
        execute_command(command_str) 
    elif args.command == "chat":
        chat_command()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
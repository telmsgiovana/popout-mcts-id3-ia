from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from utils import GameExit

from game import PopOutGame

console = Console()


class GameInterface:
    def __init__(self):
        self.game = PopOutGame()

    # =========================================================
    # VISUALIZAÇÃO
    # =========================================================

    def render_board(self):
        table = Table(show_header=True, header_style="bold blue")

        # Cabeçalhos (colunas)
        for col in range(self.game.cols):
            table.add_column(str(col), justify="center")

        symbols = {0: "·", 1: "[red]X[/red]", 2: "[yellow]O[/yellow]"}

        for row in self.game.board:
            table.add_row(*[symbols[cell] for cell in row])

        console.print(table)
        console.print(f"\n[bold magenta]Jogador atual: {symbols[self.game.current_player]}[/bold magenta]")

    # =========================================================
    # INPUT DO UTILIZADOR
    # =========================================================

    def get_player_move(self):
        valid_moves = self.game.get_valid_moves()

        console.print(f"\nMovimentos disponíveis: {valid_moves}")
        console.print("[dim]Digite 'q' ou 'exit' para sair[/dim]")

        while True:
            # NÃO usar "choices" aqui (permite q/exit)
            move_type = Prompt.ask("Tipo de jogada").strip().lower()

            # VERIFICAÇÃO DE SAÍDA (AQUI!)
            if move_type in ["q", "exit"]:
                confirm = Prompt.ask("Tem certeza que quer sair? (y/n)", choices=["y", "n"])
                if confirm == "y":
                    raise GameExit()
                else:
                    continue

            # agora pede coluna
            col = Prompt.ask("Coluna").strip().lower()

            # VERIFICAÇÃO DE SAÍDA (TAMBÉM AQUI!)
            if col in ["q", "exit"]:
                confirm = Prompt.ask("Tem certeza que quer sair? (y/n)", choices=["y", "n"])
                if confirm == "y":
                    raise GameExit()
                else:
                    continue

            # 🔹 valida número
            try:
                col = int(col)
            except:
                console.print("[red]Coluna inválida[/red]")
                continue

            # 🔹 valida tipo de jogada
            if move_type not in ["drop", "pop"]:
                console.print("[red]Tipo inválido (use drop/pop)[/red]")
                continue

            # 🔹 valida jogada completa
            if (move_type, col) in valid_moves:
                return move_type, col
            else:
                console.print("[red]Jogada inválida. Tente novamente.[/red]")

    # =========================================================
    # MODOS DE JOGO
    # =========================================================

    def choose_mode(self):
        console.print("\n[bold cyan]Escolha o modo de jogo:[/bold cyan]")
        console.print("1 - Humano vs Humano")
        console.print("2 - Humano vs IA")
        console.print("3 - IA vs IA")

        while True:
            choice = Prompt.ask("Opção", choices=["1", "2", "3"])
            return int(choice)

    # =========================================================
    # LOOP PRINCIPAL
    # =========================================================

    def run(self):
        try:
            mode = self.choose_mode()

            console.print("\n[bold green]Iniciando jogo...[/bold green]\n")

            while True:
                self.render_board()

                # -----------------------------
                # ESCOLHER JOGADA
                # -----------------------------
                if mode == 1:
                    move = self.get_player_move()

                elif mode == 2:
                    if self.game.current_player == 1:
                        move = self.get_player_move()
                    else:
                        move = self.random_ai()

                elif mode == 3:
                    move = self.random_ai()

                move_type, col = move
                self.game.make_move(move_type, col)

                # -----------------------------
                # RESULTADOS
                # -----------------------------
                winner = self.game.check_winner(last_move_type=move_type)

                if winner:
                    self.render_board()
                    console.print(f"[bold green]Jogador {winner} venceu![/bold green]")
                    break

                draw = self.game.check_draw()

                if draw:
                    self.render_board()
                    console.print("[bold red]Empate[/bold red]")
                    break

        except GameExit:
            console.print("\n[bold yellow]Jogo terminado pelo utilizador.[/bold yellow]")

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Interrompido (Ctrl+C).[/bold yellow]")

        finally:
            console.print("[dim]Obrigado por jogar PopOut![/dim]")

    # =========================================================
    # IA SIMPLES (TEMPORÁRIA)
    # =========================================================

    def random_ai(self):
        import random
        return random.choice(self.game.get_valid_moves())


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":
    interface = GameInterface()
    interface.run()
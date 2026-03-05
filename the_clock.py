#!/usr/bin/env python3
"""
Colorful live terminal clock → then simple number guessing game
Date is fixed: March 05, 2026
Press Ctrl+C on clock → starts the minigame
"""

import os
import time
import random
import sys
from datetime import datetime


# ─── ANSI Colors ─────────────────────────────────────────────────────────────
class Colors:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    CYAN     = "\033[96m"
    GREEN    = "\033[92m"
    YELLOW   = "\033[93m"
    BLUE     = "\033[94m"
    MAGENTA  = "\033[95m"
    RED      = "\033[91m"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def live_clock():
    print(f"{Colors.YELLOW}Live clock started... (Ctrl+C to stop and play mini-game){Colors.RESET}\n")
    time.sleep(1.2)

    try:
        while True:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")

            # Cycle colors every second for fun
            sec = int(time_str[-2:])
            if sec % 3 == 0:
                tcolor = Colors.MAGENTA
            elif sec % 3 == 1:
                tcolor = Colors.CYAN
            else:
                tcolor = Colors.YELLOW

            clear_screen()

            print(f"{Colors.BOLD}{Colors.BLUE}═══════════════════════════════════════════════{Colors.RESET}")
            print(f"      {Colors.CYAN}T E R M I N A L   C L O C K{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.BLUE}═══════════════════════════════════════════════{Colors.RESET}\n")

            print(f"   {Colors.GREEN}Date :{Colors.RESET}  March 05, 2026")
            print(f"   {tcolor}Time :{Colors.RESET}  {tcolor}{time_str}{Colors.RESET}\n")

            print(f"{Colors.BOLD}{Colors.BLUE}═══════════════════════════════════════════════{Colors.RESET}")
            print(f"   {Colors.YELLOW}(updates every second)   Ctrl+C → start game{Colors.RESET}\n")

            # Sleep aligned to real seconds for smoother feel
            time.sleep(1.0 - (time.time() % 1.0))

    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.GREEN}Clock stopped.{Colors.RESET}\n")
        time.sleep(0.6)


def number_guessing_game():
    clear_screen()
    print(f"{Colors.BOLD}{Colors.MAGENTA}╔════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}║         NUMBER GUESSING GAME       ║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}╚════════════════════════════════════╝{Colors.RESET}\n")

    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 8

    print(f"{Colors.CYAN}I thought of a number between 1 and 100.{Colors.RESET}")
    print(f"You have {max_attempts} tries. Good luck!\n")
    print(f"{Colors.YELLOW}Ctrl+C = quit anytime{Colors.RESET}\n")

    while attempts < max_attempts:
        try:
            guess_str = input(f"{Colors.GREEN}Attempt {attempts+1}/{max_attempts} → Guess: {Colors.RESET}").strip()
            if not guess_str:
                print(f"{Colors.YELLOW}Please enter a number.{Colors.RESET}")
                continue

            guess = int(guess_str)
            attempts += 1

            if guess == secret:
                clear_screen()
                print(f"\n{Colors.BOLD}{Colors.GREEN}🎉  YES! You got it!{Colors.RESET}")
                print(f"The number was {Colors.BOLD}{secret}{Colors.RESET}")
                print(f"You needed {attempts} attempt{'s' if attempts > 1 else ''}.")
                print(f"\n{Colors.YELLOW}Well played!{Colors.RESET}\n")
                return
            elif guess < secret:
                print(f"{Colors.RED}Too low!{Colors.RESET}")
            else:
                print(f"{Colors.RED}Too high!{Colors.RESET}")

            print()
        except ValueError:
            print(f"{Colors.YELLOW}That's not a number... try again.{Colors.RESET}")
        except KeyboardInterrupt:
            clear_screen()
            print(f"\n{Colors.RED}Game aborted.{Colors.RESET}\n")
            return

    clear_screen()
    print(f"{Colors.RED}Game over! You ran out of attempts.{Colors.RESET}")
    print(f"The secret number was → {Colors.BOLD}{secret}{Colors.RESET} ←\n")


def main():
    # Hide cursor for cleaner look
    print("\033[?25l", end="", flush=True)

    try:
        live_clock()
    except KeyboardInterrupt:
        pass

    # After clock is stopped → launch game
    number_guessing_game()

    # Final cleanup
    clear_screen()
    print(f"{Colors.GREEN}Thanks for playing! See you next time.{Colors.RESET}\n")
    print("\033[?25h", end="", flush=True)  # show cursor again


if __name__ == "__main__":
    if not sys.stdout.isatty():
        print("Best viewed in a real terminal (not piped/redirected output)")
        sys.exit(1)

    main()

#!/usr/bin/env python3
"""
Colorful live terminal clock → ULTRA interactive number guessing game
"""

import os
import time
import random
import sys
from datetime import datetime

# ─── ANSI Colors ─────────────────────────────────────────────────────────────
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    DIM = "\033[2m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def live_clock():
    print(f"{Colors.YELLOW}Live clock running...  Ctrl+C → GAME ON{Colors.RESET}\n")
    time.sleep(1)
    try:
        while True:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            tcolor = [Colors.MAGENTA, Colors.CYAN, Colors.YELLOW][now.second % 3]

            clear_screen()
            print(f"{Colors.BOLD}{Colors.BLUE}═"*55 + Colors.RESET)
            print(f"      {Colors.CYAN}T E R M I N A L   C L O C K{Colors.RESET}    ")
            print(f"{Colors.BOLD}{Colors.BLUE}═"*55 + Colors.RESET + "\n")
            print(f" {Colors.GREEN}Date :{Colors.RESET} March 05, 2026")
            print(f" {tcolor}Time :{Colors.RESET} {tcolor}{time_str}{Colors.RESET}\n")
            print(f"{Colors.BOLD}{Colors.BLUE}═"*55 + Colors.RESET)
            print(f" {Colors.YELLOW}Press Ctrl+C to start the guessing game!{Colors.RESET}\n")
            time.sleep(1.0 - (time.time() % 1.0))
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.GREEN}Entering game mode...{Colors.RESET}\n")
        time.sleep(0.6)

# ─── Ultra Interactive Guessing Game ─────────────────────────────────────────
def number_guessing_game():
    score = 0
    high_score = 0
    streak = 0

    while True:
        clear_screen()
        print(f"{Colors.MAGENTA}{'═'*48}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}     U L T R A   G U E S S   A R E N A     {Colors.RESET}")
        print(f"{Colors.MAGENTA}{'═'*48}{Colors.RESET}\n")

        print(f" {Colors.CYAN}Score:{Colors.RESET} {Colors.BOLD}{score}{Colors.RESET}   {Colors.YELLOW}High:{Colors.RESET} {Colors.BOLD}{high_score}{Colors.RESET}")
        print(f" {Colors.GREEN}Streak:{Colors.RESET} {streak}x\n")

        # Difficulty selection
        print(f"{Colors.YELLOW}Choose difficulty:{Colors.RESET}")
        print("  1 = Easy   (1–50, 12 attempts)")
        print("  2 = Normal (1–100, 9 attempts)")
        print("  3 = Hard   (1–200, 7 attempts)\n")
        diff_choice = input(f"{Colors.CYAN}→ {Colors.RESET}").strip()

        if diff_choice == "1":
            max_n, max_attempts = 50, 12
            diff_name = "Easy"
        elif diff_choice == "3":
            max_n, max_attempts = 200, 7
            diff_name = "Hard"
        else:
            max_n, max_attempts = 100, 9
            diff_name = "Normal"

        secret = random.randint(1, max_n)
        attempts = 0
        start_time = time.time()
        low, high = 1, max_n

        # Lifelines (one use each per game)
        lifeline_5050 = True
        lifeline_extra = True
        lifeline_parity = True

        print(f"\n{Colors.CYAN}Difficulty: {Colors.BOLD}{diff_name}{Colors.RESET}  →  Range: 1–{max_n}   Attempts: {max_attempts}\n")
        print(f"{Colors.YELLOW}Commands:  hint, 50, extra, parity, quit{Colors.RESET}\n")

        while attempts < max_attempts:
            try:
                elapsed = time.time() - start_time
                prompt = f"{Colors.GREEN}#{attempts+1}/{max_attempts}  Guess → {Colors.RESET}"
                guess_str = input(prompt).strip().lower()

                # Speed feedback
                if elapsed < 5 and attempts == 0 and guess_str.isdigit():
                    print(f"{Colors.DIM}(Quick start!){Colors.RESET}")

                if guess_str in ('q', 'quit', 'exit'):
                    print(f"\n{Colors.RED}Leaving arena...{Colors.RESET}\n")
                    return

                # Lifeline: 50/50
                if guess_str == '50' and lifeline_5050:
                    if secret <= max_n // 2:
                        high = max_n // 2
                    else:
                        low = max_n // 2 + 1
                    print(f"{Colors.YELLOW}50:50 used → range narrowed to {low}–{high}{Colors.RESET}")
                    lifeline_5050 = False
                    continue

                # Lifeline: +2 attempts
                if guess_str == 'extra' and lifeline_extra:
                    max_attempts += 2
                    print(f"{Colors.YELLOW}Extra attempts used → now {max_attempts} total{Colors.RESET}")
                    lifeline_extra = False
                    continue

                # Lifeline: parity
                if guess_str == 'parity' and lifeline_parity:
                    par = "even" if secret % 2 == 0 else "odd"
                    print(f"{Colors.YELLOW}Parity hint: the number is {par}{Colors.RESET}")
                    lifeline_parity = False
                    continue

                if guess_str == 'hint':
                    print(f"{Colors.YELLOW}Range hint → {low} – {high}{Colors.RESET}")
                    continue

                guess = int(guess_str)
                attempts += 1
                now_time = time.time()

                # Update range
                if guess < secret:  low  = max(low,  guess + 1)
                if guess > secret:  high = min(high, guess - 1)

                if guess == secret:
                    diff_time = now_time - start_time
                    clear_screen()

                    print(f"\n{Colors.GREEN}{'╔' + '═'*30 + '╗'}{Colors.RESET}")
                    print(f"{Colors.GREEN}║  🎉  VICTORY !   🎉  ║{Colors.RESET}")
                    print(f"{Colors.GREEN}{'╚' + '═'*30 + '╝'}{Colors.RESET}\n")

                    print(f"  Secret → {Colors.BOLD}{secret}{Colors.RESET}")
                    print(f"  Attempts → {attempts} / {max_attempts}")
                    print(f"  Time → {diff_time:.1f} s\n")

                    points = max(100 - attempts*8 - int(diff_time*2), 10)
                    score += points
                    streak += 1

                    if streak >= 3:
                        print(f"{Colors.YELLOW}COMBO ×{streak} !  +{points//2} bonus!{Colors.RESET}")
                        score += points // 2

                    if score > high_score:
                        high_score = score
                        print(f"{Colors.YELLOW}★ NEW HIGH SCORE ★{Colors.RESET}")

                    print(f"\n  {Colors.CYAN}Total score: {score}{Colors.RESET}\n")
                    print("\a")  # terminal bell
                    time.sleep(2.3)
                    break

                # Temperature scale
                diff = abs(guess - secret)
                temp = ""
                if diff <= 2:    temp, bell = f"{Colors.RED}🔥🔥🔥 SCORCHING!", "\a"
                elif diff <= 5:  temp = f"{Colors.RED}🔥🔥 BURNING!"
                elif diff <= 10: temp = f"{Colors.YELLOW}🔥 HOT!"
                elif diff <= 20: temp = f"{Colors.CYAN}≈ WARM"
                elif diff <= 40: temp = f"{Colors.BLUE}❄️ COLD"
                else:            temp = f"{Colors.BLUE}❄️❄️ FREEZING"

                direction = "WAY too high" if guess > secret + 40 else \
                            "too high" if guess > secret else \
                            "WAY too low" if guess < secret - 40 else "too low"

                print(f"{Colors.BOLD}{direction.upper()}{Colors.RESET}  {temp}{Colors.RESET}")

                if bell: print(bell, end="", flush=True)

                # Direction change feedback
                if attempts >= 2:
                    prev_diff = abs(prev_guess - secret)
                    if diff < prev_diff:    print(f"{Colors.GREEN}↗ closer!{Colors.RESET}")
                    elif diff > prev_diff:  print(f"{Colors.RED}↘ farther...{Colors.RESET}")

                prev_guess = guess
                print()

            except ValueError:
                print(f"{Colors.YELLOW}Enter a number or command (hint/50/extra/parity/quit){Colors.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}Match aborted.{Colors.RESET}\n")
                return

        else:
            clear_screen()
            print(f"\n{Colors.RED}{'╔' + '═'*30 + '╗'}{Colors.RESET}")
            print(f"{Colors.RED}║     GAME OVER      ║{Colors.RESET}")
            print(f"{Colors.RED}{'╚' + '═'*30 + '╝'}{Colors.RESET}\n")
            print(f"  The number was → {Colors.BOLD}{secret}{Colors.RESET}\n")
            streak = 0
            score = max(0, score - 40)
            time.sleep(2.2)

        # Next round?
        print(f"{Colors.CYAN}Another round? (y/n){Colors.RESET} ", end="")
        if input().strip().lower() not in ('y', 'yes', ''):
            clear_screen()
            print(f"{Colors.GREEN}Session ended → Score: {score}   High: {high_score}   Best streak: {streak}{Colors.RESET}\n")
            print(f"{Colors.YELLOW}See you in the arena again soon!{Colors.RESET}\n")
            break

def main():
    print("\033[?25l", end="", flush=True)   # hide cursor
    try:
        live_clock()
    except KeyboardInterrupt:
        pass

    try:
        number_guessing_game()
    finally:
        clear_screen()
        print("\033[?25h", end="", flush=True)  # restore cursor
        print(f"{Colors.GREEN}Thanks for playing!{Colors.RESET}\n")

if __name__ == "__main__":
    if not sys.stdout.isatty():
        print("Run in a real terminal please :)")
        sys.exit(1)
    main()

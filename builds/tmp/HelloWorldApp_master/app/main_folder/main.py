from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

print(Fore.GREEN + Style.BRIGHT + "Hello from your portable Python app!")
print(Fore.CYAN + "This is printed in cyan.")
print(Fore.YELLOW + "And this is yellow.")
print(Fore.RED + Style.DIM + "This is dim red text.")
print(Style.RESET_ALL + "\nEverything is back to normal now.")

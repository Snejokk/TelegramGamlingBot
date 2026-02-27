import time, random, os

clear = lambda: os.system("cls" if os.name=="nt" else "clear")

W, StartPossition, StartSpeed = 45, 0.0, random.uniform(0.05, 0.11)
LeftWinzone, rightWinzone = random.randint(12, 18), random.randint(25, 32)

for i in range(60):
    StartPossition = (StartPossition + StartSpeed) % 1.0
    StartSpeed *= 0.965  
    Possition = int(StartPossition * W)

    bar = ["█" if LeftWinzone <= j < rightWinzone else "—" for j in range(W)]
    bar[min(Possition, W-1)] = "◆"
    
    clear()
    print(f"  [{''.join(bar)}]")
    print(f"   0.0{' ' * (W-8)}1.0")
    print(f"  {' ' * (Possition+1)}▲ {StartPossition:.2f}")
    print(f"\n Крутим{'.' * (i % 4 + 1)}")
    

    time.sleep(0.02 + 0.12 * (i/60)**2)

# Финальный результат
Possition = int(StartPossition * W)
bar = ["█" if LeftWinzone <= j < rightWinzone else "—" for j in range(W)]
bar[min(Possition, W-1)] = "◆"

clear()
print(f"  [{''.join(bar)}]")
print(f"   0.0{' ' * (W-8)}1.0")
print(f"  {' ' * (Possition+1)}▲ {StartPossition:.2f}")

win = LeftWinzone <= Possition < rightWinzone

print(f"\n  {'\U0001F389 ПОБЕДА!' if win else '\U0001F480 МИМО...'}")
while True:
    print("========= PATTERN MENU =========")
    print("1. Solid Square") 
    print("2. Hollow Square")
    print("3. Right Triangle")
    print("4. Inverted Triangle")
    print("5. Pyramid")
    print("6. Inverted Pyramid")
    print("7. Diamond")
    print("8. Hollow Diamond")
    print("9. Number Pyramid")
    print("10. Floyd's Triangle")
    print("11. Exit")

    option=int(input("Press the corresponding number (1-11) to use the menu. "))
    if 1<= option <= 10:
        n=int(input("Enter the size of pattern. "))

    count = 1

    if option==1:
        for i in range(1, n+1):
            for j in range(1, n+1):
                print("* ", end="")
            print("")

    if option==2:
        for i in range(1, n+1):
            for j in range(1, n+1):
                if ((i == 1) or (i == n)) or ((j == 1) or (j == n)):
                    print("* ", end="")
                else:
                    print("  ", end="")    
            print("")

    if option==3:
        for i in range(1, n+1):
            for j in range(1, i+1):
                print("* ", end="")  
            print("")

    if option==4:
        for i in range(n, 0, -1):
            for j in range(1, i+1):
                print("* ", end="")
            print()

    if option==5:
        for i in range(1, n+1):
            for j in range(1,2*n+1):
                if n-i+1<=j<=n+i-1:
                    print("* ", end="")
                else:
                    print("  ", end="")
            print()

    if option==6:
        for i in range(n, 0, -1):
            for j in range(1, 2*n+1):
                if n-i+1<=j<=n+i-1:
                    print("* ", end="")
                else:
                    print("  ", end="")
            print()

    if option==7:
        for i in range(1, n+1):
                for j in range(1,2*n+1):
                    if n-i+1<=j<=n+i-1:
                        print("* ", end="")
                    else:
                        print("  ", end="")
                print()
        for i in range(n-1, 0, -1):
                for j in range(1, 2*n+1):
                    if n-i+1<=j<=n+i-1:
                        print("* ", end="")
                    else:
                        print("  ", end="")
                print()

    if option==8:
        for i in range(1, n+1):
            for j in range(1, 2*n+1):
                if j == n-i+1 or j == n+i-1 : 
                    print("* ", end="")
                else:
                    print("  ", end="")
            print()
        for i in range(n-1, 0, -1):
                for j in range(1, 2*n+1):
                    if j == n-i+1 or j == n+i-1 : 
                        print("* ", end="")
                    else:
                        print("  ", end="")
                print()

    if option==9:
        for i in range(1,n+1):
            for j in range(1, 2*n+1):
                if n-i+1<=j<=n+i-1 :
                    print(i, " ", end="")
                else:
                    print("  ", end="")
            print()

    if option==10:
        for i in range(1,n+1):
            for j in range(1, i+1):
                print(count, end=" ")
                count+=1
            print()

    if option==11:
        print("Exiting the menu.")
        break

with open("input.txt", "r") as f:
    pos = 50
    count = 0
    for line in f:
        letter = line[0]
        numbers = int(line[1:])
        print("Letter: " + letter + ", numbers: " + str(numbers))

        match letter:
            case 'L':
                dir = -1
            case 'R':
                dir = 1

        pos = (pos + dir*numbers) % 100
        if pos == 0:
            count += 1
        print("New position:", pos, ", count =", count)


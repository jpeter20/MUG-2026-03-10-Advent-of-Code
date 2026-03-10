with open("input.txt", "r") as f:
    newpos = 50
    count = 0
    for line in f:
        line = line.rstrip()
        oldpos = newpos
        letter = line[0]
        move = int(line[1:])
        if move == 0:
            continue

        match letter:
            case 'L':
                dir = -1
            case 'R':
                dir = 1

        print("Line:", line, ", old pos:", oldpos, end='')

        # Calculate number of full wrap-arounds; each passes 0 again
        wraps = move // 100
        if wraps >= 1:
            print(", wrap", wraps, end='')
        count += wraps

        # Calculate remaining moves
        move -= wraps*100

        # Get proper direction for move
        move *= dir

        # Move the partial wrap-around
        newpos = oldpos + move

        # See if we went off the edge, and increment count if so,
        # but only if we didn't start at 0 (prevent double-count).
        if (newpos != newpos % 100):
            newpos = newpos % 100
            if oldpos != 0:
                count += 1
        # Count landing on 0 once.
        elif newpos == 0:
            count += 1
        print(", new pos:", newpos, ", count =", count, "move:", move)

print("Final result:", count)

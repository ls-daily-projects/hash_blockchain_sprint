def get_indices_of_item_weights(weights, length, limit):
    i = 0
    j = length - 1

    while(i < j):
        lhs = weights[i]
        rhs = weights[j]
        if lhs + rhs == limit:
            return (i, j) if i > j else (j, i)

        i += 1
        j -= 1

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")

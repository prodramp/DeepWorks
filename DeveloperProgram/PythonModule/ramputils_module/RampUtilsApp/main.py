choices = ['addition', 'subtraction', 'multiplication', 'division']


def validate_choice(choice):
    if choice not in choices:
        return False
    return True


def validate_values(argv):
    all_value = True
    if len(argv) > 0:
        for each_val in argv:
            if type(each_val).__name__ not in ['int', 'float', 'int64', 'float64']:
                all_value = False
    return all_value


def calc(choice, *argv):
    result_message = "Unsupported Choice"
    result_value = 0
    result_status = False

    # Check 1
    if validate_choice(choice) is False:
        return result_status, result_value, result_message

    # Check 2
    if validate_values(argv) is False:
        result_message = "Please submit all values are numeric"
        return result_status, result_value, result_message

    # Implementation
    if choice == 'addition':
        if len(argv) > 0:
            for each_val in argv:
                result_value = result_value + each_val
            result_status = True
            result_message = "Addition is successful"
    elif choice == 'subtraction':
        if len(argv) != 2:
            result_message = "Subtraction needs only 2 values.."
        else:
            result_value = argv[0] - argv[1]
            result_status = True
            result_message = "Subtraction is successful"
    elif choice == 'multiplication':
        if len(argv) > 0:
            result_value = argv[0]
            for val_index in range(len(argv))[1:]:
                result_value = result_value * argv[val_index]
            result_status = True
            result_message = "Multiplication is successful"
    elif choice == 'division':
        if len(argv) != 2:
            result_message = "Division needs only 2 values.."
        else:
            if argv[1] == 0:
                result_message = "Division is not possible with 0 value"
            else:
                result_value = argv[0] / argv[1]
                result_status = True
                result_message = "Division is successful"

    return result_status, result_value, result_message


if __name__ == '__main__':
    print(calc('multiplication', 5600, 10, 1, 2, 5))
    print(calc('division', 5600, '1'))
    print(calc('subtraction', 5600, 10, 2))
    print(calc('addition', 5600, 10, 1, 45, 6, 7, 45))

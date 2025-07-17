with open("test.py", "r") as f:
    for i, line in enumerate(f, start=1):
        print(f"Line {i}: {repr(line)}")  # Shows raw formatting
        if "\t" in line:
            print(f"Tab found on line {i}")

            A = [1, 2, 3, 4]
            with open("test.py", "r") as f:
                for i, line in enumerate(f, start=1):
                    print(f)

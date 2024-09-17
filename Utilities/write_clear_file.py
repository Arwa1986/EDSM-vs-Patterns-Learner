def write_to_file(filename, content):
    # Open the file in write mode ('w') or append mode ('a')
    with open(filename, 'a') as file:  # 'a' for append mode
        file.write(content)
        file.write('\n')  # Add a new line if needed

def clear_file(filename):
    with open(filename, 'w'):
        pass  # Opening in 'w' mode truncates the file, clearing its contents.

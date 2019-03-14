import fileinput


def prepare(source, template_file, target):
    with fileinput.FileInput(template_file, inplace=True) as file:
        for line in file:
            print(line.replace(source, target), end='')
    with open(template_file) as oldfile, open('new_descriptor.json', 'w') as newfile:
        for line in oldfile:
            if not (('"' + 'host' + '"') in line):
                newfile.write(line)

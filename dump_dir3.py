import csv


def clean_text(s: str):
    s = s.strip()
    if s[0] == s[-1] == '"':
        return s[1:-1]
    return s


def main():
    with open('organigrama.csv', 'r', encoding='utf-8') as source:
        reader = csv.reader(source, delimiter=';', quotechar='"')
        next(reader) # Ignorar primera fila de nombres
        for row in reader:
            
            id_dir3 = row[1]
            id_sirhus = row[2]
            nombre_organismo = clean_text(row[3])
            depende_de = row[7]
            print(id_dir3, nombre_organismo, '<--', depende_de)


if __name__ == "__main__":
    main()

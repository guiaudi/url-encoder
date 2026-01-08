from database import init_db
from service import encoder_url, resolver_codigo


def main():
    init_db()

    url = input("Digite a URL para encodar: ")
    codigo = encoder_url(url)

    print(f"URL curta: http://localhost/{codigo}")

if __name__ == "__main__":
    main()

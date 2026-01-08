from database import get_connection
from encoder import gerar_codigo


def criar_url_curta(original_url: str) -> str:
    if not original_url:
        raise ValueError("URL vazia")

    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se a URL já existe
    cursor.execute(
        "SELECT encoded_url FROM urls WHERE original_url = ?",
        (original_url,)
    )
    resultado = cursor.fetchone()

    if resultado:
        conn.close()
        return resultado[0]

    # Gera código único
    while True:
        codigo = gerar_codigo()
        cursor.execute(
            "SELECT 1 FROM urls WHERE encoded_url = ?",
            (codigo,)
        )
        if not cursor.fetchone():
            break

    # Insere no banco
    cursor.execute(
        "INSERT INTO urls (original_url, encoded_url) VALUES (?, ?)",
        (original_url, codigo)
    )

    conn.commit()
    conn.close()

    return codigo


def buscar_url_original(codigo: str) -> str | None:
    if not codigo:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original_url FROM urls WHERE encoded_url = ?",
        (codigo,)
    )
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None

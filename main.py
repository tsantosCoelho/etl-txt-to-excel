import pandas as pd
import re

arquivo = "dados.txt"

registros = []
data_atual = None
linha_temp = None

with open(arquivo, "r", encoding="latin-1") as f:
    for linha in f:
        linha = linha.strip()

        # Detecta data
        if re.match(r"\d{2}/\d{2}/\d{4}", linha):
            data_atual = linha[:10]
            continue

        # Detecta linha de lançamento (começa com número + lote)
        if re.match(r"^\d+\s+\d+/\d+/\d+", linha):
            linha_temp = linha

        # Detecta histórico e FINALIZA o registro
        elif "Histórico:" in linha and linha_temp:
            historico = linha.replace("Histórico:", "").strip()

            # Extrai valor no final da linha anterior
            match_valor = re.search(r"([\d\.,]+)$", linha_temp)
            valor = match_valor.group(1) if match_valor else None

            registros.append({
                "Data": data_atual,
                "Linha": linha_temp,
                "Historico": historico,
                "Valor": valor
            })

            linha_temp = None

# DEBUG (não tira isso ainda)
print("Registros encontrados:", len(registros))

if len(registros) == 0:
    print("⚠️ Nenhum registro foi capturado. Verifique o TXT.")
    exit()

# DataFrame
df = pd.DataFrame(registros)

# Converter valor
def limpa_valor(v):
    if v:
        v = v.replace(".", "").replace(",", ".")
        return float(v)
    return None

df["Valor"] = df["Valor"].apply(limpa_valor)

# Exportar
df.to_excel("saida.xlsx", index=False)

print("✅ Arquivo gerado: saida.xlsx")

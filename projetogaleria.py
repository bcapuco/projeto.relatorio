import pandas as pd
import glob
import os

# Coletar arquivos CSV
csv_files = [file for file in glob.glob('/home/capuco/VSCODE/SRC/Arquivocsv/*.csv') if os.path.isfile(file)]

# Concatenar os DataFrames
df = pd.concat((pd.read_csv(file, delimiter=';') for file in csv_files), ignore_index=True)

# Remover espaços em branco dos nomes das colunas
df.columns = [col.strip() for col in df.columns]

# Imprimir os nomes das colunas
print(df.columns.tolist())

# Criação do HTML com base nos dados
html_content = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventário Patrimonial</title>
    <link rel="stylesheet" href="SRC/css/stilizacao.css">
    <script src="SRC/Js/filtro.js"></script>
   </head>
<body>
    <h1>Inventário Patrimonial 2024 </h1>
        
    <label for="especieFiltro">Filtrar por Espécie:</label>
    <input type="text" id="especieFiltro" oninput="filtrar()" placeholder="Espécie">

    <label for="plaquetaFiltro">Filtrar por Plaqueta:</label>
    <input type="text" id="plaquetaFiltro" oninput="filtrar()" placeholder="Plaqueta">

    <label for="qrcodefiltro">Filtrar por QRCODE:</label>
    <input type="text" id="qrcodeFiltro" oninput="filtrar()" placeholder="QRCODE">

    <label for="localizacaoFiltro">Filtrar por Localização:</label>
    <input type="text" id="localizacaoFiltro" oninput="filtrar()" placeholder="Localização">

    <label for="responsavelFiltro">Filtrar por Responsável:</label>
    <input type="text" id="responsavelFiltro" oninput="filtrar()" placeholder="Responsável">

    <table>
        <thead>
            <tr>                      
                <th>ESPECIE</th>
                <th>PLAQUETA</th>
                <th>QRCODE</th>
                <!--<th>LOCALIZAÇÃO ANTERIOR</th>-->
                <th>LOCALIZAÇÃO</th>
                <th>RESPONSÁVEL</th>
                <th>CONSERVAÇÃO</th>
                <th class="valor-liquido">VALOR LÍQUIDO</th>
                <th>ESTATUS</th>
                <th>IMAGEM PLAQUETA</th>
                <th>IMAGEM PATRIMONIO</th>
            </tr>
        </thead>
        <tbody id="tabela">
            <!-- Linhas da tabela geradas dinamicamente -->
"""

# Adicionando dados à tabela
for index, row in df.iterrows():
    plaqueta_unicode = row['plaqueta_unicode']

    # Se o valor estiver vazio ou for NaN, definir "S/T" como valor padrão
    if pd.isna(plaqueta_unicode) or plaqueta_unicode.strip() == '':
        plaqueta_unicode_formatado = 'S/T'
    else:
        # Formatação para incluir "CON-" e garantir que os números tenham 4 dígitos
        try:
            plaqueta_unicode_formatado = f"CON-{int(plaqueta_unicode):04d}"  # Formato desejado
        except ValueError:
            plaqueta_unicode_formatado = plaqueta_unicode 
    
    if pd.isna(row['plaqueta_qrcode']):
        plaqueta_qrcode_formatado = 'S/T'  # Defina um valor padrão, caso seja NaN
    else:
        plaqueta_qrcode_formatado = str(int(float(row['plaqueta_qrcode']))).zfill(5)

    # Formatando o valor atual para duas casas decimais diretamente
    valor_liquido_formatado = f"R$ {float(row['valor_atual']):.2f}"

    html_content += f"""
    <tr> 
        <td>{row['patrimonio_unicode']}</td>
        <td>{plaqueta_unicode_formatado}</td>
        <td>{plaqueta_qrcode_formatado}</td>
        <!--<td>{row['localizacao_anterior']}</td>-->
        <td>{row['localizacao_unicode']}</td>
        <td>{row['responsavel_unicode']}</td>
        <td>{row['conservacao_display']}</td>
        <td>{valor_liquido_formatado}</td> 
        <td>{row['status_display']}</td>
        <td><img src="{row['imagem_plaqueta']}" alt="Imagem da Plaqueta" width="150"></td>
        <td><img src="{row['imagem_patrimonio']}" alt="Imagem do Patrimônio" width="150"></td>
    </tr>
    """

html_content += """
        </tbody>
    </table>
   
    
    <script src="SRC/js/filtro.js"></script>
</body>
</html>
"""

# Salvar o conteúdo em um arquivo HTML
with open('inventario.html', 'w') as file:
    file.write(html_content)




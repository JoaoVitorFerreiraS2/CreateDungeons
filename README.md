# 🏰 Gerador de Mapas Procedurais

Este projeto é um gerador de mapas procedurais que cria imagens de mapas baseados em corredores e paredes, utilizando a biblioteca **cairo** para renderização. O código permite personalizar o tamanho do mapa, ativar/desativar a exibição de uma grade e incluir um mini-mapa no canto inferior direito.

## 📌 Funcionalidades
✅ **Geração Procedural** – Os mapas são criados aleatoriamente com caminhos e paredes.  
✅ **Personalização** – O usuário pode definir a largura e altura do mapa.  
✅ **Mini-Mapa Opcional** – Pequena prévia do mapa no canto inferior direito.  
✅ **Grade Opcional** – Exibição de uma grade para melhor visualização.  
✅ **Exportação para PNG** – O mapa gerado é salvo como uma imagem `.png`.  

## 🚀 Como Usar
1. Certifique-se de ter o **Python 3.x** instalado.  
2. Instale a biblioteca necessária com:
   ```bash
   pip install pycairo
   ```
3. Responda às perguntas para personalizar o mapa:
- Ativar ou não o mini-mapa.
- Ativar ou não a grade.
- Definir largura e altura do mapa.
- Escolher o nome do arquivo de saída.
4. O mapa será gerado e salvo automaticamente como um arquivo .png.

## 🖼️ Exemplo de Saída
O gerador cria imagens de mapas com corredores brancos e paredes cinza-escuro sobre um fundo preto. Se ativado, um mini-mapa e uma grade de referência são adicionados.

### 📜 Licença
Este projeto é distribuído sob a licença MIT.

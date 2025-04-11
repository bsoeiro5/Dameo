# <font size="80">Dameo</font>
*******
Trabalho realizado por:

* Álvaro Castro (FCUP_IACD:202405722)
* Bernardo Soeiro (FCUP_IACD:202406233) 
* Francisco Machado (FCUP_IACD:202403514)
<div style="padding: 10px;padding-left:5%">
<img src="fotos/Cienciasporto.png" style="float:left; height:75px;width:200px">
<img src="fotos/Feuporto.png" style="float:left ; height:75px; padding-left:20px;width:200px">
</div>

<div style="clear:both;"></div>

******
### SOBRE O PROJETO 
No segundo semestre do primeiro ano da Licenciatura em Inteligência Artificial e Ciência de Dados, na Faculdade de Ciências da Universidade do Porto, fomos desafiados a desenvolver uma Inteligência Artificial capaz de jogar jogos de tabuleiro competitivos, neste caso, um jogo para dois jogadores. O objetivo deste projeto passa por explorar algoritmos de pesquisa adversária, nomeadamente Minimax, Alfa-Beta Cuts e Monte Carlo Tree Search (MCTS). Estes métodos são aplicados com diferentes configurações e níveis de profundidade, sendo avaliados em função do seu desempenho em diferentes situações de jogo. 

O “Dameo” foi inventado no ano 2000 pelo designer de jogos abstratos holandês Christian Freeling. O jogo em análise foi concebido com o objetivo de dar um toque mais moderno e dinâmico ao famoso jogo das damas, eliminando alguns obstáculos estratégicos. Desde o seu surgimento, o “Dameo” é considerado um dos jogos mais elegantes e equilibrados.

O objetivo central do jogador no “Dameo” é capturar todas as peças adversárias ou imobilizar o oponente, ganhando, assim, o jogo. Não obstante, se ambos os jogadores ficarem sem movimentos ou repetirem jogadas três vezes, empatam.

>Para aceder à documentação completa e formalização do problema, deve por favor abrir o ficheiro [Dameo_Relatorio.docx](https://www.canva.com/design/DAGj4WibOJA/8QEdnWDrN7lQNhZXu5mRaA/view?utm_content=DAGj4WibOJA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hba45ba0366)

## Como fazer o download e utilizar a interface  
#### Primeiro passo:
Extraia o .zip da página github e descomprima o ficheiro
#### Segundo passo: 
Instale `numpy` e `pygame` no diretório pelo terminal 
```
pip install numpy
pip install pygame
```
#### Terceiro passo: **IMPORTANTE** 
Entre no diretório do ficheiro main.py pelo terminal (no folder [/dameo main](/dameo_sub)) 
```
cd (diretório da pasta)
```
#### Quarto passo 
Corra o programa 
```
python3 dameo.py
```
*****
*****

## Navegação do Menu Principal

### Menu Principal
São disponibilizadas duas opções:

- **Jogar**: Clique neste botão para começar a configurar um jogo  
- **Regras**: Clique para ver as regras do jogo  

### Seleção do Tamanho do Tabuleiro
Depois de clicar em **"Jogar"**, selecione entre:

- **Tabuleiro 6x6** (menor, jogabilidade mais rápida)  
- **Tabuleiro 8x8** (tamanho padrão)  
- **Tabuleiro 12x12** (maior, jogabilidade mais complexa)  

Clique em **"Continuar"** após fazer a sua seleção.

### Seleção do Modo de Jogo
Escolha entre:

- **Player vs Player**  
- **Player vs Computer**  
- **Computer vs Computer**  

Clique em **"Continuar"** para prosseguir.

### Seleção de Algoritmo (para jogadores controlados pelo computador)
- **MCTS** (Monte Carlo Tree Search)  
- **Minimax**  
- **Alpha-Beta**  
- **Random**  

Clique em **"Continuar"** após a seleção.

### Seleção de Dificuldade (exceto para o algoritmo Random)
- **Fácil**  
- **Médio**  
- **Difícil**  

Clique em **"Continuar"** para iniciar o jogo.

### Controles de Navegação

- **Botão Voltar**: Na parte inferior de cada tela do menu, há um botão "Voltar" para voltar ao menu anterior  
- **Tecla ESC**: Pressione *Escape* para voltar ao menu anterior  
- **Rato**: Clique nos botões para fazer seleções  

> A interface foi projetada para ser intuitiva, com posicionamento claro dos botões. Todos os botões estão posicionados no lado esquerdo da tela, com destaque na seleção quando uma opção é escolhida.


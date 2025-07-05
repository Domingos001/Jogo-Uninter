# Bubble Beam

Um jogo de nave 2D com inspiração retrô, onde o jogador deve sobreviver a hordas de inimigos em diferentes fases, cada uma com desafios e objetivos únicos. O jogo conta com múltiplos modos, incluindo cooperativo, competitivo e um ranking de pontuações persistente.



---

## Principais Funcionalidades

* **Múltiplos Modos de Jogo:**
    * **Campanha Single Player:** Avance por 3 fases com dificuldade crescente.
    * **Cooperativo Local:** Jogue com um amigo para atingir os objetivos das fases juntos.
    * **Competitivo Local:** Dispute com um amigo em uma arena de 1 minuto para ver quem faz mais pontos.
* **Variedade de Inimigos:** 3 tipos de inimigos com padrões de movimento diferentes, do mais simples ao mais complexo.
* **Fases Dinâmicas:** Cada fase tem seus próprios objetivos, trilha sonora e um cenário com efeito de profundidade (parallax scrolling).
* **Ranking com Banco de Dados:** Um sistema de high score que salva o nome, a pontuação e a data dos 5 melhores jogadores em um banco de dados SQLite.
* **Controles Duplos:** Suporte para dois jogadores simultâneos com controles distintos (Setas + Enter para P1, WASD + Espaço para P2).



##  Como Jogar (Controles)

### Menu Principal
* **Setas (Cima / Baixo):** Navegar entre as opções.
* **Enter:** Selecionar uma opção.

### Durante o Jogo

| Ação | Jogador 1 | Jogador 2 |
| :--- | :--- | :--- |
| **Mover para Cima** | Seta para Cima | W |
| **Mover para Baixo** | Seta para Baixo | S |
| **Atirar** | Enter | Barra de Espaço |

---

##  Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Biblioteca Gráfica:** Pygame
* **Banco de Dados:** SQLite 3 (para o ranking de scores)
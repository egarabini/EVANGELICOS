# Validação Mira - 10 Anjos, Satanás e Demônios

## Checklist previsto

- [ ] HTML gerado em `decks/10-anjos-satanas-e-demonios/index.html`.
- [ ] Conteúdo visível em português brasileiro.
- [ ] Pasta numerada para manter sequência do curso.
- [ ] Logo local `canal_sandeco_logo.png`.
- [ ] Referência a `header-bg.mp4`.
- [ ] Tema escuro com cor principal do projeto.
- [ ] Navegação card a card.
- [ ] Botão de próximo card e barra de progresso.
- [ ] D3.js carregado.
- [ ] Animações com entrada e loop interno.
- [ ] Sem placeholders do template.
- [ ] Sem cores antigas do Mira.
- [ ] Sem travessão.

## Resultado

Validação local concluída.

- HTML gerado em `decks/10-anjos-satanas-e-demonios/index.html`.
- 10 cards de estudo, além da abertura e do rodapé.
- 5 animações D3 com entrada e loop interno:
  - `animateCreated`
  - `animateWorship`
  - `animateProtection`
  - `animateDeception`
  - `animateVictory`
- Assets locais presentes:
  - `canal_sandeco_logo.png`
  - `header-bg.mp4`
- Logo presente no header e no rodapé.
- Vídeo de header com `autoplay`, `muted`, `loop`, `playsinline`, opacidade 50% e overlay em gradiente.
- Ganchos de navegação presentes:
  - `reading-progress`
  - `next-card`
  - `header-next-btn`
- Bibliotecas carregadas:
  - Tailwind
  - Lucide
  - D3 v7
  - AOS
- Cards marcados com `max-w-5xl` e `p-10`.
- Verificação sem ocorrências de placeholders do template.
- Verificação sem cores antigas do Mira.
- Verificação sem travessão.

Observação: `header-bg.mp4` foi criado como placeholder local, seguindo o padrão dos decks anteriores. A abertura usa fallback visual em CSS caso o vídeo esteja vazio.

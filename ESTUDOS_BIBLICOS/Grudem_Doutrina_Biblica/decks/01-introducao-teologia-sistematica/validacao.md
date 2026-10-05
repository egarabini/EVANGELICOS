# Relatório de Validação: Introdução à Teologia Sistemática

**Arquivo:** `decks/introducao-teologia-sistematica/index.html`  
**Data:** 2026-06-16

## Resultado geral

- **Passou:** estrutura, cores, navegação, D3, logo local, quantidade mínima de cards e ausência de placeholders.
- **Avisos:** `header-bg.mp4` existe, mas está vazio porque o projeto não possui vídeos em `videos_header/` e `ffmpeg` não está disponível para gerar um vídeo real. O HTML inclui fallback visual animado em CSS no header.
- **Falhas críticas encontradas:** nenhuma nos checks textuais executados.

## Checks executados

### Críticos

- **PASS A1:** cor primária `#FF904D` presente.
- **PASS A1:** cores proibidas `#FFA203` e `#e47d5b` ausentes.
- **PASS A2:** fundo `#000000` presente no `body`.
- **PASS A3:** `rgba(255, 144, 77, ...)` presente.
- **PASS B1/B2:** logo `canal_sandeco_logo.png` referenciada no header e no rodapé.
- **PASS B3:** arquivo `canal_sandeco_logo.png` existe no deck.
- **PASS C1/C3/C4/C5:** vídeo de header referenciado, atributos obrigatórios presentes, opacidade 50% e overlay com `linear-gradient`.
- **WARN C2:** `header-bg.mp4` existe, mas é um placeholder vazio por ausência de vídeos locais.

### Importantes

- **PASS D1:** cards usam `max-w-5xl`.
- **PASS D2:** cards usam `p-8` ou `p-10`.
- **PASS D3:** `<main>` usa `gap-[60vh]`.
- **PASS D4:** `backdrop-filter: blur(10px)` presente.
- **PASS E1:** fonte Inter carregada.
- **PASS E2:** títulos de cards usam `text-4xl`.
- **PASS F1-F7:** barra de progresso, botão próximo card, botão iniciar, AOS, Lucide, D3 e `setupFullScreenWrappers` presentes.

### Qualidade

- **PASS G1:** 9 cards no corpo da apresentação.
- **PASS G3:** CTA presente no meio do deck.
- **PASS G5:** sem placeholders residuais dos templates.
- **PASS:** 5 animações D3 com loop interno contínuo.

## Observações de animação

- Slide 1: partículas sobem continuamente no header.
- Slide 2: temas orbitam a Bíblia e o núcleo pulsa.
- Slide 3: fragmentos alternam entre dispersão e organização.
- Slide 4: a luz percorre a ponte Escritura, crença e vida.
- Slide 8: a balança doutrinária oscila em loop.
- Slide 9: marcador percorre continuamente o ciclo de estudo.

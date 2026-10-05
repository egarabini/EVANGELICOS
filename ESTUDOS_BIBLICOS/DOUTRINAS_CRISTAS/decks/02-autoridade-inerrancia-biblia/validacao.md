# Relatório de Validação: A Autoridade e Inerrância da Bíblia

**Arquivo:** `decks/autoridade-inerrancia-biblia/index.html`  
**Data:** 2026-06-16

## Resultado geral

- **Passou:** estrutura, cores, navegação, D3, logo local, quantidade mínima de cards e ausência de placeholders.
- **Avisos:** `header-bg.mp4` existe, mas está vazio porque o projeto não possui vídeos reais em `videos_header/`. O HTML inclui fallback visual animado em CSS no header.
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

- **PASS G1:** 10 cards no corpo da apresentação.
- **PASS G3:** CTA presente no meio do deck.
- **PASS G5:** sem placeholders residuais dos templates.
- **PASS:** 5 animações D3 com loop interno contínuo.

## Observações de animação

- Header: partículas sobem continuamente.
- Slide 2: fontes bíblicas convergem para a Escritura e o selo pulsa.
- Slide 3: ondas saem da Palavra e alcançam o coração em loop.
- Slide 6: a linha de verdade atravessa as declarações continuamente.
- Slide 9: dominós de consequências inclinam e se recompõem.
- Slide 10: o fundamento escrito pulsa sustentando fé, ensino, obediência e igreja.

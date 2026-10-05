<!-- template_slide.md — Template para Slides do Mira -->

<!-- ================================================ -->
<!-- SLIDE: {NOME DO SLIDE}                          -->
<!-- ================================================ -->
<div class="slide" data-slide="{NÚMERO}">
  <div class="mira-card">

    <!-- ================================================ -->
    <!-- CARD HEADER                                     -->
    <!-- ================================================ -->
    <div class="card-header">
      <!-- Label opcional (ex: "Capítulo 01") -->
      <span class="card-label">{LABEL}</span>

      <!-- Título do slide (máx 6 palavras, sem ícone) -->
      <h2 class="card-title">{TÍTULO DO SLIDE}</h2>

      <!-- Subtítulo opcional -->
      <p class="card-subtitle">{SUBTÍTULO Opcional}</p>
    </div>

    <!-- ================================================ -->
    <!-- CARD CANVAS (ANIMAÇÃO D3.JS)                    -->
    <!-- ================================================ -->
    <div class="card-canvas">
      <svg id="animacao-{N}" viewBox="0 0 1920 800" class="animacao-svg">
        <!-- D3.js vai renderizar aqui -->
      </svg>
    </div>

    <!-- ================================================ -->
    <!-- CARD BASE (DESCRIÇÃO + PÍLULAS)                 -->
    <!-- ================================================ -->
    <div class="card-base">

      <!-- Descrição ou legenda -->
      <p class="card-description">
        {DESCRIÇÃO OU LEGENDA DO SLIDE}
      </p>

      <!-- Pílulas (tags/pontos-chave) -->
      <div class="card-pills">
        <span class="pill" style="background: var(--mira-primary);">
          {PÍLULA 1}
        </span>
        <span class="pill" style="background: var(--mira-secondary);">
          {PÍLULA 2}
        </span>
        <span class="pill" style="background: var(--mira-accent);">
          {PÍLULA 3}
        </span>
      </div>

    </div>

    <!-- ================================================ -->
    <!-- REPLAY BUTTON (opcional)                         -->
    <!-- ================================================ -->
    <button class="replay-btn" onclick="replayAnimacao({N})">
      <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
      </svg>
    </button>

  </div>
</div>

<!-- ================================================ -->
<!-- ANIMAÇÃO D3.JS (SCRIPT)                           -->
<!-- ================================================ -->
<script>
  // Configuração da animação
  const config_{N} = {
    duration: {DURAÇÃO_MS},        // Ex: 5000
    loop: true,                    // Sempre true
    easing: d3.easeCubic,         // Função de easing
  };

  // Função de animação
  function animacao_{N}(svg) {

    // === ELEMENTOS ===
    // Criar elementos D3 aqui
    const g = svg.append("g")
      .attr("class", "grupo-principal");

    // === COREOGRAFIA DE ENTRADA ===
    // Animação inicial
    g.selectAll(".elemento")
      .data(dados)
      .enter()
      .append("circle")
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .attr("r", 0)                     // Começa invisível
      .transition()
      .duration(config_{N}.duration)   // Duração da entrada
      .ease(config_{N}.easing)
      .attr("r", d => d.r);            // Tamanho final

    // === LOOP INTERNO PERPÉTUO ===
    // Animação que continua forever
    function loop() {
      g.selectAll(".elemento")
        .transition()
        .duration(2000)                // Duração do loop
        .attr("cx", d => d.x + Math.sin(Date.now() / 1000) * 50)
        .transition()
        .duration(2000)
        .attr("cx", d => d.x - Math.sin(Date.now() / 1000) * 50)
        .on("end", function repeat() {
          loop();                      // Repete forever
        });
    }

    // Iniciar loop
    loop();
  }

  // Inicializar animação quando o slide estiver visível
  const observer_{N} = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const svg = d3.select("#animacao-{N}");
        animacao_{N}(svg);
        observer_{N}.disconnect();     // Executa uma vez
      }
    });
  }, { threshold: 0.5 });

  observer_{N}.observe(document.querySelector(`[data-slide="{N}"]`));
</script>

<!-- ================================================ -->
<!-- INSTRUÇÕES DE USO                                -->
<!-- ================================================ -->
<!--
1. Copie este código para o arquivo index.html do deck
2. Substitua todos os campos entre chaves {} pelas informações reais
3. Implemente a animação D3.js na função animacao_{N}
4. Adicione o CSS necessário (se aplicável)
5. Teste a animação no navegador

CAMPOS OBRIGATÓRIOS:
- {NOME DO SLIDE}          — Nome descritivo do slide
- {NÚMERO}                  — Número do slide (1, 2, 3...)
- {TÍTULO DO SLIDE}        — Título (máx 6 palavras, sem ícone)
- {DESCRIÇÃO OU LEGENDA}   — Texto descritivo
- {DURAÇÃO_MS}             — Duração da entrada em ms (ex: 5000)

CAMPOS OPCIONAIS:
- {LABEL}                  — Label opcional no header
- {SUBTÍTULO}              — Subtítulo opcional
- {PÍLULA 1, 2, 3}         — Tags/pontos-chave

REGRAS DE ANIMAÇÃO:
- Toda animação deve ENTRAR com coreografia
- DEPOIS continuar em loop interno perpétuo
- Animação estática é PROIBIDA
- Use sempre CSS variables do tema

CSS VARIABLES DO TEMA:
- var(--mira-primary)      — Laranja primário
- var(--mira-secondary)    — Azul secundário
- var(--mira-accent)       — Verde de destaque
- var(--mira-bg-primary)   — Fundo principal
- var(--mira-bg-card)      — Fundo dos cards
- var(--mira-text-primary) — Texto principal
-->

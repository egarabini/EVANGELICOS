# Slides — Templates de Slides

> **Templates HTML para criar slides individuais**

---

## Sobre Esta Pasta

Esta pasta contém templates de slides HTML usados como base para criar apresentações animadas com o Mira.

---

## Templates Disponíveis

### card_capa.html

Template para slide de capa:
- Título principal
- Subtítulo
- Informações sobre o apresentador
- Animação de entrada

### card_encerramento.html

Template para slide de encerramento:
- Mensagem final
- Call to action
- Informações de contato
- Animação de saída

### card_conteudo.html

Template para slide de conteúdo:
- Título
- Conteúdo principal
- Pílulas de resumo
- Animação interativa

---

## Estrutura de um Slide

```html
<div class="mira-card">
  <!-- Header -->
  <div class="card-header">
    <h2 class="card-title">Título do Slide</h2>
  </div>

  <!-- Canvas de animação -->
  <div class="card-canvas">
    <svg id="animacao"></svg>
  </div>

  <!-- Base -->
  <div class="card-base">
    <p class="card-description">Descrição ou legenda</p>
    <div class="card-pills">
      <span class="pill">Pílula 1</span>
      <span class="pill">Pílula 2</span>
    </div>
  </div>
</div>
```

---

## Como Criar Novo Template

1. Copie um template existente
2. Modifique conforme necessário
3. Use CSS variables do tema
4. Teste em diferentes temas
5. Documente o propósito

---

> *"Bons templates economizam tempo e garantem consistência."*

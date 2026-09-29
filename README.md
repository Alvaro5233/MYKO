<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MYKO — Hongos funcionales, cultivados por nosotros</title>
<style>
  :root{
    --ink: #40281F;
    --ink-soft: #6B4A3A;
    --paper: #F6EFE6;
    --paper-alt: #FFFCF5;
    --green: #17684C;
    --green-deep: #0F4E38;
    --white: #FFFFFF;
    --cream-soft: #D9C9B4;
    --line: #E4D6C2;
    --line-dark: rgba(246,239,230,0.2);
    --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
    --sans: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }

  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{
    margin:0;
    background:var(--paper);
    color:var(--ink);
    font-family:var(--sans);
    line-height:1.6;
    -webkit-font-smoothing:antialiased;
  }
  a{color:inherit;}
  img,svg{display:block;max-width:100%;}
  :focus-visible{
    outline:3px solid var(--green);
    outline-offset:3px;
    border-radius:4px;
  }
  section{scroll-margin-top:76px;}
  .wrap{
    max-width:1140px;
    margin:0 auto;
    padding:0 32px;
  }
  h1,h2,h3{font-family:var(--serif); font-weight:700; margin:0;}
  .eyebrow{
    font-size:0.92rem;
    color:var(--green);
    font-weight:600;
    margin:0 0 12px;
  }

  /* ---------- Nav ---------- */
  .nav{
    position:sticky;
    top:0;
    z-index:30;
    background:rgba(64,40,31,0.96);
    backdrop-filter:blur(8px);
  }
  .nav-inner{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:24px;
    padding:16px 32px;
    max-width:1140px;
    margin:0 auto;
  }
  .brand{
    font-family:var(--serif);
    font-size:1.4rem;
    letter-spacing:0.03em;
    color:var(--paper);
  }
  .nav-right{
    display:flex;
    align-items:center;
    gap:22px;
  }
  .nav-links{
    display:flex;
    align-items:center;
    gap:26px;
    list-style:none;
    margin:0;
    padding:0;
    overflow-x:auto;
    scrollbar-width:none;
  }
  .nav-links::-webkit-scrollbar{display:none;}
  .nav-links a{
    white-space:nowrap;
    text-decoration:none;
    color:var(--cream-soft);
    font-size:0.94rem;
    font-weight:500;
    padding:6px 2px;
    border-bottom:2px solid transparent;
    transition:border-color 0.2s ease, color 0.2s ease;
  }
  .nav-links a:hover{
    color:var(--paper);
    border-bottom-color:var(--green);
  }
  .nav-links a.nav-cta{
    color:var(--ink);
    background:var(--paper);
    padding:8px 16px;
    border-radius:999px;
    font-weight:600;
  }
  .nav-links a.nav-cta:hover{
    background:var(--white);
    border-bottom-color:transparent;
  }
  .cart-button{
    display:flex;
    align-items:center;
    gap:8px;
    background:transparent;
    border:1px solid var(--line-dark);
    color:var(--paper);
    font-family:var(--sans);
    font-size:0.9rem;
    font-weight:600;
    padding:8px 14px;
    border-radius:999px;
    cursor:pointer;
    flex-shrink:0;
    transition:border-color 0.2s ease, background 0.2s ease;
  }
  .cart-button:hover{border-color:var(--cream-soft); background:rgba(246,239,230,0.06);}
  .cart-button svg{width:17px; height:17px; stroke:var(--paper); fill:none; stroke-width:1.8;}
  .cart-count{
    background:var(--green);
    color:var(--white);
    font-size:0.78rem;
    font-weight:700;
    min-width:19px;
    height:19px;
    border-radius:999px;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:0 5px;
  }

  /* ---------- Hero ---------- */
  .hero{padding:100px 0 92px; background:var(--paper);}
  .hero-grid{
    display:grid;
    grid-template-columns:1.05fr 0.95fr;
    gap:56px;
    align-items:center;
  }
  .hero h1{
    font-size:clamp(2.5rem, 4.2vw, 3.6rem);
    line-height:1.1;
    max-width:15ch;
    margin-bottom:22px;
  }
  .hero p{
    font-size:1.15rem;
    color:var(--ink-soft);
    max-width:44ch;
    margin:0 0 34px;
  }
  .btn-row{display:flex; gap:16px; flex-wrap:wrap;}
  .btn{
    display:inline-block;
    text-decoration:none;
    font-size:1rem;
    font-weight:600;
    padding:15px 30px;
    border-radius:999px;
    transition:transform 0.15s ease, background 0.15s ease;
    border:none;
    cursor:pointer;
    font-family:var(--sans);
  }
  .btn-primary{
    background:var(--ink);
    color:var(--paper);
    border:1px solid var(--ink);
  }
  .btn-primary:hover{background:var(--green-deep); border-color:var(--green-deep); transform:translateY(-1px);}
  .btn-ghost{
    background:transparent;
    color:var(--ink);
    border:1px solid var(--ink-soft);
  }
  .btn-ghost:hover{border-color:var(--ink); transform:translateY(-1px);}
  .btn-on-dark{background:var(--paper); color:var(--ink); border:1px solid var(--paper);}
  .btn-on-dark:hover{background:var(--white);}

  .shroom{width:100%; max-width:420px; margin-left:auto;}
  .shroom-line{
    fill:none;
    stroke:var(--ink);
    stroke-width:1.8;
    stroke-linecap:round;
    stroke-linejoin:round;
    stroke-dasharray:1600;
    stroke-dashoffset:1600;
    animation:draw-shroom 1.9s ease-out forwards;
  }
  .shroom-line--accent{stroke:var(--green); animation-delay:0.3s;}
  @keyframes draw-shroom{ to{ stroke-dashoffset:0; } }
  @media (prefers-reduced-motion: reduce){
    .shroom-line{animation:none; stroke-dashoffset:0;}
    .btn, .card, .pillar, .proceso-node{transition:none;}
  }

  /* ---------- El problema (banda oscura) ---------- */
  .problema{
    background:var(--ink);
    color:var(--paper);
    padding:88px 0;
  }
  .problema-inner{max-width:62ch;}
  .problema-lead{
    font-size:1.2rem;
    color:var(--cream-soft);
    margin:0 0 18px;
  }
  .problema-words{
    display:flex;
    flex-wrap:wrap;
    gap:12px 28px;
    margin:0 0 40px;
    padding:0;
    list-style:none;
    font-family:var(--serif);
    font-size:1.15rem;
    color:var(--paper);
  }
  .problema-words li::before{
    content:"·";
    color:var(--green);
    margin-right:10px;
  }
  .problema h2{
    font-size:clamp(1.7rem, 2.8vw, 2.2rem);
    color:var(--paper);
    max-width:20ch;
  }

  /* ---------- El hongo ---------- */
  .melena{
    padding:96px 0;
    background:var(--paper-alt);
    border-top:1px solid var(--line);
    border-bottom:1px solid var(--line);
  }
  .melena-grid{
    display:grid;
    grid-template-columns:0.85fr 1.15fr;
    gap:56px;
    align-items:center;
  }
  .melena h2{
    font-size:clamp(1.9rem, 2.8vw, 2.3rem);
    margin-bottom:18px;
  }
  .melena p{color:var(--ink-soft); font-size:1.02rem; margin:0 0 16px;}
  .melena-facts{display:flex; gap:28px; margin-top:26px; flex-wrap:wrap;}
  .melena-fact{border-left:2px solid var(--green); padding-left:14px;}
  .melena-fact strong{display:block; font-family:var(--serif); font-size:1.05rem; color:var(--ink);}
  .melena-fact span{font-size:0.87rem; color:var(--ink-soft);}
  .melena-art{width:100%; max-width:300px;}

  /* ---------- Por qué Myko (pilares) ---------- */
  .porque{padding:92px 0 96px; background:var(--paper);}
  .section-head{max-width:60ch; margin-bottom:48px;}
  .section-head h2{font-size:clamp(2rem, 3vw, 2.5rem); margin-bottom:14px;}
  .section-head p{color:var(--ink-soft); font-size:1.05rem; margin:0;}

  .pillars{display:grid; grid-template-columns:repeat(4, 1fr); gap:32px;}
  .pillar-icon{width:40px; height:40px; margin-bottom:16px; stroke:var(--green); fill:none; stroke-width:1.7;}
  .pillar h3{font-size:1.08rem; margin-bottom:8px;}
  .pillar p{color:var(--ink-soft); font-size:0.93rem; margin:0; max-width:28ch;}

  /* ---------- Proceso ---------- */
  .proceso{
    padding:96px 0 100px;
    background:var(--ink);
    color:var(--paper);
  }
  .proceso .section-head h2{color:var(--paper);}
  .proceso .section-head p{color:var(--cream-soft);}
  .proceso-chain{
    display:flex;
    align-items:center;
    gap:0;
    flex-wrap:wrap;
  }
  .proceso-node{
    display:flex;
    flex-direction:column;
    align-items:center;
    text-align:center;
    gap:10px;
    width:110px;
  }
  .proceso-dot{
    width:14px; height:14px;
    border-radius:50%;
    background:var(--cream-soft);
  }
  .proceso-node.is-final .proceso-dot{background:var(--green); width:18px; height:18px;}
  .proceso-node span{
    font-family:var(--serif);
    font-size:0.92rem;
    letter-spacing:0.02em;
    color:var(--paper);
  }
  .proceso-node.is-final span{color:var(--green); font-weight:700; font-size:1.05rem;}
  .proceso-arrow{
    flex:1;
    min-width:24px;
    height:1px;
    background:var(--line-dark);
    margin:0 4px;
    align-self:flex-start;
    margin-top:7px;
  }

  /* ---------- Producto ---------- */
  .producto{padding:96px 0 100px; background:var(--paper);}
  .cards{display:grid; grid-template-columns:repeat(3, 1fr); gap:26px;}
  .card{
    background:var(--paper-alt);
    border:1px solid var(--line);
    border-radius:8px;
    padding:30px 26px;
    border-top:4px solid var(--card-accent, var(--green));
    display:flex;
    flex-direction:column;
  }
  .card:nth-child(1){--card-accent: var(--ink);}
  .card:nth-child(2){--card-accent: var(--green);}
  .card:nth-child(3){--card-accent: var(--ink-soft);}
  .card h3{font-size:1.2rem; margin-bottom:6px;}
  .card .fact{display:inline-block; font-size:0.88rem; font-weight:600; color:var(--card-accent, var(--green)); margin-bottom:12px;}
  .card p{color:var(--ink-soft); font-size:0.95rem; margin:0;}
  .card-footer{
    margin-top:20px;
    padding-top:16px;
    border-top:1px solid var(--line);
    display:flex;
    align-items:center;
    gap:12px;
  }
  .btn-add-cart{
    background:var(--ink);
    color:var(--paper);
    border:1px solid var(--ink);
    border-radius:999px;
    padding:10px 20px;
    font-size:0.9rem;
    font-weight:600;
    cursor:pointer;
    font-family:var(--sans);
    transition:background 0.15s ease;
  }
  .btn-add-cart:hover{background:var(--green-deep); border-color:var(--green-deep);}
  .btn-add-cart:disabled{
    background:var(--line);
    border-color:var(--line);
    color:var(--ink-soft);
    cursor:not-allowed;
  }
  .card-feedback{
    font-size:0.82rem;
    color:var(--green);
    min-height:1em;
  }
  .card-feedback[data-state="error"]{color:#A24A32;}

  /* ---------- Comunidad ---------- */
  .comunidad{padding:96px 0 100px; background:var(--paper-alt); border-top:1px solid var(--line); border-bottom:1px solid var(--line);}
  .comunidad-grid{display:grid; grid-template-columns:1fr 0.9fr; gap:56px;}
  .steps{display:flex; flex-direction:column; gap:26px;}
  .step{display:flex; gap:18px; align-items:flex-start;}
  .step-num{
    flex-shrink:0; width:32px; height:32px; border-radius:50%;
    border:1.5px solid var(--green); color:var(--green);
    display:flex; align-items:center; justify-content:center;
    font-family:var(--serif); font-size:0.92rem;
  }
  .step h3{font-size:1.02rem; margin-bottom:4px;}
  .step p{color:var(--ink-soft); font-size:0.92rem; margin:0; max-width:38ch;}

  .membership-card{
    background:var(--ink);
    color:var(--paper);
    border-radius:10px;
    padding:36px 32px;
  }
  .membership-card h3{font-size:1.3rem; margin-bottom:6px;}
  .membership-price{font-family:var(--serif); font-size:1.9rem; color:var(--green); margin:6px 0 8px;}
  .membership-price span{font-size:0.92rem; color:var(--cream-soft); font-family:var(--sans);}
  .membership-note{font-size:0.85rem; color:var(--cream-soft); margin:0 0 22px;}
  .membership-list{list-style:none; margin:0 0 28px; padding:0; display:flex; flex-direction:column; gap:12px;}
  .membership-list li{display:flex; gap:10px; align-items:flex-start; color:var(--cream-soft); font-size:0.93rem;}
  .membership-list svg{width:17px; height:17px; flex-shrink:0; margin-top:2px; stroke:var(--green); fill:none; stroke-width:2.2;}
  .membership-card .btn{width:100%; text-align:center;}

  /* ---------- Ciencia ---------- */
  .ciencia{padding:96px 0 92px; background:var(--paper);}
  .ciencia-grid{display:grid; grid-template-columns:repeat(3, 1fr); gap:32px; margin-bottom:36px;}
  .ciencia-col h3{font-size:1rem; margin-bottom:10px; color:var(--ink);}
  .ciencia-col p{color:var(--ink-soft); font-size:0.93rem; margin:0;}
  .ciencia-col{border-top:2px solid var(--col-accent, var(--green)); padding-top:16px;}
  .ciencia-col:nth-child(1){--col-accent: var(--green);}
  .ciencia-col:nth-child(2){--col-accent: var(--ink-soft);}
  .ciencia-col:nth-child(3){--col-accent: var(--ink);}
  .ciencia-disclaimer{
    font-size:0.85rem;
    color:var(--ink-soft);
    border-left:2px solid var(--line);
    padding-left:16px;
    max-width:64ch;
  }

  /* ---------- Nosotros ---------- */
  .nosotros{padding:96px 0 100px; background:var(--ink); color:var(--paper);}
  .nosotros .section-head h2{color:var(--paper);}
  .nosotros .section-head p{color:var(--cream-soft);}
  .nosotros-lead{
    font-family:var(--serif);
    font-size:1.3rem;
    color:var(--paper);
    max-width:36ch;
    margin-bottom:44px;
  }
  .team{display:grid; grid-template-columns:repeat(3, 1fr); gap:32px; margin-bottom:44px;}
  .team-member{border-top:1px solid var(--line-dark); padding-top:18px;}
  .team-member h3{font-size:1.1rem; color:var(--paper); margin-bottom:4px;}
  .team-member span{font-size:0.86rem; color:var(--green); font-weight:600;}
  .team-member p{font-size:0.92rem; color:var(--cream-soft); margin:8px 0 0;}
  .nosotros-story{max-width:70ch; color:var(--cream-soft); font-size:1rem;}
  .nosotros-story p{margin:0 0 14px;}

  /* ---------- CTA final ---------- */
  .cta-final{
    padding:88px 0;
    background:var(--green);
    color:var(--white);
    text-align:center;
  }
  .cta-final h2{font-size:clamp(2rem, 3.4vw, 2.8rem); color:var(--white); margin-bottom:10px;}
  .cta-final p{font-size:1.1rem; color:rgba(255,255,255,0.85); margin:0 0 8px;}
  .cta-final .price{font-family:var(--serif); font-size:1.6rem; margin:14px 0 28px;}
  .cta-final .btn-primary{background:var(--white); color:var(--green-deep); border-color:var(--white);}
  .cta-final .btn-primary:hover{background:var(--paper);}

  /* ---------- Footer ---------- */
  footer{padding:48px 0 36px; background:var(--ink); border-top:1px solid var(--line-dark);}
  .footer-inner{display:flex; flex-wrap:wrap; justify-content:space-between; align-items:flex-end; gap:20px;}
  .footer-brand{font-family:var(--serif); font-size:1.1rem; color:var(--paper);}
  .footer-contact{color:var(--cream-soft); font-size:0.92rem;}
  .footer-contact a{color:var(--green); text-decoration:underline; text-decoration-color:var(--green);}
  .copyright{width:100%; margin-top:22px; font-size:0.82rem; color:var(--cream-soft);}

  /* ---------- Carrito (panel lateral) ---------- */
  .cart-overlay{
    position:fixed;
    inset:0;
    background:rgba(64,40,31,0.45);
    z-index:40;
    opacity:0;
    pointer-events:none;
    transition:opacity 0.2s ease;
  }
  .cart-overlay.is-open{opacity:1; pointer-events:auto;}
  .cart-panel{
    position:fixed;
    top:0;
    right:0;
    bottom:0;
    width:min(380px, 92vw);
    background:var(--paper-alt);
    z-index:41;
    padding:28px 26px;
    transform:translateX(100%);
    transition:transform 0.25s ease;
    display:flex;
    flex-direction:column;
    overflow-y:auto;
  }
  .cart-panel.is-open{transform:translateX(0);}
  .cart-panel-head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:22px;
  }
  .cart-panel-head h3{font-size:1.25rem;}
  .cart-close{
    background:none;
    border:none;
    font-size:1.4rem;
    line-height:1;
    color:var(--ink);
    cursor:pointer;
    padding:4px;
  }
  .cart-items{
    display:flex;
    flex-direction:column;
    gap:16px;
    flex:1;
  }
  .cart-empty{color:var(--ink-soft); font-size:0.95rem;}
  .cart-item{
    display:flex;
    justify-content:space-between;
    gap:12px;
    border-bottom:1px solid var(--line);
    padding-bottom:14px;
    font-size:0.92rem;
  }
  .cart-item strong{display:block; font-family:var(--serif); font-size:1rem;}
  .cart-item span{color:var(--ink-soft); font-size:0.85rem;}
  .cart-item-price{font-weight:600; white-space:nowrap;}
  .cart-total{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding-top:18px;
    margin-top:6px;
    border-top:1px solid var(--line);
    font-family:var(--serif);
    font-size:1.15rem;
  }

  /* ---------- Responsive ---------- */
  @media (max-width: 900px){
    .hero-grid{grid-template-columns:1fr;}
    .shroom{margin:0 auto; max-width:300px;}
    .pillars{grid-template-columns:repeat(2, 1fr);}
    .melena-grid{grid-template-columns:1fr;}
    .melena-art{margin:0 auto 8px; max-width:220px;}
    .cards{grid-template-columns:1fr;}
    .comunidad-grid{grid-template-columns:1fr; gap:44px;}
    .ciencia-grid{grid-template-columns:1fr; gap:24px;}
    .team{grid-template-columns:1fr;}
    .proceso-chain{flex-direction:column; align-items:flex-start;}
    .proceso-node{width:auto; flex-direction:row; text-align:left;}
    .proceso-arrow{display:none;}
  }
  @media (max-width: 520px){
    .wrap{padding:0 20px;}
    .nav-inner{padding:14px 20px; gap:14px;}
    .nav-links{gap:14px;}
    .nav-links a{font-size:0.86rem;}
    .hero{padding:60px 0 56px;}
    .problema, .melena, .porque, .proceso, .producto, .comunidad, .ciencia, .nosotros, .cta-final{padding-top:60px; padding-bottom:60px;}
    .pillars{grid-template-columns:1fr;}
  }
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <div class="brand">MYKO</div>
    <div class="nav-right">
      <ul class="nav-links">
        <li><a href="#inicio">Inicio</a></li>
        <li><a href="#hongo">Melena de León</a></li>
        <li><a href="#proceso">Proceso</a></li>
        <li><a href="#producto">Producto</a></li>
        <li><a href="#nosotros">Nosotros</a></li>
        <li><a href="#comunidad" class="nav-cta">Comunidad</a></li>
      </ul>
      <button type="button" class="cart-button" id="cart-toggle" aria-haspopup="true" aria-expanded="false">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M3 4h2l2.4 12.4a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.6L21 8H6" stroke-linecap="round" stroke-linejoin="round"></path><circle cx="10" cy="21" r="1.3"></circle><circle cx="17" cy="21" r="1.3"></circle></svg>
        <span class="cart-count" id="cart-count">0</span>
      </button>
    </div>
  </div>
</nav>

<div class="cart-overlay" id="cart-overlay"></div>
<aside class="cart-panel" id="cart-panel" aria-label="Carrito de compra">
  <div class="cart-panel-head">
    <h3>Tu carrito</h3>
    <button type="button" class="cart-close" id="cart-close" aria-label="Cerrar carrito">&times;</button>
  </div>
  <div class="cart-items" id="cart-items">
    <p class="cart-empty" id="cart-empty">Tu carrito está vacío.</p>
  </div>
  <div class="cart-total" id="cart-total" hidden>
    <span>Total</span>
    <span id="cart-total-amount">$0 MXN</span>
  </div>
</aside>

<section id="inicio" class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>El poder de los hongos, cultivado por nosotros</h1>
      <p>MYKO es una marca mexicana de hongos funcionales que cultiva su propia melena de león, de la cepa a la cosecha, para construir una nueva forma de relacionarnos con la naturaleza y el rendimiento humano.</p>
      <div class="btn-row">
        <a href="#nosotros" class="btn btn-primary">Conoce MYKO</a>
        <a href="#producto" class="btn btn-ghost">Ver producto</a>
      </div>
    </div>
    <svg class="shroom" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ilustración de un hongo Melena de León">
      <path class="shroom-line" d="M110 30c34 0 58 22 58 52 0 8-2 14-6 20 6 6 9 13 9 21 0 20-18 34-41 34H92c-25 0-45-15-45-35 0-9 4-17 10-23-5-6-8-13-8-21 0-27 24-48 61-48Z"></path>
      <path class="shroom-line shroom-line--accent" d="M78 120c-2 14-2 28 2 40M96 128c-1 16 0 30 4 42M116 128c1 16 2 30-1 42M136 122c3 14 4 28 1 40"></path>
      <path class="shroom-line shroom-line--accent" d="M70 78c-4 10-4 20 1 28M150 76c4 10 4 20-1 28M92 58c-3 8-3 16 1 22M130 58c3 8 3 16-1 22"></path>
    </svg>
  </div>
</section>

<section class="problema">
  <div class="wrap problema-inner">
    <p class="problema-lead">Vivimos conectados, cansados y constantemente estimulados.</p>
    <ul class="problema-words">
      <li>Café</li>
      <li>Pantallas</li>
      <li>Estrés</li>
      <li>Jornadas largas</li>
    </ul>
    <h2>Creemos que la naturaleza puede formar parte de una mejor forma de vivir.</h2>
  </div>
</section>

<section id="hongo" class="melena">
  <div class="wrap melena-grid">
    <svg class="melena-art" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ilustración simplificada de la Melena de León">
      <circle cx="100" cy="95" r="55" fill="none" stroke="var(--ink)" stroke-width="1.8"></circle>
      <g stroke="var(--green)" stroke-width="1.6" stroke-linecap="round" fill="none">
        <path d="M60 110c-3 12-3 24 1 34"></path>
        <path d="M78 122c-2 14-1 26 3 36"></path>
        <path d="M100 126c0 15 1 27 4 38"></path>
        <path d="M122 122c2 14 1 26-3 36"></path>
        <path d="M140 110c3 12 3 24-1 34"></path>
      </g>
    </svg>
    <div>
      <span class="eyebrow">Nuestro primer hongo</span>
      <h2>Melena de León</h2>
      <p><em>Hericium erinaceus</em> es el punto de partida de MYKO. La elegimos porque es uno de los hongos funcionales más estudiados dentro del mundo de la cognición y el bienestar, y porque su cultivo es un buen primer reto para dominar antes de expandirnos a otras especies.</p>
      <p>No la presentamos como una promesa médica. La presentamos como lo que es: un hongo funcional con un perfil de compuestos interesante, cultivado por nosotros de principio a fin.</p>
      <div class="melena-facts">
        <div class="melena-fact">
          <strong>Hericium erinaceus</strong>
          <span>Nombre científico</span>
        </div>
        <div class="melena-fact">
          <strong>Erinacinas</strong>
          <span>Compuestos de interés</span>
        </div>
        <div class="melena-fact">
          <strong>Cultivo propio</strong>
          <span>De la cepa al producto</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="porque">
  <div class="wrap">
    <div class="section-head">
      <h2>¿Por qué MYKO?</h2>
      <p>Cuatro cosas que nos distinguen de comprar una cápsula genérica.</p>
    </div>
    <div class="pillars">
      <div class="pillar">
        <svg class="pillar-icon" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M16 5c8 0 13 6 13 13s-5 13-13 13S3 25 3 18 8 5 16 5Z"></path>
          <path d="M16 12v12M11 16l5-4 5 4" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        <h3>Cultivado por nosotros</h3>
        <p>Controlamos progresivamente el proceso, desde la cepa hasta el producto final.</p>
      </div>
      <div class="pillar">
        <svg class="pillar-icon" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <circle cx="16" cy="13" r="8"></circle>
          <path d="M16 5v-3M9 25l-2 6M23 25l2 6M13 30h6" stroke-linecap="round"></path>
        </svg>
        <h3>Hongos funcionales</h3>
        <p>Seleccionamos especies con interés real dentro de la investigación en hongos funcionales.</p>
      </div>
      <div class="pillar">
        <svg class="pillar-icon" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M16 4l11 5v7c0 8-5 13.5-11 16-6-2.5-11-8-11-16V9l11-5Z" stroke-linejoin="round"></path>
          <path d="M11 16l4 4 7-8" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        <h3>Transparencia</h3>
        <p>Queremos que sepas qué estás consumiendo y de dónde viene, sin letra chica.</p>
      </div>
      <div class="pillar">
        <svg class="pillar-icon" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <circle cx="16" cy="16" r="12"></circle>
          <path d="M16 9v7l5 3" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
        <h3>Hecho para tu día</h3>
        <p>Una forma sencilla de incorporar hongos funcionales a una rutina real, no a un ideal.</p>
      </div>
    </div>
  </div>
</section>

<section id="proceso" class="proceso">
  <div class="wrap">
    <div class="section-head">
      <h2>Nuestro proceso</h2>
      <p>Del hongo al producto. Todo empieza con nosotros.</p>
    </div>
    <div class="proceso-chain">
      <div class="proceso-node"><div class="proceso-dot"></div><span>Cepa</span></div>
      <div class="proceso-arrow"></div>
      <div class="proceso-node"><div class="proceso-dot"></div><span>Micelio</span></div>
      <div class="proceso-arrow"></div>
      <div class="proceso-node"><div class="proceso-dot"></div><span>Cultivo</span></div>
      <div class="proceso-arrow"></div>
      <div class="proceso-node"><div class="proceso-dot"></div><span>Fructificación</span></div>
      <div class="proceso-arrow"></div>
      <div class="proceso-node"><div class="proceso-dot"></div><span>Cosecha</span></div>
      <div class="proceso-arrow"></div>
      <div class="proceso-node"><div class="proceso-dot"></div><span>Secado</span></div>
      <div class="proceso-arrow"></div>
      <div class="proceso-node is-final"><div class="proceso-dot"></div><span>MYKO</span></div>
    </div>
  </div>
</section>

<section id="producto" class="producto">
  <div class="wrap">
    <div class="section-head">
      <h2>Melena de León MYKO</h2>
      <p>Nuestra primera línea, cultivada por nosotros de principio a fin.</p>
    </div>
    <div class="cards">
      <article class="card" data-producto-id="101" data-producto-nombre="Cápsulas Melena de León" data-producto-precio="300">
        <h3>Cápsulas</h3>
        <span class="fact">$300 MXN · 60 cápsulas</span>
        <p>Nuestra presentación más práctica para incorporarla a tu rutina diaria, sin preparación.</p>
        <div class="card-footer">
          <button type="button" class="btn-add-cart" data-add-to-cart>Agregar al carrito</button>
        </div>
        <p class="card-feedback" data-feedback></p>
      </article>
      <article class="card" data-producto-id="102" data-producto-nombre="Polvo Melena de León" data-producto-precio="300">
        <h3>Polvo</h3>
        <span class="fact">$300 MXN · gramaje en definición</span>
        <p>Para quienes prefieren dosificar a su manera o combinarla en bebidas y recetas.</p>
        <div class="card-footer">
          <button type="button" class="btn-add-cart" data-add-to-cart>Agregar al carrito</button>
        </div>
        <p class="card-feedback" data-feedback></p>
      </article>
      <article class="card">
        <h3>Próximamente</h3>
        <span class="fact">Reishi · Shiitake · Cordyceps</span>
        <p>La melena de león es el primer paso. La visión de MYKO es ampliar la línea a otras especies de hongos funcionales.</p>
        <div class="card-footer">
          <button type="button" class="btn-add-cart" disabled>Aún no disponible</button>
        </div>
      </article>
    </div>
  </div>
</section>

<section id="comunidad" class="comunidad">
  <div class="wrap">
    <div class="section-head">
      <h2>Comunidad MYKO</h2>
      <p>Una membresía que no solo te da descuento: te mantiene informado.</p>
    </div>
    <div class="comunidad-grid">
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <div>
            <h3>Elige tu plan</h3>
            <p>Activa tu membresía MYKO en un par de minutos, sin compromisos largos.</p>
          </div>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <div>
            <h3>Compra con descuento</h3>
            <p>Tu descuento aplica automáticamente en cada producto MYKO mientras tu membresía esté activa.</p>
          </div>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <div>
            <h3>Mantente informado</h3>
            <p>Recibe contenido curado sobre hongos funcionales y entra a la comunidad privada MYKO.</p>
          </div>
        </div>
      </div>
      <div class="membership-card">
        <h3>Membresía MYKO</h3>
        <div class="membership-price">$99 MXN <span>/ mes</span></div>
        <p class="membership-note">Precio de lanzamiento, sujeto a ajuste.</p>
        <ul class="membership-list">
          <li><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5 12l4 4 10-10" stroke-linecap="round" stroke-linejoin="round"></path></svg>Descuento en cada compra de producto MYKO</li>
          <li><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5 12l4 4 10-10" stroke-linecap="round" stroke-linejoin="round"></path></svg>Contenido curado sobre hongos funcionales, directo a tu correo</li>
          <li><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5 12l4 4 10-10" stroke-linecap="round" stroke-linejoin="round"></path></svg>Acceso a la comunidad privada MYKO</li>
          <li><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M5 12l4 4 10-10" stroke-linecap="round" stroke-linejoin="round"></path></svg>Acceso anticipado a nuevas especies y productos</li>
        </ul>
        <a href="#" class="btn btn-on-dark">Unirme a la membresía</a>
      </div>
    </div>
  </div>
</section>

<section class="ciencia">
  <div class="wrap">
    <div class="section-head">
      <h2>¿Qué sabemos sobre la melena de León?</h2>
      <p>Preferimos ser claros sobre lo que la evidencia dice hoy, no venderte una promesa.</p>
    </div>
    <div class="ciencia-grid">
      <div class="ciencia-col">
        <h3>Lo que se ha observado</h3>
        <p>Estudios preliminares en modelos celulares y animales han observado compuestos como las erinacinas, relacionados con procesos del sistema nervioso.</p>
      </div>
      <div class="ciencia-col">
        <h3>Lo que sigue en investigación</h3>
        <p>La investigación en humanos sobre cognición, memoria y manejo del estrés todavía es limitada, con estudios pequeños y resultados que necesitan confirmarse.</p>
      </div>
      <div class="ciencia-col">
        <h3>Lo que no afirmamos</h3>
        <p>No decimos que la melena de león cure, trate o prevenga ninguna enfermedad, ni que "te haga más inteligente". Nos tomamos los hongos en serio, no las promesas fáciles.</p>
      </div>
    </div>
    <p class="ciencia-disclaimer">MYKO no sustituye diagnóstico, tratamiento médico ni asesoría profesional. Esta información es únicamente educativa; consulta a un profesional de la salud antes de iniciar cualquier suplemento.</p>
  </div>
</section>

<section id="nosotros" class="nosotros">
  <div class="wrap">
    <div class="section-head">
      <h2>Nosotros</h2>
      <p>Tres amigos. Una obsesión por los hongos.</p>
    </div>
    <p class="nosotros-lead">Empezamos con placas de cultivo en un cuarto, aprendiendo a fuerza de contaminaciones y ensayo y error, porque queríamos construir algo real alrededor de los hongos funcionales — no solo revender cápsulas.</p>
    <div class="team">
      <div class="team-member">
        <h3>Álvaro</h3>
        <span>Finanzas y estrategia</span>
        <p>Estructura del negocio, costos y modelo comercial.</p>
      </div>
      <div class="team-member">
        <h3>Ricardo</h3>
        <span>Biología y cultivo</span>
        <p>Cepas, procesos biológicos y cuidado del hongo.</p>
      </div>
      <div class="team-member">
        <h3>Orlando</h3>
        <span>Marketing y comunicación</span>
        <p>Contenido, comercialización y la voz de MYKO.</p>
      </div>
    </div>
    <div class="nosotros-story">
      <p>Primero cultivamos melena de león. Después dominamos el cultivo. Después ampliamos especies. Después desarrollamos productos. La meta a largo plazo es construir una marca mexicana de referencia en hongos funcionales — controlando cada vez más de nuestra propia cadena de producción, desde la cepa hasta el producto final.</p>
    </div>
  </div>
</section>

<section class="cta-final">
  <div class="wrap">
    <h2>Empieza con MYKO</h2>
    <p>Conoce nuestra melena de león.</p>
    <div class="price">$300 MXN</div>
    <a href="#producto" class="btn btn-primary">Comprar</a>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="footer-inner">
      <div class="footer-brand">MYKO</div>
      <div class="footer-contact">Escríbenos a <a href="mailto:hola@myko.mx">hola@myko.mx</a></div>
    </div>
    <p class="copyright">© 2026 MYKO. Todos los derechos reservados.</p>
  </div>
</footer>

<script>
(function(){
  // URL del backend de carrito.py. Cámbiala cuando lo desplieguen fuera de tu máquina.
  var API_URL = "http://localhost:5000/carrito/agregar";

  // Mientras no exista login, simulamos un cliente y un carrito fijos para esta sesión del navegador.
  var idCarrito = Math.floor(Math.random() * 100000);
  var codigoCliente = Math.floor(Math.random() * 100000);

  var carrito = []; // Copia local para pintar el panel; la fuente de verdad es el backend.

  var cartToggle = document.getElementById("cart-toggle");
  var cartClose = document.getElementById("cart-close");
  var cartOverlay = document.getElementById("cart-overlay");
  var cartPanel = document.getElementById("cart-panel");
  var cartCount = document.getElementById("cart-count");
  var cartItemsEl = document.getElementById("cart-items");
  var cartEmptyEl = document.getElementById("cart-empty");
  var cartTotalEl = document.getElementById("cart-total");
  var cartTotalAmountEl = document.getElementById("cart-total-amount");

  function abrirCarrito(){
    cartPanel.classList.add("is-open");
    cartOverlay.classList.add("is-open");
    cartToggle.setAttribute("aria-expanded", "true");
  }
  function cerrarCarrito(){
    cartPanel.classList.remove("is-open");
    cartOverlay.classList.remove("is-open");
    cartToggle.setAttribute("aria-expanded", "false");
  }
  cartToggle.addEventListener("click", abrirCarrito);
  cartClose.addEventListener("click", cerrarCarrito);
  cartOverlay.addEventListener("click", cerrarCarrito);

  function pintarCarrito(){
    cartCount.textContent = carrito.length;

    if (carrito.length === 0) {
      cartEmptyEl.style.display = "block";
      cartTotalEl.hidden = true;
      cartItemsEl.innerHTML = "";
      cartItemsEl.appendChild(cartEmptyEl);
      return;
    }

    cartEmptyEl.style.display = "none";
    cartItemsEl.innerHTML = "";
    var total = 0;

    carrito.forEach(function(item){
      total += item.monto_total;
      var row = document.createElement("div");
      row.className = "cart-item";
      row.innerHTML =
        '<div><strong>' + item.nombre_producto + '</strong><span>Cantidad: ' + item.cantidad + '</span></div>' +
        '<div class="cart-item-price">$' + item.monto_total.toFixed(2) + ' MXN</div>';
      cartItemsEl.appendChild(row);
    });

    cartTotalEl.hidden = false;
    cartTotalAmountEl.textContent = "$" + total.toFixed(2) + " MXN";
  }

  function mostrarFeedback(card, mensaje, estado){
    var feedback = card.querySelector("[data-feedback]");
    if (!feedback) return;
    feedback.textContent = mensaje;
    feedback.setAttribute("data-state", estado);
  }

  document.querySelectorAll("[data-add-to-cart]").forEach(function(boton){
    boton.addEventListener("click", function(){
      var card = boton.closest(".card");
      var numeroDeProducto = parseInt(card.getAttribute("data-producto-id"), 10);

      boton.disabled = true;
      mostrarFeedback(card, "Agregando…", "loading");

      fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id_carrito: idCarrito,
          codigo_de_cliente: codigoCliente,
          numero_de_producto: numeroDeProducto,
          cantidad: 1
        })
      })
        .then(function(res){
          return res.json().then(function(data){ return { ok: res.ok, data: data }; });
        })
        .then(function(resultado){
          boton.disabled = false;
          if (!resultado.ok) {
            mostrarFeedback(card, resultado.data.error || "No se pudo agregar el producto.", "error");
            return;
          }
          carrito.push(resultado.data);
          pintarCarrito();
          mostrarFeedback(card, "Agregado al carrito", "success");
          abrirCarrito();
        })
        .catch(function(){
          boton.disabled = false;
          mostrarFeedback(card, "No se pudo conectar con el servidor. ¿Está corriendo carrito.py?", "error");
        });
    });
  });

  pintarCarrito();
})();
</script>

</body>
</html>

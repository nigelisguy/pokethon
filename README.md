<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>POKéTHON</title>

  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg: #0f172a;
      --card: #1e293b;
      --accent: #22c55e;
      --text: #e2e8f0;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Inter', sans-serif;
    }

    body {
      background: linear-gradient(180deg, #020617, #0f172a);
      color: var(--text);
    }

    header {
      text-align: center;
      padding: 30px 10px;
      border-bottom: 1px solid #334155;
      animation: fadeIn 1s ease;
    }

    header h1 {
      font-family: 'Press Start 2P', cursive;
      font-size: 24px;
      color: var(--accent);
      margin-bottom: 10px;
    }

    nav {
      margin-top: 15px;
    }

    nav a {
      text-decoration: none;
      margin: 0 10px;
    }

    nav button {
      background: transparent;
      border: 1px solid var(--accent);
      color: var(--accent);
      padding: 8px 14px;
      border-radius: 10px;
      cursor: pointer;
      transition: 0.3s;
    }

    nav button:hover {
      background: var(--accent);
      color: black;
      transform: scale(1.05);
    }

    .container {
      max-width: 900px;
      margin: auto;
      padding: 30px 20px;
    }

    .card {
      background: var(--card);
      padding: 20px;
      border-radius: 16px;
      margin-bottom: 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
      animation: slideUp 0.6s ease;
    }

    h2 {
      margin-bottom: 10px;
      color: var(--accent);
    }

    ul {
      padding-left: 20px;
    }

    .download-btn {
      display: block;
      text-align: center;
      margin-top: 20px;
    }

    .download-btn button {
      background: var(--accent);
      border: none;
      padding: 12px 20px;
      font-size: 16px;
      border-radius: 12px;
      cursor: pointer;
      transition: 0.3s;
    }

    .download-btn button:hover {
      transform: scale(1.08);
      box-shadow: 0 0 20px var(--accent);
    }

    footer {
      text-align: center;
      padding: 20px;
      opacity: 0.6;
    }

    @keyframes fadeIn {
      from {opacity: 0; transform: translateY(-10px);} 
      to {opacity: 1; transform: translateY(0);} 
    }

    @keyframes slideUp {
      from {opacity: 0; transform: translateY(20px);} 
      to {opacity: 1; transform: translateY(0);} 
    }
  </style>
</head>

<body>

<header>
  <h1>POKéTHON</h1>
  <p>ek</p>

  <nav>
    <a href="#about"><button>About</button></a>
    <a href="#developers"><button>Credits</button></a>
    <a href="#versions"><button>Versions</button></a>
    <a href="#download"><button>Download</button></a>
  </nav>
</header>

<div class="container">

  <div class="card" id="about">
    <h2>About</h2>
    <p><strong>Version:</strong> 0.6</p>
    <p>POKéTHON is an early-build Pokémon-style project with experimental features and multiplayer elements.</p>
  </div>

  <div class="card" id="developers">
    <h2>Developers</h2>
    <ul>
      <li>skdsh aka nigelisguy @2026</li>
    </ul>

    <h3>Testers</h3>
    <ul>
      <li>tszmariop</li>
      <li>gnnadia123</li>
    </ul>
  </div>

  <div class="card" id="versions">
    <h2>Versions</h2>
    <ul>
      <li>Save system</li>
      <li>Items + Pokéballs</li>
      <li>Multiplayer</li>
    </ul>

    <h2>Next Updates</h2>
    <ul>
      <li>NPCs</li>
      <li>Better maps</li>
      <li>Enemy trainers</li>
    </ul>
  </div>

  <div class="card" id="download">
    <h2>Download</h2>

    <div class="download-btn">
      <a href="https://github.com/YOUR-USERNAME/YOUR-REPO/releases/latest">
        <button>⬇ Download Latest Version</button>
      </a>
    </div>
  </div>

</div>

<footer>
  <p>POKéTHON © 2026</p>
</footer>

</body>
</html>

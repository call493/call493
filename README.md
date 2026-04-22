<img src="https://capsule-render.vercel.app/api?type=venom&height=220&color=0:0d1117,100:238636&text=B.%20Mandara&fontSize=60&fontColor=FFFFFF&animation=fadeIn&fontAlignY=40&desc=Software%20Developer&descSize=22&descColor=FFFFFF&descAlignY=65&font=monospace" width="100%"/>

<svg width="100%" height="280" viewBox="0 0 1200 280" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <style>
      .term {
        font-family: "Geist Mono", "JetBrains Mono", "Fira Code", monospace;
        font-size: 22px;
        fill: #ffffff;
      }

      .prompt {
        fill: #238636;
      }

      .glow {
        filter: drop-shadow(0 0 6px #238636);
      }

      .line {
        opacity: 0;
      }

      /* TYPEWRITER BASE */
      .typing {
        overflow: hidden;
        white-space: nowrap;
        width: 0;
      }

      /* CURSOR (only active line uses it) */
      .cursor::after {
        content: "█";
        margin-left: 4px;
        animation: blink 0.8s infinite;
      }

      @keyframes blink {
        50% { opacity: 0; }
      }

      @keyframes show {
        to { opacity: 1; }
      }

      /* TYPING KEYFRAMES */
      @keyframes type1 { from { width: 0 } to { width: 110px } }
      @keyframes type2 { from { width: 0 } to { width: 180px } }
      @keyframes type3 { from { width: 0 } to { width: 200px } }

      /* TIMELINE */
      .l1 { animation: show 0s forwards 0.5s; }
      .l2 { animation: show 0s forwards 2s; }

      .l3 { animation: show 0s forwards 4s; }
      .cmd1 {
        animation: type1 2s steps(12,end) forwards 4s;
      }
      .cursor1 { animation: cursorOn 2s linear 4s forwards; }

      .l4 { animation: show 0s forwards 6.5s; }

      .l5 { animation: show 0s forwards 8.5s; }
      .cmd2 {
        animation: type2 2s steps(20,end) forwards 8.5s;
      }
      .cursor2 { animation: cursorOn 2s linear 8.5s forwards; }

      .l6 { animation: show 0s forwards 11s; }

      .l7 { animation: show 0s forwards 13s; }
      .cmd3 {
        animation: type3 2s steps(22,end) forwards 13s;
      }
      .cursor3 { animation: cursorOn 2s linear 13s forwards; }

      .l8 { animation: show 0s forwards 15.5s; }

      /* Cursor visibility control */
      @keyframes cursorOn {
        0% { opacity: 1; }
        99% { opacity: 1; }
        100% { opacity: 0; }
      }

      /* LOOP */
      svg {
        animation: loop 18s linear infinite;
      }

      @keyframes loop {
        0% { opacity: 1; }
        100% { opacity: 1; }
      }
    </style>
  </defs>

  <foreignObject x="80" y="40" width="1040" height="220">
    <div xmlns="http://www.w3.org/1999/xhtml"
         style="font-family: Geist Mono, JetBrains Mono, monospace;
                color: white;
                line-height: 1.6;">

      <!-- BOOT -->
      <div class="line l1 glow">Initializing system...</div>

      <div class="line l2 glow">
        Loading modules ██████████ 100%
      </div>

      <!-- whoami -->
      <div class="line l3 glow">
        <span style="color:#238636;">mandara@github:~$</span>
        <span class="typing cmd1"> whoami</span>
        <span class="cursor cursor1"></span>
      </div>

      <div class="line l4 glow">
        B. Mandara — Software Developer
      </div>

      <!-- skills -->
      <div class="line l5 glow">
        <span style="color:#238636;">mandara@github:~$</span>
        <span class="typing cmd2"> skills --list</span>
        <span class="cursor cursor2"></span>
      </div>

      <div class="line l6 glow">
        UI/UX • Systems Design
      </div>

    </div>
  </foreignObject>

</svg>

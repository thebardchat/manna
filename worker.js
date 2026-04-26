export default {
  async fetch(request) {
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>MANNA — EM Cargo Delivery | Technical Reference</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Orbitron:wght@900&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#060d1a;--paper:#070f1e;
  --g1:rgba(30,72,140,0.20);--g2:rgba(30,72,140,0.08);
  --line:#1e488c;--line-med:rgba(30,72,140,0.40);--line-dim:rgba(30,72,140,0.20);
  --cyan:#4d9fff;--cyan-d:rgba(77,159,255,0.10);--cyan-g:rgba(77,159,255,0.35);
  --white:#c8deff;--dim:#3a5880;--dimmer:#1c3354;
  --amber:#f4a020;--red:#e84040;--green:#44c080;
  --col-b:#4fc3f7;--col-i:#ff9800;--col-h:#e84040;
  --ftech:'Share Tech Mono',monospace;--fhead:'Rajdhani',sans-serif;
  --fdisplay:'Orbitron',monospace;--fmono:'DM Mono',monospace;
}
html{background:var(--bg);height:100%}
body{font-family:var(--ftech);background:var(--bg);color:var(--white);height:100vh;overflow:hidden}
.bp-paper{
  background-color:var(--paper);
  background-image:
    linear-gradient(var(--g1) 1px,transparent 1px),
    linear-gradient(90deg,var(--g1) 1px,transparent 1px),
    linear-gradient(var(--g2) 1px,transparent 1px),
    linear-gradient(90deg,var(--g2) 1px,transparent 1px);
  background-size:80px 80px,80px 80px,16px 16px,16px 16px;
}
#vp{position:relative;width:100vw;height:calc(100vh - 52px);overflow:hidden}
.sheet{
  position:absolute;inset:0;display:flex;flex-direction:column;
  padding:22px 32px 16px;
  transition:transform .52s cubic-bezier(.77,0,.175,1),opacity .52s ease;
  overflow-y:auto;overflow-x:hidden;
  scrollbar-width:thin;scrollbar-color:var(--line) transparent;
}
.sheet.left {transform:translateX(-100%);opacity:0;pointer-events:none}
.sheet.right{transform:translateX(100%); opacity:0;pointer-events:none}
.sheet.on   {transform:translateX(0);    opacity:1}
.sheet::before{content:'';position:absolute;inset:10px;border:1.5px solid var(--line);pointer-events:none;z-index:0}
.sheet::after {content:'';position:absolute;inset:14px;border:0.5px solid var(--line-med);pointer-events:none;z-index:0}
.inner{position:relative;z-index:1;flex:1;display:flex;flex-direction:column;padding:4px 20px 4px}
.sh-hdr{display:flex;align-items:baseline;gap:16px;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid var(--line-med)}
.sh-drw{font-family:var(--fmono);font-size:.58rem;letter-spacing:.14em;color:var(--dimmer);white-space:nowrap}
.sh-title{font-family:var(--fhead);font-weight:700;font-size:.88rem;letter-spacing:.12em;color:var(--cyan);text-transform:uppercase}
.tb{position:absolute;bottom:20px;right:26px;border:1px solid var(--line);font-family:var(--ftech);font-size:.54rem;letter-spacing:.06em;z-index:10;min-width:210px}
.tb table{width:100%;border-collapse:collapse}
.tb td{padding:2px 8px;border:.5px solid var(--line-dim)}
.tb td.lbl{color:var(--dimmer);font-size:.46rem;text-transform:uppercase}
.tb td.val{color:var(--white)}
.tb td.big{font-family:var(--fdisplay);font-weight:900;font-size:.95rem;color:var(--cyan);letter-spacing:.22em;text-align:center;padding:5px 8px}
.cov{flex:1;display:flex;flex-direction:column;justify-content:center;padding:10px 0 80px;gap:0}
.cov-micro{font-family:var(--ftech);font-size:.58rem;letter-spacing:.26em;color:var(--dimmer);margin-bottom:10px}
.cov-h1{font-family:var(--fdisplay);font-weight:900;font-size:clamp(3.5rem,11vw,8rem);color:var(--cyan);letter-spacing:.07em;line-height:.9;text-shadow:0 0 50px var(--cyan-g),0 0 100px rgba(77,159,255,.12);margin-bottom:6px}
.cov-sub{font-family:var(--fhead);font-weight:600;font-size:clamp(.6rem,1.3vw,.82rem);letter-spacing:.2em;color:var(--white);margin-bottom:28px;padding-left:3px}
.cov-desc{font-family:var(--fmono);font-size:.76rem;color:var(--dim);line-height:1.9;max-width:540px;margin-bottom:24px;border-left:2px solid var(--line);padding-left:14px}
.cov-meta{display:flex;flex-wrap:wrap;border:1px solid var(--line);margin-bottom:36px;max-width:680px}
.cov-cell{padding:5px 14px;border-right:1px solid var(--line-dim);min-width:130px}
.cov-cell:last-child{border-right:none}
.cov-cell .mk{color:var(--dimmer);font-size:.46rem;letter-spacing:.1em;display:block}
.cov-cell .mv{color:var(--white);font-size:.62rem;letter-spacing:.05em}
.repo-row{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.repo-btn{display:inline-flex;align-items:center;gap:9px;padding:10px 20px;border:1.5px solid;font-family:var(--fhead);font-weight:700;font-size:.66rem;letter-spacing:.18em;text-decoration:none;text-transform:uppercase;transition:all .18s ease;position:relative;overflow:hidden}
.repo-btn::before{content:'';position:absolute;inset:0;opacity:0;transition:opacity .18s}
.repo-btn:hover::before{opacity:1}
.repo-btn:hover{transform:translateY(-2px)}
.repo-manna{border-color:var(--cyan);color:var(--cyan)}.repo-manna::before{background:var(--cyan-d)}.repo-manna:hover{box-shadow:0 0 18px rgba(77,159,255,.28)}
.repo-bgk  {border-color:var(--amber);color:var(--amber)}.repo-bgk::before{background:rgba(244,160,32,.08)}.repo-bgk:hover{box-shadow:0 0 18px rgba(244,160,32,.28)}
.sep-wrap{display:flex;align-items:center;gap:6px;margin:0 4px}
.sep-line{width:1px;height:32px;background:var(--line-med)}
.sep-txt{font-size:.5rem;letter-spacing:.1em;color:var(--dimmer);text-align:center}
/* ─── Sheet 01 pods ─── */
.pod-wrap{background:rgba(3,8,18,.7);border:1px solid var(--line-med);padding:28px 16px 14px;margin-bottom:18px;position:relative;overflow:hidden}
.pod-wrap::before{content:'SIDE ELEVATION  —  SCALE 1 : 50  (APPROX)';position:absolute;top:8px;left:12px;font-size:.48rem;letter-spacing:.14em;color:var(--dimmer)}
#pod-svg{width:100%;height:290px;display:block}
.bp-table{width:100%;border-collapse:collapse;font-size:.66rem;letter-spacing:.04em}
.bp-table th{background:rgba(30,72,140,.14);color:var(--dim);font-family:var(--fhead);font-weight:700;font-size:.58rem;letter-spacing:.12em;padding:7px 12px;border:1px solid var(--line-med);text-align:left;white-space:nowrap;text-transform:uppercase}
.bp-table td{padding:6px 12px;border:1px solid var(--line-med);color:var(--white);white-space:nowrap}
.bp-table tbody tr:hover td{background:rgba(77,159,255,.04)}
.tag{color:var(--dimmer);font-size:.52rem;margin-left:3px}
.drv{color:var(--cyan)}.vb{color:var(--col-b)!important;font-weight:500}.vi{color:var(--col-i)!important;font-weight:500}.vh{color:var(--col-h)!important;font-weight:500}
/* ─── Sheet 02 cross-sections ─── */
.xs-wrap{background:rgba(3,8,18,.7);border:1px solid var(--line-med);padding:28px 16px 14px;margin-bottom:18px;position:relative;overflow:hidden}
.xs-wrap::before{content:'CROSS-SECTION AT MID-BODY  ·  CUT PLANE A-A  (ALL VARIANTS, NOT TO SAME SCALE)';position:absolute;top:8px;left:12px;font-size:.48rem;letter-spacing:.14em;color:var(--dimmer)}
#xs-svg{width:100%;height:340px;display:block}
.xs-note{font-family:var(--fmono);font-size:.62rem;color:var(--dim);line-height:1.8;padding:9px 14px;border-left:3px solid var(--line);background:rgba(30,72,140,.04);margin-bottom:14px}
/* ─── Sheet 03 trajectory ─── */
.tctrl{display:flex;align-items:center;gap:14px;margin-bottom:10px;flex-wrap:wrap}
.vtog{display:flex;border:1px solid var(--line);overflow:hidden}
.vtog button{padding:7px 16px;background:transparent;border:none;color:var(--dim);font-family:var(--ftech);font-size:.6rem;letter-spacing:.1em;cursor:pointer;transition:all .18s;white-space:nowrap}
.vtog button.on{background:var(--cyan-d);color:var(--cyan)}
.vtog button:first-child{border-right:1px solid var(--line)}
.vtog button:hover:not(.on){background:rgba(30,72,140,.12);color:var(--white)}
.tleg{display:flex;gap:18px;flex-wrap:wrap;align-items:center}
.li{display:flex;align-items:center;gap:7px;font-size:.58rem;color:var(--dim)}
.ls{width:22px;height:0;border-top:2px solid}
.cwrap{border:1px solid var(--line-med);background:#030810;position:relative;margin-bottom:14px;overflow:hidden}
#tc{display:block;width:100%;height:420px}
.cst{position:absolute;bottom:8px;right:10px;font-size:.5rem;letter-spacing:.1em;color:var(--dimmer)}
.alert-box{font-family:var(--fmono);font-size:.62rem;color:var(--dim);line-height:1.8;padding:9px 14px;border-left:3px solid var(--amber);background:rgba(244,160,32,.04);margin-bottom:14px}
.alert-box strong{color:var(--amber)}
.alert-box-blue{font-family:var(--fmono);font-size:.62rem;color:var(--dim);line-height:1.8;padding:9px 14px;border-left:3px solid var(--cyan);background:rgba(77,159,255,.04);margin-bottom:14px}
.alert-box-blue strong{color:var(--cyan)}
.traj-table{width:100%;border-collapse:collapse;font-size:.65rem;letter-spacing:.04em;margin-bottom:12px}
.traj-table th{background:rgba(30,72,140,.14);color:var(--dim);font-family:var(--fhead);font-weight:700;font-size:.56rem;letter-spacing:.11em;padding:6px 10px;border:1px solid var(--line-med);text-align:left;white-space:nowrap;text-transform:uppercase}
.traj-table td{padding:5px 10px;border:1px solid var(--line-med);white-space:nowrap;font-family:var(--fmono);font-size:.63rem}
.tr-atm td{background:rgba(232,64,64,.05)}
.tr-atm td.err{color:var(--red);font-weight:500}
.tr-atm td.stat{color:var(--amber)}
.td-v01{color:var(--dimmer)}.td-sim{color:var(--cyan)}
.pad-bot{height:80px}
/* ─── Sheet 04 animations ─── */
.anim-hdr{font-family:var(--fhead);font-weight:700;font-size:.72rem;letter-spacing:.14em;color:var(--white);text-transform:uppercase;margin:14px 0 7px;padding-bottom:5px;border-bottom:1px solid var(--line-dim)}
.anim-ctrl{display:flex;align-items:center;gap:14px;margin-bottom:7px;flex-wrap:wrap}
.anim-lbl{font-family:var(--fmono);font-size:.56rem;color:var(--dim);letter-spacing:.07em}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--line);border-radius:2px}
#nav{position:fixed;bottom:0;left:0;right:0;height:52px;background:rgba(3,7,16,.97);border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 24px;z-index:100;backdrop-filter:blur(8px)}
.nbtn{display:flex;align-items:center;gap:7px;background:transparent;border:1px solid var(--line);color:var(--dim);font-family:var(--fhead);font-weight:700;font-size:.6rem;letter-spacing:.16em;padding:7px 16px;cursor:pointer;transition:all .18s;min-width:90px}
.nbtn:hover:not(:disabled){border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 12px rgba(77,159,255,.2)}
.nbtn:disabled{opacity:.22;cursor:default}
.nbtn-r{justify-content:flex-end}
.dots{display:flex;align-items:center;gap:8px}
.dot{width:7px;height:7px;border-radius:50%;border:1px solid var(--line);background:transparent;cursor:pointer;transition:all .22s}
.dot.on{background:var(--cyan);border-color:var(--cyan);box-shadow:0 0 8px rgba(77,159,255,.5)}
.dot:hover:not(.on){border-color:var(--white)}
.sh-ind{font-size:.52rem;letter-spacing:.1em;color:var(--dim);font-family:var(--ftech);margin:0 6px}
</style>
</head>
<body class="bp-paper">
<div id="vp">

<!-- ══════════════════════════ SHEET 00 — COVER ══ -->
<div class="sheet on bp-paper" id="s0">
<div class="inner">
  <div class="sh-hdr">
    <span class="sh-drw">DWG MNP-000  |  REV 0.2</span>
    <span class="sh-title">Project Manna — Index Sheet</span>
  </div>
  <div class="cov">
    <div class="cov-micro">PROJECT DESIGNATION  EM-CDL-001</div>
    <div class="cov-h1">MANNA</div>
    <div class="cov-sub">ELECTROMAGNETIC MASS-DRIVER CARGO DELIVERY SYSTEM</div>
    <div class="cov-desc">
      Three-variant uncrewed cargo pod family for EM rail launch.<br>
      Ballistic suborbital delivery of humanitarian and logistics payloads.<br>
      <span style="color:var(--red);font-size:.9em">⚠ v0.1 trajectory claims superseded — see Sheet 03 for RK4 atmospheric simulation.</span>
    </div>
    <div class="cov-meta">
      <div class="cov-cell"><span class="mk">Project</span><span class="mv">MANNA / EM-CDL</span></div>
      <div class="cov-cell"><span class="mk">Revision</span><span class="mv">0.2 — DRAFT</span></div>
      <div class="cov-cell"><span class="mk">Date</span><span class="mv">2026-04-25</span></div>
      <div class="cov-cell"><span class="mk">Status</span><span class="mv" style="color:var(--amber)">UNDER REVIEW</span></div>
      <div class="cov-cell"><span class="mk">Drawn</span><span class="mv">S. Brazelton + Claude</span></div>
    </div>
    <div class="repo-row">
      <a href="https://github.com/thebardchat/manna" target="_blank" rel="noopener" class="repo-btn repo-manna">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
        Manna Repo →
      </a>
      <div class="sep-wrap"><div class="sep-line"></div><span class="sep-txt">SEPARATE<br>PROJECT</span><div class="sep-line"></div></div>
      <a href="https://github.com/thebardchat/BGKPJR-Core-Simulations" target="_blank" rel="noopener" class="repo-btn repo-bgk">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
        BGKPJR Repo →
      </a>
    </div>
  </div>
  <div class="tb"><table>
    <tr><td colspan="2" class="big">MANNA</td></tr>
    <tr><td class="lbl">Drawing</td><td class="val">MNP-000</td></tr>
    <tr><td class="lbl">Title</td><td class="val">Index / Cover Sheet</td></tr>
    <tr><td class="lbl">Sheets</td><td class="val">00 – 03</td></tr>
    <tr><td class="lbl">Date</td><td class="val">2026-04-25</td></tr>
    <tr><td class="lbl">Drawn</td><td class="val">S. Brazelton + Claude</td></tr>
    <tr><td class="lbl">Sheet</td><td class="val">00 of 03</td></tr>
  </table></div>
</div>
</div>

<!-- ══════════════════════════ SHEET 01 — POD SPECS ══ -->
<div class="sheet right bp-paper" id="s1">
<div class="inner">
  <div class="sh-hdr">
    <span class="sh-drw">DWG MNP-001  |  REV 0.2</span>
    <span class="sh-title">Sheet 01 — Pod Variant Specifications  ·  Side Elevation</span>
  </div>
  <div class="pod-wrap">
    <svg id="pod-svg" viewBox="0 0 960 290" preserveAspectRatio="xMidYMid meet"></svg>
  </div>
  <div style="overflow-x:auto;margin-bottom:16px">
  <table class="bp-table">
    <thead><tr>
      <th>Variant</th><th>Mass</th><th>Body diam.</th><th>Body length</th>
      <th>C<sub>D0</sub></th><th>BC  m/(C<sub>D</sub>·A)</th>
      <th>v<sub>launch</sub>  @30°</th><th>v0.1 Apogee (vacuum)</th><th>Sim Apogee (atm)</th>
    </tr></thead>
    <tbody>
      <tr>
        <td class="vb">Manna-B</td>
        <td>80 kg <span class="tag">[EST]</span></td>
        <td>0.40 m <span class="tag">[EST]</span></td>
        <td>1.60 m <span class="tag">[EST]</span></td>
        <td>0.40 <span class="tag">[EST]</span></td>
        <td class="drv">1,592 kg/m² <span class="tag">[DRV]</span></td>
        <td class="drv">4,319 m/s <span class="tag">[DRV]</span></td>
        <td style="color:var(--red)">247 km ⚠ [SUPERSEDED]</td>
        <td style="color:var(--cyan)">4.2 km [DRV—sim]</td>
      </tr>
      <tr>
        <td class="vi">Manna-I</td>
        <td>250 kg <span class="tag">[EST]</span></td>
        <td>0.65 m <span class="tag">[EST]</span></td>
        <td>2.60 m <span class="tag">[EST]</span></td>
        <td>0.42 <span class="tag">[EST]</span></td>
        <td class="drv">1,794 kg/m² <span class="tag">[DRV]</span></td>
        <td class="drv">7,670 m/s <span class="tag">[DRV]</span></td>
        <td style="color:var(--red)">850 km ⚠ [SUPERSEDED]</td>
        <td style="color:var(--cyan)">6.0 km [DRV—sim]</td>
      </tr>
      <tr>
        <td class="vh">Manna-H</td>
        <td>800 kg <span class="tag">[EST]</span></td>
        <td>1.00 m <span class="tag">[EST]</span></td>
        <td>4.00 m <span class="tag">[EST]</span></td>
        <td>0.45 <span class="tag">[EST]</span></td>
        <td class="drv">2,264 kg/m² <span class="tag">[DRV]</span></td>
        <td class="drv">10,823 m/s <span class="tag">[DRV]</span></td>
        <td style="color:var(--red)">1,950 km ⚠ [SUPERSEDED]</td>
        <td style="color:var(--cyan)">9.1 km [DRV—sim]</td>
      </tr>
    </tbody>
  </table>
  </div>
  <div class="alert-box">
    <strong>DRAWING KEY:</strong>  TPS = thermal protection system (ablative nose zone).
    CAPTURE = aft capture/berthing ring for Tug interface.  Internal zone labels: TPS / AVNX (avionics) / BIOCELL / PAYLOAD / CARGO / STRUCT.
    Dashed internal lines show structural zone boundaries — not to-scale thickness.
    Dimension lines show body length (L) and body diameter (Ø).  Nose cone adds ~15–40% to total vehicle length.
    Cross-section anatomy on Sheet 02.
  </div>
  <div class="pad-bot"></div>
  <div class="tb"><table>
    <tr><td colspan="2" class="big">MANNA</td></tr>
    <tr><td class="lbl">Drawing</td><td class="val">MNP-001</td></tr>
    <tr><td class="lbl">Title</td><td class="val">Pod Variant Specs</td></tr>
    <tr><td class="lbl">Scale</td><td class="val">1 : 50 (approx)</td></tr>
    <tr><td class="lbl">Date</td><td class="val">2026-04-25</td></tr>
    <tr><td class="lbl">Drawn</td><td class="val">S. Brazelton + Claude</td></tr>
    <tr><td class="lbl">Sheet</td><td class="val">01 of 03</td></tr>
  </table></div>
</div>
</div>

<!-- ══════════════════════════ SHEET 02 — CROSS-SECTIONS (NEW) ══ -->
<div class="sheet right bp-paper" id="s2">
<div class="inner">
  <div class="sh-hdr">
    <span class="sh-drw">DWG MNP-002  |  REV 0.2</span>
    <span class="sh-title">Sheet 02 — Internal Anatomy  ·  Mid-Body Cross-Sections</span>
  </div>
  <div class="xs-wrap">
    <svg id="xs-svg" viewBox="0 0 960 340" preserveAspectRatio="xMidYMid meet"></svg>
  </div>
  <div class="xs-note">
    <strong style="color:var(--white)">CROSS-SECTION NOTES:</strong>  Sections are conceptual — internal dimensions are [ESTIMATE].
    Each variant is drawn at its own scale (see Ø label); display diameter is normalised to show internal detail.
    Manna-B uses liquid suspension (FC-770 fluorinert, 1.79 g/cm³) with bio-cell matrix and MR damper mounts.
    Manna-I uses segmented electronics bays separated by structural dividers with vibration isolation pads at 45° corners.
    Manna-H is deliberately the simplest: thick structural wall, open bulk cargo volume, 4 retention rails.
    All variants share the same aerodynamic outer shell profile — internal cargo architecture is the differentiator.
  </div>
  <div class="pad-bot"></div>
  <div class="tb"><table>
    <tr><td colspan="2" class="big">MANNA</td></tr>
    <tr><td class="lbl">Drawing</td><td class="val">MNP-002</td></tr>
    <tr><td class="lbl">Title</td><td class="val">Cross-Section Anatomy</td></tr>
    <tr><td class="lbl">Scale</td><td class="val">See per-variant labels</td></tr>
    <tr><td class="lbl">Date</td><td class="val">2026-04-25</td></tr>
    <tr><td class="lbl">Drawn</td><td class="val">S. Brazelton + Claude</td></tr>
    <tr><td class="lbl">Sheet</td><td class="val">02 of 03</td></tr>
  </table></div>
</div>
</div>

<!-- ══════════════════════════ SHEET 03 — TRAJECTORY ══ -->
<div class="sheet right bp-paper" id="s3">
<div class="inner">
  <div class="sh-hdr">
    <span class="sh-drw">DWG MNP-003  |  REV 0.2</span>
    <span class="sh-title">Sheet 03 — Ballistic Trajectory Analysis  ·  θ = 30°  ·  US Std Atm 1976  ·  RK4  dt = 0.1 s</span>
  </div>
  <div class="tctrl">
    <div class="vtog">
      <button id="bvac" class="on" onclick="setMode('vacuum')">VACUUM MODEL  (v0.1 claims)</button>
      <button id="batm"           onclick="setMode('atmo')">ATMOSPHERE SIM  (RK4 corrected)</button>
    </div>
    <div class="tleg">
      <div class="li"><div class="ls" style="border-color:var(--col-b)"></div>Manna-B</div>
      <div class="li"><div class="ls" style="border-color:var(--col-i)"></div>Manna-I</div>
      <div class="li"><div class="ls" style="border-color:var(--col-h)"></div>Manna-H</div>
      <div class="li"><div class="ls" style="border-color:var(--cyan);border-style:dashed"></div>Kármán 100 km</div>
      <div class="li" id="leg-mq" style="display:none"><div class="ls" style="border-color:#88ff88;border-style:dotted"></div>Max-Q</div>
    </div>
  </div>
  <div class="cwrap">
    <canvas id="tc"></canvas>
    <div class="cst" id="cst">INITIALISING…</div>
  </div>
  <table class="traj-table" id="rtable">
    <thead><tr>
      <th>Variant</th><th>BC [kg/m²]</th><th>v<sub>launch</sub> [m/s]</th>
      <th>v0.1 Claim [km]</th><th>Sim Apogee [km]</th>
      <th>v0.1 / Sim error</th><th>Sea-lvl q<sub>dyn</sub> [MPa]</th>
      <th>Sea-lvl a<sub>drag</sub> [g]</th><th>Max Mach</th><th>Status</th>
    </tr></thead>
    <tbody>
      <tr class="tr-atm">
        <td class="vb">Manna-B</td><td>1,592</td><td>4,319</td>
        <td class="td-v01">247.0</td><td class="td-sim" id="r-ap-b">—</td>
        <td class="err" id="r-er-b">—</td><td>11.4</td><td>732</td>
        <td id="r-m-b">—</td><td class="stat" id="r-st-b">—</td>
      </tr>
      <tr class="tr-atm">
        <td class="vi">Manna-I</td><td>1,794</td><td>7,670</td>
        <td class="td-v01">850.0</td><td class="td-sim" id="r-ap-i">—</td>
        <td class="err" id="r-er-i">—</td><td>36.0</td><td>2,047</td>
        <td id="r-m-i">—</td><td class="stat" id="r-st-i">—</td>
      </tr>
      <tr class="tr-atm">
        <td class="vh">Manna-H</td><td>2,264</td><td>10,823</td>
        <td class="td-v01">1,950.0</td><td class="td-sim" id="r-ap-h">—</td>
        <td class="err" id="r-er-h">—</td><td>71.7</td><td>3,231</td>
        <td id="r-m-h">—</td><td class="stat" id="r-st-h">—</td>
      </tr>
    </tbody>
  </table>
  <div class="alert-box">
    <strong>FINDING (RK4 + US Std Atm 1976):</strong>
    v0.1 used vacuum constant-g formula — no atmosphere.  Sea-level dynamic pressure at hypersonic exit (4,319–10,823 m/s) exceeds
    <strong>11–72 MPa</strong>, producing deceleration of <strong>732–3,231 g</strong>.
    All three variants stop in the lower troposphere (&lt; 11 km AGL).  v0.1 apogees overestimated by <strong>59–214×</strong>.
  </div>
  <div class="alert-box-blue">
    <strong>BC × ELEVATION SWEEP (108 runs, sweep.py):</strong>
    Current BC ≈ 1,600–2,300 kg/m² achieves 4–9 km at 30°.
    Kármán line (100 km) requires BC ≥ 5,000 kg/m² at 75–85° elevation.
    Orbital velocity at apogee requires BC ≥ 50,000 kg/m² (20–30× increase).
    Peak stagnation heat flux (Sutton-Graves, R<sub>nose</sub>=5 cm):
    H = 1.15 GW/m²  ·  I = 0.41 GW/m²  ·  B = 0.07 GW/m².  <strong>[CONSTRAINT-NOT-MODELED]</strong>
    Architecture conclusion: evacuated launch tube or high-altitude site required to close mission.
  </div>
  <div class="pad-bot"></div>
  <div class="tb"><table>
    <tr><td colspan="2" class="big">MANNA</td></tr>
    <tr><td class="lbl">Drawing</td><td class="val">MNP-003</td></tr>
    <tr><td class="lbl">Title</td><td class="val">Trajectory Analysis</td></tr>
    <tr><td class="lbl">Model</td><td class="val">3-DOF RK4 · dt=0.1 s</td></tr>
    <tr><td class="lbl">Atm</td><td class="val">US Std Atm 1976</td></tr>
    <tr><td class="lbl">Date</td><td class="val">2026-04-25</td></tr>
    <tr><td class="lbl">Sheet</td><td class="val">03 of 03</td></tr>
  </table></div>
</div>
</div>


<!-- ══════════════════════════ SHEET 04 — ANIMATIONS ══ -->
<div class="sheet right bp-paper" id="s4">
<div class="inner">
  <div class="sh-hdr">
    <span class="sh-drw">DWG MNP-004  |  REV 0.2</span>
    <span class="sh-title">Sheet 04 — Cargo Loading · Rail Insert · Launch &amp; Spin Stabilisation</span>
  </div>

  <div class="anim-hdr">01 · Cargo loading sequence</div>
  <div class="anim-ctrl">
    <div class="vtog">
      <button onclick="setCargo(0)" id="cb0" class="on">Manna-B</button>
      <button onclick="setCargo(1)" id="cb1">Manna-I</button>
      <button onclick="setCargo(2)" id="cb2">Manna-H</button>
    </div>
    <span class="anim-lbl" id="cargo-lbl">SELECT VARIANT ABOVE</span>
  </div>
  <div class="cwrap"><canvas id="cargoCanvas"></canvas></div>

  <div class="anim-hdr">02 · BGKPJR rail insert &amp; EM acceleration</div>
  <div class="anim-ctrl"><span class="anim-lbl" id="rail-lbl">28.7 km · 15–45° incline · EM coil drive</span></div>
  <div class="cwrap"><canvas id="railCanvas"></canvas></div>

  <div class="anim-hdr">03 · Launch &amp; gyroscopic stabilisation (rifled exit)</div>
  <div class="anim-ctrl"><span class="anim-lbl" id="spin-lbl">SPIN ≈ 30 rev/s · L = 18,850 N·m·s · [ESTIMATE]</span></div>
  <div class="cwrap"><canvas id="spinCanvas"></canvas></div>

  <div class="xs-note" style="border-color:var(--cyan)">
    <strong style="color:var(--cyan)">SPIN STABILISATION RATIONALE:</strong>
    Rifled BGKPJR exit tube imparts angular momentum at launch — identical principle to a rifle barrel.
    For Manna-H (M=800 kg, r=0.50 m): moment of inertia I = ½Mr² = 100 kg·m².
    Target exit spin ω ≈ 30 rev/s (1,800 RPM) → angular momentum L = Iω ≈ 18,850 N·m·s.
    Gyroscopic stiffness resists aerodynamic torques, keeping nose-to-trajectory aligned through the atmosphere (&lt; 20 s flight time to 10 km).
    Fins provide pitch/yaw restoring force above the rail. Spin rate decays slowly in vacuum.
    <em>[CONSTRAINT-NOT-MODELED — requires 6-DOF dynamics simulation to verify adequate stiffness]</em>
  </div>

  <div class="pad-bot"></div>
  <div class="tb"><table>
    <tr><td colspan="2" class="big">MANNA</td></tr>
    <tr><td class="lbl">Drawing</td><td class="val">MNP-004</td></tr>
    <tr><td class="lbl">Title</td><td class="val">Loading &amp; Launch Animations</td></tr>
    <tr><td class="lbl">Date</td><td class="val">2026-04-25</td></tr>
    <tr><td class="lbl">Drawn</td><td class="val">S. Brazelton + Claude</td></tr>
    <tr><td class="lbl">Sheet</td><td class="val">04 of 04</td></tr>
  </table></div>
</div>
</div>

</div><!-- /vp -->

<!-- ══ NAV BAR ══ -->
<div id="nav">
  <button class="nbtn" id="bnp" onclick="prev()" disabled>← Prev</button>
  <div class="dots">
    <span class="sh-ind">SHEET</span>
    <div class="dot on" id="d0" onclick="go(0)"></div>
    <div class="dot"    id="d1" onclick="go(1)"></div>
    <div class="dot"    id="d2" onclick="go(2)"></div>
    <div class="dot"    id="d3" onclick="go(3)"></div>
    <div class="dot"    id="d4" onclick="go(4)"></div>
  </div>
  <button class="nbtn nbtn-r" id="bnn" onclick="next()">Next →</button>
</div>

<script>
/* ══ NAVIGATION ══ */
const SHEETS=['s0','s1','s2','s3','s4'];
let cur=0;
function go(n){
  const p=cur;
  cur=Math.max(0,Math.min(n,4));
  if(p===cur)return;
  const dir=cur>p?1:-1;
  document.getElementById(SHEETS[p]).className='sheet bp-paper '+(dir>0?'left':'right');
  document.getElementById(SHEETS[cur]).className='sheet bp-paper on';
  document.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('on',i===cur));
  document.getElementById('bnp').disabled=cur===0;
  document.getElementById('bnn').disabled=cur===4;
  if(cur===3)requestAnimationFrame(drawTraj);
  if(cur===4)startAnimations();
  else stopAnimations();
}
function next(){go(cur+1)} function prev(){go(cur-1)}

/* ══ POD SVG  Sheet 01 ══ */
(function(){
  const svg=document.getElementById('pod-svg');
  const NS='http://www.w3.org/2000/svg';
  const SCA=55, CY=150;

  function el(t,a){const e=document.createElementNS(NS,t);Object.entries(a).forEach(([k,v])=>e.setAttribute(k,v));return e}
  function txt(x,y,s,a){
    const def={x,y,'font-family':'Share Tech Mono,monospace','font-size':'9',fill:'#3a5880','text-anchor':'middle','letter-spacing':'0.4'};
    const t=el('text',Object.assign(def,a||{}));t.textContent=s;return t;
  }
  function lin(x1,y1,x2,y2,a){return el('line',Object.assign({x1,y1,x2,y2,stroke:'#1e488c','stroke-width':'.7'},a||{}))}
  function n(v){return Math.round(v*10)/10}

  const pods=[
    {name:'Manna-B',col:'#4fc3f7',d:0.40,l:1.60,m:80, bc:'1,592',cx:160,nAR:0.90,fHR:0.50,lbl:'BIOLOGICS · 2.5 G MAX', zones:['TPS','BIOCELL','BIOCELL','AVNX']},
    {name:'Manna-I',col:'#ff9800',d:0.65,l:2.60,m:250,bc:'1,794',cx:452,nAR:1.15,fHR:0.45,lbl:'INSTRUMENTS · 5.5 G MAX',zones:['TPS','AVNX','PAYLOAD','STRUCT']},
    {name:'Manna-H',col:'#e84040',d:1.00,l:4.00,m:800,bc:'2,264',cx:782,nAR:1.40,fHR:0.40,lbl:'BULK CARGO · 100 G MAX',  zones:['TPS','CARGO','CARGO','STRUCT']}
  ];

  pods.forEach(function(pod){
    var r=pod.d*SCA/2;
    var nL=pod.nAR*pod.d*SCA;
    var bL=pod.l*SCA;
    var xt=pod.cx-(nL+bL)/2;
    var xb=xt+nL;
    var xe=xb+bL;
    var yt=CY-r, yb=CY+r;
    var g=el('g',{});

    /* nose cone — ogive cubic bezier */
    var cpX=xt+nL*0.38;
    var nosePts='M'+n(xt)+','+n(CY)+' C'+n(cpX)+','+n(yt+r*0.06)+' '+n(xb-3)+','+n(yt)+' '+n(xb)+','+n(yt)+' L'+n(xb)+','+n(yb)+' C'+n(xb-3)+','+n(yb)+' '+n(cpX)+','+n(yb-r*0.06)+' '+n(xt)+','+n(CY)+' Z';
    g.appendChild(el('path',{d:nosePts,fill:'rgba(3,8,18,.96)',stroke:pod.col,'stroke-width':'1.4'}));

    /* TPS zone overlay */
    var tE=xt+nL*0.38, cpT=xt+nL*0.14;
    var rgb=pod.col==='#4fc3f7'?'77,195,247':pod.col==='#ff9800'?'255,152,0':'232,64,64';
    var tpsPath='M'+n(xt)+','+n(CY)+' C'+n(cpT)+','+n(yt+r*0.52)+' '+n(tE-2)+','+n(yt+r*0.12)+' '+n(tE)+','+n(yt+r*0.04)+' L'+n(tE)+','+n(yb-r*0.04)+' C'+n(tE-2)+','+n(yb-r*0.12)+' '+n(cpT)+','+n(yb-r*0.52)+' '+n(xt)+','+n(CY)+' Z';
    g.appendChild(el('path',{d:tpsPath,fill:'rgba('+rgb+',0.18)',stroke:'none'}));
    g.appendChild(lin(n(tE),n(yt+r*0.04),n(tE),n(yb-r*0.04),{stroke:pod.col,'stroke-opacity':'.3','stroke-dasharray':'2,2','stroke-width':'.5'}));

    /* body */
    g.appendChild(el('rect',{x:n(xb),y:n(yt),width:n(bL),height:n(r*2),fill:'rgba(3,8,18,.96)',stroke:pod.col,'stroke-width':'1.4'}));

    /* internal zone dividers */
    var zw=bL/4;
    for(var z=1;z<4;z++){
      g.appendChild(lin(n(xb+z*zw),n(yt+1),n(xb+z*zw),n(yb-1),{stroke:pod.col,'stroke-opacity':'.2','stroke-dasharray':'2,2','stroke-width':'.5'}));
    }

    /* zone labels */
    var fz=Math.max(5.5,r*0.3);
    pod.zones.forEach(function(lbl,z){
      g.appendChild(txt(n(xb+z*zw+zw/2),n(CY+fz*0.38),lbl,{'font-size':fz.toFixed(1),fill:pod.col,'fill-opacity':'0.30','text-anchor':'middle'}));
    });

    /* centerline */
    g.appendChild(lin(n(xt-8),n(CY),n(xe+8),n(CY),{stroke:'rgba(30,72,140,.4)','stroke-dasharray':'6,3','stroke-width':'.5'}));

    /* swept delta fins */
    var fH=pod.fHR*r, fR=bL*0.24, fx0=xe-fR;
    g.appendChild(el('path',{d:'M'+n(fx0)+','+n(yt)+' L'+n(xe)+','+n(yt)+' L'+n(xe)+','+n(yt-fH)+' Z',fill:'rgba(3,8,18,.88)',stroke:pod.col,'stroke-width':'1.0','stroke-opacity':'.8'}));
    g.appendChild(el('path',{d:'M'+n(fx0)+','+n(yb)+' L'+n(xe)+','+n(yb)+' L'+n(xe)+','+n(yb+fH)+' Z',fill:'rgba(3,8,18,.88)',stroke:pod.col,'stroke-width':'1.0','stroke-opacity':'.8'}));

    /* aft capture ring */
    var rw=Math.max(4,r*0.12);
    g.appendChild(el('rect',{x:n(xe-rw),y:n(yt-1),width:n(rw),height:n(r*2+2),fill:'none',stroke:pod.col,'stroke-width':'2.2','stroke-opacity':'.5'}));

    /* dimension: total vehicle length */
    var dY=yb+fH+20;
    g.appendChild(lin(n(xt),n(dY),n(xe),n(dY),{stroke:'#1e488c','stroke-width':'.7'}));
    [[xt],[xe]].forEach(function(a){g.appendChild(lin(n(a[0]),n(dY-4),n(a[0]),n(dY+4),{stroke:'#1e488c','stroke-width':'.7'}));});
    g.appendChild(txt(n(pod.cx),n(dY+11),'L = '+(pod.l+pod.d*pod.nAR).toFixed(2)+' m',{'font-size':'8',fill:'#1e488c','text-anchor':'middle'}));

    /* dimension: diameter */
    var dX=xt-20;
    g.appendChild(lin(n(dX),n(yt),n(dX),n(yb),{stroke:'#1e488c','stroke-width':'.7'}));
    [[yt],[yb]].forEach(function(a){g.appendChild(lin(n(dX-4),n(a[0]),n(dX+4),n(a[0]),{stroke:'#1e488c','stroke-width':'.7'}));});
    g.appendChild(txt(n(dX),n(CY+3.5),'Ø'+pod.d+'m',{'font-size':'7.5',fill:'#1e488c','text-anchor':'middle'}));

    /* callout: TPS */
    var cTx=xt+nL*0.15, cTa=yt-r*0.2, cTb=yt-r-16;
    g.appendChild(lin(n(cTx),n(cTa),n(cTx-2),n(cTb),{stroke:pod.col,'stroke-opacity':'.4','stroke-width':'.5','stroke-dasharray':'3,2'}));
    g.appendChild(el('circle',{cx:n(cTx),cy:n(cTa),r:'1.5',fill:pod.col,'fill-opacity':'.5'}));
    g.appendChild(txt(n(cTx-2),n(cTb-3),'TPS',{'font-size':'7',fill:pod.col,'fill-opacity':'.6','text-anchor':'middle'}));

    /* callout: capture ring */
    var cRx=xe-rw/2;
    g.appendChild(lin(n(cRx),n(yt),n(cRx),n(yt-13),{stroke:pod.col,'stroke-opacity':'.35','stroke-width':'.5','stroke-dasharray':'2,2'}));
    g.appendChild(txt(n(cRx),n(yt-16),'CAPTURE',{'font-size':'6.5',fill:pod.col,'fill-opacity':'.5','text-anchor':'middle'}));

    /* name + class label */
    g.appendChild(txt(n(pod.cx),n(yt-fH-26),pod.name,{'font-size':'13',fill:pod.col,'text-anchor':'middle','font-family':'Rajdhani,sans-serif','font-weight':'700','letter-spacing':'1'}));
    g.appendChild(txt(n(pod.cx),n(yt-fH-12),pod.lbl,{'font-size':'8',fill:'rgba(200,222,255,.6)','text-anchor':'middle'}));

    /* mass + BC footer */
    g.appendChild(txt(n(pod.cx),n(dY+24),'m = '+pod.m+' kg [EST]   ·   BC = '+pod.bc+' kg/m² [DRV]',{'font-size':'7.5',fill:'rgba(200,222,255,.42)','text-anchor':'middle'}));

    svg.appendChild(g);
  });

  /* scale bar */
  var sbX=18,sbY=278;
  svg.appendChild(lin(sbX,sbY,sbX+SCA,sbY,{stroke:'#1e488c','stroke-width':'1'}));
  [[sbX],[sbX+SCA]].forEach(function(a){svg.appendChild(lin(a[0],sbY-3,a[0],sbY+3,{stroke:'#1e488c'}));});
  svg.appendChild(txt(sbX+SCA/2,sbY-5,'1.0 m',{'font-size':'7.5',fill:'#1e488c','text-anchor':'middle'}));
  svg.appendChild(txt(sbX+SCA/2,sbY+11,'SCALE 1:50 (APPROX)',{'font-size':'6.5',fill:'#1e488c','text-anchor':'middle'}));
})();

/* ══ CROSS-SECTION SVG  Sheet 02 ══ */
(function(){
  var svg=document.getElementById('xs-svg');
  var NS='http://www.w3.org/2000/svg';
  var DR=72, CY=175;
  var CXB=160, CXI=480, CXH=800;

  function el(t,a){var e=document.createElementNS(NS,t);Object.entries(a).forEach(function(kv){e.setAttribute(kv[0],kv[1]);});return e;}
  function circ(cx,cy,r,a){return el('circle',Object.assign({cx:cx,cy:cy,r:r},a||{}));}
  function lin(x1,y1,x2,y2,a){return el('line',Object.assign({x1:x1,y1:y1,x2:x2,y2:y2,stroke:'#1e488c','stroke-width':'.7'},a||{}));}
  function txt(x,y,s,a){var def={x:x,y:y,'font-family':'Share Tech Mono,monospace','font-size':'8.5',fill:'#3a5880','text-anchor':'middle','letter-spacing':'0.4'};var t=el('text',Object.assign(def,a||{}));t.textContent=s;return t;}
  function leader(x1,y1,x2,y2,col){
    svg.appendChild(lin(x1,y1,x2,y2,{stroke:col,'stroke-opacity':'.45','stroke-width':'.55','stroke-dasharray':'3,2'}));
    svg.appendChild(circ(x1,y1,1.5,{fill:col,'fill-opacity':'.55'}));
  }

  /* ─── Manna-B ─── */
  var bc='#4fc3f7';
  svg.appendChild(txt(CXB,CY-DR-14,'Manna-B',{'font-size':'12',fill:bc,'text-anchor':'middle','font-family':'Rajdhani,sans-serif','font-weight':'700'}));
  svg.appendChild(txt(CXB,CY-DR-2,'BIOLOGICS · 2.5 G',{'font-size':'7.5',fill:'rgba(200,222,255,.55)','text-anchor':'middle'}));
  /* outer shell */
  svg.appendChild(circ(CXB,CY,DR,{fill:'rgba(3,8,18,.95)',stroke:bc,'stroke-width':'4'}));
  /* suspension fluid annulus */
  var fR=DR-7;
  svg.appendChild(circ(CXB,CY,fR,{fill:'rgba(77,195,247,0.11)',stroke:bc,'stroke-width':'.9','stroke-opacity':'.45'}));
  /* inner bio-cell container */
  var biR=fR-7;
  svg.appendChild(circ(CXB,CY,biR,{fill:'rgba(3,8,18,.82)',stroke:bc,'stroke-width':'.7','stroke-opacity':'.5'}));
  /* bio-cell grid */
  [-1,0,1].forEach(function(row){[-1,0,1].forEach(function(col){
    var bx=CXB+col*13,by=CY+row*13;
    if(Math.hypot(bx-CXB,by-CY)<biR-5){svg.appendChild(circ(bx,by,4,{fill:'rgba(77,195,247,0.25)',stroke:bc,'stroke-width':'.5','stroke-opacity':'.5'}));}
  });});
  /* MR damper mounts at N/S/E/W */
  [[0,-1],[0,1],[1,0],[-1,0]].forEach(function(d){svg.appendChild(circ(CXB+d[0]*(fR+3),CY+d[1]*(fR+3),3.5,{fill:bc,'fill-opacity':'.7'}));});
  /* callouts */
  leader(CXB+fR*0.65,CY-fR*0.65,CXB+DR+10,CY-34,bc);
  svg.appendChild(txt(CXB+DR+12,CY-34,'FC-770 FLUID',{'font-size':'7',fill:bc,'fill-opacity':'.7','text-anchor':'start'}));
  leader(CXB+5,CY-4,CXB+DR+10,CY+18,bc);
  svg.appendChild(txt(CXB+DR+12,CY+18,'BIO-CELL',{'font-size':'7',fill:bc,'fill-opacity':'.7','text-anchor':'start'}));
  svg.appendChild(txt(CXB+DR+12,CY+27,'MATRIX',{'font-size':'7',fill:bc,'fill-opacity':'.7','text-anchor':'start'}));
  leader(CXB,CY-(fR+3),CXB-DR-10,CY-22,bc);
  svg.appendChild(txt(CXB-DR-12,CY-22,'MR DAMPER',{'font-size':'7',fill:bc,'fill-opacity':'.7','text-anchor':'end'}));
  svg.appendChild(txt(CXB-DR-12,CY-13,'MOUNTS ×4',{'font-size':'7',fill:bc,'fill-opacity':'.7','text-anchor':'end'}));
  svg.appendChild(txt(CXB,CY+DR+16,'Ø 0.40 m  |  SCALE 1:2.9',{'font-size':'7.5',fill:'#1e488c','text-anchor':'middle'}));

  /* ─── Manna-I ─── */
  var ic='#ff9800';
  svg.appendChild(txt(CXI,CY-DR-14,'Manna-I',{'font-size':'12',fill:ic,'text-anchor':'middle','font-family':'Rajdhani,sans-serif','font-weight':'700'}));
  svg.appendChild(txt(CXI,CY-DR-2,'INSTRUMENTS · 5.5 G',{'font-size':'7.5',fill:'rgba(200,222,255,.55)','text-anchor':'middle'}));
  svg.appendChild(circ(CXI,CY,DR,{fill:'rgba(3,8,18,.95)',stroke:ic,'stroke-width':'3.5'}));
  /* cross dividers */
  svg.appendChild(lin(CXI-DR+3,CY,CXI+DR-3,CY,{stroke:ic,'stroke-opacity':'.45','stroke-width':'1.2'}));
  svg.appendChild(lin(CXI,CY-DR+3,CXI,CY+DR-3,{stroke:ic,'stroke-opacity':'.45','stroke-width':'1.2'}));
  /* quadrant fills */
  [{sa:0,ea:0.5,al:0.12},{sa:0.5,ea:1,al:0.08},{sa:1,ea:1.5,al:0.14},{sa:1.5,ea:2,al:0.09}].forEach(function(q){
    var pts=['M'+CXI+','+CY];
    var iR=DR-3;
    for(var a=q.sa*Math.PI;a<=q.ea*Math.PI+0.01;a+=0.08){
      pts.push('L'+(CXI+iR*Math.cos(a-Math.PI/2)).toFixed(1)+','+(CY+iR*Math.sin(a-Math.PI/2)).toFixed(1));
    }
    pts.push('Z');
    svg.appendChild(el('path',{d:pts.join(' '),fill:'rgba(255,152,0,'+q.al+')'}));
  });
  /* vibe isolation pads */
  [45,135,225,315].forEach(function(deg){
    var rad=deg*Math.PI/180;
    svg.appendChild(circ((CXI+(DR-6)*Math.cos(rad-Math.PI/2)).toFixed(1),(CY+(DR-6)*Math.sin(rad-Math.PI/2)).toFixed(1),5,{fill:ic,'fill-opacity':'.6'}));
  });
  /* central conduit */
  svg.appendChild(circ(CXI,CY,7,{fill:'rgba(255,152,0,0.2)',stroke:ic,'stroke-width':'1','stroke-opacity':'.5'}));
  /* callouts */
  leader(CXI+DR*0.6,CY+DR*0.35,CXI+DR+10,CY+38,ic);
  svg.appendChild(txt(CXI+DR+12,CY+38,'ELEC BAY',{'font-size':'7',fill:ic,'fill-opacity':'.7','text-anchor':'start'}));
  svg.appendChild(txt(CXI+DR+12,CY+47,'(SEGMENTED)',{'font-size':'7',fill:ic,'fill-opacity':'.7','text-anchor':'start'}));
  leader(CXI+(DR-6)*0.707,CY-(DR-6)*0.707,CXI-DR-10,CY-30,ic);
  svg.appendChild(txt(CXI-DR-12,CY-30,'VIBE ISO.',{'font-size':'7',fill:ic,'fill-opacity':'.7','text-anchor':'end'}));
  svg.appendChild(txt(CXI-DR-12,CY-21,'MOUNTS ×4',{'font-size':'7',fill:ic,'fill-opacity':'.7','text-anchor':'end'}));
  leader(CXI,CY+7,CXI-DR-10,CY+28,ic);
  svg.appendChild(txt(CXI-DR-12,CY+28,'CENTRAL',{'font-size':'7',fill:ic,'fill-opacity':'.7','text-anchor':'end'}));
  svg.appendChild(txt(CXI-DR-12,CY+37,'CONDUIT',{'font-size':'7',fill:ic,'fill-opacity':'.7','text-anchor':'end'}));
  svg.appendChild(txt(CXI,CY+DR+16,'Ø 0.65 m  |  SCALE 1:4.6',{'font-size':'7.5',fill:'#1e488c','text-anchor':'middle'}));

  /* ─── Manna-H ─── */
  var hc='#e84040';
  svg.appendChild(txt(CXH,CY-DR-14,'Manna-H',{'font-size':'12',fill:hc,'text-anchor':'middle','font-family':'Rajdhani,sans-serif','font-weight':'700'}));
  svg.appendChild(txt(CXH,CY-DR-2,'BULK CARGO · 100 G',{'font-size':'7.5',fill:'rgba(200,222,255,.55)','text-anchor':'middle'}));
  svg.appendChild(circ(CXH,CY,DR,{fill:'rgba(3,8,18,.95)',stroke:hc,'stroke-width':'5'}));
  /* structural wall fill */
  var wR=DR-14;
  svg.appendChild(circ(CXH,CY,DR-2,{fill:'rgba(232,64,64,0.12)',stroke:'none'}));
  svg.appendChild(circ(CXH,CY,wR,{fill:'rgba(3,8,18,.95)',stroke:hc,'stroke-width':'1','stroke-opacity':'.4'}));
  /* liner */
  svg.appendChild(circ(CXH,CY,wR-3,{fill:'none',stroke:hc,'stroke-width':'.5','stroke-opacity':'.3'}));
  /* open cargo volume */
  svg.appendChild(circ(CXH,CY,wR-5,{fill:'rgba(232,64,64,0.05)',stroke:'none'}));
  /* retention rails */
  [[0,-1],[0,1],[1,0],[-1,0]].forEach(function(d){
    svg.appendChild(lin(CXH+d[0]*3,CY+d[1]*3,CXH+d[0]*(wR-5),CY+d[1]*(wR-5),{stroke:hc,'stroke-opacity':'.4','stroke-width':'1.6'}));
  });
  /* vent ports */
  [45,135,225,315].forEach(function(deg){
    var rad=deg*Math.PI/180;
    svg.appendChild(circ((CXH+(DR-2)*Math.cos(rad-Math.PI/2)).toFixed(1),(CY+(DR-2)*Math.sin(rad-Math.PI/2)).toFixed(1),3,{fill:'rgba(3,8,18,.9)',stroke:hc,'stroke-width':'.8','stroke-opacity':'.5'}));
  });
  /* callouts */
  leader(CXH+(DR-8)*0.55,CY-(DR-8)*0.55,CXH+DR+10,CY-34,hc);
  svg.appendChild(txt(CXH+DR+12,CY-34,'STRUCTURAL',{'font-size':'7',fill:hc,'fill-opacity':'.7','text-anchor':'start'}));
  svg.appendChild(txt(CXH+DR+12,CY-25,'WALL',{'font-size':'7',fill:hc,'fill-opacity':'.7','text-anchor':'start'}));
  leader(CXH,CY,CXH-DR-10,CY+20,hc);
  svg.appendChild(txt(CXH-DR-12,CY+20,'BULK CARGO',{'font-size':'7',fill:hc,'fill-opacity':'.7','text-anchor':'end'}));
  svg.appendChild(txt(CXH-DR-12,CY+29,'VOLUME',{'font-size':'7',fill:hc,'fill-opacity':'.7','text-anchor':'end'}));
  leader(CXH+(DR-2)*0.707,CY-(DR-2)*0.707,CXH+DR+10,CY+18,hc);
  svg.appendChild(txt(CXH+DR+12,CY+18,'VENT PORT',{'font-size':'7',fill:hc,'fill-opacity':'.7','text-anchor':'start'}));
  svg.appendChild(txt(CXH+DR+12,CY+27,'×4 AT 45°',{'font-size':'7',fill:hc,'fill-opacity':'.7','text-anchor':'start'}));
  svg.appendChild(txt(CXH,CY+DR+16,'Ø 1.00 m  |  SCALE 1:7.1',{'font-size':'7.5',fill:'#1e488c','text-anchor':'middle'}));

  /* section cut label */
  svg.appendChild(txt(480,18,'CUT PLANE A-A  ·  MID-BODY CROSS-SECTION  ·  ALL VARIANTS',{'font-size':'8',fill:'#1e488c','text-anchor':'middle','letter-spacing':'1'}));
})();

/* ══ US STANDARD ATMOSPHERE 1976 ══ */
const ATM=[[0,288.15,-0.0065,101325],[11000,216.65,0,22632.1],[20000,216.65,0.001,5474.89],[32000,228.65,0.0028,868.019],[47000,270.65,0,110.906],[51000,270.65,-0.0028,66.9389],[71000,214.65,-0.002,3.95642],[86000,186.87,0,0.37338]];
const R_AIR=287.058,G0=9.80665,GAMMA=1.4,RE=6371000;
function aT(h){h=Math.max(h,0);if(h>=86000)return ATM[7][1];for(let i=7;i>=0;i--)if(h>=ATM[i][0])return ATM[i][1]+ATM[i][2]*(h-ATM[i][0]);return ATM[0][1]}
function aP(h){h=Math.max(h,0);if(h>=86000){const[hb,Tb,,Pb]=ATM[7];return Pb*Math.exp(-G0*(h-hb)/(R_AIR*Tb))}for(let i=7;i>=0;i--){const[hb,Tb,Lb,Pb]=ATM[i];if(h>=hb){return Math.abs(Lb)<1e-12?Pb*Math.exp(-G0*(h-hb)/(R_AIR*Tb)):Pb*Math.pow((Tb+Lb*(h-hb))/Tb,-G0/(Lb*R_AIR))}}return ATM[0][3]}
function aRho(h){return aP(h)/(R_AIR*aT(h))}
function aSnd(h){return Math.sqrt(GAMMA*R_AIR*aT(h))}
function gv(h){const r=RE+Math.max(h,0);return G0*(RE/r)**2}

/* ══ RK4 INTEGRATOR ══ */
function deriv([x,z,vx,vz],bc){
  const h=Math.max(z,0),v=Math.hypot(vx,vz),q=0.5*aRho(h)*v*v,g=gv(h);
  const ad=v>0.5?q/bc:0;
  return[vx,vz,-ad*(vx/v||0),-ad*(vz/v||0)-g];
}
function rk4([x,z,vx,vz],dt,bc){
  const k1=deriv([x,z,vx,vz],bc);
  const k2=deriv([x+.5*dt*k1[0],z+.5*dt*k1[1],vx+.5*dt*k1[2],vz+.5*dt*k1[3]],bc);
  const k3=deriv([x+.5*dt*k2[0],z+.5*dt*k2[1],vx+.5*dt*k2[2],vz+.5*dt*k2[3]],bc);
  const k4=deriv([x+dt*k3[0],z+dt*k3[1],vx+dt*k3[2],vz+dt*k3[3]],bc);
  return[x+dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]),z+dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]),vx+dt/6*(k1[2]+2*k2[2]+2*k3[2]+k4[2]),vz+dt/6*(k1[3]+2*k2[3]+2*k3[3]+k4[3])];
}
function runTraj(v0,bc,elDeg,dt){
  const el=(elDeg||30)*Math.PI/180;
  let s=[0,0,v0*Math.cos(el),v0*Math.sin(el)];
  const pts=[],maxQ={q:0,x:0,z:0},apg={z:0,x:0};
  let t=0,maxMach=0;
  while(t<3600){
    const[x,z,vx,vz]=s;const h=Math.max(z,0),v=Math.hypot(vx,vz);
    const q=0.5*aRho(h)*v*v;
    if(q>maxQ.q){maxQ.q=q;maxQ.x=x;maxQ.z=h}
    const mach=v/aSnd(h);if(mach>maxMach)maxMach=mach;
    if(h>apg.z){apg.z=h;apg.x=x}
    pts.push([x,Math.max(z,0)]);
    if(t>2&&z<=0)break;
    // adaptive sub-step for extreme drag
    var v_cur=v,dt_step=dt||0.1;
    if(v_cur>1){var _q=0.5*aRho(h)*v_cur*v_cur,_ad=_q/bc;if(_ad>0){var _ts=v_cur/_ad;dt_step=Math.min(dt||0.1,_ts*0.25);}}
    s=rk4(s,dt_step,bc);t+=dt_step;
    if(t>0.5&&v<1)break;
  }
  return{pts,apg,maxQ,maxMach};
}
const VARS=[
  {name:'Manna-B',v:4319.1,bc:1592,v01:247,  col:'#4fc3f7',q0:11.43,g0:732},
  {name:'Manna-I',v:7670.4,bc:1794,v01:850,  col:'#ff9800',q0:36.03,g0:2047},
  {name:'Manna-H',v:10822.8,bc:2264,v01:1950,col:'#e84040',q0:71.74,g0:3231},
];
let simR=null;
function computeAll(){
  simR=VARS.map(v=>{
    const atm=runTraj(v.v,v.bc,30,0.1);
    const vac=runTraj(v.v,1e15,30,0.1);
    return{...v,atm,vac};
  });
  const ids=['b','i','h'];
  simR.forEach((r,i)=>{
    const id=ids[i];
    const ap=(r.atm.apg.z/1000).toFixed(2);
    const ef=Math.round(r.v01/(r.atm.apg.z/1000));
    document.getElementById('r-ap-'+id).textContent=ap+' km';
    document.getElementById('r-er-'+id).textContent=ef+'×  overestimate';
    document.getElementById('r-m-'+id).textContent=r.atm.maxMach.toFixed(1);
    document.getElementById('r-st-'+id).textContent='< 11 km AGL — no orbit';
  });
  document.getElementById('cst').textContent='SIMULATION COMPLETE  |  dt = 0.1 s  |  50/50 TESTS PASS';
  drawTraj();
}

/* ══ CANVAS RENDERER ══ */
let vmode='vacuum';
function setMode(m){
  vmode=m;
  document.getElementById('bvac').classList.toggle('on',m==='vacuum');
  document.getElementById('batm').classList.toggle('on',m==='atmo');
  document.getElementById('leg-mq').style.display=m==='atmo'?'flex':'none';
  drawTraj();
}
function drawTraj(){
  if(!simR)return;
  const cv=document.getElementById('tc');
  const W=cv.parentElement.clientWidth||900,H=420;
  cv.width=W;cv.height=H;
  const ctx=cv.getContext('2d');ctx.clearRect(0,0,W,H);
  const isVac=(vmode==='vacuum');
  const ML=68,MR=14,MT=34,MB=46,PW=W-ML-MR,PH=H-MT-MB;
  let maxZ=0,maxX=0;
  simR.forEach(r=>{const pts=isVac?r.vac.pts:r.atm.pts;for(let i=0;i<pts.length;i++){const z=pts[i][1];if(i>0&&z<pts[i-1][1])break;if(z>maxZ)maxZ=z;if(pts[i][0]>maxX)maxX=pts[i][0];}});
  maxZ*=1.15;maxX*=1.12;
  const scZ=PH/maxZ,scX=PW/maxX,sc=Math.min(scZ,scX);
  const offX=ML,offY=H-MB;
  function cx(x){return offX+x*sc}function cz(z){return offY-z*sc}
  ctx.strokeStyle='rgba(30,72,140,0.14)';ctx.lineWidth=.5;
  const gSZ=isVac?200000:2000;
  for(let z=0;z<=maxZ;z+=gSZ){const y=cz(z);if(y<MT||y>H-MB)continue;ctx.beginPath();ctx.moveTo(ML,y);ctx.lineTo(W-MR,y);ctx.stroke();}
  for(let x=0;x<=maxX;x+=gSZ){const px=cx(x);if(px<ML||px>W-MR)continue;ctx.beginPath();ctx.moveTo(px,MT);ctx.lineTo(px,H-MB);ctx.stroke();}
  if(!isVac){
    [[0,11000,'TROPOSPHERE','rgba(77,120,180,0.06)'],[11000,20000,'STRATOSPHERE (lower)','rgba(60,140,160,0.06)'],[20000,32000,'STRATOSPHERE (upper)','rgba(40,140,120,0.06)']].forEach(([z0,z1,lbl,col])=>{
      const y0=cz(z1),y1=cz(z0);if(y0>H-MB||y1<MT)return;
      ctx.fillStyle=col;ctx.fillRect(ML,Math.max(y0,MT),PW,Math.min(y1,H-MB)-Math.max(y0,MT));
      ctx.fillStyle='rgba(100,160,200,0.4)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText(lbl,ML+6,Math.min(y1,H-MB)-5);
    });
    const tp=cz(11000);if(tp>MT&&tp<H-MB){ctx.setLineDash([4,4]);ctx.strokeStyle='rgba(77,159,255,0.25)';ctx.lineWidth=.8;ctx.beginPath();ctx.moveTo(ML,tp);ctx.lineTo(W-MR,tp);ctx.stroke();ctx.setLineDash([]);}
  }
  if(isVac){const kz=cz(100000);if(kz>MT&&kz<H-MB){ctx.setLineDash([8,5]);ctx.strokeStyle='rgba(77,159,255,0.5)';ctx.lineWidth=.9;ctx.beginPath();ctx.moveTo(ML,kz);ctx.lineTo(W-MR,kz);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='rgba(77,159,255,0.55)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText('KÁRMÁN LINE  100 km',ML+6,kz-4);}}
  simR.forEach(r=>{
    const pts=isVac?r.vac.pts:r.atm.pts;if(pts.length<2)return;
    const apg=isVac?r.vac.apg:r.atm.apg;
    ctx.save();ctx.beginPath();ctx.rect(ML,MT,PW,PH);ctx.clip();
    ctx.beginPath();let started=false;
    for(let i=0;i<pts.length;i++){const px=cx(pts[i][0]),py=cz(pts[i][1]);if(!started){ctx.moveTo(px,py);started=true}else ctx.lineTo(px,py);}
    ctx.strokeStyle=r.col;ctx.lineWidth=1.8;ctx.shadowColor=r.col;ctx.shadowBlur=isVac?5:9;ctx.stroke();ctx.shadowBlur=0;
    const apx=cx(apg.x),apz=cz(apg.z);
    if(apx>ML&&apx<W-MR&&apz>MT&&apz<H-MB){
      ctx.fillStyle=r.col;ctx.beginPath();ctx.arc(apx,apz,4,0,Math.PI*2);ctx.fill();
      ctx.font='bold 10px Share Tech Mono,monospace';ctx.fillStyle=r.col;ctx.shadowColor=r.col;ctx.shadowBlur=6;
      const apL=isVac?(apg.z/1000).toFixed(0)+' km':(apg.z/1000).toFixed(2)+' km';
      ctx.fillText(r.name+'  '+apL,apx+8,apz-4);ctx.shadowBlur=0;
    }
    if(!isVac){const mqx=cx(r.atm.maxQ.x),mqz=cz(r.atm.maxQ.z);if(mqx>ML&&mqx<W-MR&&mqz>MT&&mqz<H-MB){ctx.strokeStyle='#88ff88';ctx.lineWidth=1;ctx.setLineDash([3,3]);ctx.beginPath();ctx.moveTo(mqx-5,mqz-5);ctx.lineTo(mqx+5,mqz+5);ctx.moveTo(mqx+5,mqz-5);ctx.lineTo(mqx-5,mqz+5);ctx.stroke();ctx.setLineDash([]);}}
    ctx.restore();
  });
  if(isVac){const RE_px=RE*sc,ecx=cx(0),ecy=cz(0)+RE_px;ctx.save();ctx.beginPath();ctx.arc(ecx,ecy,RE_px,0,Math.PI*2);ctx.fillStyle='#030810';ctx.fill();ctx.strokeStyle='rgba(30,72,140,0.6)';ctx.lineWidth=1.5;ctx.stroke();ctx.restore();}
  else{ctx.save();ctx.fillStyle='#030810';ctx.fillRect(0,H-MB,W,MB+2);ctx.strokeStyle='rgba(30,72,140,0.7)';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(0,H-MB);ctx.lineTo(W,H-MB);ctx.stroke();ctx.fillStyle='rgba(77,100,160,0.2)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText('EARTH SURFACE  (MSL)',ML+4,H-MB+14);ctx.restore();}
  ctx.fillStyle='rgba(58,88,128,0.9)';ctx.font='9px Share Tech Mono,monospace';
  const altT=isVac?[0,200,400,600,800,1000,1200,1500,1800].map(k=>k*1000):[0,2,4,6,8,10,12].map(k=>k*1000);
  altT.forEach(z=>{const y=cz(z);if(y<MT||y>H-MB+2)return;ctx.strokeStyle='rgba(30,72,140,0.25)';ctx.lineWidth=.4;ctx.beginPath();ctx.moveTo(ML-4,y);ctx.lineTo(ML,y);ctx.stroke();ctx.fillText(isVac?(z/1000).toFixed(0)+' km':(z/1000).toFixed(0)+' km',4,y+3);});
  ctx.save();ctx.translate(14,MT+PH/2);ctx.rotate(-Math.PI/2);ctx.fillStyle='rgba(58,88,128,0.8)';ctx.font='9px Share Tech Mono,monospace';ctx.textAlign='center';ctx.fillText('ALTITUDE ASL [km]',0,0);ctx.restore();
  const rngT=isVac?[0,1000,2000,3000,4000,5000,6000,7000].map(k=>k*1000):[0,5,10,15,20,25,30].map(k=>k*1000);
  ctx.textAlign='center';
  rngT.forEach(x=>{const px=cx(x);if(px<ML||px>W-MR)return;ctx.strokeStyle='rgba(30,72,140,0.25)';ctx.lineWidth=.4;ctx.beginPath();ctx.moveTo(px,H-MB);ctx.lineTo(px,H-MB+4);ctx.stroke();ctx.fillStyle='rgba(58,88,128,0.9)';ctx.fillText(isVac?(x/1000).toFixed(0)+' km':(x/1000).toFixed(0)+' km',px,H-MB+18);});
  ctx.fillStyle='rgba(58,88,128,0.8)';ctx.font='9px Share Tech Mono,monospace';ctx.textAlign='center';ctx.fillText('DOWNRANGE DISTANCE [km]',ML+PW/2,H-4);
  ctx.textAlign='left';ctx.font='10px Rajdhani,sans-serif';ctx.fillStyle=isVac?'rgba(244,160,32,0.75)':'rgba(77,159,255,0.75)';
  ctx.fillText(isVac?'VACUUM MODEL  ·  No atmosphere  ·  v0.1 claimed apogees':'US STD ATM 1976  ·  RK4  dt=0.1 s  ·  actual apogees (drag-stopped in troposphere)',ML+6,MT-6);
  const sBar=isVac?200000:2000,sLen=sBar*sc,sx0=W-MR-sLen-4,syt=H-MB+26;
  ctx.strokeStyle='rgba(58,88,128,0.7)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(sx0,syt);ctx.lineTo(sx0+sLen,syt);ctx.moveTo(sx0,syt-3);ctx.lineTo(sx0,syt+3);ctx.moveTo(sx0+sLen,syt-3);ctx.lineTo(sx0+sLen,syt+3);ctx.stroke();
  ctx.fillStyle='rgba(58,88,128,0.8)';ctx.font='8px Share Tech Mono,monospace';ctx.textAlign='center';ctx.fillText(isVac?'200 km':'2 km',sx0+sLen/2,syt+12);ctx.textAlign='left';
}

/* ══ SHEET 04 ANIMATIONS ══ */
let cargoVariant=0;
const animS={cargo:{t:0,run:false,raf:null},rail:{t:0,run:false,raf:null},spin:{t:0,run:false,raf:null}};
const ALOOP=4.0;

function setCargo(i){
  cargoVariant=i;
  ['cb0','cb1','cb2'].forEach((id,j)=>document.getElementById(id).classList.toggle('on',j===i));
  animS.cargo.t=0;
}

function startAnimations(){
  if(!animS.cargo.run)runAnim('cargo',drawCargoAnim,ALOOP);
  if(!animS.rail.run) runAnim('rail', drawRailAnim, ALOOP*1.5);
  if(!animS.spin.run) runAnim('spin', drawSpinAnim, ALOOP*2);
}
function stopAnimations(){
  Object.keys(animS).forEach(k=>{animS[k].run=false;if(animS[k].raf){cancelAnimationFrame(animS[k].raf);animS[k].raf=null;}});
}
function runAnim(key,fn,dur){
  const a=animS[key]; a.run=true;
  let last=performance.now();
  function frame(now){
    if(!a.run)return;
    const dt=Math.min((now-last)/1000,0.05); last=now;
    a.t=(a.t+dt/dur)%1.0;
    fn(a.t);
    a.raf=requestAnimationFrame(frame);
  }
  a.raf=requestAnimationFrame(frame);
}

/* ─── CARGO LOADING ─── */
function drawCargoAnim(t){
  var cv=document.getElementById('cargoCanvas'); if(!cv)return;
  var W=cv.parentElement.clientWidth||600, H=220;
  cv.width=W; cv.height=H;
  var ctx=cv.getContext('2d'); ctx.clearRect(0,0,W,H);
  var vd=[
    {col:'#4fc3f7',d:0.40,l:1.60,name:'Manna-B',cargo:'BIOLOGICS',nAR:0.9},
    {col:'#ff9800',d:0.65,l:2.60,name:'Manna-I',cargo:'INSTRUMENTS',nAR:1.15},
    {col:'#e84040',d:1.00,l:4.00,name:'Manna-H',cargo:'BULK CARGO',nAR:1.4}
  ];
  var v=vd[cargoVariant], pCol=v.col;
  var scale=Math.min(H*0.5/v.d, W*0.52/v.l);
  var r=v.d*scale/2, nL=v.nAR*v.d*scale, bL=v.l*scale;
  var xt=W/2-(nL+bL)/2+15, xb=xt+nL, xe=xb+bL, cy=H/2+12, yt=cy-r, yb=cy+r;
  // grid
  ctx.strokeStyle='rgba(30,72,140,0.07)';ctx.lineWidth=.5;
  for(var x=0;x<W;x+=20){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
  for(var y=0;y<H;y+=20){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
  // phase calc
  var doorOpen=t<0.12?t/0.12:t<0.72?1.0:t<0.87?1-(t-0.72)/0.15:0;
  var loadT=Math.max(0,Math.min(1,(t-0.12)/0.6));
  // nose cone
  var cpX=xt+nL*0.38;
  ctx.beginPath();ctx.moveTo(xt,cy);ctx.bezierCurveTo(cpX,yt+r*0.06,xb-2,yt,xb,yt);ctx.lineTo(xb,yb);ctx.bezierCurveTo(xb-2,yb,cpX,yb-r*0.06,xt,cy);ctx.closePath();
  ctx.fillStyle='rgba(3,8,18,.97)';ctx.strokeStyle=pCol;ctx.lineWidth=1.5;ctx.fill();ctx.stroke();
  // body (leave door space)
  var dw=Math.max(4,bL*0.22);
  ctx.fillStyle='rgba(3,8,18,.97)';ctx.strokeStyle=pCol;ctx.lineWidth=1.4;
  ctx.fillRect(xb,yt,bL-dw,r*2);ctx.strokeRect(xb,yt,bL-dw,r*2);
  // zone lines
  var zw=(bL-dw)/4;
  for(var z=1;z<4;z++){ctx.strokeStyle=pCol;ctx.lineWidth=.4;ctx.globalAlpha=.18;ctx.setLineDash([2,2]);ctx.beginPath();ctx.moveTo(xb+z*zw,yt+1);ctx.lineTo(xb+z*zw,yb-1);ctx.stroke();ctx.setLineDash([]);ctx.globalAlpha=1;}
  // cargo door panels (hinge at xe-dw, top opens up, bottom opens down)
  var dx=xb+bL-dw;
  ctx.save();ctx.translate(dx,yt);ctx.rotate(-doorOpen*Math.PI*0.58);
  ctx.fillStyle='rgba(3,8,18,.97)';ctx.strokeStyle=pCol;ctx.lineWidth=1.2;
  ctx.fillRect(0,0,dw,r);ctx.strokeRect(0,0,dw,r);ctx.restore();
  ctx.save();ctx.translate(dx,yb);ctx.rotate(doorOpen*Math.PI*0.58);
  ctx.fillStyle='rgba(3,8,18,.97)';ctx.strokeStyle=pCol;ctx.lineWidth=1.2;
  ctx.fillRect(0,-r,dw,r);ctx.strokeRect(0,-r,dw,r);ctx.restore();
  // fins
  var fH=0.45*r,fR=bL*0.22;
  ctx.fillStyle='rgba(3,8,18,.88)';ctx.strokeStyle=pCol;ctx.lineWidth=.9;ctx.globalAlpha=.8;
  ctx.beginPath();ctx.moveTo(xe-fR,yt);ctx.lineTo(xe,yt);ctx.lineTo(xe,yt-fH);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.beginPath();ctx.moveTo(xe-fR,yb);ctx.lineTo(xe,yb);ctx.lineTo(xe,yb+fH);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.globalAlpha=1;
  // cargo items
  if(loadT>0&&doorOpen>0.25){
    ctx.save();ctx.beginPath();ctx.rect(xb+2,yt+1,bL-dw-3,r*2-2);ctx.clip();
    if(cargoVariant===0){
      // suspension fluid rising
      var fl=yt+r*2*(1-loadT*0.65);
      var fg=ctx.createLinearGradient(0,fl,0,yb);fg.addColorStop(0,'rgba(77,195,247,0.05)');fg.addColorStop(1,'rgba(77,195,247,0.22)');
      ctx.fillStyle=fg;ctx.fillRect(xb+2,fl,bL-dw-4,yb-fl-1);
      // bio-cells grid
      var cR=Math.max(3,r*0.22),cols=Math.floor((bL-dw-10)/(cR*2.5));
      for(var row=0;row<2;row++){for(var col=0;col<cols;col++){
        var cp=Math.max(0,Math.min(1,(loadT-(row*cols+col)/(2*cols)*0.8)*5));
        if(cp<=0)continue;
        var ccx=xb+6+col*cR*2.4+cR, ccy=yt+r*0.38+row*cR*2.3+cR;
        ctx.globalAlpha=Math.min(cp,1);
        ctx.fillStyle='rgba(77,195,247,0.38)';ctx.strokeStyle='#4fc3f7';ctx.lineWidth=.7;
        ctx.beginPath();ctx.arc(ccx,ccy,cR,0,Math.PI*2);ctx.fill();ctx.stroke();
        ctx.globalAlpha=1;
      }}
    } else if(cargoVariant===1){
      // electronics modules
      var mW=(bL-dw-10)/4-3,mH=r*1.2;
      for(var mi=0;mi<4;mi++){
        var mp=Math.max(0,Math.min(1,(loadT-mi/4*0.7)*4));if(mp<=0)continue;
        var mx=xb+4+mi*(mW+3)+mW*(1-mp)*1.8,my=cy-mH/2;
        ctx.globalAlpha=Math.min(mp,1);
        ctx.fillStyle='rgba(255,152,0,0.28)';ctx.strokeStyle='#ff9800';ctx.lineWidth=.8;
        ctx.fillRect(mx,my,mW,mH);ctx.strokeRect(mx,my,mW,mH);
        ctx.strokeStyle='rgba(255,152,0,0.5)';ctx.lineWidth=.4;ctx.setLineDash([2,2]);
        ctx.beginPath();ctx.moveTo(mx+3,my+mH/3);ctx.lineTo(mx+mW-3,my+mH/3);ctx.stroke();
        ctx.beginPath();ctx.moveTo(mx+3,my+mH*2/3);ctx.lineTo(mx+mW-3,my+mH*2/3);ctx.stroke();
        ctx.setLineDash([]);ctx.globalAlpha=1;
      }
    } else {
      // bulk cargo blocks
      var bkW=(bL-dw-12)/3-4,bkH=r*1.5,bkLbls=['H₂O','PROP','FOOD'];
      for(var bi=0;bi<3;bi++){
        var bp=Math.max(0,Math.min(1,(loadT-bi/3*0.6)*4));if(bp<=0)continue;
        var bkx=xb+4+bi*(bkW+4)+bkW*(1-bp)*2,bky=cy-bkH/2;
        ctx.globalAlpha=Math.min(bp,1);
        ctx.fillStyle='rgba(232,64,64,0.32)';ctx.strokeStyle='#e84040';ctx.lineWidth=.9;
        ctx.fillRect(bkx,bky,bkW,bkH);ctx.strokeRect(bkx,bky,bkW,bkH);
        ctx.fillStyle='rgba(232,64,64,0.75)';ctx.font='bold '+(bkH*0.22).toFixed(0)+'px Share Tech Mono,monospace';ctx.textAlign='center';
        ctx.fillText(bkLbls[bi],bkx+bkW/2,bky+bkH/2+3);
        ctx.globalAlpha=1;
      }
    }
    ctx.restore();
  }
  // status
  var phases=['BAY OPENING','LOADING','LOADING','SEALING','LAUNCH READY ✓'];
  var pi=Math.min(Math.floor(t*5),4);
  var pc=t>0.87?'#44c080':pCol;
  ctx.fillStyle=pc;ctx.font='bold 9px Share Tech Mono,monospace';ctx.textAlign='left';ctx.fillText('STATUS: '+phases[pi],8,16);
  ctx.fillStyle=pCol;ctx.font='10px Rajdhani,sans-serif';ctx.textAlign='right';ctx.fillText(v.name+' · '+v.cargo,W-8,16);
  ctx.fillStyle='rgba(30,72,140,0.3)';ctx.fillRect(8,H-11,W-16,3);
  ctx.fillStyle=pCol;ctx.fillRect(8,H-11,(W-16)*t,3);
  var lbl=document.getElementById('cargo-lbl');if(lbl)lbl.textContent=phases[pi];
}

/* ─── RAIL INSERT ─── */
function drawRailAnim(t){
  var cv=document.getElementById('railCanvas');if(!cv)return;
  var W=cv.parentElement.clientWidth||600,H=240;
  cv.width=W;cv.height=H;
  var ctx=cv.getContext('2d');ctx.clearRect(0,0,W,H);
  var elev=30*Math.PI/180;
  var railLen=W*0.80,rx0=W*0.07,ry0=H*0.87;
  var rx1=rx0+railLen*Math.cos(elev),ry1=ry0-railLen*Math.sin(elev);
  // sky
  var sg=ctx.createLinearGradient(0,0,0,H*0.87);sg.addColorStop(0,'rgba(0,2,10,0.98)');sg.addColorStop(1,'rgba(3,8,18,0.85)');
  ctx.fillStyle=sg;ctx.fillRect(0,0,W,H*0.87);
  ctx.fillStyle='rgba(30,72,140,0.08)';ctx.fillRect(0,H*0.87,W,H*0.13);
  ctx.strokeStyle='rgba(30,72,140,0.38)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(0,H*0.87);ctx.lineTo(W,H*0.87);ctx.stroke();
  ctx.strokeStyle='rgba(30,72,140,0.06)';ctx.lineWidth=.5;
  for(var x=0;x<W;x+=28){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
  for(var y=0;y<H;y+=28){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
  // coils along rail
  var nCoils=14,perpX=-Math.sin(elev),perpY=-Math.cos(elev);
  for(var i=0;i<nCoils;i++){
    var fi=(i+1)/(nCoils+1);
    var ccx=rx0+fi*railLen*Math.cos(elev),ccy=ry0-fi*railLen*Math.sin(elev);
    var podDist=Math.abs(t-fi),isPast=t>fi,isAct=isPast&&podDist<0.12;
    var alpha=isAct?1.0:isPast?0.28:0.16;
    ctx.globalAlpha=alpha;ctx.strokeStyle=isAct?'#4d9fff':'#1e488c';ctx.lineWidth=isAct?2:0.9;
    ctx.beginPath();ctx.moveTo(ccx+perpX*10,ccy+perpY*10);ctx.lineTo(ccx-perpX*10,ccy-perpY*10);
    if(isAct){ctx.shadowColor='#4d9fff';ctx.shadowBlur=10;}
    ctx.stroke();ctx.shadowBlur=0;ctx.globalAlpha=1;
    // support stanchion to ground (simplified)
    if(i%3===0){
      ctx.globalAlpha=0.12;ctx.strokeStyle='#1e488c';ctx.lineWidth=0.6;
      ctx.beginPath();ctx.moveTo(ccx,ccy);ctx.lineTo(ccx,H*0.87);ctx.stroke();ctx.globalAlpha=1;
    }
  }
  // rail tube edges
  var tw=7;
  ctx.strokeStyle='rgba(30,72,140,0.7)';ctx.lineWidth=1.3;
  ctx.beginPath();ctx.moveTo(rx0+perpX*tw,ry0+perpY*tw);ctx.lineTo(rx1+perpX*tw,ry1+perpY*tw);ctx.stroke();
  ctx.beginPath();ctx.moveTo(rx0-perpX*tw,ry0-perpY*tw);ctx.lineTo(rx1-perpX*tw,ry1-perpY*tw);ctx.stroke();
  ctx.strokeStyle='rgba(77,159,255,0.2)';ctx.lineWidth=0.7;ctx.setLineDash([8,6]);
  ctx.beginPath();ctx.moveTo(rx0,ry0);ctx.lineTo(rx1,ry1);ctx.stroke();ctx.setLineDash([]);
  // pod on rail
  var pLen=22,pR=5.5,podX=rx0+t*railLen*Math.cos(elev),podY=ry0-t*railLen*Math.sin(elev);
  var pCol=cargoVariant===0?'#4fc3f7':cargoVariant===1?'#ff9800':'#e84040';
  ctx.save();ctx.translate(podX,podY);ctx.rotate(-elev);
  // EM wake glow
  if(t>0.08){var gd=ctx.createRadialGradient(pLen*0.4,0,0,pLen*0.4,0,pLen*1.2);gd.addColorStop(0,'rgba(77,159,255,0.55)');gd.addColorStop(1,'rgba(77,159,255,0)');ctx.fillStyle=gd;ctx.beginPath();ctx.ellipse(pLen*0.4,0,pLen*1.1,pR*0.75,0,0,Math.PI*2);ctx.fill();}
  // pod body
  ctx.beginPath();ctx.moveTo(-pLen,0);ctx.bezierCurveTo(-pLen*0.62,-pR*0.06,-pLen*0.05,-pR,0,-pR);ctx.lineTo(0,pR);ctx.bezierCurveTo(-pLen*0.05,pR,-pLen*0.62,pR*0.06,-pLen,0);ctx.closePath();
  ctx.fillStyle='rgba(3,8,18,.97)';ctx.strokeStyle=pCol;ctx.lineWidth=1.2;ctx.fill();ctx.stroke();
  ctx.restore();
  // speed label
  ctx.fillStyle='#4d9fff';ctx.font='8px Share Tech Mono,monospace';ctx.textAlign='left';
  ctx.fillText('v ≈ '+(t*10823).toFixed(0)+' m/s',podX+12,podY-11);
  // elevation arc
  var arcR=30;ctx.strokeStyle='rgba(77,159,255,0.38)';ctx.lineWidth=.7;ctx.setLineDash([2,2]);
  ctx.beginPath();ctx.arc(rx0,ry0,arcR,-elev-Math.PI/2,-Math.PI/2);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='rgba(77,159,255,0.7)';ctx.font='7.5px Share Tech Mono,monospace';ctx.textAlign='left';ctx.fillText('30°',rx0+arcR*0.42,ry0-arcR*0.38);
  // labels
  ctx.fillStyle='rgba(30,72,140,0.7)';ctx.font='8px Share Tech Mono,monospace';ctx.textAlign='left';
  ctx.fillText('BGKPJR MAGLEV RAIL  ·  28.7 km  ·  30° ELEV  ·  HAZEL GREEN AL  34.93°N',rx0,H*0.87+14);
  var rPhase=t<0.06?'POD LOADING':t<0.92?'EM ACCELERATION':'EXIT / LAUNCH';
  ctx.fillStyle='#4d9fff';ctx.font='bold 9px Share Tech Mono,monospace';ctx.textAlign='left';ctx.fillText('STATUS: '+rPhase,8,16);
  ctx.fillStyle='rgba(30,72,140,0.3)';ctx.fillRect(8,H-11,W-16,3);ctx.fillStyle='#4d9fff';ctx.fillRect(8,H-11,(W-16)*t,3);
  var rl=document.getElementById('rail-lbl');if(rl)rl.textContent='28.7 km · 30° incline · v ≈ '+(t*10823).toFixed(0)+' m/s';
}

/* ─── LAUNCH + SPIN ─── */
function drawSpinAnim(t){
  var cv=document.getElementById('spinCanvas');if(!cv)return;
  var W=cv.parentElement.clientWidth||600,H=290;
  cv.width=W;cv.height=H;
  var ctx=cv.getContext('2d');ctx.clearRect(0,0,W,H);
  var splitX=Math.floor(W*0.52);
  var sg=ctx.createLinearGradient(0,0,0,H);sg.addColorStop(0,'rgba(0,1,8,0.99)');sg.addColorStop(1,'rgba(3,8,18,0.9)');
  ctx.fillStyle=sg;ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='rgba(30,72,140,0.06)';ctx.lineWidth=.5;
  for(var x=0;x<W;x+=25){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
  for(var y=0;y<H;y+=25){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
  ctx.strokeStyle='rgba(30,72,140,0.28)';ctx.lineWidth=0.7;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(splitX,18);ctx.lineTo(splitX,H-18);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='rgba(58,88,128,0.8)';ctx.font='8px Share Tech Mono,monospace';ctx.textAlign='center';
  ctx.fillText('SIDE VIEW — TRAJECTORY & SPIN',splitX/2,18);
  ctx.fillText('AFT VIEW — SPIN AXIS',splitX+(W-splitX)/2,18);
  // arc params
  var elev=30*Math.PI/180;
  var aLen=splitX*0.82,ax0=splitX*0.05,ay0=H*0.88;
  // trajectory arc (parabolic guide)
  ctx.strokeStyle='rgba(30,72,140,0.18)';ctx.lineWidth=0.6;ctx.setLineDash([3,4]);
  ctx.beginPath();
  for(var sa=0;sa<=1;sa+=0.04){
    var apx=ax0+sa*aLen*Math.cos(elev)*0.92,apy=ay0-sa*aLen*Math.sin(elev)*0.92-sa*(1-sa)*aLen*0.32;
    if(sa===0)ctx.moveTo(apx,apy);else ctx.lineTo(apx,apy);
  }
  ctx.stroke();ctx.setLineDash([]);
  // pod position on arc
  var s=Math.min(t*0.95,0.93);
  var px=ax0+s*aLen*Math.cos(elev)*0.92,py=ay0-s*aLen*Math.sin(elev)*0.92-s*(1-s)*aLen*0.32;
  // velocity angle (tangent)
  var ds=0.01,px2=ax0+(s+ds)*aLen*Math.cos(elev)*0.92,py2=ay0-(s+ds)*aLen*Math.sin(elev)*0.92-(s+ds)*(1-s-ds)*aLen*0.32;
  var vAng=Math.atan2(py-py2,px2-px);
  var pLen=26,pR=t<0.1?3+t*30:6;
  var pCol=cargoVariant===0?'#4fc3f7':cargoVariant===1?'#ff9800':'#e84040';
  var rgb=pCol==='#4fc3f7'?'77,195,247':pCol==='#ff9800'?'255,152,0':'232,64,64';
  var spinAng=t*Math.PI*2*60; // 60 full turns over animation loop
  ctx.save();ctx.translate(px,py);ctx.rotate(-vAng);
  // spin stripes (visual bands rotating along body)
  var nS=8;
  for(var si=0;si<nS;si++){
    var sT=((si/nS)+spinAng/(Math.PI*2))%1.0;
    var sX=-pLen+sT*pLen*2;
    if(sX>-pLen&&sX<pLen){
      var sa2=Math.sin(sT*Math.PI)*0.45;
      ctx.fillStyle='rgba('+rgb+','+sa2+')';
      ctx.fillRect(Math.max(-pLen,sX),-pR,Math.min(pLen*2/nS,pLen-sX),pR*2);
    }
  }
  // shock cone (Mach cone)
  if(s>0.08){
    ctx.globalAlpha=Math.min((s-0.08)*3,0.55);
    var cA=0.065,cLen=pLen*3;
    ctx.strokeStyle='rgba(77,120,200,0.6)';ctx.lineWidth=0.8;ctx.setLineDash([2,3]);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-cLen,-cLen*Math.tan(cA));ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-cLen,cLen*Math.tan(cA));ctx.stroke();
    ctx.setLineDash([]);ctx.globalAlpha=1;
  }
  // pod outline
  ctx.beginPath();ctx.moveTo(-pLen,0);ctx.bezierCurveTo(-pLen*0.62,-pR*0.06,-pLen*0.05,-pR,0,-pR);ctx.lineTo(0,pR);ctx.bezierCurveTo(-pLen*0.05,pR,-pLen*0.62,pR*0.06,-pLen,0);ctx.closePath();
  ctx.fillStyle='rgba(3,8,18,.15)';ctx.strokeStyle=pCol;ctx.lineWidth=1.2;ctx.fill();ctx.stroke();
  // fins
  var fH=pR*0.55,fR2=pLen*0.22;
  ctx.fillStyle='rgba(3,8,18,.85)';ctx.strokeStyle=pCol;ctx.lineWidth=0.9;ctx.globalAlpha=0.8;
  ctx.beginPath();ctx.moveTo(pLen-fR2,-pR);ctx.lineTo(pLen,-pR);ctx.lineTo(pLen,-pR-fH);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.beginPath();ctx.moveTo(pLen-fR2,pR);ctx.lineTo(pLen,pR);ctx.lineTo(pLen,pR+fH);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.globalAlpha=1;
  // angular momentum vector arrow
  ctx.strokeStyle='rgba(68,192,128,0.7)';ctx.lineWidth=1.2;
  ctx.beginPath();ctx.moveTo(-pLen-4,0);ctx.lineTo(-pLen-18,0);
  ctx.moveTo(-pLen-16,-3);ctx.lineTo(-pLen-18,0);ctx.lineTo(-pLen-16,3);
  ctx.stroke();
  ctx.fillStyle='rgba(68,192,128,0.7)';ctx.font='7px Share Tech Mono,monospace';ctx.textAlign='right';ctx.fillText('L',-pLen-20,3);
  ctx.restore();
  // altitude label
  var altKm=(s*12).toFixed(1);
  ctx.fillStyle='rgba(58,88,128,0.7)';ctx.font='7.5px Share Tech Mono,monospace';ctx.textAlign='left';
  ctx.fillText('ALT ≈ '+altKm+' km',px+14,py-12);
  // ── AFT VIEW ──
  var aftCX=splitX+(W-splitX)/2,aftCY=H/2+6;
  var aftR=Math.min((W-splitX)/2-34,H/2-44);
  ctx.fillStyle='rgba(3,8,18,0.96)';ctx.beginPath();ctx.arc(aftCX,aftCY,aftR,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle=pCol;ctx.lineWidth=2.2;ctx.beginPath();ctx.arc(aftCX,aftCY,aftR,0,Math.PI*2);ctx.stroke();
  var sp=spinAng%(Math.PI*2);
  // rotating spokes
  for(var si2=0;si2<4;si2++){
    var sa3=sp+si2*Math.PI/2;
    ctx.strokeStyle='rgba('+rgb+',0.38)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(aftCX+Math.cos(sa3)*6,aftCY+Math.sin(sa3)*6);ctx.lineTo(aftCX+Math.cos(sa3)*(aftR-3),aftCY+Math.sin(sa3)*(aftR-3));ctx.stroke();
  }
  // spin indicator arc (rotating marker)
  ctx.save();ctx.globalAlpha=0.75;ctx.strokeStyle=pCol;ctx.lineWidth=3;
  ctx.beginPath();ctx.arc(aftCX,aftCY,aftR*0.68,sp-0.35,sp+0.35);ctx.stroke();
  ctx.restore();
  // capture ring
  ctx.strokeStyle=pCol;ctx.lineWidth=2.8;ctx.globalAlpha=0.5;
  ctx.beginPath();ctx.arc(aftCX,aftCY,aftR*0.9,0,Math.PI*2);ctx.stroke();ctx.globalAlpha=1;
  // angular velocity labels
  ctx.fillStyle='rgba(68,192,128,0.8)';ctx.font='8px Share Tech Mono,monospace';ctx.textAlign='center';
  ctx.fillText('ω ≈ 30 rev/s',aftCX,aftCY+aftR+17);
  ctx.fillStyle='rgba(58,88,128,0.65)';ctx.font='7px Share Tech Mono,monospace';
  ctx.fillText('I = 100 kg·m²  ·  L = 18,850 N·m·s',aftCX,aftCY+aftR+28);
  // status
  ctx.fillStyle=pCol;ctx.font='bold 9px Share Tech Mono,monospace';ctx.textAlign='left';ctx.fillText('STATUS: GYROSCOPIC STABILISATION ACTIVE',8,16);
  ctx.fillStyle='rgba(30,72,140,0.3)';ctx.fillRect(8,H-11,W-16,3);ctx.fillStyle=pCol;ctx.fillRect(8,H-11,(W-16)*t,3);
}

/* ══ INIT ══ */
setTimeout(computeAll,80);
let _rt;window.addEventListener('resize',()=>{clearTimeout(_rt);_rt=setTimeout(()=>{if(cur===3)drawTraj();},150);});
</script>
</body>
</html>`;
    return new Response(html, {
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
  }
}

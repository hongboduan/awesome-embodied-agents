/* Embodied Agent Atlas — dependency-free, source-linked research cards. */
(function (global) {
  'use strict';

  const C = Object.freeze({ paper: '#f5f3ed', ink: '#183c33', lime: '#d4e884', muted: '#69746c', line: '#d5d9cc', white: '#fffefa', pale: '#ecefe4' });
  const SANS = '"Noto Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif';
  const SERIF = '"Noto Serif SC", "Songti SC", Georgia, "Times New Roman", serif';
  const CATEGORY = { planning: '推理与规划', spatial: '空间理解', memory: '记忆与知识', code: '代码与工具', recovery: '监控与恢复', policies: 'VLA / WAM', learning: '自我改进', evaluation: '基准与评测' };
  const TASK = { navigation: '导航', manipulation: '操作', mobile: '移动操作', qa: '问答', general: '通用任务' };
  const ENVIRONMENT = { real: '真机', simulation: '仿真', virtual: '虚拟环境' };
  const REVIEW = { 'full-review': '全文核读', 'source-checked': '原始来源核对', candidate: '候选 · 待审核', 'ai-draft': 'AI 解读 · 待复核' };
  const clean = value => String(value == null ? '' : value).replace(/\r\n?/g, '\n').trim();
  const arr = value => Array.isArray(value) ? value.map(clean).filter(Boolean) : [];
  const fallback = (value, other) => clean(value) || other;
  const titleOf = p => fallback(p.shortTitle, fallback(p.title, '未命名论文'));
  const paperUrl = p => clean(p.links && p.links.paper) || '来源链接未提供';
  const clamp = (n, min, max) => Math.min(max, Math.max(min, n));

  function font(ctx, size, weight, serif) {
    ctx.font = (weight || 400) + ' ' + size + 'px ' + (serif ? SERIF : SANS);
    ctx.textBaseline = 'top';
  }
  function box(ctx, x, y, w, h, fill, stroke, radius) {
    const r = Math.min(radius || 0, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h); ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.closePath();
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 1.5; ctx.stroke(); }
  }
  function line(ctx, x, y, end, color) {
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(end, y); ctx.lineWidth = 1.5; ctx.strokeStyle = color || C.line; ctx.stroke();
  }

  // Respect explicit line breaks, prefer word boundaries, and split long URLs safely.
  function wrap(ctx, value, width) {
    const output = [];
    for (const paragraph of clean(value).split('\n')) {
      if (!paragraph) { output.push(''); continue; }
      const tokens = paragraph.match(/[\u3400-\u9fff\uf900-\ufaff]|\s+|[^\s\u3400-\u9fff\uf900-\ufaff]+/gu) || [];
      let current = '';
      for (let token of tokens) {
        if (!current) token = token.replace(/^\s+/, '');
        if (!token) continue;
        if (ctx.measureText(current + token).width <= width) { current += token; continue; }
        if (/^[，。！？；：、）》】〕〉”’」』…,.!?;:%]/u.test(token) && Array.from(current).length > 1) {
          const previous = Array.from(current); const carry = previous.pop();
          output.push(previous.join('').trimEnd()); current = carry + token; continue;
        }
        if (current) { output.push(current.trimEnd()); current = ''; token = token.trimStart(); }
        if (ctx.measureText(token).width <= width) { current = token; continue; }
        for (const ch of Array.from(token)) {
          if (current && ctx.measureText(current + ch).width > width) { output.push(current); current = ''; }
          current += ch;
        }
      }
      if (current) output.push(current.trimEnd());
    }
    return output.length ? output : [''];
  }

  function fitted(ctx, value, width, height, options) {
    const o = options || {};
    const max = o.size || 32, min = o.min || 20, leading = o.leading || 1.48;
    let size = max, lines;
    for (; size >= min; size--) {
      font(ctx, size, o.weight, o.serif);
      lines = wrap(ctx, value, width);
      if (lines.length * size * leading <= height) break;
    }
    size = Math.max(size, min); font(ctx, size, o.weight, o.serif); lines = wrap(ctx, value, width);
    let clipped = false;
    const count = Math.max(1, Math.floor(height / (size * leading)));
    if (lines.length > count) {
      clipped = true; lines = lines.slice(0, count);
      const tail = o.tail || '…（全文见论文页）';
      let end = lines[count - 1];
      while (end && ctx.measureText(end + tail).width > width) end = Array.from(end).slice(0, -1).join('');
      lines[count - 1] = end + tail;
    }
    return { size, leading, lines, clipped, height: lines.length * size * leading };
  }
  function text(ctx, value, x, y, w, h, options) {
    const o = options || {}, layout = fitted(ctx, value, w, h, o);
    font(ctx, layout.size, o.weight, o.serif); ctx.fillStyle = o.color || C.ink;
    layout.lines.forEach((part, i) => ctx.fillText(part, x, y + i * layout.size * layout.leading));
    if (layout.clipped && o.warn !== false && ctx.canvas.atlasWarnings) ctx.canvas.atlasWarnings.push((o.name || '文本') + '过长，已明确标记省略；请查看完整论文页。');
    return y + layout.height;
  }
  function tiny(ctx, value, x, y, color, size) {
    font(ctx, size || 20, 500); ctx.fillStyle = color || C.muted; ctx.fillText(value, x, y);
  }
  function pill(ctx, value, x, y, dark) {
    font(ctx, 19, 500); const w = ctx.measureText(value).width + 30;
    box(ctx, x, y, w, 40, dark ? C.ink : C.pale, null, 20);
    tiny(ctx, value, x + 15, y + 10, dark ? C.paper : C.ink, 19);
    return w;
  }
  function pills(ctx, values, x, y, width, maxRows) {
    let pos = x, row = 0;
    for (const value of values) {
      font(ctx, 19, 500); const w = ctx.measureText(value).width + 30;
      if (pos + w > x + width) { row++; pos = x; }
      if (row >= (maxRows || 2)) break;
      if (w > width) continue;
      pill(ctx, value, pos, y + row * 52); pos += w + 12;
    }
  }
  function sourceId(p) {
    const url = paperUrl(p), match = url.match(/(?:abs|pdf)\/([\d.]+(?:v\d+)?)/i);
    return match ? 'arXiv:' + match[1] : fallback(p.id, '论文来源见链接');
  }
  function header(ctx, p, page, total) {
    const W = ctx.canvas.width;
    box(ctx, 72, 56, 31, 31, C.ink, null, 4);
    tiny(ctx, 'EA', 77, 64, C.lime, 14);
    tiny(ctx, 'EMBODIED AGENT ATLAS', 117, 61, C.ink, 20);
    const label = (REVIEW[p.review] || '来源待核实') + '  /  ' + String(page + 1).padStart(2, '0') + '—' + String(total).padStart(2, '0');
    font(ctx, 18, 500); ctx.fillStyle = C.muted; ctx.fillText(label, W - 72 - ctx.measureText(label).width, 62);
    line(ctx, 72, 115, W - 72);
  }
  function footer(ctx, p) {
    const W = ctx.canvas.width, H = ctx.canvas.height, hasWarnings = ctx.canvas.atlasWarnings.length > 0;
    line(ctx, 72, H - 123, W - 72);
    tiny(ctx, sourceId(p) + (p.date ? '  ·  ' + clean(p.date) : ''), 72, H - 100, C.ink, 18);
    const right = '仅供研究阅读 · 结论以原文为准';
    font(ctx, 17, 400); ctx.fillStyle = C.muted; ctx.fillText(right, W - 72 - ctx.measureText(right).width, H - 99);
    text(ctx, paperUrl(p), 72, H - 68, W - 144, 27, { size: 17, min: 14, leading: 1.1, color: C.muted, tail: '…', name: '来源链接' });
    if (hasWarnings) tiny(ctx, '部分文字已标记省略，完整内容请查看论文页。', 72, H - 33, C.ink, 16);
  }
  function section(ctx, index, heading) {
    tiny(ctx, 'RESEARCH NOTE  /  ' + index, 80, 171, C.muted, 20);
    text(ctx, heading, 76, 221, 930, 112, { size: 68, min: 45, leading: 1.2, serif: true, name: '页标题' });
  }
  function tagNames(p) {
    return arr(p.categories).map(c => CATEGORY[c] || c).concat(arr(p.environment).map(e => ENVIRONMENT[e] || e));
  }
  function numbered(values, none) {
    const all = arr(values);
    return all.length ? all.map((v, i) => String(i + 1).padStart(2, '0') + '  ' + v).join('\n\n') : none;
  }

  const imageCache = new Map();
  function validFigurePath(p) {
    const path = clean(p.figure && p.figure.path);
    return /^assets\/papers\/[a-zA-Z0-9._/-]+\.(png|jpe?g|webp)$/i.test(path) && !path.includes('..') ? path : '';
  }
  async function loadFigure(p) {
    const path = validFigurePath(p);
    if (!path || typeof global.Image !== 'function') return null;
    if (!imageCache.has(path)) imageCache.set(path, new Promise(resolve => {
      const img = new global.Image();
      let settled = false;
      const finish = value => { if (settled) return; settled = true; global.clearTimeout(timer); resolve(value); };
      const timer = global.setTimeout(() => finish(null), 12000);
      img.onload = () => finish(img);
      img.onerror = () => finish(null);
      img.src = path;
    }));
    return imageCache.get(path);
  }
  function figure(ctx, p, img, x, y, width, height) {
    box(ctx, x, y, width, height, '#ffffff', C.line, 12);
    const f = p.figure || {};
    const label = f.kind === 'page-preview' ? 'PDF 页面预览' : (clean(f.figureLabel) || '论文原图');
    const source = clean(f.sourceUrl).match(/arxiv\.org\/(?:pdf|abs)\/([0-9]{4}\.[0-9]{4,5})(v[0-9]+)/);
    const version = source ? 'arXiv:' + source[1] + source[2] : (f.version ? 'PDF v' + f.version : '图像版本未记录');
    tiny(ctx, img ? label + '  ·  ' + version + (f.page ? '  ·  PDF p.' + f.page : '') : '论文插图待提取', x + 22, y + 18, C.muted, 18);
    if (img) {
      const iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
      const areaW = width - 36, areaH = height - 94, scale = Math.min(areaW / iw, areaH / ih);
      ctx.drawImage(img, x + (width - iw * scale) / 2, y + 54 + (areaH - ih * scale) / 2, iw * scale, ih * scale);
      text(ctx, clean(f.caption) || '原图与版权归论文作者；请结合原文阅读。', x + 22, y + height - 35, width - 44, 25, { size: 16, min: 15, leading: 1.1, color: C.muted, tail: '…', warn: false, name: '原图图注' });
    } else {
      text(ctx, validFigurePath(p) ? '原文图像暂时无法加载' : '原文图像正在整理', x + 45, y + height / 2 - 30, width - 90, 66, { size: 30, min: 23, leading: 1.3, color: C.muted });
      tiny(ctx, '完整框架请查看来源 PDF', x + 45, y + height / 2 + 45, C.muted, 19);
      if (validFigurePath(p)) ctx.canvas.atlasWarnings.push('原图暂未加载，已保留 PDF 来源。');
    }
  }

  function portrait(ctx, p, page, img) {
    header(ctx, p, page, 5);
    if (page === 0) {
      tiny(ctx, '论文阅读  /  EMBODIED AGENTS', 80, 157, C.muted, 21);
      text(ctx, titleOf(p), 73, 208, 934, 165, { size: 96, min: 44, leading: 1.12, serif: true, name: '论文简称' });
      text(ctx, fallback(p.title, titleOf(p)), 80, 391, 915, 111, { size: 28, min: 22, leading: 1.35, name: '论文标题' });
      figure(ctx, p, img, 72, 529, 936, 443);
      box(ctx, 72, 995, 936, 271, C.ink, null, 13);
      tiny(ctx, '一句话读懂', 103, 1022, C.lime, 22);
      text(ctx, fallback(p.summaryZh, '中文摘要尚待整理，请查看原文。'), 103, 1073, 874, 156, { size: 35, min: 26, leading: 1.5, color: C.paper, name: '核心结论' });
    } else if (page === 1) {
      section(ctx, '02', '它在解决什么问题？');
      box(ctx, 80, 374, 8, 35, C.lime);
      tiny(ctx, '研究问题', 107, 382, C.muted, 23);
      text(ctx, fallback(p.problem, '研究问题尚未核实，请查看原文。'), 80, 451, 916, 418, { size: 39, min: 25, leading: 1.6, name: '研究问题' });
      line(ctx, 80, 895, 1000);
      tiny(ctx, '论文核心思路', 80, 931, C.muted, 21);
      text(ctx, fallback(p.summaryZh, '核心思路尚待整理。'), 80, 977, 916, 179, { size: 31, min: 23, leading: 1.5, name: '核心思路' });
      const scope = arr(p.tasks).map(t => TASK[t] || t).concat(arr(p.environment).map(e => ENVIRONMENT[e] || e));
      pills(ctx, scope.length ? scope : ['适用场景待核实'], 80, 1196, 920, 1);
    } else if (page === 2) {
      section(ctx, '03', '方法如何运转？');
      if (img) {
        figure(ctx, p, img, 80, 365, 920, 385);
        text(ctx, fallback(p.method, '方法细节尚未核实，请查看原文。'), 80, 787, 918, 211, { size: 32, min: 23, leading: 1.5, name: '方法概述' });
        line(ctx, 80, 1022, 1000);
        tiny(ctx, '模型角色与输出接口', 80, 1054, C.muted, 21);
        text(ctx, fallback(p.role && p.role.model, '模型角色未核实') + '\n' + fallback(p.role && p.role.output, '输出接口未核实'), 80, 1101, 918, 157, { size: 27, min: 22, leading: 1.5, name: '系统接口' });
      } else {
        text(ctx, fallback(p.method, '方法细节尚未核实，请查看原文。'), 80, 375, 918, 280, { size: 33, min: 23, leading: 1.5, name: '方法概述' });
        tiny(ctx, '系统分工  /  逐项理解方法', 80, 687, C.muted, 21);
        const rows = [['model', '模型角色'], ['output', '输出接口'], ['memory', '状态与记忆'], ['recovery', '失败恢复'], ['adaptation', '适配方式']];
        const role = p.role || {};
        rows.forEach(([key, label], i) => {
          const y = 739 + i * 105;
          box(ctx, 80, y, 920, 94, i % 2 ? C.paper : C.pale, C.line, 7);
          tiny(ctx, label, 102, y + 34, C.muted, 22);
          ctx.beginPath(); ctx.moveTo(268, y + 18); ctx.lineTo(268, y + 76); ctx.strokeStyle = C.line; ctx.lineWidth = 1.5; ctx.stroke();
          text(ctx, fallback(role[key], '未核实'), 291, y + 19, 681, 65, { size: 25, min: 19, leading: 1.32, name: label });
        });
      }
    } else if (page === 3) {
      section(ctx, '04', '结果与证据');
      tiny(ctx, '论文报告 · 请结合评测设置阅读', 80, 374, C.muted, 21);
      text(ctx, numbered(p.findings, '量化结果尚未核实，请查看原文。'), 80, 429, 915, 446, { size: 34, min: 22, leading: 1.5, name: '论文主要结果' });
      box(ctx, 64, 910, 952, 353, C.pale, null, 12);
      tiny(ctx, '原始来源索引', 92, 937, C.ink, 22);
      const evidence = Array.isArray(p.evidence) ? p.evidence : [];
      const evidenceText = evidence.length ? evidence.map((e, i) => '[' + (i + 1) + '] ' + fallback(e.label, e.page ? 'PDF p.' + e.page : '原始来源') + '：' + fallback(e.claim, '具体结论请核对原文') + '\n' + fallback(e.source, paperUrl(p))).join('\n\n') : '尚未提供逐条证据，请先核对论文原文。';
      text(ctx, evidenceText, 92, 985, 884, 253, { size: 23, min: 17, leading: 1.3, name: '证据索引' });
    } else {
      section(ctx, '05', '边界与进一步思考');
      tiny(ctx, '局限与适用条件', 80, 374, C.muted, 21);
      text(ctx, numbered(p.limitations, '局限尚未整理；未披露不代表不存在。'), 80, 429, 915, 453, { size: 34, min: 22, leading: 1.5, name: '局限与边界' });
      box(ctx, 64, 920, 952, 252, C.ink, null, 12);
      tiny(ctx, '编辑提问  /  用于选题与复现', 94, 947, C.lime, 21);
      text(ctx, '模型何时介入？\n哪些状态需要显式保存？\n失败以后，系统如何恢复？', 94, 997, 873, 150, { size: 31, min: 27, leading: 1.5, color: C.paper, name: '编辑提问' });
      text(ctx, '对照环境先验、评测协议与适配成本，再判断方法是否适合自己的任务。', 80, 1210, 917, 67, { size: 22, min: 19, leading: 1.4, color: C.muted, name: '阅读提示' });
    }
    footer(ctx, p);
  }

  function landscape(ctx, p, img) {
    header(ctx, p, 0, 1);
    text(ctx, titleOf(p), 70, 149, 1776, 108, { size: 83, min: 42, serif: true, leading: 1.12, name: '论文简称' });
    text(ctx, fallback(p.title, titleOf(p)), 74, 268, 1760, 66, { size: 26, min: 21, leading: 1.26, name: '论文标题' });
    text(ctx, fallback(p.summaryZh, '中文摘要尚待整理，请查看原文。'), 74, 342, 1760, 71, { size: 29, min: 23, leading: 1.35, name: '核心结论' });
    figure(ctx, p, img, 72, 438, 890, 474);
    const blocks = [
      ['01', '研究问题', fallback(p.problem, '尚待核实')],
      ['02', '核心方法', fallback(p.method, '尚待核实')],
      ['03', '结果与证据', numbered(p.findings, '尚待核实').replace(/\n\n/g, '\n')],
      ['04', '适用边界', numbered(p.limitations, '尚待核实').replace(/\n\n/g, '\n')]
    ];
    blocks.forEach(([n, heading, content], i) => {
      const x = 986 + (i % 2) * 442, y = 438 + Math.floor(i / 2) * 249, dark = i === 2;
      box(ctx, x, y, 418, 225, dark ? C.ink : C.white, dark ? null : C.line, 10);
      tiny(ctx, n + '  /  ' + heading, x + 21, y + 20, dark ? C.lime : C.ink, 23);
      line(ctx, x + 21, y + 59, x + 397, dark ? '#567263' : C.line);
      text(ctx, content, x + 21, y + 77, 376, 130, { size: 22, min: 18, leading: 1.4, color: dark ? C.paper : C.ink, name: heading });
    });
    footer(ctx, p);
  }

  async function render(paper, options) {
    if (!paper || typeof paper !== 'object') throw new TypeError('AtlasCards.render 需要论文记录。');
    if (typeof document === 'undefined') throw new Error('卡片渲染需要浏览器 Canvas。');
    await ready();
    const img = await loadFigure(paper);
    const o = options || {}, format = o.format === 'landscape' ? 'landscape' : 'portrait';
    const page = format === 'landscape' ? 0 : clamp(Math.floor(Number(o.page) || 0), 0, 4);
    const canvas = document.createElement('canvas');
    canvas.width = format === 'landscape' ? 1920 : 1080;
    canvas.height = format === 'landscape' ? 1080 : 1440;
    canvas.atlasWarnings = [];
    canvas.dataset.format = format; canvas.dataset.page = String(page);
    canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', titleOf(paper) + ' · ' + (format === 'landscape' ? '横版论文卡片' : '竖版论文卡片 ' + (page + 1) + '/5'));
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('当前浏览器不支持 Canvas 2D。');
    ctx.fillStyle = C.paper; ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (format === 'landscape') landscape(ctx, paper, img); else portrait(ctx, paper, page, img);
    canvas.dataset.truncated = canvas.atlasWarnings.length ? 'true' : 'false';
    return canvas;
  }

  function filename(paper, suffix) {
    const stem = titleOf(paper).replace(/[\\/:*?"<>|\u0000-\u001f]/g, '-').replace(/\s+/g, '-').slice(0, 80);
    return (stem || 'paper') + '-' + suffix;
  }
  function toBlob(canvas) {
    return new Promise((resolve, reject) => canvas.toBlob(blob => blob ? resolve(blob) : reject(new Error('生成 PNG 失败，请重试。')), 'image/png'));
  }
  function save(blob, name) {
    const url = URL.createObjectURL(blob), anchor = document.createElement('a');
    anchor.href = url; anchor.download = name; anchor.style.display = 'none';
    document.body.appendChild(anchor); anchor.click(); anchor.remove();
    global.setTimeout(() => URL.revokeObjectURL(url), 60000);
  }
  async function ready() { if (document.fonts && document.fonts.ready) await document.fonts.ready; }
  async function download(paper, options) {
    await ready();
    const canvas = await render(paper, options), blob = await toBlob(canvas);
    const name = filename(paper, canvas.dataset.format + '-' + (Number(canvas.dataset.page) + 1) + '.png');
    save(blob, name);
    return { filename: name, width: canvas.width, height: canvas.height, warnings: canvas.atlasWarnings.slice() };
  }

  const CRC_TABLE = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    return t;
  })();
  function crc32(bytes) { let c = 0xffffffff; for (const b of bytes) c = CRC_TABLE[(c ^ b) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
  function zipStored(files) {
    const encoder = new TextEncoder(), locals = [], centers = [];
    let offset = 0, centralSize = 0;
    const d = new Date(), date = ((Math.max(1980, d.getFullYear()) - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    const time = (d.getHours() << 11) | (d.getMinutes() << 5) | Math.floor(d.getSeconds() / 2);
    for (const file of files) {
      const name = encoder.encode(file.name), data = file.bytes, crc = crc32(data);
      const local = new Uint8Array(30 + name.length), lv = new DataView(local.buffer);
      lv.setUint32(0, 0x04034b50, true); lv.setUint16(4, 20, true); lv.setUint16(6, 0x0800, true);
      lv.setUint16(10, time, true); lv.setUint16(12, date, true); lv.setUint32(14, crc, true);
      lv.setUint32(18, data.length, true); lv.setUint32(22, data.length, true); lv.setUint16(26, name.length, true); local.set(name, 30);
      const center = new Uint8Array(46 + name.length), cv = new DataView(center.buffer);
      cv.setUint32(0, 0x02014b50, true); cv.setUint16(4, 20, true); cv.setUint16(6, 20, true); cv.setUint16(8, 0x0800, true);
      cv.setUint16(12, time, true); cv.setUint16(14, date, true); cv.setUint32(16, crc, true);
      cv.setUint32(20, data.length, true); cv.setUint32(24, data.length, true); cv.setUint16(28, name.length, true); cv.setUint32(42, offset, true); center.set(name, 46);
      locals.push(local, data); centers.push(center); offset += local.length + data.length; centralSize += center.length;
    }
    const end = new Uint8Array(22), ev = new DataView(end.buffer);
    ev.setUint32(0, 0x06054b50, true); ev.setUint16(8, files.length, true); ev.setUint16(10, files.length, true);
    ev.setUint32(12, centralSize, true); ev.setUint32(16, offset, true);
    return new Blob(locals.concat(centers, [end]), { type: 'application/zip' });
  }
  async function downloadAll(paper, options) {
    if (options && options.format === 'landscape') return download(paper, { format: 'landscape' });
    await ready();
    const files = [], warnings = [];
    for (let page = 0; page < 5; page++) {
      const canvas = await render(paper, { format: 'portrait', page }), blob = await toBlob(canvas);
      files.push({ name: filename(paper, 'portrait-' + String(page + 1).padStart(2, '0') + '.png'), bytes: new Uint8Array(await blob.arrayBuffer()) });
      warnings.push(...canvas.atlasWarnings.map(w => '第 ' + (page + 1) + ' 页：' + w));
    }
    const name = filename(paper, 'portrait-5-cards.zip');
    save(zipStored(files), name);
    return { filename: name, count: 5, width: 1080, height: 1440, warnings };
  }
  function bibEscape(value) {
    const escapes = { '\\': '\\textbackslash{}', '{': '\\{', '}': '\\}', '&': '\\&', '%': '\\%', '_': '\\_', '#': '\\#', '$': '\\$', '~': '\\~{}', '^': '\\^{}' };
    return Array.from(clean(value).replace(/\n/g, ' ')).map(ch => escapes[ch] || ch).join('');
  }
  function bibAuthors(value) {
    return bibEscape(clean(value).replace(/\s*[;；、]\s*/g, ' and ').replace(/(?:\s+|、)(?:等|et\s+al\.?|and\s+others)\s*$/i, ' and others'));
  }
  function getBibtex(paper) {
    const p = paper || {}, year = p.year || (clean(p.date).match(/^\d{4}/) || [''])[0];
    const key = (titleOf(p).replace(/[^a-z0-9]/gi, '') || 'EmbodiedAgent') + (year || '');
    const fields = ['  title = {{' + bibEscape(fallback(p.title, titleOf(p))) + '}}'];
    if (clean(p.authors) && clean(p.authors) !== '未核实') fields.push('  author = {' + bibAuthors(p.authors) + '}');
    if (year) fields.push('  year = {' + year + '}');
    const url = clean(p.links && p.links.paper), arxiv = url.replace(/\.pdf(?:$|[?#])/i, '').match(/(?:arxiv\.org\/(?:abs|pdf)\/)([\d.]+(?:v\d+)?)/i);
    if (arxiv) { fields.push('  eprint = {' + arxiv[1] + '}'); fields.push('  archivePrefix = {arXiv}'); }
    if (/^https:\/\//i.test(url)) fields.push('  url = {' + bibEscape(url) + '}');
    return '@misc{' + key + ',\n' + fields.join(',\n') + '\n}\n';
  }

  global.AtlasCards = Object.freeze({ render, download, downloadAll, getBibtex });
})(typeof window !== 'undefined' ? window : globalThis);

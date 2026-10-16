(function (root) {
  'use strict';

  const DAY = 86400000;
  const BEIJING_OFFSET = 8 * 3600000;
  const array = value => Array.isArray(value) ? value : [];
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  const safeUrl = value => {
    try { const url = new URL(value); return url.protocol === 'https:' ? url.href : ''; }
    catch (_) { return ''; }
  };

  // Date-only editorial fields denote a Beijing calendar day, not UTC midnight.
  function timestamp(value) {
    if (value instanceof Date) return Number.isFinite(value.getTime()) ? value.getTime() : null;
    if (typeof value !== 'string' || !value.trim()) return null;
    let text = value.trim();
    const match = text.match(/^(\d{4})-(\d{2})-(\d{2})(?:$|T)/);
    if (!match) return null;
    const check = new Date(Date.UTC(+match[1], +match[2] - 1, +match[3]));
    if (check.getUTCFullYear() !== +match[1] || check.getUTCMonth() !== +match[2] - 1 || check.getUTCDate() !== +match[3]) return null;
    if (/^\d{4}-\d{2}-\d{2}$/.test(text)) text += 'T00:00:00+08:00';
    else if (!/(Z|[+-]\d{2}:?\d{2})$/i.test(text)) text += 'Z';
    const result = Date.parse(text);
    return Number.isFinite(result) ? result : null;
  }

  function beijingDay(ms) { return new Date(ms + BEIJING_OFFSET).toISOString().slice(0, 10); }
  function beijingTime(ms) { return new Date(ms + BEIJING_OFFSET).toISOString().slice(0, 16).replace('T', ' '); }
  function paperStatus(paper) {
    if (!paper) return '条目待核对';
    if (paper.review === 'candidate') return '候选 · 待精读';
    if (paper.review === 'ai-draft') return 'AI 草稿 · 待人工复核';
    if (paper.deepRead) return '精选 · 完整精读';
    if (paper.review === 'source-checked') return paper.curated ? '精选 · 原始来源已核对' : '原始来源已核对';
    return paper.curated ? '精选收录' : '研究条目';
  }

  /** Pure summary. The optional clock makes Beijing day boundaries testable. */
  function summary(data = {}, now = new Date()) {
    data = data && typeof data === 'object' ? data : {};
    const nowMs = now instanceof Date ? now.getTime() : typeof now === 'number' ? now : timestamp(now);
    if (!Number.isFinite(nowMs)) throw new TypeError('AtlasUpdates.summary requires a valid now value');
    const start = Math.floor((nowMs + BEIJING_OFFSET) / DAY) * DAY - BEIJING_OFFSET - 6 * DAY;
    const papers = array(data.papers).filter(p => p && p.id);
    const paperMap = new Map(papers.map(p => [String(p.id), p]));
    const seen = new Set();
    const events = array(data.events).filter(e => e && typeof e === 'object').map(event => ({
      ...event, timestamp: timestamp(event.date || event.timestamp || event.at)
    })).filter(e => e.timestamp !== null && e.timestamp <= nowMs).sort((a, b) => a.timestamp - b.timestamp).filter(e => {
      // Keep the first observation: duplicate discovery records must not look new again.
      const paperId = String(e.paperId || '');
      if ((e.type === 'discovered' || e.type === 'version') && !paperId) return false;
      const key = e.type === 'discovered' ? 'discovered:' + paperId : e.type === 'version'
        ? ['version', paperId, e.fromVersion ?? '', e.toVersion ?? ''].join(':')
        : e.id ? 'event:' + e.id : [e.type, paperId, e.timestamp, e.title].join(':');
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }).map(e => ({ ...e, paper: paperMap.get(String(e.paperId)), day: beijingDay(e.timestamp) }));
    const curated = [...paperMap.values()].filter(p => p.curated === true).map(p => ({
      id: 'collected-' + p.id, paperId: p.id, type: 'collected', title: p.shortTitle || p.title,
      timestamp: timestamp(p.addedAt), paper: p, date: p.addedAt
    })).filter(e => e.timestamp !== null && e.timestamp <= nowMs).map(e => ({ ...e, day: beijingDay(e.timestamp) }));
    const recentEvents = events.filter(e => e.timestamp >= start);
    const recentCurated = curated.filter(e => e.timestamp >= start);
    const recent = [...recentEvents, ...recentCurated].sort((a, b) => b.timestamp - a.timestamp);
    const timeline = [...events, ...curated].sort((a, b) => b.timestamp - a.timestamp);
    const sourceStatus = data.updateStatus || {};
    const validPast = value => { const ms = timestamp(value); return ms !== null && ms <= nowMs ? ms : null; };
    const lastSuccess = validPast(sourceStatus.lastSuccess);
    const lastAttempt = validPast(sourceStatus.lastAttempt);
    const failed = ['error', 'failed', 'partial'].includes(sourceStatus.mode);
    const stale = lastSuccess !== null && nowMs - lastSuccess > 2 * DAY;
    const state = failed ? 'error' : lastSuccess === null ? 'waiting' : stale ? 'stale' : 'active';
    const enrichment = data.enrichmentStatus || {};
    return {
      start, end: nowMs, startDay: beijingDay(start), endDay: beijingDay(nowMs),
      counts: { discovered: recentEvents.filter(e => e.type === 'discovered').length,
        versions: recentEvents.filter(e => e.type === 'version').length, curated: recentCurated.length },
      recentEvents, recentCurated, recent, timeline,
      totalCandidates: papers.filter(p => p.review === 'candidate').length,
      status: { state, failed, stale, lastSuccess, lastAttempt,
        label: ({active: '检索持续更新', error: '本轮检索未完成', stale: '检索记录已超过 48 小时', waiting: '尚无成功检索记录'})[state] },
      enrichment: { llmMode: enrichment.llmMode || 'unknown', mode: enrichment.mode || 'unknown',
        lastFinished: validPast(enrichment.lastFinished),
        pdfExtracted: Number.isFinite(enrichment.pdfExtracted) ? enrichment.pdfExtracted : null,
        aiDraftsGenerated: Number.isFinite(enrichment.aiDraftsGenerated) ? enrichment.aiDraftsGenerated : null }
    };
  }

  function statusLine(s, expanded = false) {
    const status = s.status;
    const success = status.lastSuccess === null ? '暂无可核实的成功检索时间' : '最近成功检索：' + beijingTime(status.lastSuccess) + ' 北京时间';
    let detail = '';
    if (expanded && status.failed) detail = '<p class="au-status-detail">本轮检索暂未完成，当前保留已有研究记录。' + (status.lastAttempt !== null ? '最近尝试：' + escape(beijingTime(status.lastAttempt)) + ' 北京时间。' : '') + '</p>';
    else if (expanded && status.stale) detail = '<p class="au-status-detail">最近成功检索已超过 48 小时；当前记录不代表已经覆盖最新论文。</p>';
    return '<div class="au-status au-status-' + status.state + '"><p><span class="au-status-dot" aria-hidden="true"></span><strong>' + escape(status.label) + '</strong><span>' + escape(success) + '</span></p>' + detail + '</div>';
  }

  function countTiles(s) {
    return '<div class="au-counts" aria-label="最近七天更新统计">' + [
      [s.counts.discovered, '新增候选', '自动发现，尚待精读', '#library?filter=candidate'],
      [s.counts.versions, '版本变化', '跟踪已收录论文的更新', '#updates?range=7'],
      [s.counts.curated, '近期收录精选', '按已记录的收录日期统计', '#library?filter=curated']
    ].map(([count, label, description, url]) => '<a class="au-count" href="' + url + '"><strong>' + count + '</strong><span>' + label + '<small>' + description + '</small></span><b aria-hidden="true">↗</b></a>').join('') + '</div>';
  }

  function eventLabel(event) { return ({discovered: '发现候选', version: '版本更新', collected: '收录精选'})[event.type] || '研究记录'; }
  function titleLink(event) {
    const title = escape(event.title || event.paper?.shortTitle || event.paper?.title || '研究条目');
    if (event.paper) return '<a href="#paper=' + encodeURIComponent(event.paperId) + '">' + title + '<span aria-hidden="true"> ↗</span></a>';
    const url = safeUrl(event.url);
    return url ? '<a href="' + escape(url) + '" target="_blank" rel="noopener noreferrer">' + title + '<span aria-hidden="true"> ↗</span></a>' : title;
  }

  function renderHome(data, options = {}) {
    const container = root.document?.getElementById('recent-updates');
    if (!container) return;
    const s = summary(data, options.now || new Date());
    const latest = s.recent.slice(0, 3);
    container.innerHTML = '<section class="au-home" aria-labelledby="au-home-heading"><div class="au-heading"><div><span class="au-eyebrow">RECENT RESEARCH / 最近 7 天</span><h2 id="au-home-heading">研究在继续更新。</h2></div><a class="au-text-link" href="#updates?range=7">查看全部动态 <span aria-hidden="true">↗</span></a></div>' + countTiles(s) + statusLine(s) +
      (latest.length ? '<ul class="au-highlights">' + latest.map(e => '<li><span class="au-type au-type-' + escape(e.type) + '">' + eventLabel(e) + '</span><span class="au-highlight-title">' + titleLink(e) + '</span><time>' + escape(e.day.slice(5)) + '</time></li>').join('') + '</ul>' : '<p class="au-empty-small">最近 7 天暂无已记录的研究更新。已有精选与候选仍可浏览。</p>') +
      '<div class="au-home-foot"><span>' + escape(s.startDay) + ' — ' + escape(s.endDay) + ' · 北京时间自然日</span><a href="#library?filter=candidate">浏览待审核候选 <span aria-hidden="true">↗</span></a></div></section>';
    return s;
  }

  function eventDescription(event) {
    if (event.type === 'collected') return '依据条目记录的收录日期展示；此日期不表示审核完成时间。';
    if (event.type === 'discovered') return '自动检索发现；当前状态：' + paperStatus(event.paper) + '。';
    if (event.type === 'version') {
      const from = event.fromVersion == null ? '' : 'v' + event.fromVersion + ' → ';
      const to = event.toVersion == null ? '新版本' : 'v' + event.toVersion;
      const readVersion = event.paper?.reviewedVersion;
      return from + to + '。' + (readVersion ? '当前精读对应 v' + readVersion + '，新版本内容需单独复核。' : '版本发现不表示已经重读或审核新版本。');
    }
    return event.message || event.description || '研究动态记录。';
  }

  function enrichmentLine(s) {
    const e = s.enrichment;
    if (e.llmMode === 'not-configured') return '自动精读未启用；PDF 配图按独立流程持续处理。';
    if (e.aiDraftsGenerated !== null && e.lastFinished !== null) return '最近一轮生成 AI 草稿 ' + e.aiDraftsGenerated + ' 篇，仍需人工复核。';
    return '配图、候选与经审核的解读分别维护；自动发现不等于已完成精读。';
  }

  function renderPage(data, options = {}) {
    const container = root.document?.getElementById('updates-view');
    if (!container) return;
    const s = summary(data, options.now || new Date());
    const range = options.range === 'all' ? 'all' : '7';
    const records = range === 'all' ? s.timeline : s.recent;
    const groups = new Map();
    records.forEach(event => { if (!groups.has(event.day)) groups.set(event.day, []); groups.get(event.day).push(event); });
    container.innerHTML = '<div class="au-page"><div class="page-kicker">RESEARCH UPDATES / 研究动态</div><div class="page-heading"><div><h1>追新，也跟进变化。</h1><p>从自动发现到精选收录，每一种变化分别记录。</p></div></div>' +
      '<p class="au-count-period">最近 7 天 · ' + escape(s.startDay) + ' — ' + escape(s.endDay) + '</p>' + countTiles(s) + statusLine(s, true) + '<p class="au-process-note">' + escape(enrichmentLine(s)) + ' 当前有 <a href="#library?filter=candidate">' + s.totalCandidates + ' 篇待审核候选 ↗</a>。</p>' +
      '<div class="au-timeline-head"><div><h2>更新记录</h2><p>' + (range === 'all' ? '全部可用记录' : escape(s.startDay) + ' — ' + escape(s.endDay)) + ' · 北京时间</p></div><nav class="au-range" aria-label="更新记录时间范围"><a href="#updates?range=7"' + (range === '7' ? ' aria-current="page"' : '') + '>最近 7 天</a><a href="#updates?range=all"' + (range === 'all' ? ' aria-current="page"' : '') + '>全部记录</a></nav></div>' +
      (records.length ? '<div class="au-timeline">' + [...groups].map(([day, events]) => '<section class="au-day" aria-label="' + escape(day) + ' 的研究动态"><h3><time datetime="' + escape(day) + '">' + escape(day) + '</time><small>' + events.length + ' 条记录</small></h3><div class="au-day-records">' + events.map(e => '<article class="au-record"><div class="au-record-meta"><span class="au-type au-type-' + escape(e.type) + '">' + eventLabel(e) + '</span><span>' + escape(paperStatus(e.paper)) + '</span>' + (e.type === 'version' && e.toVersion != null ? '<span>发现 v' + escape(e.toVersion) + '</span>' : '') + '</div><h4>' + titleLink(e) + '</h4><p>' + escape(eventDescription(e)) + '</p></article>').join('') + '</div></section>').join('') + '</div>' : '<div class="au-empty"><h3>这个时间范围暂无更新记录</h3><p>可以查看全部记录，或继续浏览已收录的研究。</p><a href="#library">返回研究合集 ↗</a></div>') +
      '<p class="au-audit-note">“发现候选”与“版本变化”来自检索日志；“收录精选”依据条目中已有的收录日期，不代表审核发生时间。相同发现与相同版本变化已去重。版本事件保留历史，条目状态展示当前记录。</p></div>';
    return s;
  }

  const api = { summary, renderHome, renderPage };
  root.AtlasUpdates = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);

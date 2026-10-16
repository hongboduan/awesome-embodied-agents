/* Evidence-backed reading routes. Kept independent from the collection filters. */
(function () {
  'use strict';
  const list = value => Array.isArray(value) ? value : [];
  const escape = value => String(value == null ? '' : value).replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
  const safeUrl = value => { try { const url = new URL(value); return url.protocol === 'https:' ? url.href : ''; } catch { return ''; } };
  const title = paper => paper.shortTitle || paper.name || paper.title || paper.id || '未命名';
  const date = paper => paper.date || paper.addedAt || paper.discoveredAt || '';
  const labels = {uses_model:'使用模型', evaluated_on:'评测于', extends:'扩展', distills:'蒸馏自', comparison:'编辑对照'};
  const link = (url, label, className = '') => safeUrl(url) ? `<a class="${className}" href="${escape(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${escape(label)} <span aria-hidden="true">↗</span></a>` : '';
  const routeUrl = (routeId, focusId) => '#map?' + new URLSearchParams({route: routeId, ...(focusId ? {focus: focusId} : {})}).toString();
  const teamUrl = teamId => '#teams?' + new URLSearchParams({team: teamId}).toString();
  const paperUrl = id => '#paper=' + encodeURIComponent(id);
  const unique = values => [...new Set(values)];
  const routeIds = route => unique([...list(route.paperIds), ...list(route.backgroundIds), ...list(route.frontierIds)]);
  const sourcesHtml = sources => list(sources).map(source => link(source.url, source.label || '原始来源', 'map-source')).filter(Boolean).join('');
  function sourceType(paper) { return paper.sourceType === 'project' ? '项目' : paper.sourceType === 'article' ? '观点' : '论文'; }
  function recordDate(paper) { return date(paper) ? `${paper.date ? '' : '收录 '}${escape(date(paper).slice(0, 10))}` : '日期待核实'; }
  function getContext(data) {
    const map = data.researchMap || {};
    const papers = new Map(list(data.papers).map(paper => [paper.id, paper]));
    const resources = new Map(list(map.resources).map(resource => [resource.id, resource]));
    const routes = list(map.routes);
    // An unresolved endpoint is never drawn as an invented node.
    const relations = list(map.relations).filter(relation => papers.has(relation.source) && (papers.has(relation.target) || resources.has(relation.target)));
    return {map, papers, resources, routes, relations, get: id => papers.get(id) || resources.get(id)};
  }
  function paperCard(paper, context, options = {}) {
    if (!paper) return '';
    const {routeId, focusId, frontier} = options;
    const connected = context.relations.some(relation => relation.source === paper.id || relation.target === paper.id);
    return `<article class="map-work${focusId === paper.id ? ' is-focused' : ''}">
      <div class="map-work-meta"><span>${sourceType(paper)}${frontier ? ' · 待核读' : ''}</span><time>${recordDate(paper)}</time></div>
      <h3><a href="${escape(paperUrl(paper.id))}" data-map-paper="${escape(paper.id)}">${escape(title(paper))}</a></h3>
      <p>${escape(paper.summaryZh || paper.problem || '中文解读待核对，请先阅读原始来源。')}</p>
      <div class="map-work-actions"><a href="${escape(paperUrl(paper.id))}" data-map-paper="${escape(paper.id)}">${frontier ? '查看候选' : '阅读研究卡'} <span aria-hidden="true">↗</span></a>${connected && routeId ? `<a href="${escape(routeUrl(routeId, paper.id))}"${focusId === paper.id ? ' aria-current="true"' : ''}>查看关联</a>` : ''}</div>
    </article>`;
  }
  function routeTabs(context, selectedId) {
    return `<nav class="map-route-grid" aria-label="选择研究脉络">${context.routes.map((route, index) => `<a class="map-route-tab${selectedId === route.id ? ' active' : ''}" href="${escape(routeUrl(route.id))}"${selectedId === route.id ? ' aria-current="page"' : ''}><span class="map-route-number">0${index + 1}</span><span class="map-route-kicker">${escape(route.kicker || 'READING ROUTE')}</span><strong>${escape(route.title)}</strong><span class="map-route-question">${escape(route.question || route.summary || '')}</span><span class="map-route-count">${list(route.paperIds).filter(id => context.papers.has(id)).length} 项重点阅读 <span aria-hidden="true">↗</span></span></a>`).join('')}</nav>`;
  }
  function shortLines(value, width = 17, maxLines = 2) {
    const lines = []; let line = '', size = 0;
    for (const character of String(value)) {
      const weight = /[\x00-\x7F]/.test(character) ? 0.55 : 1;
      if (size + weight > width) { lines.push(line); line = ''; size = 0; }
      line += character; size += weight;
    }
    if (line) lines.push(line);
    if (lines.length > maxLines) { lines.length = maxLines; lines[maxLines - 1] = lines[maxLines - 1].slice(0, -1) + '…'; }
    return lines;
  }
  function graphHtml(focusId, relations, context, routeId) {
    const focus = context.get(focusId);
    if (!focus || !relations.length) return '';
    const neighborIds = unique(relations.map(relation => relation.source === focusId ? relation.target : relation.source)).slice(0, 6);
    const visibleIds = new Set([focusId, ...neighborIds]);
    const visible = relations.filter(relation => visibleIds.has(relation.source) && visibleIds.has(relation.target));
    const rowCount = Math.ceil(neighborIds.length / 2);
    const height = Math.max(220, rowCount * 108 + 30), centerY = height / 2;
    const positions = new Map([[focusId, {x: 450, y: centerY}]]);
    neighborIds.forEach((id, index) => {
      const sideIndex = Math.floor(index / 2), sideCount = Math.ceil((neighborIds.length - index % 2) / 2);
      positions.set(id, {x: index % 2 ? 770 : 130, y: centerY + (sideIndex - (sideCount - 1) / 2) * 108});
    });
    function edge(relation) {
      const from = positions.get(relation.source), to = positions.get(relation.target);
      const direction = to.x > from.x ? 1 : -1;
      const sx = from.x + direction * 105, tx = to.x - direction * 105;
      const path = `M ${sx} ${from.y} C ${(sx + tx) / 2} ${from.y}, ${(sx + tx) / 2} ${to.y}, ${tx} ${to.y}`;
      return `<g class="map-edge${relation.editorial ? ' editorial' : ''}" role="button" tabindex="0" data-map-relation="${escape(relation.id)}" aria-label="${escape(title(context.get(relation.source)) + ' ' + (labels[relation.type] || relation.label || '关联') + ' ' + title(context.get(relation.target)) + '，查看依据')}"><path class="map-edge-hit" d="${path}"/><path class="map-edge-line" d="${path}"${relation.editorial ? '' : ' marker-end="url(#atlas-map-arrow)"'}/></g>`;
    }
    function node(id) {
      const entity = context.get(id), point = positions.get(id), selected = id === focusId;
      const isResource = context.resources.has(id);
      const href = isResource ? safeUrl(entity.url) : routeUrl(routeId, id);
      const lines = shortLines(title(entity), 16, 2);
      const tag = isResource ? ({model:'基础模型', benchmark:'评测基准', platform:'平台'}[entity.kind] || '研究资源') : sourceType(entity);
      const content = `<rect x="${point.x - 105}" y="${point.y - 36}" width="210" height="72" rx="8"/><text class="map-node-type" x="${point.x}" y="${point.y - 19}">${escape(tag)}${selected ? ' · 当前焦点' : ''}</text><text class="map-node-title" x="${point.x}" y="${point.y + (lines.length === 1 ? 8 : 2)}">${lines.map((line, index) => `<tspan x="${point.x}" dy="${index ? 18 : 0}">${escape(line)}</tspan>`).join('')}</text>`;
      return href ? `<a class="map-node${selected ? ' focus' : ''}${isResource ? ' resource' : ''}" href="${escape(href)}"${isResource ? ' target="_blank" rel="noopener noreferrer"' : ''} aria-label="${escape(title(entity) + (isResource ? '，查看官方来源' : '，以此为焦点'))}">${content}</a>` : `<g class="map-node resource">${content}</g>`;
    }
    return `<div class="map-graph" aria-label="当前研究的一跳关联图"><svg viewBox="0 0 900 ${height}" role="img" aria-labelledby="atlas-map-graph-title"><title id="atlas-map-graph-title">${escape(title(focus))} 的来源关联图。实线箭头从使用或扩展的工作指向被使用的模型、基准或前作；虚线表示编辑对照。下方提供等价的关系文字与出处。</title><defs><marker id="atlas-map-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="#74896b"/></marker></defs>${visible.map(edge).join('')}${[focusId, ...neighborIds].map(node).join('')}</svg>${unique(relations.map(relation => relation.source === focusId ? relation.target : relation.source)).length > 6 ? '<p class="map-small-note">图中显示 6 个邻近节点；完整关系与出处见下方列表。</p>' : ''}</div>`;
  }
  function relationHtml(relation, context) {
    const source = context.get(relation.source), target = context.get(relation.target);
    const targetLink = context.papers.has(target.id) ? `<a href="${escape(paperUrl(target.id))}" data-map-paper="${escape(target.id)}">${escape(title(target))} ↗</a>` : link(target.url, title(target));
    return `<details class="map-relation${relation.editorial ? ' editorial' : ''}" data-map-evidence="${escape(relation.id)}"><summary><span class="map-relation-line" aria-hidden="true"></span><span class="map-relation-text"><strong>${escape(title(source))}</strong><span class="map-relation-verb">${escape(labels[relation.type] || relation.label || '关联')}</span><strong>${escape(title(target))}</strong></span><span class="map-relation-badge">${relation.editorial ? '编辑对照' : '原始来源'}</span><span class="map-expand" aria-hidden="true">＋</span></summary><div class="map-relation-body"><p>${escape(relation.explanation || '请查看下列原始来源。')}</p><div class="map-sources">${sourcesHtml(relation.sources)}</div><div class="map-relation-footer"><span>${relation.checkedAt ? '核对于 ' + escape(relation.checkedAt) : ''}</span>${targetLink}</div></div></details>`;
  }
  function mapHtml(context, options) {
    const route = context.routes.find(item => item.id === options.routeId) || context.routes[0];
    if (!route) return '<div class="map-empty"><h2>研究脉络正在整理</h2><p>可以先在论文合集阅读已收录的工作。</p><a href="#library">返回论文合集 ↗</a></div>';
    const papers = list(route.paperIds).map(id => context.papers.get(id)).filter(Boolean);
    const allowed = new Set(routeIds(route));
    const explicitFocus = options.focusId && context.papers.has(options.focusId) ? options.focusId : '';
    const focusId = explicitFocus || papers.find(paper => context.relations.some(relation => relation.source === paper.id || relation.target === paper.id))?.id || papers[0]?.id;
    const focus = context.get(focusId);
    const relations = context.relations.filter(relation => relation.source === focusId || relation.target === focusId);
    const backgrounds = list(route.backgroundIds).map(id => context.papers.get(id)).filter(Boolean);
    const frontier = list(route.frontierIds).map(id => context.papers.get(id)).filter(Boolean);
    const routeRelations = context.relations.filter(relation => allowed.has(relation.source) || allowed.has(relation.target));
    const teams = list(context.map.teams).filter(team => list(team.workIds).some(id => allowed.has(id)));
    const shareUrl = routeUrl(route.id, explicitFocus);
    return `<div class="map-page">
      <div class="page-kicker"><span>RESEARCH CONNECTIONS / 研究脉络</span><span>${escape(context.map.updatedAt || '')}</span></div>
      <div class="page-heading map-heading"><div><h1>沿着问题，读懂研究之间的联系。</h1><p>从近期具身 Agent 工作出发，把方法、模型与评测依据放在一起。</p></div><button class="outline-btn map-share" data-map-share="${escape(shareUrl)}">分享脉络 ↗</button></div>
      ${routeTabs(context, route.id)}
      <section class="map-route-intro" aria-labelledby="map-route-title"><div class="map-section-eyebrow">${escape(route.kicker || 'READING ROUTE')}</div><h2 id="map-route-title">${escape(route.question || route.title)}</h2><p>${escape(route.summary || '')}</p>${route.readingQuestion ? `<div class="map-reading-question"><span>带着问题读</span><p>${escape(route.readingQuestion)}</p></div>` : ''}<div class="map-route-stats"><span>${papers.length} 项重点工作</span><span>${routeRelations.filter(relation => !relation.editorial).length} 条来源关系</span><span>${routeRelations.filter(relation => relation.editorial).length} 组编辑对照</span></div></section>
      <section class="map-connections" aria-labelledby="map-connections-title"><div class="map-section-heading"><div><span class="map-section-eyebrow">CONNECTIONS / 关联与依据</span><h2 id="map-connections-title">${focus ? escape(title(focus)) : '选择一项工作'}</h2></div>${papers.length ? `<label class="map-focus-label">当前焦点<select data-map-focus data-map-route="${escape(route.id)}" aria-label="选择关系图焦点">${unique([...(focusId ? [focusId] : []), ...papers.map(paper => paper.id)]).map(id => `<option value="${escape(id)}"${id === focusId ? ' selected' : ''}>${escape(title(context.get(id)))}</option>`).join('')}</select></label>` : ''}</div><p class="map-legend"><span><i class="solid" aria-hidden="true"></i>实线：原始材料支持</span><span><i class="dashed" aria-hidden="true"></i>虚线：编辑对照</span></p><p class="map-small-note">箭头从当前使用或扩展的工作指向其模型、基准或前作；发表先后不自动构成继承关系。</p>${focus && !allowed.has(focusId) ? '<p class="map-cross-route">当前焦点来自关联工作；下方仍保留本路线的阅读清单。</p>' : ''}${graphHtml(focusId, relations, context, route.id)}<div class="map-relation-list">${relations.length ? relations.map(relation => relationHtml(relation, context)).join('') : '<p class="map-empty-inline">这项工作尚未录入有出处的关联。可先阅读研究卡，或切换焦点查看其他工作。</p>'}</div></section>
      <section class="map-reading-list" aria-labelledby="map-reading-title"><div class="map-section-heading"><div><span class="map-section-eyebrow">READING LIST / 重点阅读</span><h2 id="map-reading-title">${escape(route.title)}</h2></div>${papers.length > 1 ? `<button class="outline-btn" data-map-compare="${escape(papers.slice(0, 3).map(paper => paper.id).join('|'))}">对照前 ${Math.min(3, papers.length)} 项 ↗</button>` : ''}</div><p class="map-small-note">按研究问题组织阅读，日期保留真实首发时间；顺序不代表性能排名或技术继承。</p><div class="map-work-grid">${papers.map(paper => paperCard(paper, context, {routeId:route.id, focusId})).join('')}</div></section>
      ${backgrounds.length ? `<details class="map-background"><summary><span>追溯背景 <small>${backgrounds.length} 项早期基础工作</small></span><span aria-hidden="true">＋</span></summary><p class="map-small-note">用于理解当前工作的方法来源，保留原始发表日期。</p><div class="map-work-grid">${backgrounds.map(paper => paperCard(paper, context, {routeId:route.id, focusId})).join('')}</div></details>` : ''}
      ${frontier.length ? `<section class="map-frontier" aria-labelledby="map-frontier-title"><div class="map-section-heading"><div><span class="map-section-eyebrow">WATCHLIST / 新近发现</span><h2 id="map-frontier-title">值得继续核读</h2></div><span class="map-review-badge">候选 · 尚未精选</span></div><p class="map-small-note">这些论文已进入自动发现列表，方法与结果还需核对，暂不据此建立技术继承关系。</p><div class="map-work-grid">${frontier.map(paper => paperCard(paper, context, {frontier:true})).join('')}</div></section>` : ''}
      ${teams.length ? `<section class="map-associated-teams"><span class="map-section-eyebrow">TEAMS / 相关团队</span><div>${teams.map(team => `<a class="map-team-chip" href="${escape(teamUrl(team.id))}">${escape(team.name)} ↗</a>`).join('')}</div></section>` : ''}
    </div>`;
  }
  function teamsHtml(context, options) {
    const teams = list(context.map.teams);
    if (!teams.length) return '<div class="map-empty"><h2>团队研究线正在整理</h2><p>团队归属以作者与官方项目来源为准。</p><a href="#map">浏览研究脉络 ↗</a></div>';
    const selected = teams.find(team => team.id === options.teamId);
    const ordered = selected ? [selected, ...teams.filter(team => team.id !== selected.id)] : teams;
    return `<div class="map-page"><div class="page-kicker"><span>RESEARCH TEAMS / 团队研究线</span><span>${escape(context.map.updatedAt || '')}</span></div><div class="page-heading map-heading"><div><h1>从一项工作，找到团队的研究线。</h1><p>从已收录成果梳理方向与联系，团队归属保留官方出处。</p></div><button class="outline-btn map-share" data-map-share="${escape(selected ? teamUrl(selected.id) : '#teams')}">分享团队页 ↗</button></div><nav class="map-team-nav" aria-label="选择研究团队">${teams.map(team => `<a href="${escape(teamUrl(team.id))}"${selected?.id === team.id ? ' aria-current="page" class="active"' : ''}>${escape(team.name)}</a>`).join('')}</nav><p class="map-small-note">以下为当前合集中的代表工作；联合成果可同时出现在多个团队名下，列表不代表团队完整成果或排名。</p><div class="map-team-list">${ordered.map(team => {
      const papers = list(team.workIds).map(id => context.papers.get(id)).filter(Boolean);
      const routes = context.routes.filter(route => routeIds(route).some(id => list(team.workIds).includes(id)));
      return `<article class="map-team${selected?.id === team.id ? ' selected' : ''}" id="${escape('map-team-' + team.id)}"><div class="map-team-header"><div><span class="map-section-eyebrow">${papers.length} 项已收录代表工作</span><h2>${escape(team.name)}</h2></div><button class="map-text-button" data-map-share="${escape(teamUrl(team.id))}" aria-label="分享 ${escape(team.name)}">分享 ↗</button></div><p class="map-team-summary">${escape(team.summary || '')}</p><div class="map-sources">${sourcesHtml(team.sources)}</div><div class="map-team-works">${papers.length ? papers.map(paper => `<a class="map-team-work" href="${escape(paperUrl(paper.id))}" data-map-paper="${escape(paper.id)}"><span class="map-team-date">${recordDate(paper)}</span><span><strong>${escape(title(paper))}</strong><span>${escape(paper.summaryZh || '')}</span></span><span aria-hidden="true">↗</span></a>`).join('') : '<p class="map-small-note">代表工作正在核对。</p>'}</div>${routes.length ? `<div class="map-team-routes"><span>相关脉络</span>${routes.map(route => `<a href="${escape(routeUrl(route.id))}">${escape(route.title)} ↗</a>`).join('')}</div>` : ''}${team.checkedAt ? `<p class="map-team-checked">团队来源核对于 ${escape(team.checkedAt)}</p>` : ''}</article>`;
    }).join('')}</div></div>`;
  }
  async function share(container, hash, options) {
    const url = new URL(window.location.href); url.hash = hash;
    if (navigator.clipboard?.writeText) {
      try { await navigator.clipboard.writeText(url.href); options.toast?.('分享链接已复制'); return; } catch { /* Keep the URL available even without clipboard access. */ }
    }
    let fallback = container.querySelector('.map-share-fallback');
    if (!fallback) { fallback = document.createElement('div'); fallback.className = 'map-share-fallback'; fallback.setAttribute('role', 'status'); container.prepend(fallback); }
    fallback.innerHTML = `<label>复制此链接分享<input aria-label="可手动复制的分享链接" readonly value="${escape(url.href)}"></label><button class="map-text-button" data-map-dismiss-share>收起</button>`;
    const input = fallback.querySelector('input'); input.focus(); input.select(); options.toast?.('请复制上方链接分享');
  }
  function bind(container, options) {
    container.onclick = event => {
      const target = event.target.closest('[data-map-paper],[data-map-relation],[data-map-compare],[data-map-share],[data-map-dismiss-share]');
      if (!target || !container.contains(target)) return;
      if (target.dataset.mapPaper && options.openPaper) { event.preventDefault(); options.openPaper(target.dataset.mapPaper); }
      else if (target.dataset.mapRelation) {
        const evidence = [...container.querySelectorAll('[data-map-evidence]')].find(element => element.dataset.mapEvidence === target.dataset.mapRelation);
        if (evidence) { evidence.open = true; evidence.querySelector('summary').focus(); evidence.scrollIntoView?.({behavior:'smooth', block:'nearest'}); }
      } else if (target.dataset.mapCompare) options.comparePapers?.(target.dataset.mapCompare.split('|'));
      else if (target.dataset.mapShare) share(container, target.dataset.mapShare, options);
      else if (target.hasAttribute('data-map-dismiss-share')) target.closest('.map-share-fallback')?.remove();
    };
    container.onchange = event => { if (event.target.matches('[data-map-focus]')) window.location.hash = routeUrl(event.target.dataset.mapRoute, event.target.value); };
    container.onkeydown = event => {
      const target = event.target.closest('[data-map-relation]');
      if (target && ['Enter', ' '].includes(event.key)) { event.preventDefault(); target.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
    };
  }
  function render(data, options = {}) {
    const view = options.view === 'teams' ? 'teams' : 'map';
    const container = document.getElementById(view + '-view');
    if (!container) return;
    const context = getContext(data || {});
    container.innerHTML = view === 'teams' ? teamsHtml(context, options) : mapHtml(context, options);
    bind(container, options);
  }
  function relatedHtml(paperId, data) {
    const context = getContext(data || {});
    const direct = context.routes.filter(route => routeIds(route).includes(paperId));
    const neighbors = new Set(context.relations.filter(relation => relation.source === paperId || relation.target === paperId).flatMap(relation => [relation.source, relation.target]));
    const routes = direct.length ? direct : context.routes.filter(route => routeIds(route).some(id => neighbors.has(id)));
    if (!routes.length) return '';
    return `<section class="map-detail-related" aria-label="相关研究脉络"><h3>放进研究脉络读</h3><p>查看关联工作、使用的模型与评测来源。</p><div>${routes.map(route => `<a href="${escape(routeUrl(route.id, paperId))}">${escape(route.title)} <span aria-hidden="true">↗</span></a>`).join('')}</div></section>`;
  }
  window.AtlasMap = {render, relatedHtml};
})();

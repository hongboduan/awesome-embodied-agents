const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const repo = path.resolve(__dirname, '..');

function environment() {
  const nodes = new Map(), handlers = {}, copied = [];
  function node(key) {
    if (!nodes.has(key)) nodes.set(key, {
      id: key.replace(/^#/, ''), innerHTML: '', textContent: '', value: '', hidden: false,
      open: false, dataset: {}, events: {}, classList: {toggle() {}, add() {}, remove() {}},
      addEventListener(type, listener) { this.events[type] = listener; },
      setAttribute() {}, getAttribute() { return null; }, focus() {}, contains() { return true; },
      querySelectorAll() { return []; }, querySelector() { return null; },
      showModal() { this.open = true; }, close() { this.open = false; this.events.close?.(); }
    });
    return nodes.get(key);
  }
  const common = {title: 'Research', shortTitle: 'Work', summaryZh: 'Evidence', date: '2026-10-14',
    categories: ['code'], curated: true, review: 'source-checked', links: {paper: 'https://example.org/paper'}};
  const data = {papers: [{...common, id: 'a'}, {...common, id: 'b'},
    {...common, id: 'candidate', curated: false, review: 'candidate'}],
    site: {focusSince: '2026-09-01'}, events: [], researchMap: {version: 1, updatedAt: '2026-10-16',
      routes: [{id: 'code-policy', title: 'Code route', summary: 'Read', question: 'When?',
        paperIds: ['a', 'b'], backgroundIds: [], frontierIds: ['candidate']}],
      resources: [{id: 'resource-model', kind: 'model', name: 'Model', url: 'https://example.org/model'}],
      relations: [{id: 'uses-model', source: 'a', target: 'resource-model', type: 'uses_model',
        editorial: false, label: 'Uses', explanation: 'Original evidence', sources: [{label: 'Source', url: 'https://example.org/source'}]},
        {id: 'compares', source: 'a', target: 'b', type: 'comparison', editorial: true,
          label: 'Comparison', explanation: 'Editorial comparison', sources: [{label: 'Both', url: 'https://example.org/both'}]}],
      teams: [{id: 'team', name: 'Team', summary: 'Work line', workIds: ['a'], sources: []}]}};
  const sandbox = {console, URL, URLSearchParams, Blob, Date, setTimeout: () => 0, clearTimeout() {},
    location: {hash: '', href: 'https://example.org/atlas/', hostname: 'example.org'},
    history: {replaceState() {}}, localStorage: {getItem: () => null, setItem() {}},
    navigator: {clipboard: {writeText: async value => copied.push(value)}},
    document: {querySelector: node, querySelectorAll: selector => selector === 'dialog'
      ? ['detail', 'studio', 'compare', 'info'].map(id => node('#' + id + '-dialog')) : [],
      getElementById: id => node('#' + id), addEventListener: (type, listener) => {handlers[type] = listener;},
      activeElement: {tagName: 'BODY'}}, ATLAS_DATA: data, addEventListener() {}, innerWidth: 1280};
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  for (const file of ['updates.js', 'map.js', 'app.js']) {
    let source = fs.readFileSync(path.join(repo, 'web', file), 'utf8');
    if (file === 'app.js') source = source.replace(/\}\)\(\);\s*$/, 'window.qa={route,state,openPaper,shareLibrary};})();');
    vm.runInContext(source, sandbox, {filename: file});
  }
  const navigate = hash => {sandbox.location.hash = hash; sandbox.qa.route();};
  const click = (href, dataset = {}) => {
    const target = {dataset, getAttribute: key => key === 'href' ? href : null, closest() { return this; }};
    const event = {target, defaultPrevented: false, preventDefault() {this.defaultPrevented = true;}};
    handlers.click(event);
    return event;
  };
  return {sandbox, data, node, navigate, click, copied, handlers};
}

test('map routes distinguish sourced edges, comparisons and unreviewed frontier', () => {
  const e = environment();
  e.navigate('#map?route=code-policy&focus=a');
  assert.equal(e.node('#map-view').hidden, false);
  assert.equal(e.node('#library-view').hidden, true);
  const html = e.node('#map-view').innerHTML;
  assert.match(html, /marker-end="url\(#atlas-map-arrow\)"/);
  assert.match(html, /map-edge editorial/);
  assert.match(html, /Original evidence/);
  assert.match(html, /候选 · 尚未精选/);
  assert.match(html, /https:\/\/example.org\/source/);
  assert.equal((html.match(/data-map-relation=/g) || []).length, 2);
});

test('opening a paper from updates keeps the update view on closing', () => {
  const e = environment();
  e.navigate('#updates?range=all');
  assert.equal(e.click('#paper=a').defaultPrevented, true);
  assert.equal(e.node('#detail-dialog').open, true);
  e.node('#detail-dialog').close();
  assert.equal(e.sandbox.location.hash, '#updates?range=all');
  assert.equal(e.sandbox.qa.state.view, 'updates');
});

test('same-route link in a detail dialog returns to the map', () => {
  const e = environment();
  const hash = '#map?route=code-policy&focus=a';
  e.navigate(hash); e.sandbox.qa.openPaper('a');
  assert.equal(e.node('#detail-dialog').open, true);
  e.click(hash);
  assert.equal(e.node('#detail-dialog').open, false);
  assert.equal(e.sandbox.qa.state.view, 'map');
});

test('shared collection links reset stale filters and preserve search, scope and sorting', async () => {
  const e = environment();
  e.sandbox.qa.state.query = 'stale query';
  e.navigate('#library?filter=candidate');
  assert.equal(e.sandbox.qa.state.query, '');
  assert.equal(e.sandbox.qa.state.filter, 'candidate');
  e.navigate('#library?filter=all&scope=all&category=code&sort=oldest&q=robot');
  await e.sandbox.qa.shareLibrary();
  const params = new URLSearchParams(e.copied[0].split('?')[1]);
  for (const [key, value] of Object.entries({filter: 'all', scope: 'all', category: 'code', sort: 'oldest', q: 'robot'})) {
    assert.equal(params.get(key), value);
  }
  e.sandbox.qa.state.savedOnly = true;
  await e.sandbox.qa.shareLibrary();
  assert.equal(e.copied.length, 1, 'local-only favorites must not be advertised as a shared collection');
});

test('missing map IDs fall back safely, and untrusted text cannot create links or markup', () => {
  const e = environment();
  e.data.researchMap.routes[0].title = '<img src=x onerror=alert(1)>';
  e.data.researchMap.relations[0].sources[0].url = 'javascript:alert(1)';
  e.navigate('#map?route=missing&focus=missing');
  const html = e.node('#map-view').innerHTML;
  assert.match(html, /&lt;img/);
  assert.doesNotMatch(html, /<img src=x|href="javascript:/);
  e.navigate('#teams?team=team');
  assert.match(e.node('#teams-view').innerHTML, /map-team selected/);
  assert.match(e.node('#teams-view').innerHTML, /#map\?route=code-policy/);
});

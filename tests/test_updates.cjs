'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { summary, renderHome, renderPage } = require('../web/updates.js');
const now = new Date('2026-10-16T08:45:00Z');
const event = (paperId, date, extra = {}) => ({ paperId, date, type: 'discovered', title: paperId, ...extra });

test('seven Beijing calendar days include their first midnight and exclude old or future records', () => {
  const s = summary({events: [event('before', '2026-10-09T15:59:59Z'), event('first', '2026-10-09T16:00:00Z'), event('today', '2026-10-16'), event('future', '2026-10-16T09:00:00Z'), event('invalid', '2026-10-35'), event('missing', undefined)]}, now);
  assert.equal(s.startDay, '2026-10-10');
  assert.equal(s.endDay, '2026-10-16');
  assert.equal(s.counts.discovered, 2);
  assert.deepEqual(s.recentEvents.map(e => e.paperId), ['first', 'today']);
  assert.equal(s.timeline.length, 3);
});

test('discovery duplicates never become fresh again; version pairs are deduplicated', () => {
  const s = summary({events: [event('a', '2026-10-01'), event('a', '2026-10-16'), event('b', '2026-10-15'), event('b', '2026-10-16'), event('c', '2026-10-15', {type: 'version', fromVersion: 1, toVersion: 2}), event('c', '2026-10-16', {type: 'version', fromVersion: 1, toVersion: 2}), event('c', '2026-10-16', {type: 'version', fromVersion: 2, toVersion: 3})]}, now);
  assert.deepEqual(s.counts, {discovered: 1, versions: 2, curated: 0});
  assert.equal(s.timeline.length, 4);
});

test('featured collection counts require a real addedAt and do not use publication or build dates', () => {
  const s = summary({updatedAt: now.toISOString(), papers: [
    {id: 'a', curated: true, addedAt: '2026-10-10', date: '2023-01-01'},
    {id: 'b', curated: true, date: '2026-10-16'},
    {id: 'c', curated: false, addedAt: '2026-10-16'},
    {id: 'd', curated: true, addedAt: '2026-10-17'},
    {id: 'e', curated: true, addedAt: '2026-02-30'}
  ]}, now);
  assert.equal(s.counts.curated, 1);
  assert.equal(s.status.state, 'waiting');
});

test('fresh build cannot hide stale or failed scans', () => {
  let s = summary({updatedAt: now.toISOString(), updateStatus: {mode: 'active', lastSuccess: '2026-10-14T08:44:59Z'}}, now);
  assert.equal(s.status.state, 'stale');
  s = summary({updateStatus: {mode: 'error', lastSuccess: '2026-10-15T04:00:00Z', lastAttempt: '2026-10-16T04:00:00Z'}}, now);
  assert.equal(s.status.state, 'error');
  assert.equal(s.status.lastSuccess, Date.parse('2026-10-15T04:00:00Z'));
  assert.equal(s.status.lastAttempt, Date.parse('2026-10-16T04:00:00Z'));
  s = summary({updateStatus: {mode: 'active', lastSuccess: '2026-10-14T08:45:00Z'}}, now);
  assert.equal(s.status.state, 'active');
});

test('empty and null data are safe and show no invented updates', () => {
  for (const data of [undefined, null, {}, {papers: null, events: null}]) {
    const s = summary(data, now);
    assert.deepEqual(s.counts, {discovered: 0, versions: 0, curated: 0});
    assert.equal(s.timeline.length, 0);
    assert.equal(s.status.state, 'waiting');
  }
});

test('UI escapes content, suppresses unsafe URLs, and keeps audit language distinct', () => {
  const home = {innerHTML: ''}, page = {innerHTML: ''};
  global.document = {getElementById: id => id === 'recent-updates' ? home : id === 'updates-view' ? page : null};
  const data = {papers: [{id: 'good', curated: true, addedAt: '2026-10-14', review: 'source-checked'}], events: [event('bad', '2026-10-16', {title: '<img src=x onerror=alert(1)>', url: 'javascript:alert(1)'})], enrichmentStatus: {llmMode: 'not-configured'}};
  renderHome(data, {now});
  renderPage(data, {range: 'all', now});
  assert.ok(home.innerHTML.includes('近期收录精选'));
  assert.ok(page.innerHTML.includes('此日期不表示审核完成时间'));
  assert.ok(page.innerHTML.includes('自动精读未启用'));
  assert.ok(page.innerHTML.includes('&lt;img'));
  assert.ok(!page.innerHTML.includes('href="javascript:'));
  assert.ok(!page.innerHTML.includes('<img'));
  assert.ok(page.innerHTML.includes('全部记录</a>'));
  delete global.document;
});

test('version events distinguish metadata, AI drafts, source checks, and full reviews', () => {
  const page = {innerHTML: ''};
  global.document = {getElementById: id => id === 'updates-view' ? page : null};
  const description = (paper, toVersion = 3) => {
    renderPage({papers: [{id: 'p', title: 'Paper', ...paper}], events: [event('p', '2026-10-16', {type: 'version', fromVersion: toVersion - 1, toVersion})]}, {now});
    return page.innerHTML.match(/<article class="au-record">[\s\S]*?<p>([\s\S]*?)<\/p>/)[1];
  };
  try {
    const candidate = description({review: 'candidate', reviewedVersion: 2, latestVersion: 3});
    assert.match(candidate, /自动发现候选/);
    assert.doesNotMatch(candidate, /当前精读|当前来源核对/);
    const draft = description({review: 'ai-draft', reviewedVersion: 3, latestVersion: 3});
    assert.match(draft, /AI 草稿对应 v3，尚待人工复核/);
    assert.doesNotMatch(draft, /当前精读|当前来源核对/);
    const checked = description({review: 'source-checked', reviewedVersion: 2, latestVersion: 3});
    assert.match(checked, /当前来源核对对应 v2/);
    assert.match(checked, /本次记录的 v3 尚待复核/);
    assert.doesNotMatch(checked, /当前精读/);
    const read = description({review: 'full-review', deepRead: true, reviewedVersion: 3, latestVersion: 3});
    assert.match(read, /当前精读对应 v3/);
    assert.doesNotMatch(read, /尚待复核/);
    const historical = description({review: 'source-checked', reviewedVersion: 3, latestVersion: 5}, 2);
    assert.match(historical, /历史版本记录/);
    assert.match(historical, /最新原文为 v5，尚待复核/);
    assert.doesNotMatch(historical, /本次记录的 v2 尚待复核/);
  } finally { delete global.document; }
});

const assert=require('node:assert/strict');
const {matches,aggregate,demo}=require('../dist/replay-core.js');
const t=s=>Date.parse(s)/1000;
const window={enabled:true,start:'09:50',end:'10:10',days:[1,2,3,4,5]};
assert(matches(t('2026-10-23T13:50:00Z'),window,'America/New_York'));
assert(!matches(t('2026-10-23T14:10:00Z'),window,'America/New_York'));
assert(!matches(t('2026-10-24T13:55:00Z'),window,'America/New_York'));
assert(matches(t('2026-11-02T14:55:00Z'),window,'America/New_York')); // EST
assert(!matches(t('2026-11-02T13:55:00Z'),window,'America/New_York'));
const overnight={enabled:true,start:'23:00',end:'02:00',days:[5]};
assert(matches(t('2026-10-24T05:00:00Z'),overnight,'America/New_York')); // Saturday 01:00 belongs to Friday
assert(!matches(t('2026-10-24T06:00:00Z'),overnight,'America/New_York'));
assert(!matches(t('2026-10-25T05:00:00Z'),overnight,'America/New_York'));
assert(!matches(t('2026-10-23T13:55:00Z'),{...window,enabled:false},'America/New_York'));
assert(!matches(t('2026-10-23T13:55:00Z'),{...window,start:'09:50',end:'09:50'},'America/New_York'));
const bars=demo(),snapshot=JSON.stringify(bars);assert.deepEqual(bars,demo());
const aggregated=aggregate(bars.slice(0,7),5);
assert.equal(aggregated.length,2);assert.equal(aggregated[1].close,bars[6].close);
assert.equal(aggregated[1].high,Math.max(bars[5].high,bars[6].high));
assert.equal(aggregated[0].open,bars[0].open);assert.equal(aggregated[0].close,bars[4].close);
assert.equal(JSON.stringify(bars),snapshot);
console.log('Replay: DST, boundaries, overnight weekdays and aggregation without lookahead passed.');

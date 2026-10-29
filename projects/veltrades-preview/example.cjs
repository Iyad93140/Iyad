const { demo, aggregate, matches } = require('./dist/replay-core.js');

// Données déterministes et entièrement synthétiques : aucune cotation réelle.
const revealed = demo().slice(0, 7);
const fiveMinuteBars = aggregate(revealed, 5);
console.log('7 bougies source révélées, regroupées en 5 minutes :');
console.table(fiveMinuteBars);

const window = { enabled: true, start: '09:50', end: '10:10', days: [1, 2, 3, 4, 5] };
const timestamp = Date.parse('2026-10-23T13:55:00Z') / 1000;
console.log('Dans le créneau 09:50-10:10 à New York :', matches(timestamp, window, 'America/New_York'));

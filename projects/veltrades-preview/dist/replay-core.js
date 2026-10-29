/* Pure replay/time-window helpers. UTC instants stay unchanged; only labels use the chosen zone. */
(function(root){
 const formatters=new Map();
 function localParts(time,zone){if(!formatters.has(zone))formatters.set(zone,new Intl.DateTimeFormat('en-US',{timeZone:zone,weekday:'short',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}));const p=Object.fromEntries(formatters.get(zone).formatToParts(new Date(time*1000)).map(v=>[v.type,v.value]));return {day:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(p.weekday),minute:+p.hour*60+(+p.minute)};}
 function minute(value){const [h,m]=value.split(':').map(Number);return h*60+m;}
 function matches(time,w,zone){if(!w.enabled)return false;const p=localParts(time,zone),s=minute(w.start),e=minute(w.end);if(s===e)return false;const overnight=s>e,day=overnight&&p.minute<e?(p.day+6)%7:p.day;return w.days.includes(day)&&(overnight?p.minute>=s||p.minute<e:p.minute>=s&&p.minute<e);}
 function aggregate(bars,tf){const out=[];for(const b of bars){const time=Math.floor(b.time/(tf*60))*tf*60,last=out.at(-1);if(last&&last.time===time){last.high=Math.max(last.high,b.high);last.low=Math.min(last.low,b.low);last.close=b.close;}else out.push({time,open:b.open,high:b.high,low:b.low,close:b.close});}return out;}
 function demo(){let seed=391,p=21520;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};return Array.from({length:600},(_,i)=>{const o=p,d=(rand()-.48)*11+Math.sin(i/31)*1.5;p=Math.round((o+d)*4)/4;return {time:Date.parse('2026-10-23T11:00:00Z')/1000+i*60,open:o,high:Math.round((Math.max(o,p)+rand()*5)*4)/4,low:Math.round((Math.min(o,p)-rand()*5)*4)/4,close:p};});}
 const api={localParts,minute,matches,aggregate,demo};root.ReplayCore=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);

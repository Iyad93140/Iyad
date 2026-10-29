import test from 'node:test';
import assert from 'node:assert/strict';
import {cleanTask, restoreTasks, transition, selectTasks} from './core.mjs';
const task={id:'abc',title:'Préparer entretien',status:'À faire'};
test('cycle des statuts et absence de mutation',()=>{
  let current=[task];
  for(const expected of ['En cours','Terminé','À faire']){
    current=transition(current,'abc');assert.equal(current[0].status,expected);
  }
  assert.equal(task.status,'À faire');
});
test('recherche insensible à la casse',()=>assert.equal(selectTasks([task],'ENTRETIEN').length,1));
test('restauration validée et refus des doublons',()=>{
  assert.deepEqual(restoreTasks(JSON.stringify([task])),[task]);
  for(const bad of ['{}','invalid',JSON.stringify([task,task]),JSON.stringify([{...task,status:'inconnu'}])])assert.throws(()=>restoreTasks(bad));
});
test('titre valide et contenu traité comme texte',()=>{
  assert.throws(()=>cleanTask({...task,title:'   '}));
  assert.throws(()=>cleanTask({...task,title:'a'.repeat(121)}));
  assert.equal(cleanTask({...task,title:'<script>alert(1)</script>'}).title,'<script>alert(1)</script>');
});

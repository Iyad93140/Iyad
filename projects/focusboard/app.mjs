import {STATES, cleanTask, restoreTasks, transition, selectTasks} from './core.mjs';
const key = 'focusboard.v1';
const board = document.querySelector('#board');
const message = document.querySelector('#message');
const search = document.querySelector('#search');
let tasks = [];
let storageBroken = false;
try { tasks = restoreTasks(localStorage.getItem(key)); }
catch { storageBroken = true; message.textContent = 'Sauvegarde inaccessible ou invalide. Le tableau reste utilisable, sans écraser cette sauvegarde.'; }
function commit(next) {
  try {
    if (!storageBroken) localStorage.setItem(key, JSON.stringify(next));
    tasks = next;
    if (!storageBroken) message.textContent = '';
    render();
  } catch { message.textContent = 'Enregistrement impossible. La modification n’a pas été appliquée.'; }
}
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function render() {
  board.replaceChildren();
  const visible = selectTasks(tasks, search.value);
  document.querySelector('#count').textContent = `${tasks.filter(t => t.status === 'Terminé').length} / ${tasks.length} terminées`;
  for (const status of STATES) {
    const column = element('section', undefined, 'column');
    const list = visible.filter(t => t.status === status);
    column.append(element('h2', `${status} · ${list.length}`));
    if (!list.length) column.append(element('p', 'Aucune tâche', 'empty'));
    for (const task of list) {
      const card = element('article', undefined, 'card');
      const actions = element('div', undefined, 'actions');
      const move = element('button', status === 'Terminé' ? 'Recommencer' : 'Étape suivante');
      move.setAttribute('aria-label', `Changer le statut de ${task.title}`);
      move.onclick = () => commit(transition(tasks, task.id));
      const remove = element('button', 'Supprimer', 'delete');
      remove.setAttribute('aria-label', `Supprimer ${task.title}`);
      remove.onclick = () => commit(tasks.filter(t => t.id !== task.id));
      actions.append(move, remove);card.append(element('p', task.title), actions);column.append(card);
    }
    board.append(column);
  }
}
document.querySelector('#add-form').onsubmit = event => {
  event.preventDefault();
  const input = document.querySelector('#title');
  try {
    if (tasks.length >= 1000) throw new Error('Limite de 1000 tâches atteinte.');
    const task = cleanTask({id: crypto.randomUUID(), title: input.value, status: STATES[0]});
    const before = tasks;
    commit([...tasks, task]);
    if (tasks !== before) input.value = '';
    input.focus();
  } catch (error) { message.textContent = error.message; }
};
search.oninput = render;
render();

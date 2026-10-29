export const STATES = ['À faire', 'En cours', 'Terminé'];
export function cleanTask(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('Tâche invalide.');
  const title = typeof input.title === 'string' ? input.title.trim() : '';
  if (!title || title.length > 120) throw new Error('Titre requis, limité à 120 caractères.');
  if (typeof input.id !== 'string' || !input.id || input.id.length > 100) throw new Error('Identifiant invalide.');
  if (!STATES.includes(input.status)) throw new Error('Statut invalide.');
  return {id: input.id, title, status: input.status};
}
export function restoreTasks(raw) {
  if (raw === null) return [];
  const data = JSON.parse(raw);
  if (!Array.isArray(data) || data.length > 1000) throw new Error('Sauvegarde invalide.');
  const tasks = data.map(cleanTask);
  if (new Set(tasks.map(t => t.id)).size !== tasks.length) throw new Error('Identifiants en double.');
  return tasks;
}
export function transition(tasks, id) {
  return tasks.map(t => t.id === id ? {...t, status: STATES[(STATES.indexOf(t.status) + 1) % STATES.length]} : t);
}
export function selectTasks(tasks, query) {
  const q = query.trim().toLocaleLowerCase('fr');
  return tasks.filter(t => t.title.toLocaleLowerCase('fr').includes(q));
}

const projectList = document.querySelector('#project-list');
const message = document.querySelector('#message');
const projectCount = document.querySelector('#project-count');
const countLabel = document.querySelector('#count-label');
const connectionState = document.querySelector('#connection-state');
const statusText = document.querySelector('#status-text');

function setStatus(state, text) {
  connectionState.classList.toggle('is-connected', state === 'connected');
  connectionState.classList.toggle('is-error', state === 'error');
  statusText.textContent = text;
}

function showMessage(text, isError = false) {
  message.textContent = text;
  message.classList.add('is-visible');
  message.classList.toggle('is-error', isError);
}

async function refreshProjects() {
  try {
    const response = await fetch('/api/projects', { cache: 'no-store' });
    if (!response.ok) throw new Error('Project list request failed');
    const projects = await response.json();
    const fragment = document.createDocumentFragment();

    projects.forEach((project, index) => {
      const link = document.createElement('a');
      link.className = 'project-link';
      link.href = project.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.style.animationDelay = `${Math.min(index * 35, 280)}ms`;

      const name = document.createElement('span');
      name.className = 'project-name';
      name.textContent = project.name;

      const arrow = document.createElement('span');
      arrow.className = 'project-arrow';
      arrow.setAttribute('aria-hidden', 'true');
      arrow.textContent = '\u2197';

      link.append(name, arrow);
      fragment.append(link);
    });

    projectList.replaceChildren(fragment);
    projectList.setAttribute('aria-busy', 'false');
    projectCount.textContent = String(projects.length);
    countLabel.textContent = projects.length === 1 ? 'project' : 'projects';
    message.classList.remove('is-visible', 'is-error');
    if (projects.length === 0) showMessage('No projects yet. Add a project and URL to the dashboard table.');
    setStatus('connected', 'Live');
  } catch {
    projectList.setAttribute('aria-busy', 'false');
    showMessage('Unable to load projects. Check the database connection and try again.', true);
    setStatus('error', 'Unavailable');
  }
}

refreshProjects();
window.setInterval(refreshProjects, 15000);
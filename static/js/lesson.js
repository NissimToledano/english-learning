// Highlight vocabulary words in reading text
document.addEventListener('DOMContentLoaded', () => {
  highlightVocab();
});

function highlightVocab() {
  const textEl = document.getElementById('reading-text');
  if (!textEl || !VOCAB_WORDS) return;

  let html = textEl.innerHTML;

  // Sort by length desc to avoid partial replacements
  const sorted = [...VOCAB_WORDS].sort((a, b) => b.english.length - a.english.length);

  sorted.forEach(word => {
    const regex = new RegExp(`\\b(${escapeRegex(word.english)})\\b`, 'gi');
    html = html.replace(regex, (match) => {
      return `<span class="vocab-word" data-hebrew="${word.hebrew}" onclick="showWordTooltip(this)">${match}<span class="word-tooltip" style="display:none">${word.hebrew}</span></span>`;
    });
  });

  textEl.innerHTML = html;
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function showWordTooltip(el) {
  const tip = el.querySelector('.word-tooltip');
  if (!tip) return;
  // Toggle tooltip
  const isVisible = tip.style.display !== 'none';
  // Hide all tooltips first
  document.querySelectorAll('.word-tooltip').forEach(t => t.style.display = 'none');
  if (!isVisible) {
    tip.style.display = 'block';
  }
}

// Word card flip
function flipCard(card) {
  card.classList.toggle('flipped');
  const hebrew = card.querySelector('.word-hebrew');
  const example = card.querySelector('.word-example');
  const hint = card.querySelector('.word-hint');

  if (card.classList.contains('flipped')) {
    if (hebrew) hebrew.classList.remove('hidden');
    if (example) example.classList.remove('hidden');
    if (hint) hint.textContent = '👆 לחץ להסתרה';
  } else {
    if (hebrew) hebrew.classList.add('hidden');
    if (example) example.classList.add('hidden');
    if (hint) hint.textContent = '👆 לחץ לתרגום';
  }
}

// Toggle all cards
let allFlipped = false;
function toggleAllCards() {
  allFlipped = !allFlipped;
  document.querySelectorAll('.word-card').forEach(card => {
    const hebrew = card.querySelector('.word-hebrew');
    const example = card.querySelector('.word-example');
    const hint = card.querySelector('.word-hint');

    if (allFlipped) {
      card.classList.add('flipped');
      if (hebrew) hebrew.classList.remove('hidden');
      if (example) example.classList.remove('hidden');
      if (hint) hint.textContent = '👆 לחץ להסתרה';
    } else {
      card.classList.remove('flipped');
      if (hebrew) hebrew.classList.add('hidden');
      if (example) example.classList.add('hidden');
      if (hint) hint.textContent = '👆 לחץ לתרגום';
    }
  });
}

// Mark reading done
async function markReadingDone(lessonId) {
  await fetch(`/lessons/${lessonId}/mark-reading`, { method: 'POST' });
  // Switch to words tab
  showTab('words', document.querySelectorAll('.tab-btn')[1]);
  // Update step indicator
  const step = document.getElementById('step-read');
  if (step) {
    step.classList.add('done');
    step.querySelector('.step-num').textContent = '✓';
  }
  const stepWords = document.getElementById('step-words');
  if (stepWords) stepWords.classList.add('active');
}

// Mark words studied
async function markWordsDone(lessonId) {
  const res = await fetch(`/lessons/${lessonId}/mark-words`, { method: 'POST' });
  if (res.ok) {
    window.location.href = `/lessons/${lessonId}/quiz`;
  }
}

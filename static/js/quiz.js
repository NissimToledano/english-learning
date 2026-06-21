// ─── Quiz State ─────────────────────────────────────────────────────────────
let currentStage = ALREADY_DONE_S1 ? 2 : 1;
let stage1Answers = [];
let stage2Answers = [];
let currentIndex = 0;
let shuffledWords = [];
let allOptions = [];

// ─── Init ────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  if (ALREADY_DONE_S2) return; // Already fully completed

  shuffledWords = shuffle([...WORDS]);
  // Build option pool (all Hebrew translations)
  allOptions = WORDS.map(w => w.hebrew);

  if (!ALREADY_DONE_S1) {
    buildStage1();
  } else {
    buildStage2();
  }
});

// ─── Stage 1: Multiple-choice translation ───────────────────────────────────
function buildStage1() {
  const container = document.getElementById('quiz-cards-stage1');
  container.innerHTML = '';
  currentIndex = 0;
  stage1Answers = [];
  renderStage1Card();
}

function renderStage1Card() {
  const container = document.getElementById('quiz-cards-stage1');
  const word = shuffledWords[currentIndex];

  // Build wrong options (3 random different ones)
  const wrong = shuffle(allOptions.filter(o => o !== word.hebrew)).slice(0, 3);
  const options = shuffle([word.hebrew, ...wrong]);

  container.innerHTML = `
    <div class="quiz-card" id="current-card">
      <div class="quiz-progress">
        <div class="progress-bar-wrap" style="flex:1">
          <div class="progress-bar-fill blue" style="width:${((currentIndex) / shuffledWords.length * 100)}%"></div>
        </div>
        <span class="quiz-progress-text">${currentIndex + 1} / ${shuffledWords.length}</span>
      </div>
      <div class="quiz-question">מה התרגום של המילה?</div>
      <div class="quiz-word">${word.english}</div>
      <div class="quiz-options" id="options-container">
        ${options.map(opt => `
          <button class="quiz-option" onclick="answerStage1('${opt.replace(/'/g, "\\'")}', '${word.hebrew.replace(/'/g, "\\'")}', this)">
            ${opt}
          </button>
        `).join('')}
      </div>
      <div id="feedback" class="quiz-feedback" style="display:none"></div>
      <button id="next-btn" class="btn btn-primary mt-2" onclick="nextStage1()" style="display:none">
        ${currentIndex + 1 < shuffledWords.length ? 'הבא ➜' : 'סיים שלב 1 ✓'}
      </button>
    </div>
  `;
}

function answerStage1(chosen, correct, btn) {
  // Disable all options
  document.querySelectorAll('.quiz-option').forEach(b => b.disabled = true);

  const isCorrect = chosen === correct;
  stage1Answers.push({
    word_id: shuffledWords[currentIndex].id,
    answer: chosen,
    is_correct: isCorrect,
  });

  btn.classList.add(isCorrect ? 'correct' : 'incorrect');
  if (!isCorrect) {
    // Highlight correct
    document.querySelectorAll('.quiz-option').forEach(b => {
      if (b.textContent.trim() === correct) b.classList.add('correct');
    });
  }

  const feedback = document.getElementById('feedback');
  feedback.style.display = 'block';
  feedback.className = `quiz-feedback ${isCorrect ? 'correct' : 'incorrect'}`;
  feedback.textContent = isCorrect ? '✓ נכון! כל הכבוד!' : `✗ לא נכון. התרגום הנכון: ${correct}`;

  document.getElementById('next-btn').style.display = 'inline-flex';
}

function nextStage1() {
  currentIndex++;
  if (currentIndex < shuffledWords.length) {
    renderStage1Card();
  } else {
    submitStage1();
  }
}

async function submitStage1() {
  const container = document.getElementById('quiz-cards-stage1');
  container.innerHTML = '<div class="text-center" style="padding:2rem">⏳ שומר תוצאות...</div>';

  const correct = stage1Answers.filter(a => a.is_correct).length;
  const score = Math.round((correct / stage1Answers.length) * 100);

  await fetch('/api/quiz/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      lesson_id: LESSON_ID,
      stage: 1,
      answers: stage1Answers,
    })
  });

  container.innerHTML = '';
  const result = document.getElementById('stage1-result');
  result.classList.remove('hidden');
  document.getElementById('stage1-score-text').textContent = score + '%';
  document.getElementById('stage1-detail').textContent = `ענית נכון על ${correct} מתוך ${stage1Answers.length} מילים`;

  // Update step indicator
  const stepEl = document.getElementById('stage-step-1');
  if (stepEl) {
    stepEl.classList.add('done');
    stepEl.querySelector('.step-num').textContent = '✓';
  }
}

// ─── Stage 2: Write a sentence ───────────────────────────────────────────────
function startStage2() {
  document.getElementById('stage-1').classList.add('hidden');
  document.getElementById('stage-2').classList.remove('hidden');
  buildStage2();

  const stepEl = document.getElementById('stage-step-2');
  if (stepEl) stepEl.classList.add('active');
}

function buildStage2() {
  currentIndex = 0;
  stage2Answers = [];
  renderStage2Card();
}

function renderStage2Card() {
  const container = document.getElementById('quiz-cards-stage2');
  const word = shuffledWords[currentIndex];

  container.innerHTML = `
    <div class="quiz-card">
      <div class="quiz-progress">
        <div class="progress-bar-wrap" style="flex:1">
          <div class="progress-bar-fill green" style="width:${(currentIndex / shuffledWords.length * 100)}%"></div>
        </div>
        <span class="quiz-progress-text">${currentIndex + 1} / ${shuffledWords.length}</span>
      </div>
      <div class="quiz-question">כתוב משפט באנגלית עם המילה:</div>
      <div class="quiz-word">${word.english}</div>
      <div style="font-size:0.85rem;color:#64748b;margin-bottom:1rem">(${word.hebrew})</div>
      ${word.example ? `<div style="font-size:0.8rem;color:#94a3b8;margin-bottom:1rem;font-style:italic">דוגמה: ${word.example}</div>` : ''}
      <div style="width:100%;max-width:500px;margin:0 auto">
        <textarea id="sentence-input" class="quiz-input" placeholder="Write your sentence here..." rows="3"
          style="text-align:left;resize:none;direction:ltr"></textarea>
      </div>
      <div id="feedback2" class="quiz-feedback" style="display:none"></div>
      <div style="display:flex;gap:1rem;justify-content:center;margin-top:1rem">
        <button class="btn btn-primary" onclick="checkStage2('${word.english.replace(/'/g, "\\'")}', ${word.id})">
          בדוק ✓
        </button>
        <button class="btn btn-outline" onclick="skipWord(${word.id})">דלג</button>
      </div>
      <button id="next-btn2" class="btn btn-success mt-2" onclick="nextStage2()" style="display:none">
        ${currentIndex + 1 < shuffledWords.length ? 'הבא ➜' : 'סיים מבחן 🎉'}
      </button>
    </div>
  `;

  document.getElementById('sentence-input').focus();

  // Allow Enter key to submit (Shift+Enter for newline)
  document.getElementById('sentence-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      checkStage2(word.english, word.id);
    }
  });
}

function checkStage2(wordEnglish, wordId) {
  const input = document.getElementById('sentence-input');
  const sentence = input.value.trim();

  if (!sentence) {
    alert('אנא כתוב משפט לפני הבדיקה');
    return;
  }

  // Disable inputs
  input.disabled = true;
  document.querySelectorAll('#quiz-cards-stage2 button').forEach(b => {
    if (b.id !== 'next-btn2') b.disabled = true;
  });

  const isCorrect = sentence.toLowerCase().includes(wordEnglish.toLowerCase()) && sentence.trim().split(' ').length >= 3;

  stage2Answers.push({
    word_id: wordId,
    answer: sentence,
    is_correct: isCorrect,
  });

  input.classList.add(isCorrect ? 'correct' : 'incorrect');
  const feedback = document.getElementById('feedback2');
  feedback.style.display = 'block';
  feedback.className = `quiz-feedback ${isCorrect ? 'correct' : 'incorrect'}`;

  if (isCorrect) {
    feedback.textContent = '✓ כל הכבוד! משפט נכון!';
  } else if (!sentence.toLowerCase().includes(wordEnglish.toLowerCase())) {
    feedback.textContent = `✗ המשפט חייב להכיל את המילה "${wordEnglish}"`;
  } else {
    feedback.textContent = '✗ נסה לכתוב משפט ארוך יותר (לפחות 3 מילים)';
  }

  document.getElementById('next-btn2').style.display = 'inline-flex';
}

function skipWord(wordId) {
  stage2Answers.push({ word_id: wordId, answer: '', is_correct: false });
  nextStage2();
}

function nextStage2() {
  currentIndex++;
  if (currentIndex < shuffledWords.length) {
    renderStage2Card();
  } else {
    submitStage2();
  }
}

async function submitStage2() {
  const container = document.getElementById('quiz-cards-stage2');
  container.innerHTML = '<div class="text-center" style="padding:2rem">⏳ שומר תוצאות...</div>';

  const correct = stage2Answers.filter(a => a.is_correct).length;
  const score = Math.round((correct / stage2Answers.length) * 100);

  await fetch('/api/quiz/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      lesson_id: LESSON_ID,
      stage: 2,
      answers: stage2Answers,
    })
  });

  container.innerHTML = '';
  const result = document.getElementById('stage2-result');
  result.classList.remove('hidden');
  document.getElementById('stage2-score-text').textContent = score + '%';
  document.getElementById('stage2-detail').textContent = `כתבת משפטים נכונים עם ${correct} מתוך ${stage2Answers.length} מילים`;

  // Update step
  const stepEl = document.getElementById('stage-step-2');
  if (stepEl) {
    stepEl.classList.add('done');
    stepEl.querySelector('.step-num').textContent = '✓';
  }
}

// ─── Retake Quiz ─────────────────────────────────────────────────────────────
function retakeQuiz() {
  window.location.reload();
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

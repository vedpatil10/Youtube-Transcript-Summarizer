const form = document.getElementById('summarize-form');
const errorBox = document.getElementById('error');
const resultBox = document.getElementById('result');
const summaryText = document.getElementById('summaryText');
const meta = document.getElementById('meta');
const submitBtn = document.getElementById('submitBtn');

function showError(message){
  errorBox.textContent = message;
  errorBox.classList.remove('hidden');
  resultBox.classList.add('hidden');
}

function showResult(summary, wordCount, sentenceCount){
  summaryText.textContent = summary;
  meta.textContent = `Sentences: ${sentenceCount}`;
  errorBox.classList.add('hidden');
  resultBox.classList.remove('hidden');
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const url = document.getElementById('url').value.trim();
  const ratio = parseFloat(document.getElementById('ratio').value);
  if(!url){
    showError('Please enter a valid YouTube URL.');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Summarizing…';

  try{
    const res = await fetch('/api/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, ratio })
    });
    const data = await res.json();
    if(!res.ok || data.status !== 'ok'){
      throw new Error(data.error || 'Failed to summarize.');
    }
    showResult(data.summary, data.word_count, data.sentence_count);
  }catch(err){
    showError(err.message || 'Unexpected error.');
  }finally{
    submitBtn.disabled = false;
    submitBtn.textContent = 'Summarize';
  }
});



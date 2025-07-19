document.getElementById('proposal-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const errorEl = document.getElementById('proposal-error') || createErrorElement(form);

    submitBtn.disabled = true;
    errorEl.textContent = '';
    errorEl.style.display = 'none';

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': form.querySelector('[name="csrf_token"]').value
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Proposal generation failed');
        }

        const data = await response.json();
        if (data.redirect) {
            window.location.href = data.redirect;
        } else if (data.content) {
            displayProposalResult(data.content);
        }
    } catch (error) {
        console.error('Proposal error:', error);
        errorEl.textContent = error.message || 'A network error occurred. Please try again.';
        errorEl.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
    }
});

function createErrorElement(form) {
    const div = document.createElement('div');
    div.id = 'proposal-error';
    div.className = 'alert alert-danger mt-3';
    form.prepend(div);
    return div;
}
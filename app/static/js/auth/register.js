// static/js/auth/register.js
// static/js/auth/register.js
document.getElementById('register-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const errorEl = document.getElementById('register-error') || createErrorElement();

    errorEl.style.display = 'none'; // Hide previous errors

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Registering...'; // Add spinner

    try {
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': form.querySelector('[name="csrf_token"]').value
            },
            credentials: 'include'
        });

        // Always try to parse JSON, even if response is not ok
        const data = await response.json();

        if (response.ok) {
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                // Should redirect on successful registration
                window.location.href = '/dashboard'; // Default success redirect
            }
        } else {
            // Handle validation errors or server errors from Flask
            if (data.status === 'validation_error' && data.errors) {
                // Display validation errors directly on form fields if possible,
                // or concatenate for a general error message.
                let errorMessage = 'Please correct the following errors:\n';
                for (const field in data.errors) {
                    errorMessage += `- ${field}: ${data.errors[field].join(', ')}\n`;
                }
                showError(errorMessage);
            } else {
                showError(data.message || 'Registration failed. Please try again.');
            }
        }
    } catch (error) {
        console.error('Registration fetch error:', error);
        showError('A network error occurred. Please try again.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Register';
    }
});


function createErrorElement() {
    const div = document.createElement('div');
    div.id = 'register-error';
    div.className = 'alert alert-danger mt-3';
    document.querySelector('#register-form').prepend(div);
    return div;
}

function showError(message) {
    const errorEl = document.getElementById('register-error');
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }
}
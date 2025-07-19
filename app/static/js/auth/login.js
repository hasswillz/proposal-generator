// static/js/auth/login.js
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('[type="submit"]');
    const errorEl = document.getElementById('login-error');

    // Clear previous errors
    errorEl.textContent = '';
    errorEl.style.display = 'none';

    try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Logging in...';

        const response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': form.querySelector('[name="csrf_token"]').value
            },
            credentials: 'same-origin'
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }

        // Successful login
        window.location.href = data.redirect || '/dashboard';

    } catch (error) {
        console.error('Login error:', error);
        errorEl.textContent = error.message || 'A network error occurred. Please try again.';
        errorEl.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Log In';
    }
});



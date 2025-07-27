// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Add Bootstrap validation classes
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('proposal-form');

    if (!form) {
        console.error('Proposal form not found!');
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Form submission intercepted');  // Debug log

        const submitBtn = form.querySelector('button[type="submit"]');
        const errorEl = document.getElementById('proposal-error');

        try {
            // Visual feedback
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm"></span>
                Generating...
            `;

            // Debug: Log form data before sending
            const formData = new FormData(form);
            console.log('Form data:', [...formData.entries()]);

            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    'X-CSRFToken': form.querySelector('[name="csrf_token"]').value
                }
            });

            console.log('Response status:', response.status);  // Debug log
            const data = await response.json();
            console.log('Response data:', data);  // Debug log

            if (!response.ok) throw new Error(data.message || 'Server error');

            if (data.redirect) {
                console.log('Redirecting to:', data.redirect);  // Debug log
                window.location.href = data.redirect;
            }

        } catch (error) {
            console.error('Generation failed:', error);
            errorEl.textContent = error.message || 'Proposal generation failed';
            errorEl.classList.remove('d-none');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate Proposal';
        }
    });
});
    // Budget formatting
    const budgetField = document.getElementById('budget');
    if (budgetField) {
        budgetField.addEventListener('blur', function() {
            if (this.value) {
                // Ensures the value is a number before formatting
                const numericValue = parseFloat(this.value);
                if (!isNaN(numericValue)) {
                    this.value = numericValue.toFixed(2);
                } else {
                    this.value = ''; // Clear if not a valid number
                }
            }
        });
    }

    // Dynamic proposal form field styling on input/change
    const proposalFormFields = document.querySelectorAll('#proposal-form .form-control, #proposal-form .form-select');
    proposalFormFields.forEach(field => {
        field.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
        field.addEventListener('change', function() { // For select fields
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
});

$('.language-link').click(function(e) {
    e.preventDefault();
    $.get($(this).attr('href'), function() {
        location.reload();
    });
});

 document.querySelectorAll('.language-switcher a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = this.href + '&_=' + new Date().getTime();
    });
});
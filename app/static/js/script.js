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

    // Generic form selector to specific ID for proposal form
    document.getElementById('proposal-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');

        // Reset form validation state if previously set
        form.classList.remove('was-validated');
        const validationFeedback = form.querySelectorAll('.invalid-feedback');
        validationFeedback.forEach(el => el.remove()); // Clear dynamic feedback

        // Manually trigger browser's form validation and check validity
        if (!form.checkValidity()) {
            form.classList.add('was-validated'); // Re-add for visual feedback
            // Scroll to the first invalid element if needed
            const firstInvalid = form.querySelector(':invalid');
            if (firstInvalid) {
                firstInvalid.focus();
                // You might also want to display specific error messages
                // This is where Flask-WTF validation errors for non-JS requests would usually appear
            }
            return; // Stop submission if browser validation fails
        }

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...'; // Add spinner

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', // Helps Flask identify AJAX requests
                    'X-CSRFToken': form.querySelector('[name="csrf_token"]').value // Include CSRF token
                }
            });

            const data = await response.json();

            if (response.ok) { // Check if the response status is 2xx
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    // Fallback or handle unexpected success without redirect
                    console.log("Proposal generated, but no redirect specified.", data);
                    alert("Proposal generated successfully!");
                    // You might want to refresh the dashboard or view the new proposal here
                    window.location.reload(); // Simple reload for demonstration
                }
            } else {
                // Handle errors from the server (e.g., validation_error, server error)
                if (data.status === 'validation_error' && data.errors) {
                    // Display validation errors under specific fields
                    for (const fieldName in data.errors) {
                        const fieldElement = form.querySelector(`[name="${fieldName}"]`);
                        if (fieldElement) {
                            fieldElement.classList.add('is-invalid');
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'invalid-feedback d-block';
                            errorDiv.textContent = data.errors[fieldName].join(', ');
                            fieldElement.parentNode.appendChild(errorDiv);
                        }
                    }
                    alert('Please correct the form errors.');
                } else {
                    // General error message
                    alert(data.message || 'Error generating proposal. Please try again.');
                }
            }

        } catch (error) {
            console.error('Proposal generation fetch error:', error);
            alert('A network error occurred. Please check your connection and try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Generate Proposal';
        }
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
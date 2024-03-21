function togglePasswordVisibility() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    const passwordToggles = document.querySelectorAll('.toggle-password');

    passwordToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function () {
            const passwordInput = this.previousElementSibling; // Get the corresponding password input
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            // Toggle the unlock/lock icon
            this.classList.toggle('fa-low-vision');
            this.classList.toggle('fa-eye');
        });
    });
}

// Call the function when the modal is fully loaded

togglePasswordVisibility();



const passwordInput = document.querySelector('input[name="password"]');
const passwordToggle = document.getElementById('password-toggle');

passwordToggle.addEventListener('click', function () {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    // Toggle the unlock/lock icon
    passwordToggle.classList.toggle('fa-low-vision');
    passwordToggle.classList.toggle('fa-eye');
});



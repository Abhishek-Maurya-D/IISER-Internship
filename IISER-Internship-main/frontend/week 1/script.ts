const form = document.getElementById('subscribe-form') as HTMLFormElement;
const emailInput = document.getElementById('email') as HTMLInputElement;
const message = document.getElementById('message') as HTMLParagraphElement;

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const email = emailInput.value;

  if (validateEmail(email)) {
    message.textContent = "You've successfully subscribed!";
    emailInput.value = '';
  } else {
    message.textContent = "Please enter a valid email address.";
    message.style.color = 'red';
  }
});

function validateEmail(email: string): boolean {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

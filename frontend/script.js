const protocolSelect = document.getElementById("protocol-select");
const runButton = document.getElementById("run-protocol");
const qberResult = document.getElementById("qber-result");

runButton.addEventListener("click", async () => {
  const selectedProtocol = protocolSelect.value;

  try {
    const response = await fetch("http://127.0.0.1:5000/run_protocol", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ protocol: selectedProtocol }),
    });

    const data = await response.json();

    if (response.ok) {
      qberResult.textContent = `QBER for ${selectedProtocol.toUpperCase()} protocol: ${data.qber}%`;
      qberResult.style.color = "white";
    } else {
      qberResult.textContent = `Error: ${data.error}`;
      qberResult.style.color = "red";
    }
  } catch (err) {
    qberResult.textContent = "Failed to contact the backend.";
    qberResult.style.color = "red";
    console.error(err);
  }
});

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

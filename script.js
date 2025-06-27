async function rewrite() {
  const inputText = document.getElementById("InputText").value.trim();
  const tone = document.getElementById("tone").value;
  const output = document.getElementById("output");

  if (!inputText) {
    output.innerText = "Please enter content to rewrite.";
    return;
  }

  output.innerText = "Rewriting... please wait.";

  try {
    const response = await fetch("http://127.0.0.1:5000/rewrite", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: inputText, tone: tone })
    });

    const data = await response.json();

    if (data.rewritten) {
      output.innerText = data.rewritten;
    } else {
      output.innerText = "Error: No rewritten content returned.";
    }
  } catch (error) {
    console.error(error);
    output.innerText = "An error occurred while rewriting.";
  }
}

function copyOutput() {
  const output = document.getElementById("output");
  navigator.clipboard.writeText(output.innerText).then(() => {
    alert("Rewritten content copied to clipboard!");
  });
}

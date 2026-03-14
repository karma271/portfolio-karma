(() => {
  const codeBlocks = document.querySelectorAll(".blog-article__body .codehilite");
  if (!codeBlocks.length) {
    return;
  }

  const fallbackCopy = (text) => {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "absolute";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    const copied = document.execCommand("copy");
    document.body.removeChild(textarea);
    return copied;
  };

  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    if (!fallbackCopy(text)) {
      throw new Error("Clipboard write failed");
    }
  };

  codeBlocks.forEach((block) => {
    const code = block.querySelector("pre code, pre");
    if (!code) {
      return;
    }

    const button = document.createElement("button");
    button.type = "button";
    button.className = "code-copy-button";
    button.textContent = "Copy";
    button.setAttribute("aria-label", "Copy code to clipboard");

    button.addEventListener("click", async () => {
      const source = code.textContent ? code.textContent.trimEnd() : "";
      if (!source) {
        return;
      }

      const originalLabel = button.textContent;
      try {
        await copyText(source);
        button.textContent = "Copied";
      } catch (_error) {
        button.textContent = "Failed";
      }

      window.setTimeout(() => {
        button.textContent = originalLabel;
      }, 1200);
    });

    block.classList.add("codehilite--copyable");
    block.appendChild(button);
  });
})();

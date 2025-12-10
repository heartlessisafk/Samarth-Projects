const API_BASE = "http://localhost:8000";

const form = document.getElementById("upload-form");
const statusDiv = document.getElementById("status");
const overlayImg = document.getElementById("overlay-img");
const meshCanvas = document.getElementById("mesh-canvas");
const gl = meshCanvas.getContext("webgl") || meshCanvas.getContext("experimental-webgl");

// Minimalistic rotating mesh placeholder (client-side) – real mesh is downloadable as .obj.
let angle = 0;

function drawPlaceholderMesh() {
  if (!gl) return;
  gl.viewport(0, 0, meshCanvas.width, meshCanvas.height);
  gl.clearColor(0.05, 0.07, 0.12, 1);
  gl.clear(gl.COLOR_BUFFER_BIT);
  // Placeholder: could plug in WebGL/three.js mesh renderer here.
}

setInterval(() => {
  angle += 0.01;
  drawPlaceholderMesh();
}, 50);

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusDiv.textContent = "Uploading and running segmentation...";
  const formData = new FormData(form);

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      statusDiv.textContent = `Error: ${err.error || res.statusText}`;
      return;
    }

    const data = await res.json();
    statusDiv.textContent = "Segmentation complete. Downloading artifacts...";

    // Fetch overlay PNG if you expose it via API; here we simply point to placeholder.
    overlayImg.src = "https://dummyimage.com/512x512/111827/ff004c&text=Segmentation+Overlay";
    statusDiv.textContent = "Done. You can also download 3D mesh and mask from the API.";
  } catch (err) {
    console.error(err);
    statusDiv.textContent = "Unexpected error. Check console.";
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const formElement = document.getElementById("uploadForm");
  const resultSection = document.getElementById("result");
  const outputImage = document.getElementById("outputImage");
  const spinnerOverlay = document.getElementById("spinner");
  const downloadButton = document.getElementById("downloadBtn");
  const toast = document.getElementById("toast");
  const scrollTopBtn = document.getElementById("scrollTopBtn");
  const imageInput = document.getElementById("imageInput");


  function showToast(message, type = "error") {
    toast.textContent = message;
    toast.className = `fixed bottom-6 left-6 px-4 py-2 rounded shadow-lg z-50 transition-opacity duration-300 ${
      type === "error" ? "bg-red-600 text-white" : "bg-green-600 text-white"
    }`;

    toast.classList.remove("opacity-0", "pointer-events-none");

    setTimeout(() => {
      toast.classList.add("opacity-0", "pointer-events-none");
    }, 3000);
  }

  formElement.addEventListener("submit", async (e) => {
    e.preventDefault();
    const file = document.getElementById("imageInput").files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    spinnerOverlay.classList.remove("hidden");

    const start = Date.now();
    let imageUrl = null;

    try {
      const response = await fetch("/api/v1/procesar", {
        method: "POST",
        body: formData,
      });

      const elapsed = Date.now() - start;
      const remainingTime = Math.max(0, 2000 - elapsed);
      await new Promise((res) => setTimeout(res, remainingTime));

      if (!response.ok) {
        throw new Error("Error en la respuesta del servidor");
      }

      const contentType = response.headers.get("Content-Type") || "";

      if (contentType.startsWith("image/")) {
        const blob = await response.blob();
        imageUrl = URL.createObjectURL(blob);

        outputImage.src = imageUrl;
        resultSection.classList.remove("hidden");

        if (downloadButton) {
          downloadButton.href = imageUrl;
          downloadButton.classList.remove("hidden");
        }

        showToast("Imagen procesada correctamente", "success");
      } else {
          try {
            const data = await response.json();
            if (data?.error) {
              showToast(data.error);
            } else {
              showToast("No se detectaron caras en la imagen.");
            }
          } catch {
            // Si no es JSON, fallback a texto plano
            const fallback = await response.text();
            showToast(fallback || "No se detectaron caras.");
          }
      }

    } catch (error) {
      showToast("No se pudo procesar la imagen. Inténtalo más tarde.");
    } finally {
      spinnerOverlay.classList.add("hidden");
    }
  });

  const descargadaMsg = document.getElementById("descargadaMsg");

  downloadButton.addEventListener("click", () => {
    showToast("Imagen descargada con éxito", "success");

    setTimeout(() => {
      // Ocultar resultados
      resultSection.classList.add("hidden");
      downloadButton.classList.add("hidden");
      outputImage.src = "";
      formElement.reset();

      // Mostrar mensaje sutil debajo
      descargadaMsg.classList.remove("hidden");

      setTimeout(() => {
        descargadaMsg.classList.add("hidden");
      }, 4000);
    }, 2000);
  });

  // Scroll-to-top
  window.addEventListener("scroll", () => {
    const threshold = window.innerHeight * 0.8; 
    if (window.scrollY > threshold) {
      scrollTopBtn.classList.remove("opacity-0", "pointer-events-none");
    } else {
      scrollTopBtn.classList.add("opacity-0", "pointer-events-none");
    }
  });

  scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Menú hamburguesa con animación y cierre al clicar fuera
  const menuToggle = document.getElementById("menuToggle");
  const mobileMenu = document.getElementById("mobileMenu");
  const lines = menuToggle.querySelectorAll(".line");

  menuToggle.addEventListener("click", (e) => {
    e.stopPropagation();

    const isOpen = !mobileMenu.classList.contains("max-h-0");

    // Alternar altura animada
    mobileMenu.classList.toggle("max-h-0");
    mobileMenu.classList.toggle("max-h-96"); // O 'max-h-screen' si tu menú es largo

    // Animación hamburguesa ↔ X
    if (isOpen) {
      // Cierra
      lines[0].classList.remove("rotate-45", "translate-y-2");
      lines[1].classList.remove("opacity-0");
      lines[2].classList.remove("-rotate-45", "-translate-y-2");
    } else {
      // Abre
      lines[0].classList.add("rotate-45", "translate-y-2");
      lines[1].classList.add("opacity-0");
      lines[2].classList.add("-rotate-45", "-translate-y-2");
    }
  });

  document.addEventListener("click", (e) => {
    const clickedOutside = !menuToggle.contains(e.target) && !mobileMenu.contains(e.target);
    const isOpen = mobileMenu.classList.contains("max-h-96");

    if (clickedOutside && isOpen) {
      // Cierra el menú suavemente
      mobileMenu.classList.remove("max-h-96");
      mobileMenu.classList.add("max-h-0");

      // Restaurar el icono hamburguesa
      lines[0].classList.remove("rotate-45", "translate-y-2");
      lines[1].classList.remove("opacity-0");
      lines[2].classList.remove("-rotate-45", "-translate-y-2");
    }
  });

  imageInput.addEventListener("change", () => {
    resultSection.classList.add("hidden");
    downloadButton.classList.add("hidden");
    descargadaMsg.classList.add("hidden");
    outputImage.src = "";
    toast.classList.add("opacity-0", "pointer-events-none");
  });


  const imageModal = document.getElementById("imageModal");
  const modalContent = document.getElementById("modalContent");
  const modalImage = document.getElementById("modalImage");
  const closeModal = document.getElementById("closeModal");

  function openImageModal(src) {
    modalImage.src = src;
    imageModal.classList.remove("hidden");

    // Forzar reflow
    void modalContent.offsetWidth;

    modalContent.classList.remove("scale-95", "opacity-0");
    modalContent.classList.add("scale-100", "opacity-100");
  }

  function closeImageModal() {
    modalContent.classList.remove("scale-100", "opacity-100");
    modalContent.classList.add("scale-95", "opacity-0");

    setTimeout(() => {
      imageModal.classList.add("hidden");
      modalImage.src = "";
    }, 300);
  }

  document.querySelectorAll("#metricas img").forEach((img) => {
    img.addEventListener("click", () => openImageModal(img.src));
  });
  closeModal.addEventListener("click", closeImageModal);
  imageModal.addEventListener("click", (e) => {
    if (e.target === imageModal) closeImageModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeImageModal();
  });

});
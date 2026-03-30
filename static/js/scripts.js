// Card hover glow and sound
document.querySelectorAll(".card").forEach((card) => {
  const audio = new Audio("static/sounds/woosh-effect.mp3");

  card.addEventListener("mouseenter", () => {
    card.style.boxShadow = "0 10px 30px rgba(255, 87, 34, 0.4)";
    audio.currentTime = 0;
    audio.play();
  });

  card.addEventListener("mouseleave", () => {
    card.style.boxShadow = "5px 5px 15px rgba(0, 0, 0, 0.4), -5px -5px 15px rgba(255, 255, 255, 0.1)";
    audio.pause();
    audio.currentTime = 0;
  });
});

// Pause/resume carousel on hover
document.addEventListener("DOMContentLoaded", () => {
  const carouselTrack = document.querySelector(".carousel-track");
  if (carouselTrack) {
    carouselTrack.addEventListener("mouseenter", () => {
      carouselTrack.style.animationPlayState = "paused";
    });
    carouselTrack.addEventListener("mouseleave", () => {
      carouselTrack.style.animationPlayState = "running";
    });
  }
});

// Smooth scroll & active navbar highlight
document.addEventListener("DOMContentLoaded", () => {
  const navItems = document.querySelectorAll(".nav-item");
  const sectionNavItems = Array.from(navItems).filter((item) => {
    const href = item.getAttribute("href");
    return href && href.startsWith("#") && href.length > 1;
  });
  const sections = document.querySelectorAll("section");

  sectionNavItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      const href = item.getAttribute("href");
      const target = href ? document.querySelector(href) : null;

      if (!target) {
        return;
      }

      e.preventDefault();
      window.scrollTo({
        top: target.offsetTop - 60,
        behavior: "smooth",
      });
    });
  });

  if (sectionNavItems.length > 0 && sections.length > 0) {
    window.addEventListener("scroll", () => {
      const scrollY = window.scrollY;
      sections.forEach((section) => {
        const matchingNavItem = document.querySelector(
          `.nav-item[href="#${section.id}"]`
        );

        if (!matchingNavItem) {
          return;
        }

        if (
          scrollY >= section.offsetTop - 70 &&
          scrollY < section.offsetTop + section.offsetHeight
        ) {
          sectionNavItems.forEach((item) => item.classList.remove("active"));
          matchingNavItem.classList.add("active");
        }
      });
    });
  }
});

// Button click sound
document.addEventListener("DOMContentLoaded", () => {
  const predictButton = document.querySelector(".submit-button");
  const clickSound = new Audio("/static/sounds/click.wav");

  if (predictButton) {
    predictButton.addEventListener("click", () => {
      clickSound.play();
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const loader = document.getElementById("page-loader");
  const loaderMessage = document.getElementById("page-loader-message");

  const showLoader = (message) => {
    if (!loader) {
      return;
    }

    if (loaderMessage && message) {
      loaderMessage.textContent = message;
    }

    loader.classList.add("is-visible");
    loader.setAttribute("aria-hidden", "false");
  };

  document.querySelectorAll("a.loading-link").forEach((link) => {
    link.addEventListener("click", (event) => {
      const href = link.getAttribute("href");

      if (
        !href ||
        href.startsWith("#") ||
        href.startsWith("mailto:") ||
        href.startsWith("tel:") ||
        event.ctrlKey ||
        event.metaKey ||
        event.shiftKey ||
        event.button !== 0
      ) {
        return;
      }

      showLoader(link.dataset.loadingMessage);
    });
  });

  document.querySelectorAll("form[data-loading-message]").forEach((form) => {
    form.addEventListener("submit", () => {
      showLoader(form.dataset.loadingMessage);
    });
  });

  window.addEventListener("pageshow", () => {
    if (!loader) {
      return;
    }

    loader.classList.remove("is-visible");
    loader.setAttribute("aria-hidden", "true");
  });
});

if (typeof particlesJS === "function" && document.getElementById("particles-js")) {
  particlesJS("particles-js", {
    particles: {
      number: { value: 80 },
      color: { value: "#00bcd4" },
      shape: { type: "circle" },
      opacity: { value: 0.3 },
      size: { value: 4 },
      line_linked: {
        enable: true,
        distance: 150,
        color: "#00bcd4",
        opacity: 0.2,
        width: 1
      },
      move: {
        enable: true,
        speed: 2,
        direction: "none",
        out_mode: "bounce"
      }
    },
    interactivity: {
      detect_on: "canvas",
      events: {
        onhover: { enable: true, mode: "repulse" }
      }
    }
  });
}

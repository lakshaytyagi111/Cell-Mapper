(() => {
      const button = document.getElementById("sos-hold-btn");
      const label = document.getElementById("sos-btn-label");
      const subtitle = document.getElementById("sos-btn-sub");
      const shareButton = document.getElementById("share-location-btn");
      const shareLabel = document.getElementById("share-location-label");
      const status = document.getElementById("interaction-status");
      let timer = null;
      let remaining = 3;
      let holding = false;
      let triggered = false;

      function stopTimer() {
        if (timer !== null) {
          window.clearInterval(timer);
          timer = null;
        }
      }

      function resetHold() {
        stopTimer();
        holding = false;
        remaining = 3;
        label.textContent = "SOS";
        subtitle.textContent = "Hold 3s";
        status.textContent = "SOS hold cancelled.";
      }

      function startHold(event) {
        if (holding || triggered || (event && event.button !== undefined && event.button !== 0)) return;
        holding = true;
        remaining = 3;
        label.textContent = String(remaining);
        subtitle.textContent = "Keep holding";
        status.textContent = "SOS hold started. Keep holding for 3 seconds.";
        timer = window.setInterval(() => {
          remaining -= 1;
          if (remaining > 0) {
            label.textContent = String(remaining);
            status.textContent = `${remaining} seconds remaining.`;
            return;
          }
          stopTimer();
          holding = false;
          triggered = true;
          label.textContent = "SENT";
          subtitle.textContent = "SOS Active";
          status.textContent = "SOS activated.";
        }, 1000);
      }

      button.addEventListener("pointerdown", (event) => {
        startHold(event);
        if (holding && button.setPointerCapture) button.setPointerCapture(event.pointerId);
      });
      button.addEventListener("pointerup", () => { if (holding) resetHold(); });
      button.addEventListener("pointercancel", () => { if (holding) resetHold(); });
      button.addEventListener("lostpointercapture", () => { if (holding) resetHold(); });
      button.addEventListener("keydown", (event) => {
        if ((event.code === "Space" || event.code === "Enter") && !event.repeat) {
          event.preventDefault();
          startHold();
        }
      });
      button.addEventListener("keyup", (event) => {
        if ((event.code === "Space" || event.code === "Enter") && holding) {
          event.preventDefault();
          resetHold();
        }
      });
      button.addEventListener("blur", () => { if (holding) resetHold(); });

      shareButton.addEventListener("click", () => {
        const isSharing = shareButton.getAttribute("aria-pressed") !== "true";
        shareButton.setAttribute("aria-pressed", String(isSharing));
        shareLabel.textContent = isSharing ? "Live link sent to 3 contacts" : "Share live location only";
        status.textContent = isSharing ? "Live location sharing enabled." : "Live location sharing disabled.";
      });
    })();

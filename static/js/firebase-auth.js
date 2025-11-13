import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js";
import {
  browserLocalPersistence,
  createUserWithEmailAndPassword,
  getAuth,
  GoogleAuthProvider,
  onAuthStateChanged,
  sendPasswordResetEmail,
  setPersistence,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";

let firebaseApp = null;
let firebaseAuth = null;
let sessionSyncInFlight = false;

const DEFAULT_ERROR = "We couldn't complete that request. Please try again.";

function ensureFirebase() {
  if (firebaseAuth) {
    return firebaseAuth;
  }

  if (!window.firebaseConfig || !window.firebaseConfig.apiKey) {
    console.warn("Firebase config missing. Authentication screen will be disabled.");
    return null;
  }

  firebaseApp = initializeApp(window.firebaseConfig);
  firebaseAuth = getAuth(firebaseApp);
  setPersistence(firebaseAuth, browserLocalPersistence).catch(() => {
    // Persistence can fail in some browsers (e.g., Safari private mode); continue without persisting.
  });
  firebaseAuth.useDeviceLanguage();
  return firebaseAuth;
}

function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : "";
}

function showMessage(container, type, message) {
  const box = container.querySelector("#authMessage");
  if (!box) {
    return;
  }
  box.classList.remove("d-none", "alert-success", "alert-danger", "alert-info");
  box.classList.add("alert", `alert-${type}`);
  box.innerHTML = message;
}

function clearMessage(container) {
  const box = container.querySelector("#authMessage");
  if (box) {
    box.classList.add("d-none");
    box.textContent = "";
  }
}

async function completeServerLogin(user, redirectTarget, intent, container) {
  if (!user || sessionSyncInFlight) {
    return;
  }
  sessionSyncInFlight = true;
  try {
    const idToken = await user.getIdToken(true);
    const response = await fetch("/auth/session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
      body: JSON.stringify({
        idToken,
        redirect: redirectTarget,
        intent,
      }),
    });

    const payload = await response.json().catch(() => ({}));

    if (!response.ok || !payload.success) {
      const message = payload.message || DEFAULT_ERROR;
      showMessage(container, "danger", message);
      sessionSyncInFlight = false;
      return;
    }

    window.location.href = payload.redirect || redirectTarget || "/";
  } catch (error) {
    console.error("Unable to create server session:", error);
    showMessage(container, "danger", DEFAULT_ERROR);
    sessionSyncInFlight = false;
  }
}

function attachLogoutHandlers(auth) {
  const logoutLinks = document.querySelectorAll('[data-auth-action="logout"]');
  logoutLinks.forEach((link) => {
    link.addEventListener("click", async (event) => {
      if (!auth) {
        return;
      }
      event.preventDefault();
      try {
        await signOut(auth);
      } catch (error) {
        console.warn("Firebase logout failed:", error);
      } finally {
        window.location.href = link.getAttribute("href");
      }
    });
  });
}

function setupTermsGate(container) {
  const termsCheckbox = container.querySelector("#signupTerms");
  const googleButton = container.querySelector("#signupGoogleBtn");
  const emailSubmit = container.querySelector("#firebaseEmailSignupSubmit");
  if (!termsCheckbox) {
    return;
  }

  const toggleState = () => {
    const enabled = termsCheckbox.checked;
    if (googleButton) {
      googleButton.disabled = !enabled;
    }
    if (emailSubmit) {
      emailSubmit.disabled = !enabled;
    }
  };

  termsCheckbox.addEventListener("change", toggleState);
  toggleState();
}

function setupLoginScreen(container, auth) {
  const redirectTarget = container.dataset.authRedirect || "/";
  const intent = container.dataset.authIntent || "user";
  const googleBtn = container.querySelector("#googleSignInBtn");
  const emailForm = container.querySelector("#emailSignInForm");
  const autoLogin = container.dataset.authAuto === "true";

  if (googleBtn) {
    googleBtn.addEventListener("click", async (event) => {
      event.preventDefault();
      clearMessage(container);
      try {
        const provider = new GoogleAuthProvider();
        const result = await signInWithPopup(auth, provider);
        await completeServerLogin(result.user, redirectTarget, intent, container);
      } catch (error) {
        console.error("Google sign-in failed:", error);
        showMessage(container, "danger", error.message || DEFAULT_ERROR);
      }
    });
  }

  if (emailForm) {
    emailForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearMessage(container);
      const email = emailForm.querySelector("#signinEmail").value.trim();
      const password = emailForm.querySelector("#signinPassword").value;
      if (!email || !password) {
        showMessage(container, "danger", "Please provide both email and password.");
        return;
      }
      try {
        const cred = await signInWithEmailAndPassword(auth, email, password);
        await completeServerLogin(cred.user, redirectTarget, intent, container);
      } catch (error) {
        console.error("Email sign-in failed:", error);
        showMessage(container, "danger", error.message || DEFAULT_ERROR);
      }
    });
  }

  if (autoLogin) {
    onAuthStateChanged(auth, (user) => {
      if (user) {
        completeServerLogin(user, redirectTarget, intent, container);
      }
    });
  }
}

function setupSignupScreen(container, auth) {
  const redirectTarget = container.dataset.authRedirect || "/";
  const intent = container.dataset.authIntent || "user";
  const googleBtn = container.querySelector("#signupGoogleBtn");
  const emailForm = container.querySelector("#firebaseEmailSignupForm");

  if (container.dataset.authRequiresTerms === "true") {
    setupTermsGate(container);
  }

  if (googleBtn) {
    googleBtn.addEventListener("click", async (event) => {
      event.preventDefault();
      clearMessage(container);
      try {
        const provider = new GoogleAuthProvider();
        const result = await signInWithPopup(auth, provider);
        await completeServerLogin(result.user, redirectTarget, intent, container);
      } catch (error) {
        console.error("Google signup failed:", error);
        showMessage(container, "danger", error.message || DEFAULT_ERROR);
      }
    });
  }

  if (emailForm) {
    emailForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearMessage(container);

      const email = emailForm.querySelector("#signupEmail").value.trim();
      const password = emailForm.querySelector("#signupPassword").value;
      const confirm = emailForm.querySelector("#signupConfirmPassword").value;

      if (!email || !password || !confirm) {
        showMessage(container, "danger", "Please complete all required fields.");
        return;
      }
      if (password !== confirm) {
        showMessage(container, "danger", "Passwords do not match. Please try again.");
        return;
      }

      try {
        const cred = await createUserWithEmailAndPassword(auth, email, password);
        await completeServerLogin(cred.user, redirectTarget, intent, container);
      } catch (error) {
        console.error("Email signup failed:", error);
        showMessage(container, "danger", error.message || DEFAULT_ERROR);
      }
    });
  }
}

function setupPasswordResetScreen(container, auth) {
  const redirectTarget = container.dataset.authRedirect || "";
  const form = container.querySelector("#passwordResetForm");
  if (!form) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearMessage(container);
    const emailInput = form.querySelector("#resetEmail");
    const email = emailInput.value.trim();
    if (!email) {
      showMessage(container, "danger", "Please provide the email associated with your account.");
      return;
    }

    try {
      await sendPasswordResetEmail(auth, email);
      showMessage(
        container,
        "success",
        "Check your inbox for a Firebase password reset email. Follow the link to set a new password."
      );
      if (redirectTarget) {
        setTimeout(() => {
          window.location.href = redirectTarget;
        }, 4000);
      }
    } catch (error) {
      console.error("Password reset failed:", error);
      showMessage(container, "danger", error.message || DEFAULT_ERROR);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const auth = ensureFirebase();
  if (!auth) {
    return;
  }

  attachLogoutHandlers(auth);

  const container = document.getElementById("authContainer");
  if (!container) {
    return;
  }

  const mode = container.dataset.authMode;
  if (mode === "login") {
    setupLoginScreen(container, auth);
  } else if (mode === "signup") {
    setupSignupScreen(container, auth);
  } else if (mode === "password-reset") {
    setupPasswordResetScreen(container, auth);
  }
});

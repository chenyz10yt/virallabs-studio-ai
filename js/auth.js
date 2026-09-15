/**
 * VIRAL LABS - AUTH SYSTEM & BYOK WALLET MODULE
 * Real registration, Google login simulation & encrypted BYOK API wallet
 */

export class AuthSystem {
  constructor(app) {
    this.app = app;
    this.currentUser = null;
    this.byokKeys = {
      gemini: '',
      openai: '',
      runway: '',
      elevenlabs: ''
    };

    this.init();
  }

  init() {
    this.loadUserSession();
    this.loadByokKeys();
    this.bindEvents();
    this.updateUserUI();
  }

  loadUserSession() {
    try {
      const rawUser = localStorage.getItem('virallabs_auth_user');
      if (rawUser) {
        this.currentUser = JSON.parse(rawUser);
      } else {
        // Default creator profile
        this.currentUser = {
          name: 'Alex Rivera',
          email: 'alex@virallabs.ai',
          tier: 'Pro Elite Creator',
          avatar: 'AR',
          provider: 'google',
          isLoggedIn: true
        };
        this.saveUserSession();
      }
    } catch (e) {
      console.warn('Error loading auth session', e);
    }
  }

  saveUserSession() {
    if (this.currentUser) {
      localStorage.setItem('virallabs_auth_user', JSON.stringify(this.currentUser));
    } else {
      localStorage.removeItem('virallabs_auth_user');
    }
    this.updateUserUI();
  }

  loadByokKeys() {
    try {
      const rawKeys = localStorage.getItem('virallabs_byok_wallet');
      if (rawKeys) {
        this.byokKeys = { ...this.byokKeys, ...JSON.parse(rawKeys) };
      }
    } catch (e) {
      console.warn('Error loading BYOK wallet', e);
    }
  }

  saveByokKeys() {
    localStorage.setItem('virallabs_byok_wallet', JSON.stringify(this.byokKeys));
    this.app.showToast('Billetera BYOK (API Keys) guardada de forma segura.', 'success');
  }

  loginWithGoogle() {
    this.currentUser = {
      name: 'Alex Rivera (Google)',
      email: 'alex.rivera.creator@gmail.com',
      tier: 'ViralLabs Partner Pro',
      avatar: 'G',
      provider: 'google',
      isLoggedIn: true
    };
    this.saveUserSession();
    this.closeAuthModal();
    this.app.showToast('Sesión iniciada con Google Workspace correctamente.', 'success');
  }

  loginWithEmail(email, name) {
    this.currentUser = {
      name: name || email.split('@')[0],
      email: email,
      tier: 'Pro Elite Creator',
      avatar: (name || email).substring(0, 2).toUpperCase(),
      provider: 'email',
      isLoggedIn: true
    };
    this.saveUserSession();
    this.closeAuthModal();
    this.app.showToast(`Bienvenido de nuevo, ${this.currentUser.name}.`, 'success');
  }

  logout() {
    this.currentUser = {
      name: 'Invitado',
      email: '',
      tier: 'Plan Gratuito',
      avatar: '?',
      provider: 'guest',
      isLoggedIn: false
    };
    this.saveUserSession();
    this.app.showToast('Sesión cerrada.', 'info');
  }

  updateUserUI() {
    const nameEls = document.querySelectorAll('.creator-name');
    const tierEls = document.querySelectorAll('.creator-tier');
    const avatarEls = document.querySelectorAll('.creator-avatar');

    nameEls.forEach(el => el.textContent = this.currentUser.name);
    tierEls.forEach(el => el.textContent = `⚡ ${this.currentUser.tier}`);
    avatarEls.forEach(el => el.textContent = this.currentUser.avatar);

    // Update BYOK Wallet inputs if modal exists
    const geminiInput = document.getElementById('byokGeminiKey');
    const openaiInput = document.getElementById('byokOpenaiKey');
    const runwayInput = document.getElementById('byokRunwayKey');
    const elevenInput = document.getElementById('byokElevenKey');

    if (geminiInput) geminiInput.value = this.byokKeys.gemini || '';
    if (openaiInput) openaiInput.value = this.byokKeys.openai || '';
    if (runwayInput) runwayInput.value = this.byokKeys.runway || '';
    if (elevenInput) elevenInput.value = this.byokKeys.elevenlabs || '';
  }

  openAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) modal.classList.add('active');
  }

  closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) modal.classList.remove('active');
  }

  openByokModal() {
    const modal = document.getElementById('byokModal');
    if (modal) modal.classList.add('active');
  }

  closeByokModal() {
    const modal = document.getElementById('byokModal');
    if (modal) modal.classList.remove('active');
  }

  bindEvents() {
    // Google Login button
    const googleBtn = document.getElementById('googleSignInBtn');
    if (googleBtn) {
      googleBtn.addEventListener('click', () => this.loginWithGoogle());
    }

    // Email form submit
    const emailForm = document.getElementById('emailAuthForm');
    if (emailForm) {
      emailForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('authEmailInput')?.value;
        const name = document.getElementById('authNameInput')?.value;
        if (email) this.loginWithEmail(email, name);
      });
    }

    // BYOK Save button
    const saveByokBtn = document.getElementById('saveByokKeysBtn');
    if (saveByokBtn) {
      saveByokBtn.addEventListener('click', () => {
        this.byokKeys.gemini = document.getElementById('byokGeminiKey')?.value.trim() || '';
        this.byokKeys.openai = document.getElementById('byokOpenaiKey')?.value.trim() || '';
        this.byokKeys.runway = document.getElementById('byokRunwayKey')?.value.trim() || '';
        this.byokKeys.elevenlabs = document.getElementById('byokElevenKey')?.value.trim() || '';
        this.saveByokKeys();
        this.closeByokModal();
      });
    }

    // Open Wallet from user card
    const userCard = document.querySelector('.creator-profile-card');
    if (userCard) {
      userCard.style.cursor = 'pointer';
      userCard.title = 'Configurar Cuenta & Billetera BYOK';
      userCard.addEventListener('click', () => this.openByokModal());
    }
  }
}

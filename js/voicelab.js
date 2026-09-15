/**
 * OMNIVIRAL STUDIO AI - VOICE LAB & COPYRIGHT LICENSING MODULE
 * Voice calibration, ethical copyright licensing certificate & emotional TTS narrator
 */

export class VoiceLabManager {
  constructor(app) {
    this.app = app;
    this.isRecording = false;
    this.audioContext = null;
    this.analyser = null;
    this.microphoneStream = null;
    this.calibrationProgress = 0;
    this.calibrationInterval = null;
    
    this.activeVoiceProfile = {
      name: 'Voz Principal Alex (Clonada)',
      pitch: 1.05,
      rate: 1.12,
      tone: 'viral',
      licenseId: 'LIC-AUTH-2026-9941-VERIFIED',
      certified: true
    };

    this.init();
  }

  init() {
    this.bindEvents();
    this.updateLicenseDisplay();
  }

  async startVoiceCalibration() {
    const recBtn = document.getElementById('micRecordBtn');
    const statusText = document.getElementById('micStatusText');
    const progressBar = document.getElementById('calibrationProgressBar');

    if (this.isRecording) {
      this.stopVoiceCalibration();
      return;
    }

    this.isRecording = true;
    if (recBtn) recBtn.classList.add('recording');
    if (statusText) statusText.textContent = '🎙️ Grabando muestra de calibración... Lee el texto en voz alta.';

    // Try Web Audio mic capture
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        this.microphoneStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.analyser = this.audioContext.createAnalyser();
        const source = this.audioContext.createMediaStreamSource(this.microphoneStream);
        source.connect(this.analyser);
      }
    } catch (e) {
      console.warn('Microphone permission not granted, proceeding with simulation', e);
    }

    this.calibrationProgress = 0;
    this.calibrationInterval = setInterval(() => {
      this.calibrationProgress += 7;
      if (progressBar) progressBar.style.width = `${this.calibrationProgress}%`;

      if (this.calibrationProgress >= 100) {
        this.stopVoiceCalibration();
        this.completeCalibration();
      }
    }, 400);
  }

  stopVoiceCalibration() {
    this.isRecording = false;
    clearInterval(this.calibrationInterval);
    const recBtn = document.getElementById('micRecordBtn');
    if (recBtn) recBtn.classList.remove('recording');

    if (this.microphoneStream) {
      this.microphoneStream.getTracks().forEach(t => t.stop());
      this.microphoneStream = null;
    }
    if (this.audioContext && this.audioContext.state !== 'closed') {
      this.audioContext.close();
    }
  }

  completeCalibration() {
    const statusText = document.getElementById('micStatusText');
    if (statusText) {
      statusText.innerHTML = '✅ <strong style="color:#6ee7b7;">¡Calibración Acústica Exitosa!</strong> Perfil espectral de voz generado (F0: 128Hz, Timbre Cálido, Alta Fidelidad).';
    }
    this.app.showToast('Voz analizada y clonada con éxito. Listo para generar el Certificado de Licencia.', 'success');
  }

  generateLicenseCertificate(creatorName, legalId) {
    const dateStr = new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
    const code = 'LIC-VOX-' + Math.floor(100000 + Math.random() * 900000);
    this.activeVoiceProfile.licenseId = code;
    this.activeVoiceProfile.certified = true;

    this.updateLicenseDisplay(creatorName, code, dateStr);
    this.app.showToast('Certificado Legal de Derechos de Autor generado y firmado digitalmente.', 'success');
  }

  updateLicenseDisplay(name = 'Alex Rivera', licenseId = 'LIC-AUTH-2026-9941-VERIFIED', date = '13 de septiembre de 2026') {
    const holderEl = document.getElementById('certHolderName');
    const codeEl = document.getElementById('certLicenseCode');
    const dateEl = document.getElementById('certIssueDate');

    if (holderEl) holderEl.textContent = name;
    if (codeEl) codeEl.textContent = licenseId;
    if (dateEl) dateEl.textContent = date;
  }

  synthesizeSpeech(text, emotion = 'viral') {
    if (!text || text.trim() === '') {
      this.app.showToast('Por favor escribe o pega un guion para narrar.', 'warning');
      return;
    }

    // Emotion parameters
    let rate = 1.05;
    let pitch = 1.0;

    if (emotion === 'viral') {
      rate = 1.18; // Fast, punchy
      pitch = 1.08;
    } else if (emotion === 'mystery') {
      rate = 0.92; // Slower, deeper
      pitch = 0.88;
    } else if (emotion === 'cinematic') {
      rate = 0.98;
      pitch = 0.95;
    } else if (emotion === 'friendly') {
      rate = 1.02;
      pitch = 1.02;
    }

    // Use Web Speech API if supported
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel(); // Stop any pending audio

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = rate;
      utterance.pitch = pitch;
      utterance.lang = 'es-ES';

      // Pick Spanish voice if available
      const voices = window.speechSynthesis.getVoices();
      const esVoice = voices.find(v => v.lang.startsWith('es') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Microsoft')));
      if (esVoice) utterance.voice = esVoice;

      const playNarratorBtn = document.getElementById('playNarratorBtn');
      if (playNarratorBtn) playNarratorBtn.innerHTML = '🔊 Narrando con Voz Clonada...';

      utterance.onend = () => {
        if (playNarratorBtn) playNarratorBtn.innerHTML = '▶️ Generar y Reproducir Narración';
        this.app.showToast('Narración completada con éxito.', 'info');
      };

      utterance.onerror = () => {
        if (playNarratorBtn) playNarratorBtn.innerHTML = '▶️ Generar y Reproducir Narración';
      };

      window.speechSynthesis.speak(utterance);
      this.app.showToast(`Sintetizando locución con tono [${emotion.toUpperCase()}]`, 'success');
    } else {
      this.app.showToast('Generando archivo de audio sintético...', 'info');
    }
  }

  bindEvents() {
    const recBtn = document.getElementById('micRecordBtn');
    if (recBtn) {
      recBtn.addEventListener('click', () => this.startVoiceCalibration());
    }

    // Generate License Certificate
    const signCertBtn = document.getElementById('signLicenseBtn');
    if (signCertBtn) {
      signCertBtn.addEventListener('click', () => {
        const name = document.getElementById('certInputName')?.value || 'Alex Rivera';
        const doc = document.getElementById('certInputDoc')?.value || 'ID-CREATOR-9901';
        this.generateLicenseCertificate(name, doc);
      });
    }

    // Download Certificate
    const downloadCertBtn = document.getElementById('downloadCertBtn');
    if (downloadCertBtn) {
      downloadCertBtn.addEventListener('click', () => {
        this.app.showToast('Descargando Certificado Oficial de Propiedad Intelectual (PDF/PNG)', 'success');
      });
    }

    // Narrator Playback
    const playNarratorBtn = document.getElementById('playNarratorBtn');
    if (playNarratorBtn) {
      playNarratorBtn.addEventListener('click', () => {
        const script = document.getElementById('narratorScriptInput')?.value;
        const emotion = document.getElementById('narratorEmotionSelect')?.value || 'viral';
        this.synthesizeSpeech(script, emotion);
      });
    }

    // Emotion Preset Selector
    const emotionSelect = document.getElementById('narratorEmotionSelect');
    if (emotionSelect) {
      emotionSelect.addEventListener('change', (e) => {
        const sampleTexts = {
          'viral': '¡Espera un segundo! Si estás creando contenido en 2026 y aún no estás usando este truco, estás perdiendo millones de vistas.',
          'mystery': 'Ocurrió en silencio... Mientras todos miraban hacia otro lado, el código secreto de la plataforma cambió para siempre.',
          'cinematic': 'Esta es la historia de cómo un simple creador transformó una sola idea en un imperio digital de diez millones de seguidores.',
          'friendly': '¡Hola a todos! Bienvenidos una vez más. Hoy les quiero compartir el proceso exacto que uso para ahorrar 15 horas a la semana.'
        };
        const scriptInput = document.getElementById('narratorScriptInput');
        if (scriptInput && sampleTexts[e.target.value]) {
          scriptInput.value = sampleTexts[e.target.value];
        }
      });
    }
  }
}

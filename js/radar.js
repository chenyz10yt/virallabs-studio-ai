/**
 * OMNIVIRAL STUDIO AI - ALGORITHM RADAR & MONETIZATION CALCULATOR MODULE
 * Hook evaluation engine, viral niches database & dynamic monetization revenue estimator
 */

export class RadarManager {
  constructor(app) {
    this.app = app;
    this.init();
  }

  init() {
    this.bindEvents();
    this.calculateEarnings();
    this.evaluateHook('Si creas contenido y tardas más de 30 minutos por video, estás tirando tu dinero...');
  }

  evaluateHook(text) {
    if (!text || text.trim() === '') return;

    // Algorithm heuristic scoring
    const words = text.trim().split(/\s+/);
    let score = 70;

    const powerWords = [
      'secreto', 'nadie', 'truco', 'cambió', 'dinero', 'error', 'cuidado', 'urgente',
      'millones', 'gratis', 'prohibido', 'fácil', 'rápido', 'tiempo', 'ia', 'trucos'
    ];

    let powerHits = 0;
    const lower = text.toLowerCase();
    powerWords.forEach(pw => {
      if (lower.includes(pw)) {
        powerHits++;
        score += 5;
      }
    });

    // Ideal hook length: 8 to 22 words
    if (words.length >= 8 && words.length <= 22) {
      score += 8;
    } else if (words.length > 30) {
      score -= 10;
    }

    // Has numbers? (e.g. 5 herramientas, 30 minutos, 2026)
    if (/\d+/.test(text)) {
      score += 7;
    }

    score = Math.min(99, Math.max(45, score));

    // Update Radial Meter
    const scoreNumEl = document.getElementById('radialScoreNumber');
    const radialCircle = document.getElementById('radialScoreCircle');

    if (scoreNumEl) scoreNumEl.textContent = score;
    if (radialCircle) {
      radialCircle.style.setProperty('--score-pct', score);
    }

    // Update Criteria Bars
    const curiosity = Math.min(100, score + 4);
    const urgency = Math.min(100, score - 2 + (powerHits * 3));
    const clarity = Math.min(100, Math.max(60, 100 - words.length));

    const curBar = document.getElementById('curiosityScoreBar');
    const urgBar = document.getElementById('urgencyScoreBar');
    const claBar = document.getElementById('clarityScoreBar');

    if (curBar) curBar.style.width = `${curiosity}%`;
    if (urgBar) urgBar.style.width = `${urgency}%`;
    if (claBar) claBar.style.width = `${clarity}%`;

    // Suggestions
    const suggestionsEl = document.getElementById('hookAiSuggestions');
    if (suggestionsEl) {
      suggestionsEl.innerHTML = `
        <div style="background:rgba(99, 102, 241, 0.1); border-left:3px solid #6366f1; padding:10px 14px; border-radius:4px; font-size:0.82rem; margin-top:10px;">
          <strong>💡 Sugerencia del Algoritmo:</strong> Tu gancho tiene un nivel de curiosidad de ${curiosity}%. 
          Prueba acortar las primeras 4 palabras para que el impacto visual coincida con el corte del primer segundo.
        </div>
      `;
    }
  }

  calculateEarnings() {
    const viewsSlider = document.getElementById('sliderViews');
    const brandsSlider = document.getElementById('sliderBrands');
    const tierSelect = document.getElementById('selectAudienceTier');

    const views = parseInt(viewsSlider?.value || 500000);
    const brandsCount = parseInt(brandsSlider?.value || 2);
    const tierMultiplier = parseFloat(tierSelect?.value || 1.2);

    // Platform RPM calculation:
    // Base RPM for 1000 views: ~$0.75 in Tier 1.5
    const baseRpm = 0.85 * tierMultiplier;
    const adRevenue = Math.round((views / 1000) * baseRpm);

    // Average brand sponsorship value per 100k views: ~$350
    const brandValuePerDeal = Math.max(300, Math.round((views / 100000) * 350));
    const brandRevenue = brandsCount * brandValuePerDeal;

    const totalMonthly = adRevenue + brandRevenue;
    const totalAnnual = totalMonthly * 12;

    // Display formatted numbers
    const totalNumEl = document.getElementById('calcTotalNumber');
    const adRevenueEl = document.getElementById('calcAdRevenue');
    const brandRevenueEl = document.getElementById('calcBrandRevenue');
    const annualRevenueEl = document.getElementById('calcAnnualRevenue');

    const viewsLabel = document.getElementById('viewsLabelDisplay');
    const brandsLabel = document.getElementById('brandsLabelDisplay');

    if (viewsLabel) viewsLabel.textContent = `${(views / 1000).toLocaleString()}K vistas/mes`;
    if (brandsLabel) brandsLabel.textContent = `${brandsCount} patrocinios/mes`;

    if (totalNumEl) totalNumEl.textContent = `$${totalMonthly.toLocaleString()} USD`;
    if (adRevenueEl) adRevenueEl.textContent = `$${adRevenue.toLocaleString()}`;
    if (brandRevenueEl) brandRevenueEl.textContent = `$${brandRevenue.toLocaleString()}`;
    if (annualRevenueEl) annualRevenueEl.textContent = `$${totalAnnual.toLocaleString()}`;
  }

  bindEvents() {
    // Hook Evaluator Input
    const hookInput = document.getElementById('hookEvaluatorInput');
    const evaluateBtn = document.getElementById('evaluateHookBtn');

    if (evaluateBtn) {
      evaluateBtn.addEventListener('click', () => {
        const text = hookInput?.value;
        this.evaluateHook(text);
        this.app.showToast('Gancho evaluado contra métricas de retención 2026', 'success');
      });
    }

    // Monetization Sliders
    const viewsSlider = document.getElementById('sliderViews');
    const brandsSlider = document.getElementById('sliderBrands');
    const tierSelect = document.getElementById('selectAudienceTier');

    if (viewsSlider) viewsSlider.addEventListener('input', () => this.calculateEarnings());
    if (brandsSlider) brandsSlider.addEventListener('input', () => this.calculateEarnings());
    if (tierSelect) tierSelect.addEventListener('change', () => this.calculateEarnings());
  }
}

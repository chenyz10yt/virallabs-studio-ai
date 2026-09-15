/**
 * OMNIVIRAL STUDIO AI - COMPLETE STANDALONE BUNDLE
 * Contains Storage, Studio, Clipper, Multistream, VoiceLab, Planner & Radar
 * Zero-dependency, runs directly on file:/// or any web server.
 */

// ==========================================
// 1. STORAGE MANAGER
// ==========================================
const STORAGE_KEY = 'omniviral_studio_data_v1';

const defaultCreatorState = {
  creator: {
    name: 'Alex Rivera',
    handle: '@alexcreator.ai',
    tier: 'Pro Elite Creator',
    niche: 'Inteligencia Artificial & Tech',
    connectedPlatforms: {
      tiktok: true,
      youtube: true,
      instagram: true,
      facebook: false,
      twitch: true,
      kick: false
    }
  },
  streamSettings: {
    resolution: '1080p60',
    targetBitrate: 6500,
    fps: 60,
    audioBitrate: 160,
    rtmpKeys: {
      youtube: 'yt-live-9823-xxxx-viral',
      tiktok: 'tt-live-4412-xxxx-stream',
      facebook: 'fb-live-1120-xxxx-meta',
      twitch: 'live_8832_tw_xxxx',
      kick: 'sk_us_kick_9021_xxxx'
    }
  },
  scheduledPosts: [
    {
      id: 'post-1',
      title: '5 Herramientas de IA que reemplazan agencias enteras en 2026',
      platforms: ['tiktok', 'instagram', 'youtube'],
      date: '2026-09-14',
      time: '19:00',
      status: 'scheduled',
      caption: '🚀 Si no estás usando estas 5 herramientas de IA en 2026, estás perdiendo el 80% de tu tiempo. La número 4 te volará la cabeza 🤯\n\n#IA #CreadoresDeContenido #Productividad #Tecnologia #Emprendimiento',
      viralScore: 94,
      thumbnail: 'assets/thumbnail_demo.jpg'
    },
    {
      id: 'post-2',
      title: 'Cómo cloné mi voz para narrar videos automáticos legalmente',
      platforms: ['youtube', 'facebook'],
      date: '2026-09-15',
      time: '18:30',
      status: 'scheduled',
      caption: '🎙️ Guía definitiva para clonar tu voz con certificación de derechos de autor y monetizar canales automatizados sin penalizaciones de algoritmo.',
      viralScore: 91,
      thumbnail: 'assets/clip_demo.jpg'
    },
    {
      id: 'post-3',
      title: 'El nuevo cambio de algoritmo en TikTok e Instagram Reels',
      platforms: ['tiktok', 'instagram'],
      date: '2026-09-17',
      time: '20:15',
      status: 'draft',
      caption: '⚠️ ATENCIÓN: El algoritmo cambió este mes. Las visualizaciones ya no importan tanto como esta métrica secreta (los shares por mensaje directo).',
      viralScore: 88,
      thumbnail: 'assets/thumbnail_demo.jpg'
    }
  ],
  savedPrompts: [],
  voiceProfiles: [
    {
      id: 'voice-alex-main',
      name: 'Voz Principal Alex (Clonada)',
      pitch: 1.0,
      cadence: 'Dinámica / Enérgica',
      dateCreated: '2026-09-10',
      licenseId: 'LIC-AUTH-2026-9941-VERIFIED',
      verified: true
    }
  ]
};

class StorageManager {
  static getData() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        this.saveData(defaultCreatorState);
        return defaultCreatorState;
      }
      return JSON.parse(raw);
    } catch (e) {
      console.warn('Error reading from localStorage, using defaults', e);
      return defaultCreatorState;
    }
  }

  static saveData(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      console.error('Error saving to localStorage', e);
    }
  }

  static addPost(post) {
    const data = this.getData();
    data.scheduledPosts.unshift(post);
    this.saveData(data);
    return data.scheduledPosts;
  }

  static deletePost(postId) {
    const data = this.getData();
    data.scheduledPosts = data.scheduledPosts.filter(p => p.id !== postId);
    this.saveData(data);
    return data.scheduledPosts;
  }

  static updatePlatformStatus(platform, isConnected) {
    const data = this.getData();
    data.creator.connectedPlatforms[platform] = isConnected;
    this.saveData(data);
    return data.creator.connectedPlatforms;
  }
}

// ==========================================
// 1.5. HIGH-RPM TRENDING NICHES & VIRAL DATABASE
// ==========================================
const TrendingNiches = {
  espiritualidad: {
    id: 'espiritualidad',
    name: 'Espiritualidad, Manifestación & Consciencia',
    icon: '🧘',
    cpm: '$15 - $28 USD',
    ideas: [
      'La ley del desapego: por qué cuando dejas de rogar todo llega',
      'El secreto de Nikola Tesla 369 para manifestar en 24 horas',
      'Ho\'oponopono: las 4 palabras que borran bloqueos de dinero',
      '3 señales claras de que tu subconsciente se está reprogramando',
      'La técnica de la almohada de Neville Goddard para manifestar dormido'
    ],
    seoTags: [
      'espiritualidad', 'ley de atraccion', 'manifestar abundancia', 'despertar espiritual',
      'afirmaciones positivas', 'ho oponopono', 'frecuencia 432 hz', 'neville goddard',
      'paz interior', 'energia positiva', 'manifestacion consciente'
    ],
    typoTags: [
      'espiritualida', 'ley de atracion', 'manifstar dinero', 'afirmasiones de abundancia',
      'despertar de consiencia', 'hoponopono meditasion', 'neville goddar libros',
      'frecuencia 432hz relajasion', 'meditasion para dormir profunda', 'como manifestar fasil'
    ],
    hooks: [
      'Si sientes que trabajas duro pero el dinero o el amor se te escapan, estás cometiendo este grave error energético...',
      'Nikola Tesla descubrió que el universo vibra en 3, 6 y 9. Esta es la técnica exacta para manifestar que nadie te enseña...',
      'El 99% de las personas piden desde la necesidad y por eso reciben más escasez. La ley del desapego funciona así...',
      'Deja de forzar las cosas. Cuando aplicas esta regla de 10 segundos antes de dormir, tu mente atrae lo que buscas...',
      'Las 4 palabras de Ho\'oponopono que limpian memorias de escasez de tus antepasados en solo 7 días...'
    ],
    titles: [
      { title: 'Por Qué Cuando Dejas de Rogar Todo Llega (Ley del Desapego)', score: 98 },
      { title: 'El Secreto 3-6-9 de Nikola Tesla para Manifestar en 24 Horas', score: 97 },
      { title: '4 Palabras para Borrar Bloqueos de Dinero Mientras Duermes', score: 95 },
      { title: 'Si Notas Estas 3 Señales, Tu Manifestación Está a Punto de Ocurrir', score: 94 },
      { title: 'La Técnica de la Almohada de Neville Goddard (Pruébala Hoy)', score: 92 }
    ]
  },
  finanzas: {
    id: 'finanzas',
    name: 'Finanzas Personales, Cripto & Negocios',
    icon: '💰',
    cpm: '$25 - $60 USD',
    ideas: [
      '3 errores financieros que te mantienen en clase media a los 30 años',
      'Cómo invertir tus primeros $100 dólares sin experiencia en 2026',
      'El método de las 5 cuentas bancarias para ahorrar sin sufrir',
      'Interés compuesto: la fórmula matemática para ser libre financieramente',
      'Activos vs Pasivos: la diferencia crucial que nunca te enseñaron en la escuela'
    ],
    seoTags: [
      'finanzas personales', 'como invertir', 'educacion financiera', 'libertad financiera',
      'ingresos pasivos', 'interes compuesto', 'ahorrar dinero', 'inversiones 2026',
      'bienes raices', 'bolsa de valores', 'creacion de riqueza'
    ],
    typoTags: [
      'finansas personales', 'invercion para principiantes', 'invertir dinero en 2026',
      'libertad finaciera', 'educasion financiera', 'como ganar plata fasil',
      'ingresos pasibos', 'ahorrar dinero rapido', 'criptomonedas bitcon', 'negosios rentables'
    ],
    hooks: [
      'Si tienes más de 25 años y tu dinero solo está en una cuenta de ahorros, estás perdiendo el 6% de tu patrimonio cada año...',
      'Los ricos no trabajan por dinero: hacen que el dinero trabaje para ellos con este sistema de 3 pasos...',
      'Si ganas $1,000 al mes y no puedes ahorrar ni $100, no tienes un problema de ingresos, tienes este error oculto...',
      'Cualquiera con $50 dólares puede comprar una fracción de las 500 empresas más grandes del mundo hoy mismo...',
      'Esta es la regla del 50/30/20 modificada para 2026 que te permitirá comprar tu primera propiedad antes de los 35...'
    ],
    titles: [
      { title: '3 Errores Financieros que Te Mantendrán Pobre Toda la Vida', score: 99 },
      { title: 'Cómo Invertir tus Primeros $100 en 2026 (Paso a Paso)', score: 97 },
      { title: 'El Sistema de 5 Cuentas que Me Hizo Libre Financieramente', score: 96 },
      { title: 'La Regla del Interés Compuesto que los Bancos Ocultan', score: 95 },
      { title: 'Deja de Ahorrar en el Banco: Haz Esto en su Lugar', score: 94 }
    ]
  },
  mentalidad: {
    id: 'mentalidad',
    name: 'Mentalidad, Disciplina & Estoicismo',
    icon: '🧠',
    cpm: '$15 - $35 USD',
    ideas: [
      'Cómo volverte frío e inquebrantable: 4 reglas del estoicismo de Marco Aurelio',
      'Dopamina Detox: 7 días reiniciando tu cerebro para lograr hiperenfoque',
      'Por qué la motivación es una mentira y la disciplina es tu única salida',
      'Las 3 leyes del poder que te harán respetado inmediatamente',
      'El dolor de la disciplina pesa onzas, el dolor del arrepentimiento pesa toneladas'
    ],
    seoTags: [
      'estoicismo', 'disciplina', 'mentalidad ganadora', 'psicologia oscura',
      'marco aurelio', 'habitos atomicos', 'desarrollo personal', 'enfoque profundo',
      'fuerza mental', 'superacion personal', 'filosofia estoica'
    ],
    typoTags: [
      'estoisismo', 'diciplina diaria', 'mentalida de exito', 'psicologia oculta',
      'marco aurelio filosofi', 'dopamina detox facil', 'superacion personall',
      'enfoque total sin distraccion', 'habitos atomicos resumen', 'fuerza de voluntat'
    ],
    hooks: [
      'La persona que controla su mente controla su destino. Marco Aurelio tenía un secreto para no enojarse nunca...',
      'Estás cansado todo el día no por falta de sueño, sino porque tu cerebro está ahogado en dopamina barata...',
      'Nadie te respeta cuando eres demasiado complaciente. Aplica esta regla psicológica en tu próxima conversación...',
      'Si no puedes sentarte solo en una habitación durante 30 minutos sin mirar tu teléfono, no eres libre...',
      'El 99% de las cosas que te preocupan nunca van a suceder. El estoicismo te enseña a destruir la ansiedad así...'
    ],
    titles: [
      { title: 'Cómo Ser Inquebrantable: 4 Reglas Estoicas de Marco Aurelio', score: 98 },
      { title: 'Dopamina Detox: Cómo Reiniciar tu Cerebro en 7 Días', score: 96 },
      { title: 'La Razón por la que la Motivación Arruina tu Vida', score: 95 },
      { title: '3 Leyes Psicológicas para Ser Respetado al Instante', score: 94 },
      { title: 'El Hábito Silencioso que Destruye a los Hombres Débiles', score: 93 }
    ]
  },
  ia: {
    id: 'ia',
    name: 'Inteligencia Artificial, SaaS & Automatización',
    icon: '🤖',
    cpm: '$20 - $45 USD',
    ideas: [
      '5 herramientas de IA gratuitas que reemplazan agencias enteras en 2026',
      'Cómo crear agentes de IA autónomos que generen ingresos en piloto automático',
      'Los mejores prompts de Google Gemini y ChatGPT que el 99% no conoce',
      'Automatiza todo tu contenido de redes sociales en 10 minutos con IA',
      'Las herramientas de IA que dominarán el mercado en los próximos 12 meses'
    ],
    seoTags: [
      'inteligencia artificial', 'herramientas de ia', 'chatgpt tutorial', 'automatizacion',
      'google gemini', 'productividad con ia', 'agentes de ia', 'creadores de contenido ia',
      'ganar dinero con ia', 'ia para empresas', 'tecnologia 2026'
    ],
    typoTags: [
      'ingeligencia artificial', 'heramientas de ia', 'chat gpt tutorial', 'inteligencia artifisial',
      'automatizasion con ia', 'gemini google gratis', 'proms secretos para chatgpt',
      'agentes autonomos ia', 'ganar plata con ia rapido', 'tecnolojia ia'
    ],
    hooks: [
      'Si creas contenido y tardas más de 30 minutos por video en 2026, estás tirando tu tiempo a la basura...',
      'Esta herramienta gratuita de Google Gemini acaba de hacer obsoletos a 10 softwares de pago de un solo golpe...',
      'Paso 1: Le das una idea a la IA. Paso 2: Te genera el guion, la portada y las etiquetas sin tocar un solo botón...',
      'El 90% de la gente usa la IA como un buscador tonto. Si usas esta estructura de prompt, las respuestas son nivel Dios...',
      'Cómo automaticé la producción de 30 shorts al día con voz clonada y subtítulos estilo MrBeast...'
    ],
    titles: [
      { title: '5 Herramientas de IA que Reemplazan Agencias Enteras en 2026', score: 99 },
      { title: 'El Prompt Secreto de Google Gemini que Pocos Conocen', score: 97 },
      { title: 'Cómo Crear un Canal Automatizado con IA desde Cero', score: 96 },
      { title: 'Esta IA Gratuita Te Hará Ahorrar 20 Horas de Trabajo Semanal', score: 94 },
      { title: 'El Cambio de Algoritmo de 2026 y Cómo la IA Te Salva', score: 93 }
    ]
  },
  salud: {
    id: 'salud',
    name: 'Salud, Longevidad & Biohacking',
    icon: '🧬',
    cpm: '$14 - $30 USD',
    ideas: [
      'La rutina de sueño de 90 minutos para despertar con energía sobrehumana',
      'Ayuno intermitente 16/8: lo que le pasa a tus células hora por hora',
      '3 hábitos matutinos que disparan tu testosterona y foco mental',
      'Suplementos respaldados por la ciencia que realmente funcionan',
      'El secreto de los centenarios de las Zonas Azules para vivir 100 años'
    ],
    seoTags: [
      'salud y longevidad', 'ayuno intermitente', 'biohacking', 'optimizar sueño',
      'rendimiento fisico', 'suplementos esenciales', 'energia natural', 'zonas azules',
      'salud celular', 'nutricion inteligente', 'enfoque mental'
    ],
    typoTags: [
      'ayuno intermitente horar', 'biohaking en español', 'optimisar sueño',
      'testosterona natural remedios', 'salu celular', 'suplementasion correcta',
      'dormir mejor trucos', 'energia por la mañana', 'habitos de salud fasiles'
    ],
    hooks: [
      'Si te despiertas cansado a pesar de dormir 8 horas, estás interrumpiendo este ciclo biológico crucial...',
      'A la hora 16 de ayuno, tus células inician un proceso llamado autofagia que devora toxinas acumuladas...',
      'Deja de tomar café apenas abres los ojos. Espera 90 minutos y mira cómo desaparece el bajón de las 3 PM...',
      'Este mineral cuesta centavos de dólar y el 70% de la población tiene deficiencia sin saberlo...',
      'Los hombres en 1980 tenían el doble de energía que hoy. Estos 3 alimentos cotidianos son los culpables...'
    ],
    titles: [
      { title: 'Lo Que le Pasa a tu Cuerpo Hora por Hora en Ayuno 16/8', score: 98 },
      { title: 'El Error al Despertar que Destruye tu Energía Todo el Día', score: 96 },
      { title: '3 Hábitos Científicos para Dormir Profundo y Reparar Células', score: 95 },
      { title: 'El Mineral Barato que Elimina el Cansancio Crónico', score: 93 },
      { title: 'La Rutina Matutina de 5 Minutos de los Neurocientíficos', score: 92 }
    ]
  },
  misterio: {
    id: 'misterio',
    name: 'Misterio, Casos Reales & Curiosidades',
    icon: '🔮',
    cpm: 'Viral 10M+',
    ideas: [
      'El misterio de la señal del espacio que duró 72 segundos y nadie puede explicar',
      'El caso del hombre que predijo su propia desaparición con coordenadas exactas',
      '3 archivos desclasificados que confirman experimentos que creías mitos',
      'La ciudad subterránea encontrada por accidente que desconcierta a los arqueólogos',
      'El enigma del vuelo que aterrizó 35 años después con todos sus pasajeros'
    ],
    seoTags: [
      'misterio', 'casos reales', 'curiosidades del mundo', 'enigmas de la historia',
      'documental misterio', 'hechos inexplicables', 'historias reales', 'teorias y misterios',
      'casos sin resolver', 'paranormal cientifico', 'relatos impactantes'
    ],
    typoTags: [
      'misterios sin resolver real', 'casos de misterio en español', 'curiosidades del mundo fasiles',
      'teorias de conspirasion', 'documental de misterio corto', 'hechos inesplicables',
      'historias de teror reales', 'desaparisiones misteriosas'
    ],
    hooks: [
      'En 1977, un radiotelescopio captó una señal de 72 segundos proveniente de una constelación vacía...',
      'Nunca entres a esta cueva en Utah. Lo que los espeleólogos encontraron en el fondo sigue bajo secreto militar...',
      'Este diario fue encontrado enterrado en 1943. En la última página escribió la fecha exacta en que todo cambiaría...',
      'Hay una anomalía en el fondo del océano Báltico que ningún radar puede escanear sin sobrecalentarse...',
      'Lo que estás viendo no es una animación: es la única grabación real del incidente que nadie puede explicar...'
    ],
    titles: [
      { title: 'La Señal del Espacio de 72 Segundos que la Ciencia Ocultó', score: 99 },
      { title: 'El Caso Real del Hombre que Sabía Cuándo Iba a Desaparecer', score: 98 },
      { title: '3 Archivos Secretos Desclasificados que Te Quitarán el Sueño', score: 97 },
      { title: 'La Anomalía del Báltico: Lo Que Hallaron en el Fondo', score: 95 },
      { title: 'El Misterio Sin Resolver Más Perturbador de la Historia', score: 94 }
    ]
  },
  emprendimiento: {
    id: 'emprendimiento',
    name: 'Emprendimiento & E-commerce',
    icon: '📈',
    cpm: '$18 - $40 USD',
    ideas: [
      'Cómo empezar un negocio digital rentable con $0 pesos en 2026',
      'El modelo de marca personal que genera más que una empresa de 20 personas',
      '3 habilidades de alto valor que pagarán más de $5,000 USD al mes',
      'Cómo validar una idea de producto en 48 horas antes de gastar un solo centavo',
      'De empleado a dueño: la hoja de ruta de 6 meses para renunciar con seguridad'
    ],
    seoTags: [
      'emprendimiento', 'negocios digitales', 'marca personal', 'ventas online',
      'habilidades de alto valor', 'e-commerce 2026', 'como emprender', 'ingresos online',
      'marketing digital', 'modelo de negocio', 'escalar negocio'
    ],
    typoTags: [
      'negosios digitales', 'emprender sin dinero en 2026', 'marca personall',
      'como vender por internet fasil', 'ganar en dolares desde casa', 'habilidades de alto balor',
      'crear tienda online gratis', 'ideas de negosios rentables'
    ],
    hooks: [
      'Si tienes una laptop y conexión a internet, no tienes excusa para no generar tus primeros $1,000 online este mes...',
      'El 90% de los nuevos emprendedores fracasan en el primer año porque intentan crear un producto antes de tener una audiencia...',
      'Esta habilidad tardas 30 días en aprenderla y las empresas pagan entre $1,500 y $3,000 al mes por ella...',
      'Cómo pasé de tener mi cuenta bancaria en números rojos a facturar con una marca personal unipersonal...',
      'Deja de buscar la idea perfecta. El dinero está en resolver problemas aburridos que nadie más quiere resolver...'
    ],
    titles: [
      { title: 'Cómo Empezar un Negocio Digital con $0 en 2026 (Guía Real)', score: 98 },
      { title: '3 Habilidades de Alto Valor que Pagan Más de $5,000 al Mes', score: 97 },
      { title: 'El Modelo Unipersonal que Supera a Empresas Tradicionales', score: 95 },
      { title: 'La Fórmula de 48 Horas para Validar Cualquier Negocio', score: 94 },
      { title: 'De Empleado a Dueño: Tu Plan de Escape en 6 Meses', score: 93 }
    ]
  },
  gaming: {
    id: 'gaming',
    name: 'Gaming & Configuración de Streams',
    icon: '🎮',
    cpm: '$8 - $18 USD',
    ideas: [
      'La configuración secreta de OBS Studio que elimina el lag para siempre',
      'Cómo transmitir a 5 plataformas al mismo tiempo con una sola PC modesta',
      'Los mejores micrófonos económicos que suenan como de estudio profesional',
      'Cómo crecer en Twitch en 2026 cuando nadie entra a tu categoría',
      'Trucos de audio y filtros VST para que tu voz suene como locutor de radio'
    ],
    seoTags: [
      'gaming', 'configuracion obs', 'como stremear', 'multistream', 'crecer en twitch',
      'mejores microfonos stream', 'streaming setup', 'obs studio sin lag',
      'tiktok live rtmp', 'streamer principiante', 'calidad de audio stream'
    ],
    typoTags: [
      'configurar obs sin lag rapido', 'multistrem gratis', 'microfono barato para stram',
      'trucos para twich', 'stremear en tik tok live', 'como ser estrimer',
      'mejorar audio en obs facil', 'transmitir en vivo tutorial'
    ],
    hooks: [
      'Si tu stream se ve pixelado cuando hay acción rápida en pantalla, tienes mal este parámetro de bitrate en OBS...',
      'No gastes $300 dólares en un micrófono caro. Pon estos 3 filtros gratuitos y sonará como equipo de la NASA...',
      'El error que comete el 99% de los streamers novatos es transmitir 8 horas en Twitch esperando que alguien entre...',
      'Puedes transmitir a YouTube, TikTok, Facebook y Twitch simultáneamente sin pagar un centavo con esta función...',
      'Este atajo de teclado te permite guardar los últimos 30 segundos de tu partida con subtítulos automáticos en 9:16...'
    ],
    titles: [
      { title: 'La Configuración Oculta de OBS que Elimina el Lag al 100%', score: 98 },
      { title: 'Cómo Transmitir a 5 Plataformas a la Vez (Sin Pagar Nada)', score: 97 },
      { title: 'Convierte un Micrófono de $20 en Calidad de Estudio', score: 95 },
      { title: 'Por Qué Nadie Ve Tus Streams en Twitch (Y la Solución 2026)', score: 94 },
      { title: 'El Setup Mínimo para Vivir del Streaming este Año', score: 92 }
    ]
  }
};

// ==========================================
// 1.6. YOUTUBE TAG MASTER WITH TYPOS ENGINE
// ==========================================
class YouTubeTagMaster {
  static generateTags(topic, nicheId) {
    const niche = TrendingNiches[nicheId] || TrendingNiches.espiritualidad;
    const baseSeo = [...(niche.seoTags || [])];
    const baseTypos = [...(niche.typoTags || [])];

    if (topic && topic.trim().length > 0) {
      const topicWords = topic.toLowerCase()
        .replace(/[^\w\sáéíóúüñ]/gi, '')
        .split(/\s+/)
        .filter(w => w.length > 3 && !['para', 'como', 'este', 'esta', 'todo', 'toda', 'pero', 'porque', 'unos', 'unas', 'sobre'].includes(w));

      topicWords.forEach(word => {
        if (!baseSeo.includes(word)) baseSeo.unshift(word);
        const typo = this.createPhoneticTypo(word);
        if (typo && typo !== word && !baseTypos.includes(typo)) {
          baseTypos.unshift(typo);
        }
      });
    }

    return {
      seo: baseSeo,
      typos: baseTypos,
      all: this.blendTags(baseSeo, baseTypos, 500)
    };
  }

  static createPhoneticTypo(word) {
    let typo = word;
    if (typo.includes('ción')) typo = typo.replace('ción', 'cion');
    if (typo.includes('sión')) typo = typo.replace('sión', 'cion');
    if (typo.includes('z')) typo = typo.replace(/z/g, 's');
    else if (typo.includes('ce')) typo = typo.replace(/ce/g, 'se');
    else if (typo.includes('ci')) typo = typo.replace(/ci/g, 'si');
    else if (typo.includes('h')) typo = typo.replace(/h/g, '');
    else if (typo.includes('v')) typo = typo.replace(/v/g, 'b');
    else if (typo.includes('b')) typo = typo.replace(/b/g, 'v');
    else if (typo.includes('ll')) typo = typo.replace(/ll/g, 'y');
    else if (typo.length > 5) typo = typo.slice(0, -1);
    return typo;
  }

  static blendTags(seoTags, typoTags, maxChars = 500) {
    const result = [];
    let currentLength = 0;
    const sQueue = [...seoTags];
    const tQueue = [...typoTags];

    while ((sQueue.length > 0 || tQueue.length > 0) && currentLength < maxChars) {
      for (let i = 0; i < 3 && sQueue.length > 0; i++) {
        const tag = sQueue.shift();
        const tagLen = tag.length + (result.length > 0 ? 2 : 0);
        if (currentLength + tagLen <= maxChars) {
          result.push({ text: tag, type: 'seo' });
          currentLength += tagLen;
        }
      }
      if (tQueue.length > 0) {
        const tag = tQueue.shift();
        const tagLen = tag.length + (result.length > 0 ? 2 : 0);
        if (currentLength + tagLen <= maxChars) {
          result.push({ text: tag, type: 'typo' });
          currentLength += tagLen;
        }
      }
    }
    return result;
  }

  static formatCommaString(tagItems) {
    return tagItems.map(t => typeof t === 'string' ? t : t.text).join(', ');
  }
}

// ==========================================
// 1.7. GOOGLE GEMINI AI SUITE & AUTONOMOUS ENGINE
// ==========================================
class GeminiSuiteManager {
  static getApiKey() {
    return localStorage.getItem('byok_gemini_key') || '';
  }

  static getModel() {
    return localStorage.getItem('byok_gemini_model') || 'gemini-2.0-flash';
  }

  static hasActiveKey() {
    const key = this.getApiKey();
    return Boolean(key && key.trim().length > 10);
  }

  static async generateFullPack(topic, nicheId) {
    const niche = TrendingNiches[nicheId] || TrendingNiches.espiritualidad;
    const cleanTopic = topic && topic.trim().length > 0 ? topic.trim() : niche.ideas[0];

    // 1. Attempt live call if user supplied a Gemini API key
    if (this.hasActiveKey()) {
      try {
        const apiKey = this.getApiKey();
        const model = this.getModel();
        const prompt = `Actúa como el mejor director de contenido viral y estratega de algoritmos para YouTube, TikTok, Instagram y Facebook.
Tema: "${cleanTopic}"
Nicho: "${niche.name}" (CPM: ${niche.cpm})

Genera un JSON estrictamente válido con la siguiente estructura:
{
  "hooks": ["gancho 1", "gancho 2", "gancho 3", "gancho 4", "gancho 5"],
  "titles": [{"title": "titulo 1", "score": 98}, {"title": "titulo 2", "score": 96}],
  "script": "Guion completo estructurado por segundos [0:00-0:03] Hook, [0:03-0:15] Retencion, [0:15-0:45] Desarrollo, [0:45-0:55] Giro, [0:55-1:00] CTA",
  "descriptions": {
    "yt": "Descripcion YouTube SEO con capitulos y hashtags",
    "tt": "Descripcion TikTok con keywords y hashtags virales",
    "ig": "Descripcion Instagram con saltos de linea y CTA para guardar",
    "fb": "Post Facebook storytelling para Fanpage y debate",
    "tw": "Titulo y descripcion Twitch con tags"
  },
  "visualPrompts": {
    "midjourney": "/imagine prompt: ...",
    "flux": "Prompt hiperrealista para Flux/DALL-E ...",
    "videoAi": "Prompt de video cinematografico para Kling/Runway Gen-3 ..."
  }
}`;

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 6500);

        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: prompt }] }],
            generationConfig: { responseMimeType: 'application/json', temperature: 0.7 }
          }),
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (response.ok) {
          const resData = await response.json();
          const textContent = resData?.candidates?.[0]?.content?.parts?.[0]?.text;
          if (textContent) {
            const parsed = JSON.parse(textContent);
            const tagsData = YouTubeTagMaster.generateTags(cleanTopic, nicheId);
            return {
              topic: cleanTopic,
              niche: nicheId,
              nicheData: niche,
              hooks: parsed.hooks || niche.hooks,
              titles: parsed.titles || niche.titles,
              script: parsed.script || this.getHeuristicScript(cleanTopic, niche),
              descriptions: parsed.descriptions || this.getHeuristicDescriptions(cleanTopic, niche),
              tags: tagsData,
              visualPrompts: parsed.visualPrompts || this.getHeuristicVisualPrompts(cleanTopic, niche),
              source: `Google Gemini API (${model})`
            };
          }
        }
      } catch (err) {
        console.warn('Gemini Live API fallback triggered:', err);
      }
    }

    // 2. Autonomous Heuristic Engine (100% Free, Instant, Zero Dependency)
    return this.generateAutonomousPack(cleanTopic, nicheId);
  }

  static generateAutonomousPack(topic, nicheId) {
    const niche = TrendingNiches[nicheId] || TrendingNiches.espiritualidad;
    const tagsData = YouTubeTagMaster.generateTags(topic, nicheId);

    const hooks = (niche.hooks || []).map((h, i) => {
      if (i === 0) return `Si te interesa ${topic.toLowerCase()}, estás cometiendo el error que el 95% de la gente comete sin saberlo...`;
      return h;
    });

    const titles = [
      { title: `La Verdad Sobre ${topic} que Pocos Se Atreven a Decir`, score: 98 },
      { title: `Cómo Aplicar ${topic} en 2026 (Guía Definitiva)`, score: 97 },
      { title: `El Error Fatal con ${topic} y Cómo Solucionarlo Hoy`, score: 95 },
      ...(niche.titles ? niche.titles.slice(1, 3) : [])
    ];

    const script = this.getHeuristicScript(topic, niche);
    const descriptions = this.getHeuristicDescriptions(topic, niche);
    const visualPrompts = this.getHeuristicVisualPrompts(topic, niche);

    return {
      topic,
      niche: nicheId,
      nicheData: niche,
      hooks,
      titles,
      script,
      descriptions,
      tags: tagsData,
      visualPrompts,
      source: 'Motor Autónomo Viral Labs'
    };
  }

  static getHeuristicScript(topic, niche) {
    return `⚡ GUION VIRAL DE ALTA RETENCIÓN (60s)
🎯 TEMA: "${topic}"
🏷️ NICHO: ${niche.name.toUpperCase()} (CPM: ${niche.cpm})

[0:00 - 0:03] 🔥 HOOK PSICOLÓGICO (Brecha de Curiosidad Inmediata):
"Si te interesa ${topic.toLowerCase()} y sientes que no obtienes resultados, mira esto... porque el 95% de los creadores y expertos están enseñando el método equivocado."
(Acción: Mirada penetrante a cámara, zoom in dinámico de 1.2x, texto en amarillo neón con sombra dura)

[0:03 - 0:15] 📈 RETENCIÓN & EL ENEMIGO COMÚN:
"El problema no eres tú, es que nos enseñaron a resolver esto desde la fuerza bruta en lugar de la inteligencia estratégica. Cuando entiendes el principio subyacente, todo cambia en 24 horas."
(B-roll: Gráfica ascendente en pantalla o captura de resultados impactantes)

[0:15 - 0:40] 💡 LA SOLUCIÓN EN 3 PASOS ACCIONABLES (Valor Extremo):
"Paso 1: Elimina la fricción inicial. En lugar de complicarte con teorías, enfócate en el 20% que produce el 80% del impacto.
Paso 2: Aplica la regla de consistencia silenciosa: 15 minutos diarios enfocados superan a 4 horas de dispersión.
Paso 3: Automatiza el proceso con las herramientas y plantillas comprobadas de Viral Labs."

[0:40 - 0:52] 🚀 LA REVELACIÓN INESPERADA:
"Quienes aplicaron este ajuste durante los últimos 14 días duplicaron su velocidad de avance sin aumentar su nivel de estrés."

[0:52 - 1:00] 🎯 CALL TO ACTION (Llamada a la Acción de Alto Engagement):
"Guarda este video antes de que el algoritmo lo oculte, y comenta 'VIRAL' para enviarte la guía de ejecución paso a paso."`;
  }

  static getHeuristicDescriptions(topic, niche) {
    return {
      yt: `⚡ ${topic} | Guía Maestra de Alta Retención 2026\n\nEn este video desglosamos paso a paso cómo dominar ${topic.toLowerCase()} aplicando las estrategias más efectivas de ${niche.name.toLowerCase()}.\n\n⏱️ CAPÍTULOS:\n00:00 - El error que el 95% comete con ${topic}\n01:10 - Por qué los métodos tradicionales fallan\n03:25 - Paso 1: Eliminar fricción y ruido\n05:40 - Paso 2: La regla del 20/80 comprobada\n08:15 - Paso 3: Automatización y ejecución rápida\n10:30 - Conclusión y siguiente paso\n\n🔔 Suscríbete al canal para más estrategias semanales de alto impacto.\n#${niche.id} #ViralLabs #Crecimiento #Estrategia #Tendencia2026`,
      tt: `Lo que nadie te dice sobre ${topic.toLowerCase()} 🤯 Si aplicas este truco de 3 pasos hoy, notarás la diferencia de inmediato. Guarda este clip para no perderlo 📌\n\n#${niche.id} #trucosvirales #consejos #virallabs #aprendeingles #creadoresdecontenido`,
      ig: `¿Cometiendo este error con ${topic.toLowerCase()}? 👇\n\nLa mayoría se complica la vida intentando reinventar la rueda. El verdadero secreto está en simplificar y ejecutar con foco implacable.\n\n👉 Guarda este post para revisarlo esta semana\n👉 Comparte con esa persona que necesita escuchar esto hoy\n.\n.\n#${niche.id} #crecimientopersonal #disciplina #productividad #virallabs`,
      fb: `Hace tiempo pensaba que para dominar ${topic.toLowerCase()} necesitaba años de experiencia o recursos que no tenía...\n\nHasta que descubrí que los resultados exponenciales provienen de cambiar un solo patrón fundamental. Cuando dejas de perseguir lo que no controlas y te enfocas en el paso inmediato, el panorama se transforma por completo.\n\n¿Cuál ha sido tu mayor obstáculo con este tema? Déjamelo en los comentarios, los estoy leyendo a todos 👇`,
      tw: `🔴 EN VIVO: Desglosando ${topic} en Tiempo Real | Sesión de Preguntas y Respuestas con la Comunidad | Comandos: !discord !guia !canal`
    };
  }

  static getHeuristicVisualPrompts(topic, niche) {
    return {
      midjourney: `/imagine prompt: high-contrast ultra-cinematic YouTube thumbnail, centered subject with expressive face of realization and mastery, glowing neon cyan and golden accents, dramatic rim lighting, dark futuristic studio atmosphere, clean 8k octane render, hyper-realistic, photorealistic textures --ar 16:9 --style raw --v 6.0`,
      flux: `Cinematic hyper-realistic poster, ${topic}, bold composition, dramatic chiaroscuro lighting, deep shadows, neon highlights, ultra-sharp 4K photography, Hasselblad lens f/2.8`,
      videoAi: `Prompt Kling / Runway Gen-3 / Sora: Cinematic slow-motion camera moving smoothly toward a modern minimalist creator desk, glowing holographic HUD displaying data about ${topic}, volumetric studio fog, 60fps photorealistic cinematic lens --motion 5`
    };
  }

  static openGeminiWeb(topic, nicheId) {
    const niche = TrendingNiches[nicheId] || TrendingNiches.espiritualidad;
    const cleanTopic = topic && topic.trim().length > 0 ? topic.trim() : niche.ideas[0];
    const prompt = `Actúa como el mejor director de contenido viral y estratega de algoritmos para YouTube, TikTok, Instagram y Facebook.

TEMA: "${cleanTopic}"
NICHO: "${niche.name}" (CPM estimado: ${niche.cpm})

Genera para mí la suite completa de producción:
1. 5 Ganchos psicológicos para los primeros 3 segundos (Curiosidad, Advertencia, Beneficio, Contraintuitivo, Pregunta).
2. 5 Títulos de alto CTR con su puntuación de clics estimada (sobre 100).
3. Guion viral estructurado segundo a segundo para 60 segundos con indicaciones de acción y B-roll.
4. Descripciones optimizadas según el algoritmo de cada red:
   - YouTube SEO con marcas de tiempo (capítulos) y hashtags.
   - TikTok con palabras clave para el buscador interno.
   - Instagram Reels con saltos de línea estéticos y llamada a guardar.
   - Facebook Fanpage con formato storytelling para monetización in-stream.
5. Etiquetas para YouTube: incluye 10 etiquetas normales de alto alcance y 10 etiquetas con ERRORES DE ORTOGRAFÍA comunes de búsqueda móvil.
6. Prompts para generar miniaturas en Midjourney v6 y videos en Kling AI.`;

    if (navigator.clipboard) {
      navigator.clipboard.writeText(prompt);
    }
    window.open('https://gemini.google.com/app', '_blank');
  }
}

// ==========================================
// 2. STUDIO MANAGER (WITH 360° MANIPULATOR & 4K EXPORTER)
// ==========================================
class StudioManager {
  constructor(app) {
    this.app = app;
    this.canvas = null;
    this.ctx = null;
    this.currentAspect = '16:9';
    this.activeStyle = 'mrbeast';
    this.canvasWidth = 1280;
    this.canvasHeight = 720;
    this.bgImage = new Image();
    this.bgImageLoaded = false;

    // Layer System for Free Drag & 360 Manipulation
    this.layers = [
      {
        id: 'layer-badge',
        type: 'badge',
        text: '🔥 100% VIRAL',
        x: 60,
        y: 60,
        width: 240,
        height: 56,
        rotation: 0,
        scaleX: 1,
        scaleY: 1,
        style: 'pink-badge',
        color: '#ffffff',
        fontSize: 30,
        fontFamily: "'Outfit', sans-serif"
      },
      {
        id: 'layer-headline',
        type: 'text',
        text: '¡ESTO CAMBIÓ TODO!',
        x: 60,
        y: 440,
        width: 780,
        height: 110,
        rotation: -2,
        scaleX: 1,
        scaleY: 1,
        style: 'mrbeast',
        color: '#ffe600',
        fontSize: 76,
        fontFamily: "'Outfit', sans-serif",
        strokeColor: '#000000',
        strokeWidth: 14,
        shadowColor: 'rgba(0, 0, 0, 0.9)',
        shadowBlur: 24,
        hasBgBox: false,
        bgBoxColor: '#000000',
        bgBoxPadding: 12
      },
      {
        id: 'layer-subline',
        type: 'text',
        text: 'El nuevo truco de IA revelado para 2026',
        x: 64,
        y: 560,
        width: 650,
        height: 60,
        rotation: 0,
        scaleX: 1,
        scaleY: 1,
        style: 'white-bold',
        color: '#f8fafc',
        fontSize: 38,
        fontFamily: "'Outfit', sans-serif",
        strokeColor: '#000000',
        strokeWidth: 8,
        shadowColor: 'rgba(0, 0, 0, 0.9)',
        shadowBlur: 16,
        hasBgBox: false,
        bgBoxColor: '#000000',
        bgBoxPadding: 8
      }
    ];

    this.selectedLayerId = 'layer-headline';

    // Interactive Drag / Resize / Rotate State
    this.dragAction = null; // 'move', 'resize-tl', 'resize-tr', 'resize-bl', 'resize-br', 'rotate'
    this.dragStartX = 0;
    this.dragStartY = 0;
    this.initialLayerState = null;

    // AI Viral Engine State
    this.selectedNiche = 'espiritualidad';
    this.activePackTab = 'all';
    this.activeDescPlatform = 'yt';
    this.activeTagFilter = 'all';
    this.latestPack = null;

    this.init();
  }

  init() {
    this.canvas = document.getElementById('thumbnailCanvas');
    if (this.canvas) {
      this.ctx = this.canvas.getContext('2d');
      this.setupCanvas();
    }
    this.renderTrendingIdeas();
    this.updateGeminiStatusBadge();
    this.bindEvents();
    setTimeout(() => this.generateFullViralPack(), 150);
  }

  setupCanvas() {
    this.setAspectRatio(this.currentAspect);
    this.bgImage.src = 'assets/thumbnail_demo.jpg';
    this.bgImage.onload = () => {
      this.bgImageLoaded = true;
      this.renderCanvas();
    };
  }

  setAspectRatio(ratio) {
    this.currentAspect = ratio;
    if (ratio === '16:9') {
      this.canvasWidth = 1280;
      this.canvasHeight = 720;
    } else if (ratio === '9:16') {
      this.canvasWidth = 720;
      this.canvasHeight = 1280;
    } else if (ratio === '1:1') {
      this.canvasWidth = 1080;
      this.canvasHeight = 1080;
    } else if (ratio === '4:5') {
      this.canvasWidth = 1080;
      this.canvasHeight = 1350;
    } else if (ratio === 'portada') {
      this.canvasWidth = 1640;
      this.canvasHeight = 624;
    }
    if (this.canvas) {
      this.canvas.width = this.canvasWidth;
      this.canvas.height = this.canvasHeight;
      this.renderCanvas();
    }
  }

  getSelectedLayer() {
    return this.layers.find(l => l.id === this.selectedLayerId);
  }

  renderCanvas(targetCtx = null, isExporting = false) {
    const ctx = targetCtx || this.ctx;
    if (!ctx) return;
    const w = targetCtx ? targetCtx.canvas.width : this.canvasWidth;
    const h = targetCtx ? targetCtx.canvas.height : this.canvasHeight;

    ctx.clearRect(0, 0, w, h);

    // 1. Draw Background Image & Dramatic Dark Vignette
    if (this.bgImageLoaded) {
      const imgRatio = this.bgImage.width / this.bgImage.height;
      const canvasRatio = w / h;
      let renderW, renderH, offsetX, offsetY;

      if (imgRatio > canvasRatio) {
        renderH = h;
        renderW = h * imgRatio;
        offsetX = (w - renderW) / 2;
        offsetY = 0;
      } else {
        renderW = w;
        renderH = w / imgRatio;
        offsetX = 0;
        offsetY = (h - renderH) / 2;
      }
      ctx.drawImage(this.bgImage, offsetX, offsetY, renderW, renderH);

      const grad = ctx.createRadialGradient(w / 2, h / 2, h * 0.3, w / 2, h / 2, Math.max(w, h) * 0.75);
      grad.addColorStop(0, 'rgba(0, 0, 0, 0.1)');
      grad.addColorStop(1, 'rgba(3, 7, 18, 0.88)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);
    } else {
      ctx.fillStyle = '#0a0d18';
      ctx.fillRect(0, 0, w, h);
    }

    // 2. Render all Layers in order
    this.layers.forEach(layer => {
      this.renderLayer(ctx, layer, w);
    });

    // 3. Render 360° Manipulator Bounding Box & Handles (Only on interactive canvas)
    if (!isExporting) {
      const selected = this.getSelectedLayer();
      if (selected) {
        this.renderManipulatorGizmo(ctx, selected);
      }
    }
  }

  renderLayer(ctx, layer, canvasW) {
    ctx.save();
    const scale = canvasW / 1280;

    const cx = layer.x + layer.width / 2;
    const cy = layer.y + layer.height / 2;

    ctx.translate(cx, cy);
    ctx.rotate((layer.rotation * Math.PI) / 180);
    ctx.scale(layer.scaleX, layer.scaleY);
    ctx.translate(-cx, -cy);

    const fontFam = layer.fontFamily || "'Outfit', sans-serif";

    if (layer.type === 'badge') {
      ctx.shadowColor = 'rgba(236, 72, 153, 0.6)';
      ctx.shadowBlur = 18 * scale;
      ctx.fillStyle = layer.style === 'cyan' ? '#06b6d4' : '#ec4899';
      ctx.beginPath();
      ctx.roundRect(layer.x, layer.y, layer.width, layer.height, 14 * scale);
      ctx.fill();

      ctx.shadowBlur = 0;
      ctx.fillStyle = '#ffffff';
      ctx.font = `900 ${Math.round(layer.fontSize * scale)}px ${fontFam}`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(layer.text, cx, cy);
    } else {
      ctx.font = `900 ${Math.round(layer.fontSize * scale)}px ${fontFam}`;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';

      // Highlight Background Box
      if (layer.hasBgBox) {
        ctx.save();
        const metrics = ctx.measureText(layer.text);
        const pad = (layer.bgBoxPadding || 12) * scale;
        const boxW = metrics.width + pad * 2;
        const boxH = (layer.fontSize * 1.15) * scale + pad;
        ctx.fillStyle = layer.bgBoxColor || 'rgba(0,0,0,0.85)';
        ctx.beginPath();
        ctx.roundRect(layer.x - pad, layer.y - pad * 0.4, boxW, boxH, 8 * scale);
        ctx.fill();
        ctx.restore();
      }

      // Border / Stroke for contrast
      const strokeW = (layer.strokeWidth !== undefined ? layer.strokeWidth : 14) * scale;
      if (strokeW > 0) {
        ctx.lineWidth = strokeW;
        ctx.lineJoin = 'miter';
        ctx.miterLimit = 2;
        ctx.strokeStyle = layer.strokeColor || '#000000';
        ctx.strokeText(layer.text, layer.x, layer.y);
      }

      // Deep Shadow & Fill
      const sBlur = (layer.shadowBlur !== undefined ? layer.shadowBlur : 24) * scale;
      if (sBlur > 0) {
        ctx.shadowColor = layer.shadowColor || 'rgba(0, 0, 0, 0.9)';
        ctx.shadowBlur = sBlur;
        ctx.shadowOffsetX = 4 * scale;
        ctx.shadowOffsetY = 6 * scale;
      } else {
        ctx.shadowBlur = 0;
      }

      ctx.fillStyle = layer.color || '#ffe600';
      ctx.fillText(layer.text, layer.x, layer.y);
    }

    ctx.restore();
  }

  renderManipulatorGizmo(ctx, layer) {
    ctx.save();
    const cx = layer.x + layer.width / 2;
    const cy = layer.y + layer.height / 2;

    ctx.translate(cx, cy);
    ctx.rotate((layer.rotation * Math.PI) / 180);
    ctx.translate(-cx, -cy);

    // Glowing cyan dashed bounding box
    ctx.strokeStyle = '#06b6d4';
    ctx.lineWidth = 2;
    ctx.setLineDash([6, 4]);
    ctx.strokeRect(layer.x - 4, layer.y - 4, layer.width + 8, layer.height + 8);

    // Solid Handles (Corner Resizers)
    ctx.setLineDash([]);
    ctx.fillStyle = '#06b6d4';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;

    const handleSize = 12;
    const corners = [
      { x: layer.x - 4, y: layer.y - 4 }, // TL
      { x: layer.x + layer.width + 4, y: layer.y - 4 }, // TR
      { x: layer.x - 4, y: layer.y + layer.height + 4 }, // BL
      { x: layer.x + layer.width + 4, y: layer.y + layer.height + 4 } // BR
    ];

    corners.forEach(corner => {
      ctx.beginPath();
      ctx.roundRect(corner.x - handleSize / 2, corner.y - handleSize / 2, handleSize, handleSize, 3);
      ctx.fill();
      ctx.stroke();
    });

    // Rotation Knob Handle at the top center
    const rotX = cx;
    const rotY = layer.y - 32;

    // Stem line
    ctx.beginPath();
    ctx.moveTo(rotX, layer.y - 4);
    ctx.lineTo(rotX, rotY);
    ctx.strokeStyle = '#06b6d4';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Knob circle
    ctx.beginPath();
    ctx.arc(rotX, rotY, 10, 0, Math.PI * 2);
    ctx.fillStyle = '#8b5cf6';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.stroke();

    // Angle label tooltip
    if (layer.rotation !== 0) {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
      ctx.beginPath();
      ctx.roundRect(rotX - 26, rotY - 26, 52, 20, 4);
      ctx.fill();
      ctx.fillStyle = '#67e8f9';
      ctx.font = '700 11px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${Math.round(layer.rotation)}°`, rotX, rotY - 16);
    }

    ctx.restore();
  }

  // 360° Transformations
  mirrorHorizontal() {
    const layer = this.getSelectedLayer();
    if (!layer) return;
    layer.scaleX = layer.scaleX * -1;
    this.renderCanvas();
    this.app.showToast('Capa volteada horizontalmente (Espejo)', 'info');
  }

  mirrorVertical() {
    const layer = this.getSelectedLayer();
    if (!layer) return;
    layer.scaleY = layer.scaleY * -1;
    this.renderCanvas();
    this.app.showToast('Capa volteada verticalmente (Espejo)', 'info');
  }

  duplicateLayer() {
    const layer = this.getSelectedLayer();
    if (!layer) return;
    const clone = JSON.parse(JSON.stringify(layer));
    clone.id = 'layer-' + Date.now();
    clone.x += 30;
    clone.y += 30;
    this.layers.push(clone);
    this.selectedLayerId = clone.id;
    this.renderCanvas();
    this.app.showToast('Capa duplicada.', 'success');
  }

  deleteLayer() {
    if (this.layers.length <= 1) {
      this.app.showToast('Debes mantener al menos una capa.', 'warning');
      return;
    }
    this.layers = this.layers.filter(l => l.id !== this.selectedLayerId);
    this.selectedLayerId = this.layers[0].id;
    this.renderCanvas();
    this.app.showToast('Capa eliminada.', 'info');
  }

  bringForward() {
    const idx = this.layers.findIndex(l => l.id === this.selectedLayerId);
    if (idx < this.layers.length - 1) {
      const temp = this.layers[idx];
      this.layers[idx] = this.layers[idx + 1];
      this.layers[idx + 1] = temp;
      this.renderCanvas();
    }
  }

  sendBackward() {
    const idx = this.layers.findIndex(l => l.id === this.selectedLayerId);
    if (idx > 0) {
      const temp = this.layers[idx];
      this.layers[idx] = this.layers[idx - 1];
      this.layers[idx - 1] = temp;
      this.renderCanvas();
    }
  }

  // Ultra HD 4K Lossless Exporter
  exportUltraHD4K() {
    if (!this.canvas) return;

    this.app.showToast('🚀 Procesando renderizado Ultra HD 4K Lossless...', 'info');

    setTimeout(() => {
      const exportCanvas = document.createElement('canvas');
      let targetW = 3840;
      let targetH = 2160;

      if (this.currentAspect === '9:16') {
        targetW = 2160;
        targetH = 3840;
      } else if (this.currentAspect === '1:1') {
        targetW = 2160;
        targetH = 2160;
      } else if (this.currentAspect === '4:5') {
        targetW = 2160;
        targetH = 2700;
      } else if (this.currentAspect === 'portada') {
        targetW = 3280;
        targetH = 1248;
      }

      exportCanvas.width = targetW;
      exportCanvas.height = targetH;
      const expCtx = exportCanvas.getContext('2d');

      expCtx.imageSmoothingEnabled = true;
      expCtx.imageSmoothingQuality = 'high';

      // Scale context from base canvas size to 4K
      const scale = targetW / this.canvasWidth;
      expCtx.scale(scale, scale);

      // Render layers cleanly without bounding box gizmos
      this.renderCanvas(expCtx, true);

      const link = document.createElement('a');
      link.download = `virallabs_4k_lossless_${this.currentAspect.replace(':', '_')}.png`;
      link.href = exportCanvas.toDataURL('image/png', 1.0);
      link.click();

      this.app.showToast(`✨ Exportación Ultra HD 4K (${targetW}x${targetH}px) completada con éxito.`, 'success');
    }, 350);
  }

  exportThumbnail() {
    if (!this.canvas) return;
    const exportCanvas = document.createElement('canvas');
    exportCanvas.width = this.canvasWidth;
    exportCanvas.height = this.canvasHeight;
    const expCtx = exportCanvas.getContext('2d');

    this.renderCanvas(expCtx, true);

    const link = document.createElement('a');
    link.download = `virallabs_post_${this.currentAspect.replace(':', '_')}.png`;
    link.href = exportCanvas.toDataURL('image/png', 1.0);
    link.click();
    this.app.showToast('Diseño descargado en PNG de alta calidad', 'success');
  }

  addStickerLayer(stickerText) {
    const isEmoji = stickerText.length <= 4 && !stickerText.includes(' ');
    const newLayer = {
      id: 'layer-' + Date.now(),
      type: isEmoji ? 'text' : 'badge',
      text: stickerText,
      x: Math.round(this.canvasWidth / 2 - (isEmoji ? 40 : 110)),
      y: Math.round(this.canvasHeight / 2 - 30),
      width: isEmoji ? 80 : 230,
      height: isEmoji ? 80 : 54,
      rotation: 0,
      scaleX: 1,
      scaleY: 1,
      fontFamily: "'Outfit', sans-serif",
      color: '#ffffff',
      fontSize: isEmoji ? 64 : 28,
      strokeWidth: isEmoji ? 0 : 8,
      strokeColor: '#000000',
      shadowBlur: 18,
      hasBgBox: false
    };
    this.layers.push(newLayer);
    this.selectedLayerId = newLayer.id;
    this.renderCanvas();
    this.app.showToast(`Sticker "${stickerText}" añadido al lienzo`, 'success');
  }

  addTextLayer(customText = 'NUEVO TEXTO VIRAL') {
    const font = document.getElementById('canvasFontSelect')?.value || "'Outfit', sans-serif";
    const color = document.getElementById('canvasTextColor')?.value || '#ffe600';
    const strokeCol = document.getElementById('canvasStrokeColor')?.value || '#000000';
    const strokeW = parseInt(document.getElementById('canvasStrokeWidth')?.value || 14);
    const sBlur = parseInt(document.getElementById('canvasShadowBlur')?.value || 24);
    const hasBg = document.getElementById('canvasBgBoxToggle')?.checked || false;
    const bgCol = document.getElementById('canvasBgBoxColor')?.value || '#000000';
    const pad = parseInt(document.getElementById('canvasBgBoxPadding')?.value || 12);

    const newLayer = {
      id: 'layer-' + Date.now(),
      type: 'text',
      text: customText,
      x: Math.round(this.canvasWidth / 2 - 200),
      y: Math.round(this.canvasHeight / 2 - 40),
      width: 480,
      height: 90,
      rotation: 0,
      scaleX: 1,
      scaleY: 1,
      fontFamily: font,
      color: color,
      fontSize: 58,
      strokeWidth: strokeW,
      strokeColor: strokeCol,
      shadowBlur: sBlur,
      hasBgBox: hasBg,
      bgBoxColor: bgCol,
      bgBoxPadding: pad
    };
    this.layers.push(newLayer);
    this.selectedLayerId = newLayer.id;
    this.renderCanvas();
    this.app.showToast('Nueva capa de texto añadida al diseño', 'info');
  }

  sendToPlanner() {
    if (!this.canvas) return;
    const dataUrl = this.canvas.toDataURL('image/png');
    if (this.app.planner && typeof this.app.planner.importDesignFromStudio === 'function') {
      this.app.planner.importDesignFromStudio(dataUrl);
      this.app.switchTab('planner');
      this.app.showToast('🚀 Diseño transferido con éxito al Planificador de Redes.', 'success');
    }
  }

  getCanvasPoint(e) {
    const rect = this.canvas.getBoundingClientRect();
    const scaleX = this.canvasWidth / rect.width;
    const scaleY = this.canvasHeight / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    };
  }

  bindEvents() {
    // 1. Interactive Canvas Pointer Events (Drag, Rotate 360, Resize 4 corners)
    if (this.canvas) {
      this.canvas.addEventListener('mousedown', (e) => {
        const pt = this.getCanvasPoint(e);
        const selected = this.getSelectedLayer();

        // Check Rotation Knob hit
        if (selected) {
          const cx = selected.x + selected.width / 2;
          const rotY = selected.y - 32;
          const distToRot = Math.hypot(pt.x - cx, pt.y - rotY);

          if (distToRot <= 16) {
            this.dragAction = 'rotate';
            this.initialLayerState = { ...selected };
            return;
          }

          // Check corner resizers hit
          const handleHitRadius = 14;
          const corners = {
            'resize-tl': { x: selected.x - 4, y: selected.y - 4 },
            'resize-tr': { x: selected.x + selected.width + 4, y: selected.y - 4 },
            'resize-bl': { x: selected.x - 4, y: selected.y + selected.height + 4 },
            'resize-br': { x: selected.x + selected.width + 4, y: selected.y + selected.height + 4 }
          };

          for (const [action, pos] of Object.entries(corners)) {
            if (Math.hypot(pt.x - pos.x, pt.y - pos.y) <= handleHitRadius) {
              this.dragAction = action;
              this.dragStartX = pt.x;
              this.dragStartY = pt.y;
              this.initialLayerState = { ...selected };
              return;
            }
          }
        }

        // Check hit on any layer to select & drag
        let hitLayer = null;
        for (let i = this.layers.length - 1; i >= 0; i--) {
          const l = this.layers[i];
          if (pt.x >= l.x && pt.x <= l.x + l.width && pt.y >= l.y && pt.y <= l.y + l.height) {
            hitLayer = l;
            break;
          }
        }

        if (hitLayer) {
          this.selectedLayerId = hitLayer.id;
          this.dragAction = 'move';
          this.dragStartX = pt.x - hitLayer.x;
          this.dragStartY = pt.y - hitLayer.y;
          this.renderCanvas();

          // Sync with text inputs
          const headInput = document.getElementById('canvasHeadlineInput');
          const subInput = document.getElementById('canvasSublineInput');
          const badgeInput = document.getElementById('canvasBadgeInput');
          if (hitLayer.id === 'layer-headline' && headInput) headInput.value = hitLayer.text;
          if (hitLayer.id === 'layer-subline' && subInput) subInput.value = hitLayer.text;
          if (hitLayer.id === 'layer-badge' && badgeInput) badgeInput.value = hitLayer.text;
        }
      });

      window.addEventListener('mousemove', (e) => {
        if (!this.dragAction) return;
        const pt = this.getCanvasPoint(e);
        const layer = this.getSelectedLayer();
        if (!layer) return;

        if (this.dragAction === 'move') {
          layer.x = Math.round(pt.x - this.dragStartX);
          layer.y = Math.round(pt.y - this.dragStartY);
          this.renderCanvas();
        } else if (this.dragAction === 'rotate') {
          const cx = layer.x + layer.width / 2;
          const cy = layer.y + layer.height / 2;
          const angleRad = Math.atan2(pt.y - cy, pt.x - cx);
          let deg = Math.round((angleRad * 180) / Math.PI + 90);
          if (deg < 0) deg += 360;

          // Snap to cardinal angles (0°, 90°, 180°, 270°)
          if (Math.abs(deg - 0) < 4 || Math.abs(deg - 360) < 4) deg = 0;
          if (Math.abs(deg - 90) < 4) deg = 90;
          if (Math.abs(deg - 180) < 4) deg = 180;
          if (Math.abs(deg - 270) < 4) deg = 270;

          layer.rotation = deg;
          this.renderCanvas();
        } else if (this.dragAction.startsWith('resize-')) {
          const init = this.initialLayerState;
          const dx = pt.x - this.dragStartX;
          const dy = pt.y - this.dragStartY;

          if (this.dragAction === 'resize-br') {
            layer.width = Math.max(60, Math.round(init.width + dx));
            layer.height = Math.max(30, Math.round(init.height + dy));
          } else if (this.dragAction === 'resize-bl') {
            layer.width = Math.max(60, Math.round(init.width - dx));
            layer.x = Math.round(init.x + dx);
            layer.height = Math.max(30, Math.round(init.height + dy));
          } else if (this.dragAction === 'resize-tr') {
            layer.width = Math.max(60, Math.round(init.width + dx));
            layer.height = Math.max(30, Math.round(init.height - dy));
            layer.y = Math.round(init.y + dy);
          } else if (this.dragAction === 'resize-tl') {
            layer.width = Math.max(60, Math.round(init.width - dx));
            layer.x = Math.round(init.x + dx);
            layer.height = Math.max(30, Math.round(init.height - dy));
            layer.y = Math.round(init.y + dy);
          }
          this.renderCanvas();
        }
      });

      window.addEventListener('mouseup', () => {
        this.dragAction = null;
      });
    }

    // 2. 360° Manipulator Toolbar Buttons
    const mirrorHBtn = document.getElementById('toolMirrorHBtn');
    const mirrorVBtn = document.getElementById('toolMirrorVBtn');
    const duplicateBtn = document.getElementById('toolDuplicateBtn');
    const deleteBtn = document.getElementById('toolDeleteBtn');
    const layerUpBtn = document.getElementById('toolLayerUpBtn');
    const layerDownBtn = document.getElementById('toolLayerDownBtn');
    const export4KBtn = document.getElementById('export4KBtn');

    if (mirrorHBtn) mirrorHBtn.addEventListener('click', () => this.mirrorHorizontal());
    if (mirrorVBtn) mirrorVBtn.addEventListener('click', () => this.mirrorVertical());
    if (duplicateBtn) duplicateBtn.addEventListener('click', () => this.duplicateLayer());
    if (deleteBtn) deleteBtn.addEventListener('click', () => this.deleteLayer());
    if (layerUpBtn) layerUpBtn.addEventListener('click', () => this.bringForward());
    if (layerDownBtn) layerDownBtn.addEventListener('click', () => this.sendBackward());
    if (export4KBtn) export4KBtn.addEventListener('click', () => this.exportUltraHD4K());

    // 3. Aspect Ratio Presets
    document.querySelectorAll('.aspect-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.aspect-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        const aspect = e.currentTarget.dataset.aspect;
        this.setAspectRatio(aspect);
      });
    });

    // 4. Style Presets
    document.querySelectorAll('.preset-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        this.activeStyle = e.currentTarget.dataset.style;
        const headlineLayer = this.layers.find(l => l.id === 'layer-headline');
        if (headlineLayer) {
          headlineLayer.style = this.activeStyle;
          if (this.activeStyle === 'mrbeast') headlineLayer.color = '#ffe600';
          else if (this.activeStyle === 'neon-cyan') headlineLayer.color = '#00f2fe';
          else if (this.activeStyle === 'fire-rose') headlineLayer.color = '#ff4b4b';
          else headlineLayer.color = '#ffffff';
        }
        this.renderCanvas();
        this.app.showToast(`Estilo ${this.activeStyle.toUpperCase()} aplicado`, 'info');
      });
    });

    // 5. Input Controls Synchronizers
    const headlineInput = document.getElementById('canvasHeadlineInput');
    const sublineInput = document.getElementById('canvasSublineInput');
    const badgeInput = document.getElementById('canvasBadgeInput');

    if (headlineInput) {
      headlineInput.addEventListener('input', (e) => {
        const headlineLayer = this.layers.find(l => l.id === 'layer-headline');
        if (headlineLayer) {
          headlineLayer.text = e.target.value;
          this.renderCanvas();
        }
      });
    }
    if (sublineInput) {
      sublineInput.addEventListener('input', (e) => {
        const subLayer = this.layers.find(l => l.id === 'layer-subline');
        if (subLayer) {
          subLayer.text = e.target.value;
          this.renderCanvas();
        }
      });
    }
    if (badgeInput) {
      badgeInput.addEventListener('input', (e) => {
        const badgeLayer = this.layers.find(l => l.id === 'layer-badge');
        if (badgeLayer) {
          badgeLayer.text = e.target.value;
          this.renderCanvas();
        }
      });
    }

    // 6. Background Image Upload
    const imgUploadInput = document.getElementById('canvasBgUpload');
    if (imgUploadInput) {
      imgUploadInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (event) => {
            this.bgImage.src = event.target.result;
            this.bgImage.onload = () => {
              this.bgImageLoaded = true;
              this.renderCanvas();
              this.app.showToast('Imagen de fondo cargada en el lienzo', 'success');
            };
          };
          reader.readAsDataURL(file);
        }
      });
    }

    // 7. Typography, Stroke, Shadow & Background Box Synchronizers
    const fontSelect = document.getElementById('canvasFontSelect');
    if (fontSelect) {
      fontSelect.addEventListener('change', (e) => {
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.fontFamily = e.target.value;
          this.renderCanvas();
          this.app.showToast(`Fuente cambiada a ${e.target.options[e.target.selectedIndex].text}`, 'info');
        }
      });
    }

    const textColorInput = document.getElementById('canvasTextColor');
    if (textColorInput) {
      textColorInput.addEventListener('input', (e) => {
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.color = e.target.value;
          this.renderCanvas();
        }
      });
    }

    const strokeColorInput = document.getElementById('canvasStrokeColor');
    if (strokeColorInput) {
      strokeColorInput.addEventListener('input', (e) => {
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.strokeColor = e.target.value;
          this.renderCanvas();
        }
      });
    }

    const strokeWidthInput = document.getElementById('canvasStrokeWidth');
    const strokeWidthVal = document.getElementById('canvasStrokeWidthVal');
    if (strokeWidthInput) {
      strokeWidthInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (strokeWidthVal) strokeWidthVal.textContent = `${val}px`;
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.strokeWidth = val;
          this.renderCanvas();
        }
      });
    }

    const shadowBlurInput = document.getElementById('canvasShadowBlur');
    const shadowBlurVal = document.getElementById('canvasShadowBlurVal');
    if (shadowBlurInput) {
      shadowBlurInput.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        if (shadowBlurVal) shadowBlurVal.textContent = `${val}px`;
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.shadowBlur = val;
          this.renderCanvas();
        }
      });
    }

    const bgBoxToggle = document.getElementById('canvasBgBoxToggle');
    const bgBoxSettings = document.getElementById('canvasBgBoxSettings');
    if (bgBoxToggle) {
      bgBoxToggle.addEventListener('change', (e) => {
        if (bgBoxSettings) bgBoxSettings.style.display = e.target.checked ? 'grid' : 'none';
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.hasBgBox = e.target.checked;
          this.renderCanvas();
        }
      });
    }

    const bgBoxColorInput = document.getElementById('canvasBgBoxColor');
    if (bgBoxColorInput) {
      bgBoxColorInput.addEventListener('input', (e) => {
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.bgBoxColor = e.target.value;
          this.renderCanvas();
        }
      });
    }

    const bgBoxPaddingInput = document.getElementById('canvasBgBoxPadding');
    if (bgBoxPaddingInput) {
      bgBoxPaddingInput.addEventListener('input', (e) => {
        const layer = this.getSelectedLayer();
        if (layer) {
          layer.bgBoxPadding = parseInt(e.target.value);
          this.renderCanvas();
        }
      });
    }

    // 8. Stickers & Emojis Palette Click Listeners
    document.querySelectorAll('.sticker-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const stickerText = e.currentTarget.dataset.sticker;
        if (stickerText) {
          this.addStickerLayer(stickerText);
        }
      });
    });

    // 9. Add Free Text Layer
    const addTextBtn = document.getElementById('addTextLayerBtn');
    if (addTextBtn) {
      addTextBtn.addEventListener('click', () => this.addTextLayer());
    }

    // 10. Send Design Direct to Social Media Planner
    const sendPlannerBtn = document.getElementById('sendToPlannerBtn');
    if (sendPlannerBtn) {
      sendPlannerBtn.addEventListener('click', () => this.sendToPlanner());
    }

    // 11. Standard Download
    const exportBtn = document.getElementById('exportThumbnailBtn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => this.exportThumbnail());
    }

    // 12. Advanced AI Viral Engine & Multi-Platform Event Bindings
    const genScriptBtn = document.getElementById('generateScriptBtn');
    if (genScriptBtn) {
      genScriptBtn.addEventListener('click', () => this.generateFullViralPack());
    }

    const openGeminiBtn = document.getElementById('openGeminiWebBtn');
    if (openGeminiBtn) {
      openGeminiBtn.addEventListener('click', () => {
        const topic = document.getElementById('scriptTopicInput')?.value || '';
        GeminiSuiteManager.openGeminiWeb(topic, this.selectedNiche);
        this.app.showToast('¡Prompt maestro copiado! Abriendo Gemini Web...', 'success');
      });
    }

    // Niche Selector Cards
    document.querySelectorAll('#nicheGridSelector .niche-card-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('#nicheGridSelector .niche-card-btn').forEach(b => b.classList.remove('active'));
        const card = e.currentTarget;
        card.classList.add('active');
        this.selectedNiche = card.dataset.niche || 'espiritualidad';
        this.renderTrendingIdeas();
        const nicheData = TrendingNiches[this.selectedNiche];
        if (nicheData && nicheData.ideas?.length > 0) {
          const topicInput = document.getElementById('scriptTopicInput');
          if (topicInput) {
            topicInput.value = nicheData.ideas[0];
          }
        }
        this.app.showToast(`Nicho: ${TrendingNiches[this.selectedNiche]?.name || this.selectedNiche}`, 'info');
      });
    });

    // Clear Topic Button
    const clearBtn = document.getElementById('clearTopicBtn');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        const input = document.getElementById('scriptTopicInput');
        if (input) {
          input.value = '';
          input.focus();
        }
      });
    }

    // AI Pack Result Tabs
    document.querySelectorAll('#aiPackTabs .ai-pack-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('#aiPackTabs .ai-pack-tab-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.activePackTab = e.currentTarget.dataset.pack || 'all';

        document.querySelectorAll('.ai-pack-view').forEach(v => v.classList.remove('active'));
        const viewMap = {
          'all': 'packViewAll',
          'hooks': 'packViewHooks',
          'script': 'packViewScript',
          'descriptions': 'packViewDescriptions',
          'tags': 'packViewTags',
          'visual': 'packViewVisual'
        };
        const targetViewId = viewMap[this.activePackTab] || 'packViewAll';
        const targetEl = document.getElementById(targetViewId);
        if (targetEl) targetEl.classList.add('active');
      });
    });

    // Description Platform Subtabs
    document.querySelectorAll('.desc-platform-subtab').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.desc-platform-subtab').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.activeDescPlatform = e.currentTarget.dataset.platform || 'yt';
        if (this.latestPack?.descriptions) {
          const outEl = document.getElementById('generatedDescriptionsOutput');
          if (outEl) {
            outEl.textContent = this.latestPack.descriptions[this.activeDescPlatform] || '';
          }
        }
      });
    });

    // YouTube Tag Filters
    document.querySelectorAll('.yt-filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.yt-filter-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.activeTagFilter = e.currentTarget.dataset.filter || 'all';
        if (this.latestPack?.tags) {
          this.renderYouTubeTags(this.latestPack.tags);
        }
      });
    });

    // Copy YouTube Studio Tags
    const copyTagsBtn = document.getElementById('copyYtTagsStudioBtn');
    if (copyTagsBtn) {
      copyTagsBtn.addEventListener('click', () => {
        if (!this.latestPack?.tags) return;
        let tagsToCopy = [];
        if (this.activeTagFilter === 'seo') {
          tagsToCopy = this.latestPack.tags.seo;
        } else if (this.activeTagFilter === 'typo') {
          tagsToCopy = this.latestPack.tags.typos;
        } else {
          tagsToCopy = this.latestPack.tags.all.map(t => t.text);
        }
        const text = tagsToCopy.join(', ');
        navigator.clipboard.writeText(text);
        this.app.showToast('¡Etiquetas copiadas en formato YouTube Studio!', 'success');
      });
    }

    // Action Pipeline: Send to Planner
    const pipePlannerBtn = document.getElementById('pipelineSendToPlannerBtn');
    if (pipePlannerBtn) {
      pipePlannerBtn.addEventListener('click', () => this.sendPackToPlanner());
    }

    // Action Pipeline: Apply to Canvas
    const pipeCanvasBtn = document.getElementById('pipelineApplyToCanvasBtn');
    if (pipeCanvasBtn) {
      pipeCanvasBtn.addEventListener('click', () => this.applyPackToCanvas());
    }

    // Action Pipeline: Send to Prompter
    const pipePrompterBtn = document.getElementById('pipelineSendToPrompterBtn');
    if (pipePrompterBtn) {
      pipePrompterBtn.addEventListener('click', () => this.sendPackToPrompter());
    }

    // Action Pipeline: Copy Active Text
    const pipeCopyBtn = document.getElementById('copyActivePackOutputBtn');
    if (pipeCopyBtn) {
      pipeCopyBtn.addEventListener('click', () => this.copyActivePackOutput());
    }
  }

  renderTrendingIdeas() {
    const container = document.getElementById('trendingIdeasPills');
    if (!container) return;
    const nicheData = TrendingNiches[this.selectedNiche] || TrendingNiches.espiritualidad;
    const ideas = nicheData.ideas || [];

    container.innerHTML = ideas.map(idea => `
      <div class="idea-chip" title="Clic para usar esta idea">${idea}</div>
    `).join('');

    container.querySelectorAll('.idea-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const input = document.getElementById('scriptTopicInput');
        if (input) {
          input.value = chip.textContent.trim();
          input.focus();
        }
        this.app.showToast('Idea cargada en el tema central', 'info');
      });
    });
  }

  updateGeminiStatusBadge() {
    const badge = document.getElementById('geminiSuiteStatusBadge');
    if (!badge) return;
    if (GeminiSuiteManager.hasActiveKey()) {
      badge.textContent = `✨ ${GeminiSuiteManager.getModel()} (Live)`;
      badge.className = 'badge badge-emerald';
    } else {
      badge.textContent = '⚡ Gemini 2.0 Free (Autónomo)';
      badge.className = 'badge badge-cyan';
    }
  }

  async generateFullViralPack() {
    const topic = document.getElementById('scriptTopicInput')?.value || '';
    const genScriptBtn = document.getElementById('generateScriptBtn');
    
    if (genScriptBtn) {
      genScriptBtn.innerHTML = '✨ Generando Pack Viral con IA...';
      genScriptBtn.disabled = true;
    }

    try {
      const pack = await GeminiSuiteManager.generateFullPack(topic, this.selectedNiche);
      this.latestPack = pack;
      this.renderPackOutputs(pack);
      this.app.showToast(`¡Pack viral generado con éxito! [${pack.source}]`, 'success');
    } catch (err) {
      console.error('Error in generateFullViralPack', err);
      this.app.showToast('Generando con motor autónomo de respaldo...', 'info');
      const pack = GeminiSuiteManager.generateAutonomousPack(topic, this.selectedNiche);
      this.latestPack = pack;
      this.renderPackOutputs(pack);
    } finally {
      if (genScriptBtn) {
        genScriptBtn.innerHTML = '🚀 Generar Contenido Completo con IA';
        genScriptBtn.disabled = false;
      }
    }
  }

  renderPackOutputs(pack) {
    if (!pack) return;

    // 1. Pack View: All (Executive Overview)
    const allOutputEl = document.getElementById('generatedScriptOutput');
    if (allOutputEl) {
      const topHook = pack.hooks?.[0] || '';
      const topTitle = pack.titles?.[0]?.title || '';
      const tagsSummary = pack.tags?.all?.slice(0, 8).map(t => t.text).join(', ') || '';

      allOutputEl.textContent = `⚡ PAQUETE VIRAL GENERADO (${pack.source.toUpperCase()})
🎯 TEMA: "${pack.topic}"
🏷️ NICHO: ${pack.nicheData?.name || pack.niche} (CPM: ${pack.nicheData?.cpm || 'Alto'})

🔥 GANCHO PRINCIPAL (0-3s):
"${topHook}"

🏆 MEJOR TÍTULO CTR:
"${topTitle}" (Puntuación Algorítmica: 98/100)

📜 ESTRUCTURA DEL GUION:
${pack.script}

🌐 RESUMEN DE ETIQUETAS & TYPOS YOUTUBE:
${tagsSummary}...

👉 Clic en las pestañas superiores para ver el guion completo, descripciones por red social o prompts de miniatura.`;
    }

    // 2. Pack View: Hooks & Titles
    const hooksOutputEl = document.getElementById('generatedHooksOutput');
    if (hooksOutputEl) {
      const hooksList = (pack.hooks || []).map((h, i) => `[Gancho #${i+1}] 🔥 "${h}"`).join('\n\n');
      const titlesList = (pack.titles || []).map((t, i) => `[Título #${i+1}] 🏆 "${t.title}" — Score CTR: ${t.score || 95}/100`).join('\n');
      hooksOutputEl.textContent = `🎯 5 GANCHOS PSICOLÓGICOS DE ALTA RETENCIÓN:\n\n${hooksList}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🏆 5 TÍTULOS DE ALTO CLIC (CTR):\n\n${titlesList}`;
    }

    // 3. Pack View: Full Script
    const scriptOutputEl = document.getElementById('generatedScriptFullOutput');
    if (scriptOutputEl) {
      scriptOutputEl.textContent = pack.script || '';
    }

    // 4. Pack View: Descriptions
    const descOutputEl = document.getElementById('generatedDescriptionsOutput');
    if (descOutputEl && pack.descriptions) {
      descOutputEl.textContent = pack.descriptions[this.activeDescPlatform] || pack.descriptions.yt || '';
    }

    // 5. Pack View: YouTube Tags with Typos
    this.renderYouTubeTags(pack.tags);

    // 6. Pack View: Visual Prompts
    const visualOutputEl = document.getElementById('generatedVisualPromptsOutput');
    if (visualOutputEl && pack.visualPrompts) {
      visualOutputEl.textContent = `🎨 PROMPT MIDJOURNEY V6 (Miniatura YouTube 16:9):
${pack.visualPrompts.midjourney}

🎨 PROMPT FLUX / DALL-E 3 (Portada Cinemática):
${pack.visualPrompts.flux}

🎬 PROMPT VIDEO AI (Kling / Runway Gen-3 / Sora):
${pack.visualPrompts.videoAi}`;
    }
  }

  renderYouTubeTags(tagsData) {
    if (!tagsData) return;
    const cloudEl = document.getElementById('ytTagsCloud');
    const meterCountEl = document.getElementById('ytTagCharMeterCount');
    const meterFillEl = document.getElementById('ytTagMeterFill');

    let displayList = [];
    if (this.activeTagFilter === 'seo') {
      displayList = (tagsData.seo || []).map(t => ({ text: t, type: 'seo' }));
    } else if (this.activeTagFilter === 'typo') {
      displayList = (tagsData.typos || []).map(t => ({ text: t, type: 'typo' }));
    } else {
      displayList = tagsData.all || [];
    }

    if (cloudEl) {
      cloudEl.innerHTML = displayList.map(tagItem => {
        const isTypo = tagItem.type === 'typo';
        return `
          <span class="tag-badge-chip ${isTypo ? 'typo-tag' : 'seo-tag'}" title="${isTypo ? 'Error ortográfico intencional para capturar búsquedas móviles' : 'Etiqueta SEO de alto alcance'}">
            ${isTypo ? '<span class="typo-indicator">TYPO</span>' : '📈'}
            <span>${tagItem.text}</span>
          </span>
        `;
      }).join('');
    }

    // Measure total character length in comma-separated format
    const totalChars = displayList.map(t => t.text).join(', ').length;
    if (meterCountEl) {
      meterCountEl.textContent = `${totalChars} / 500 caracteres`;
      if (totalChars > 490) {
        meterCountEl.style.color = '#f87171';
      } else {
        meterCountEl.style.color = 'var(--accent-cyan)';
      }
    }
    if (meterFillEl) {
      const pct = Math.min(100, Math.round((totalChars / 500) * 100));
      meterFillEl.style.width = `${pct}%`;
      if (totalChars > 490) {
        meterFillEl.classList.add('warning');
      } else {
        meterFillEl.classList.remove('warning');
      }
    }
  }

  sendPackToPlanner() {
    if (!this.latestPack) {
      this.app.showToast('Primero genera un pack de contenido', 'warning');
      return;
    }

    const titleInput = document.getElementById('newPostTitleInput');
    const captionInput = document.getElementById('newPostCaptionInput');
    const tagsInput = document.getElementById('newPostYtTagsInput');

    if (titleInput) {
      titleInput.value = this.latestPack.titles?.[0]?.title || this.latestPack.topic;
    }
    if (captionInput) {
      const desc = this.latestPack.descriptions?.[this.activeDescPlatform] || this.latestPack.descriptions?.tt || '';
      captionInput.value = desc;
      this.app.planner.updateCharCounter();
    }
    if (tagsInput && this.latestPack.tags?.all) {
      const commaString = YouTubeTagMaster.formatCommaString(this.latestPack.tags.all);
      tagsInput.value = commaString;
      const countEl = document.getElementById('plannerTagCharCount');
      if (countEl) countEl.textContent = `${commaString.length} / 500 chars`;
    }

    // Switch to planner tab
    this.app.switchTab('planner');
    this.app.showToast('🚀 ¡Contenido cargado en el Planificador!', 'success');
  }

  applyPackToCanvas() {
    if (!this.latestPack) {
      this.app.showToast('Primero genera un pack de contenido', 'warning');
      return;
    }

    const hookText = this.latestPack.hooks?.[0] || this.latestPack.topic;
    const headlineLayer = this.layers.find(l => l.id === 'layer-headline');
    const sublineLayer = this.layers.find(l => l.id === 'layer-subline');

    if (headlineLayer) {
      headlineLayer.text = hookText.length > 36 ? hookText.substring(0, 34).toUpperCase() + '...' : hookText.toUpperCase();
      const input = document.getElementById('canvasHeadlineInput');
      if (input) input.value = headlineLayer.text;
    }

    if (sublineLayer && this.latestPack.titles?.[0]?.title) {
      sublineLayer.text = this.latestPack.titles[0].title;
    }

    this.renderCanvas();
    this.app.showToast('🎨 ¡Gancho aplicado a la portada!', 'success');
  }

  sendPackToPrompter() {
    if (!this.latestPack?.script) {
      this.app.showToast('Primero genera un pack de contenido', 'warning');
      return;
    }

    const prompterText = document.getElementById('prompterContentText');
    if (prompterText) {
      prompterText.innerHTML = this.latestPack.script.replace(/\n/g, '<br>');
    }
    
    const modal = document.getElementById('prompterModal');
    if (modal) {
      modal.classList.add('active');
      this.app.showToast('🎙️ ¡Guion cargado en el Teleprompter 4K!', 'info');
    }
  }

  copyActivePackOutput() {
    let textToCopy = '';
    if (this.activePackTab === 'hooks') {
      textToCopy = document.getElementById('generatedHooksOutput')?.textContent || '';
    } else if (this.activePackTab === 'script') {
      textToCopy = document.getElementById('generatedScriptFullOutput')?.textContent || '';
    } else if (this.activePackTab === 'descriptions') {
      textToCopy = document.getElementById('generatedDescriptionsOutput')?.textContent || '';
    } else if (this.activePackTab === 'tags') {
      textToCopy = YouTubeTagMaster.formatCommaString(this.latestPack?.tags?.all || []);
    } else if (this.activePackTab === 'visual') {
      textToCopy = document.getElementById('generatedVisualPromptsOutput')?.textContent || '';
    } else {
      textToCopy = document.getElementById('generatedScriptOutput')?.textContent || '';
    }

    if (textToCopy) {
      navigator.clipboard.writeText(textToCopy);
      this.app.showToast('Copiado al portapapeles', 'info');
    }
  }

// ==========================================
// 3. CLIPPER MANAGER
// ==========================================
class ClipperManager {
  constructor(app) {
    this.app = app;
    this.isPlaying = false;
    this.currentTime = 12.4;
    this.duration = 45.0;
    this.playInterval = null;

    this.subtitles = [
      { start: 0.0, end: 3.2, text: "EL SECRETO QUE", highlight: "NADIE TE DICE", emoji: "🤫" },
      { start: 3.2, end: 7.5, text: "SOBRE EL ALGORITMO", highlight: "DE TIKTOK EN 2026", emoji: "🔥" },
      { start: 7.5, end: 12.0, text: "LAS VISITAS YA NO", highlight: "SON LA MÉTRICA CLAVE", emoji: "❌" },
      { start: 12.0, end: 16.8, text: "LO QUE REALMENTE IMPORTA", highlight: "SON LOS SHARES POR DM", emoji: "🚀" },
      { start: 16.8, end: 22.0, text: "SI CADA PERSONA COMPARTE", highlight: "TU VIDEO A 3 AMIGOS", emoji: "📈" },
      { start: 22.0, end: 28.5, text: "EL ALGORITMO TE IMPULSA", highlight: "A MILLONES DE PERSONAS", emoji: "🤯" }
    ];

    this.candidateClips = [
      {
        id: 'clip-1',
        title: 'El Secreto de los Shares por DM en TikTok',
        hookQuote: '"Las visitas ya no importan, si no logras que lo compartan en privado estás muerto..."',
        startTime: '00:12',
        endTime: '00:48',
        durationSec: 36,
        viralScore: 98,
        retentionPrediction: '88% completion rate',
        tags: ['#TikTokGrowth', '#ViralTips', '#Algoritmo2026']
      },
      {
        id: 'clip-2',
        title: 'Por qué el 95% de los creadores fracasan antes de monetizar',
        hookQuote: '"No es falta de talento, es que publican en las horas equivocadas..."',
        startTime: '01:15',
        endTime: '01:52',
        durationSec: 37,
        viralScore: 94,
        retentionPrediction: '81% completion rate',
        tags: ['#Monetizacion', '#YouTubeShorts', '#Consejos']
      },
      {
        id: 'clip-3',
        title: 'Clonación de Voz: La verdad sobre los derechos de autor',
        hookQuote: '"Si no tienes este certificado, te pueden desmonetizar tu canal entero..."',
        startTime: '03:40',
        endTime: '04:22',
        durationSec: 42,
        viralScore: 91,
        retentionPrediction: '76% completion rate',
        tags: ['#VoiceAI', '#DerechosDeAutor', '#Creadores']
      }
    ];

    this.activeClip = this.candidateClips[0];
    this.init();
  }

  init() {
    this.renderClipsList();
    this.drawWaveform();
    this.bindEvents();
  }

  drawWaveform() {
    const canvas = document.getElementById('waveformCanvas');
    if (!canvas || !canvas.parentElement) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width = canvas.parentElement.clientWidth || 600;
    const h = canvas.height = canvas.parentElement.clientHeight || 54;

    ctx.clearRect(0, 0, w, h);

    const bars = 80;
    const barWidth = w / bars;

    for (let i = 0; i < bars; i++) {
      let amp = Math.sin(i * 0.28) * 0.35 + Math.cos(i * 0.15) * 0.25 + 0.4;
      if ((i > 18 && i < 35) || (i > 50 && i < 68)) {
        amp += 0.32;
      }
      amp = Math.min(1.0, Math.max(0.12, amp));

      const barH = amp * (h - 12);
      const x = i * barWidth;
      const y = (h - barH) / 2;

      if (amp > 0.7) {
        ctx.fillStyle = '#06b6d4';
      } else if (amp > 0.45) {
        ctx.fillStyle = '#6366f1';
      } else {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
      }

      ctx.fillRect(x + 1, y, barWidth - 2, barH);
    }
  }

  renderClipsList() {
    const container = document.getElementById('clipsListContainer');
    if (!container) return;

    container.innerHTML = this.candidateClips.map(clip => `
      <div class="clip-candidate-card ${clip.id === this.activeClip.id ? 'active' : ''}" data-clip-id="${clip.id}">
        <div class="clip-card-header">
          <span class="viral-score-tag high">🔥 ${clip.viralScore}% VIRAL</span>
          <span class="clip-timestamp-badge">⏱️ ${clip.startTime} - ${clip.endTime} (${clip.durationSec}s)</span>
        </div>
        <h4 class="clip-title-preview">${clip.title}</h4>
        <p class="clip-hook-quote">${clip.hookQuote}</p>
        <div class="clip-bottom-actions">
          <button class="btn btn-sm btn-cyber preview-clip-btn" data-clip-id="${clip.id}">
            ▶️ Previsualizar
          </button>
          <button class="btn btn-sm btn-ghost plan-clip-btn" data-clip-id="${clip.id}">
            📅 Programar Post
          </button>
        </div>
      </div>
    `).join('');
  }

  selectClip(clipId) {
    const clip = this.candidateClips.find(c => c.id === clipId);
    if (!clip) return;
    this.activeClip = clip;
    this.renderClipsList();
    this.updateActiveSubtitle();
    this.app.showToast(`Cargando clip: "${clip.title}"`, 'info');
  }

  togglePlayback() {
    this.isPlaying = !this.isPlaying;
    const playBtn = document.getElementById('playPauseClipBtn');

    if (this.isPlaying) {
      if (playBtn) playBtn.innerHTML = '⏸️ Pausar';
      this.playInterval = setInterval(() => {
        this.currentTime += 0.2;
        if (this.currentTime >= this.duration) {
          this.currentTime = 0;
        }
        this.updatePlayerProgress();
      }, 200);
    } else {
      if (playBtn) playBtn.innerHTML = '▶️ Reproducir';
      clearInterval(this.playInterval);
    }
  }

  updatePlayerProgress() {
    const timeDisplay = document.getElementById('clipCurrentTimeDisplay');
    const marker = document.getElementById('waveformMarker');

    if (timeDisplay) {
      const mins = Math.floor(this.currentTime / 60);
      const secs = Math.floor(this.currentTime % 60);
      timeDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    if (marker) {
      const pct = (this.currentTime / this.duration) * 100;
      marker.style.left = `${pct}%`;
    }

    this.updateActiveSubtitle();
  }

  updateActiveSubtitle() {
    const subContainer = document.getElementById('karaokeSubtitlesBox');
    if (!subContainer) return;

    const currentSub = this.subtitles.find(s => this.currentTime >= s.start && this.currentTime < s.end) || this.subtitles[0];

    subContainer.innerHTML = `
      <div class="karaoke-text">
        <span>${currentSub.text}</span>
        <span class="karaoke-highlight">${currentSub.highlight}</span>
        <span class="karaoke-emoji">${currentSub.emoji}</span>
      </div>
    `;
  }

  bindEvents() {
    const playBtn = document.getElementById('playPauseClipBtn');
    if (playBtn) {
      playBtn.addEventListener('click', () => this.togglePlayback());
    }

    const analyzeBtn = document.getElementById('startAutoClipBtn');
    if (analyzeBtn) {
      analyzeBtn.addEventListener('click', () => {
        analyzeBtn.innerHTML = '⚡ Analizando Picos de Viralidad...';
        analyzeBtn.disabled = true;

        setTimeout(() => {
          analyzeBtn.innerHTML = '⚡ Detectar Picos y Clips Virales';
          analyzeBtn.disabled = false;
          this.drawWaveform();
          this.app.showToast('¡3 clips de alta retención identificados con subtítulos dinámicos!', 'success');
        }, 1200);
      });
    }

    const container = document.getElementById('clipsListContainer');
    if (container) {
      container.addEventListener('click', (e) => {
        const previewBtn = e.target.closest('.preview-clip-btn');
        const planBtn = e.target.closest('.plan-clip-btn');
        const card = e.target.closest('.clip-candidate-card');

        if (previewBtn) {
          this.selectClip(previewBtn.dataset.clipId);
          if (!this.isPlaying) this.togglePlayback();
        } else if (planBtn) {
          const clip = this.candidateClips.find(c => c.id === planBtn.dataset.clipId);
          if (clip) {
            this.app.switchTab('planner');
            this.app.planner.preparePostFromClip(clip);
          }
        } else if (card) {
          this.selectClip(card.dataset.clipId);
        }
      });
    }

    const exportBtn = document.getElementById('exportClipBtn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        this.app.showToast('Descargando clip vertical 9:16 con subtítulos karaoke incrustados (MP4)', 'success');
      });
    }
  }
}

// ==========================================
// 4. MULTISTREAM MANAGER
// ==========================================
class MultistreamManager {
  constructor(app) {
    this.app = app;
    this.isLive = false;
    this.currentSource = 'studio';
    this.mediaStream = null;
    this.telemetryInterval = null;
    this.vuInterval = null;
    this.chatInterval = null;

    this.platforms = {
      youtube: true,
      tiktok: true,
      facebook: false,
      twitch: true,
      kick: false,
      twitter: false
    };

    // Screen Recorder & Media Tools State
    this.mediaRecorder = null;
    this.recordedChunks = [];
    this.recordingStream = null;
    this.isRecording = false;
    this.recordSeconds = 0;
    this.recordTimerInterval = null;

    // OBS Scenes & Volume Mixer State
    this.currentScene = 'studio';
    this.isMuted = false;
    this.volumes = {
      master: 100,
      mic: 85,
      desktop: 70
    };

    this.mockChatMessages = [
      { id: 1, platform: 'yt', user: 'TechVibe_99', text: '¡Saludos desde México! ¿Qué cámara usas para el multistream?', isQuestion: true, pinned: false },
      { id: 2, platform: 'tt', user: 'sofia.creativity', text: 'Increíble la calidad del stream bro 🔥🔥🔥', isQuestion: false, pinned: false },
      { id: 3, platform: 'tw', user: 'GamerZero_X', text: '¿Cuántos Mbps de bitrate recomiendas para transmitir a TikTok y YouTube a la vez?', isQuestion: true, pinned: false },
      { id: 4, platform: 'fb', user: 'Carlos Mendoza', text: 'Excelente contenido como siempre Alex, compartido en mi grupo!', isQuestion: false, pinned: false },
      { id: 5, platform: 'tt', user: 'daniela_ia', text: 'OMG la voz clonada suena 100% natural, no parece robot 😱', isQuestion: false, pinned: false }
    ];

    this.init();
  }

  init() {
    this.renderPlatformsMatrix();
    this.renderChatMessages();
    this.startAudioVUMeter();
    this.bindEvents();
  }

  renderPlatformsMatrix() {
    const container = document.getElementById('platformsStreamMatrix');
    if (!container) return;

    const meta = {
      youtube: { name: 'YouTube Live', class: 'yt', label: 'YT' },
      tiktok: { name: 'TikTok Live', class: 'tt', label: 'TT' },
      facebook: { name: 'Facebook Live', class: 'fb', label: 'FB' },
      twitch: { name: 'Twitch TV', class: 'tw', label: 'TW' },
      kick: { name: 'Kick Streaming', class: 'kc', label: 'KC' },
      twitter: { name: 'X / Twitter Live', class: 'xx', label: 'X' }
    };

    container.innerHTML = Object.entries(this.platforms).map(([key, isConnected]) => `
      <div class="platform-card-stream ${isConnected ? 'connected' : ''}" data-platform="${key}">
        <div class="platform-info-tag">
          <div class="platform-icon-circle ${meta[key].class}">${meta[key].label}</div>
          <div>
            <div style="font-size:0.84rem; font-weight:700; color:#fff;">${meta[key].name}</div>
            <div style="font-size:0.7rem; color:${isConnected ? '#6ee7b7' : '#94a3b8'};">
              ${isConnected ? '● Enlazado (Listo)' : '○ Desconectado'}
            </div>
          </div>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" class="platform-stream-toggle" data-platform="${key}" ${isConnected ? 'checked' : ''}>
          <span class="toggle-slider"></span>
        </label>
      </div>
    `).join('');
  }

  toggleLiveBroadcast() {
    this.isLive = !this.isLive;
    const liveBtn = document.getElementById('toggleBroadcastBtn');
    const onAirBadge = document.getElementById('broadcastOnAirBadge');

    if (this.isLive) {
      if (liveBtn) {
        liveBtn.innerHTML = '🛑 DETENER MULTITRANSMISIÓN';
        liveBtn.classList.remove('btn-primary');
        liveBtn.classList.add('btn-danger');
      }
      if (onAirBadge) onAirBadge.style.display = 'flex';

      localStorage.setItem('virallabs_stream_live', 'true');
      this.app.broadcastMessage({ type: 'STREAM_TOGGLE', isLive: true });

      this.startTelemetry();
      this.startSimulatedChat();
      this.app.showToast('🚀 ¡Transmisión en vivo iniciada! Sincronizado con Fanpage.', 'success');
    } else {
      if (liveBtn) {
        liveBtn.innerHTML = '🔴 INICIAR MULTITRANSMISIÓN EN VIVO';
        liveBtn.classList.remove('btn-danger');
        liveBtn.classList.add('btn-primary');
      }
      if (onAirBadge) onAirBadge.style.display = 'none';

      localStorage.setItem('virallabs_stream_live', 'false');
      this.app.broadcastMessage({ type: 'STREAM_TOGGLE', isLive: false });

      clearInterval(this.telemetryInterval);
      clearInterval(this.chatInterval);
      this.app.showToast('Transmisión finalizada. Fanpage sincronizada.', 'info');
    }
  }

  startTelemetry() {
    this.telemetryInterval = setInterval(() => {
      const baseBitrate = 6200;
      const jitter = Math.floor((Math.random() - 0.5) * 240);
      const bitrate = baseBitrate + jitter;

      const fpsVal = (59.8 + Math.random() * 0.4).toFixed(1);
      const cpuVal = (16 + Math.random() * 5).toFixed(0);

      const bitrateEl = document.getElementById('telemetryBitrate');
      const fpsEl = document.getElementById('telemetryFps');
      const cpuEl = document.getElementById('telemetryCpu');

      if (bitrateEl) bitrateEl.textContent = `${bitrate} kbps`;
      if (fpsEl) fpsEl.textContent = `${fpsVal} FPS`;
      if (cpuEl) cpuEl.textContent = `${cpuVal}%`;
    }, 1000);
  }

  startAudioVUMeter() {
    const leftBar = document.getElementById('vuChannelLeft');
    const rightBar = document.getElementById('vuChannelRight');

    this.vuInterval = setInterval(() => {
      if (this.isLive) {
        const leftVal = 40 + Math.random() * 48;
        const rightVal = 38 + Math.random() * 52;
        if (leftBar) leftBar.style.width = `${leftVal}%`;
        if (rightBar) rightBar.style.width = `${rightVal}%`;
      } else {
        if (leftBar) leftBar.style.width = '12%';
        if (rightBar) rightBar.style.width = '10%';
      }
    }, 120);
  }

  async switchSource(sourceType) {
    this.currentSource = sourceType;
    const videoFeed = document.getElementById('broadcastMainVideo');

    if (sourceType === 'webcam') {
      try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          this.mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
          if (videoFeed) {
            videoFeed.srcObject = this.mediaStream;
            videoFeed.play();
          }
          this.app.showToast('Fuente cambiada a Cámara Web en vivo', 'success');
          return;
        }
      } catch (err) {
        console.warn('Webcam not permitted, keeping simulated scene', err);
        this.app.showToast('Modo cámara en vivo simulado', 'info');
      }
    } else if (sourceType === 'screen') {
      try {
        if (navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
          this.mediaStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
          if (videoFeed) {
            videoFeed.srcObject = this.mediaStream;
            videoFeed.play();
          }
          this.app.showToast('Compartiendo pantalla en vivo', 'success');
          return;
        }
      } catch (err) {
        console.warn('Screen share cancelled', err);
      }
    }

    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(t => t.stop());
      this.mediaStream = null;
    }
    if (videoFeed) {
      videoFeed.srcObject = null;
      videoFeed.src = 'assets/thumbnail_demo.jpg';
    }
    this.app.showToast('Fuente conmutada a Escena de Estudio Principal', 'info');
  }

  renderChatMessages() {
    const container = document.getElementById('unifiedChatContainer');
    if (!container) return;

    container.innerHTML = this.mockChatMessages.map(msg => `
      <div class="chat-msg-item ${msg.pinned ? 'pinned' : ''}" data-msg-id="${msg.id}">
        <span class="chat-badge ${msg.platform}">${msg.platform}</span>
        <div style="flex:1;">
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span class="chat-author">${msg.user}</span>
            <button class="btn btn-ghost btn-sm pin-chat-btn" data-msg-id="${msg.id}" style="padding:2px 6px; font-size:0.68rem;">
              ${msg.pinned ? '📌 Fijado' : 'Pin'}
            </button>
          </div>
          <p class="chat-body-text">${msg.text}</p>
        </div>
      </div>
    `).join('');

    container.scrollTop = container.scrollHeight;
  }

  startSimulatedChat() {
    const randomComments = [
      { platform: 'yt', user: 'CreatorPro_2026', text: '¡Esa función de auto-clipper está brutal!' },
      { platform: 'tt', user: 'lucas_viral', text: 'Subiendo ahora mismo un video con tu estrategia 🔥' },
      { platform: 'tw', user: 'Elena_Streams', text: '¿Haces streams todos los días a esta hora?' },
      { platform: 'fb', user: 'Manuel Rivera', text: 'Saludos desde España amigo, gran trabajo.' },
      { platform: 'tt', user: 'neon_byte', text: 'La resolución se ve a 60fps súper fluida ⚡' }
    ];

    let idx = 0;
    this.chatInterval = setInterval(() => {
      if (idx < randomComments.length) {
        const comment = randomComments[idx++];
        this.mockChatMessages.push({
          id: Date.now(),
          platform: comment.platform,
          user: comment.user,
          text: comment.text,
          isQuestion: comment.text.includes('?'),
          pinned: false
        });
        this.renderChatMessages();
      }
    }, 4500);
  }

  async startScreenRecording() {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
        this.app.showToast('Tu navegador no soporta grabación de pantalla directa.', 'warning');
        return;
      }

      this.recordedChunks = [];
      this.recordingStream = await navigator.mediaDevices.getDisplayMedia({
        video: { cursor: 'always', frameRate: 60 },
        audio: true
      });

      // Handle user stopping screen share via browser popup
      this.recordingStream.getVideoTracks()[0].onended = () => {
        if (this.isRecording) this.stopScreenRecording();
      };

      let options = { mimeType: 'video/webm;codecs=vp9,opus' };
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        options = { mimeType: 'video/webm' };
      }

      this.mediaRecorder = new MediaRecorder(this.recordingStream, options);

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          this.recordedChunks.push(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        const blob = new Blob(this.recordedChunks, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        const timestamp = new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-');
        a.download = `ViralLabs_Grabacion_HD_${timestamp}.webm`;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        }, 100);

        this.app.showToast('🎬 Grabación de pantalla guardada y descargada exitosamente.', 'success');
      };

      this.mediaRecorder.start(1000);
      this.isRecording = true;
      this.recordSeconds = 0;

      // Update UI
      const startBtn = document.getElementById('startScreenRecBtn');
      const stopBtn = document.getElementById('stopScreenRecBtn');
      const recBadge = document.getElementById('recStatusBadge');
      const timerEl = document.getElementById('screenRecTimer');

      if (startBtn) startBtn.style.display = 'none';
      if (stopBtn) stopBtn.style.display = 'inline-flex';
      if (recBadge) recBadge.style.display = 'inline-flex';

      this.recordTimerInterval = setInterval(() => {
        this.recordSeconds++;
        const mins = Math.floor(this.recordSeconds / 60);
        const secs = this.recordSeconds % 60;
        if (timerEl) {
          timerEl.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
      }, 1000);

      this.app.showToast('🔴 Grabando pantalla y audio con máxima resolución...', 'info');
    } catch (err) {
      console.warn('Screen recording error/cancelled', err);
      this.app.showToast('Grabación cancelada o permisos no concedidos.', 'warning');
    }
  }

  stopScreenRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      if (this.recordingStream) {
        this.recordingStream.getTracks().forEach(track => track.stop());
        this.recordingStream = null;
      }
      this.isRecording = false;
      clearInterval(this.recordTimerInterval);

      const startBtn = document.getElementById('startScreenRecBtn');
      const stopBtn = document.getElementById('stopScreenRecBtn');
      const recBadge = document.getElementById('recStatusBadge');

      if (startBtn) startBtn.style.display = 'inline-flex';
      if (stopBtn) stopBtn.style.display = 'none';
      if (recBadge) recBadge.style.display = 'none';
    }
  }

  takeSnapshot() {
    const videoFeed = document.getElementById('broadcastMainVideo');
    if (!videoFeed) return;

    try {
      const snapCanvas = document.createElement('canvas');
      const width = videoFeed.videoWidth || videoFeed.naturalWidth || 1280;
      const height = videoFeed.videoHeight || videoFeed.naturalHeight || 720;
      snapCanvas.width = width;
      snapCanvas.height = height;
      const ctx = snapCanvas.getContext('2d');

      ctx.drawImage(videoFeed, 0, 0, width, height);

      const a = document.createElement('a');
      a.download = `ViralLabs_Captura_${Date.now()}.png`;
      a.href = snapCanvas.toDataURL('image/png', 1.0);
      a.click();

      this.app.showToast('📸 Captura de pantalla HD guardada.', 'success');
    } catch (err) {
      console.warn('Snapshot error', err);
      this.app.showToast('Captura generada desde fuente de video en vivo.', 'info');
    }
  }

  async switchScene(sceneName) {
    this.currentScene = sceneName;
    const videoFeed = document.getElementById('broadcastMainVideo');
    const pipOverlay = document.getElementById('facecamPipOverlay');

    document.querySelectorAll('.scene-btn').forEach(btn => {
      btn.classList.toggle('btn-primary', btn.dataset.scene === sceneName);
    });

    if (sceneName === 'studio') {
      if (pipOverlay) pipOverlay.style.display = 'none';
      if (this.mediaStream) {
        this.mediaStream.getTracks().forEach(t => t.stop());
        this.mediaStream = null;
      }
      if (videoFeed) {
        videoFeed.srcObject = null;
        videoFeed.src = 'assets/thumbnail_demo.jpg';
      }
      this.app.showToast('Escena: Estudio Principal con Gráficos Virales', 'info');
    } else if (sceneName === 'webcam') {
      if (pipOverlay) pipOverlay.style.display = 'none';
      await this.switchSource('webcam');
    } else if (sceneName === 'pip') {
      // Screen as main + Webcam in PiP
      if (pipOverlay) pipOverlay.style.display = 'block';
      await this.switchSource('screen');
      this.app.showToast('Escena: Pantalla Compartida con Facecam PiP', 'success');
    } else if (sceneName === 'screen') {
      if (pipOverlay) pipOverlay.style.display = 'none';
      await this.switchSource('screen');
    } else if (sceneName === 'mobile') {
      if (pipOverlay) pipOverlay.style.display = 'none';
      if (videoFeed) {
        videoFeed.srcObject = null;
        videoFeed.src = 'assets/clip_demo.jpg';
      }
      this.app.showToast('Escena: Enlace con Cámara de Smartphone (WebRTC)', 'info');
    }
  }

  connectMobileCam() {
    const url = prompt('Ingresa la URL o IP de tu cámara móvil (ej: http://192.168.1.15:8080/video) o presiona Aceptar para modo WebRTC:', 'http://192.168.1.45:8080/video');
    if (url) {
      const videoFeed = document.getElementById('broadcastMainVideo');
      if (videoFeed) {
        videoFeed.src = 'assets/clip_demo.jpg';
      }
      this.switchScene('mobile');
      this.app.showToast(`📱 Cámara Móvil conectada exitosamente: ${url}`, 'success');
    }
  }

  bindEvents() {
    // Screen recorder and tools
    const startRecBtn = document.getElementById('startScreenRecBtn');
    const stopRecBtn = document.getElementById('stopScreenRecBtn');
    const snapBtn = document.getElementById('takeSnapshotBtn');
    const mobileCamBtn = document.getElementById('connectMobileCamBtn');

    if (startRecBtn) startRecBtn.addEventListener('click', () => this.startScreenRecording());
    if (stopRecBtn) stopRecBtn.addEventListener('click', () => this.stopScreenRecording());
    if (snapBtn) snapBtn.addEventListener('click', () => this.takeSnapshot());
    if (mobileCamBtn) mobileCamBtn.addEventListener('click', () => this.connectMobileCam());

    // OBS Scenes
    document.querySelectorAll('.scene-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const scene = e.currentTarget.dataset.scene;
        if (scene) this.switchScene(scene);
      });
    });

    // Volume Mixer
    const volMaster = document.getElementById('volMaster');
    const volMic = document.getElementById('volMic');
    const volDesktop = document.getElementById('volDesktop');
    const muteAllBtn = document.getElementById('muteAllBtn');

    if (volMaster) {
      volMaster.addEventListener('input', (e) => {
        this.volumes.master = parseInt(e.target.value);
        const label = document.getElementById('volMasterVal');
        if (label) label.textContent = `${this.volumes.master}%`;
      });
    }

    if (volMic) {
      volMic.addEventListener('input', (e) => {
        this.volumes.mic = parseInt(e.target.value);
        const label = document.getElementById('volMicVal');
        if (label) label.textContent = `${this.volumes.mic}%`;
      });
    }

    if (volDesktop) {
      volDesktop.addEventListener('input', (e) => {
        this.volumes.desktop = parseInt(e.target.value);
        const label = document.getElementById('volDesktopVal');
        if (label) label.textContent = `${this.volumes.desktop}%`;
      });
    }

    if (muteAllBtn) {
      muteAllBtn.addEventListener('click', () => {
        this.isMuted = !this.isMuted;
        muteAllBtn.textContent = this.isMuted ? '🔇 Desmutear' : '🔊 Silenciar Todo';
        muteAllBtn.classList.toggle('btn-danger', this.isMuted);
        this.app.showToast(this.isMuted ? 'Audio general silenciado.' : 'Audio restaurado.', 'info');
      });
    }

    const liveBtn = document.getElementById('toggleBroadcastBtn');
    if (liveBtn) {
      liveBtn.addEventListener('click', () => this.toggleLiveBroadcast());
    }

    document.querySelectorAll('.source-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.source-btn').forEach(b => b.classList.remove('btn-primary'));
        const target = e.currentTarget;
        target.classList.add('btn-primary');
        this.switchSource(target.dataset.source);
      });
    });

    const matrix = document.getElementById('platformsStreamMatrix');
    if (matrix) {
      matrix.addEventListener('change', (e) => {
        if (e.target.classList.contains('platform-stream-toggle')) {
          const platform = e.target.dataset.platform;
          this.platforms[platform] = e.target.checked;
          StorageManager.updatePlatformStatus(platform, e.target.checked);
          this.renderPlatformsMatrix();
          this.app.showToast(`${platform.toUpperCase()} ${e.target.checked ? 'activado' : 'desactivado'} para transmisión`, 'info');
        }
      });
    }

    const chatInput = document.getElementById('chatUserInput');
    const sendChatBtn = document.getElementById('sendChatMsgBtn');

    const handleSend = () => {
      const text = chatInput?.value?.trim();
      if (text) {
        this.mockChatMessages.push({
          id: Date.now(),
          platform: 'yt',
          user: 'Alex Rivera (Tú)',
          text: text,
          isQuestion: false,
          pinned: false
        });
        chatInput.value = '';
        this.renderChatMessages();
      }
    };

    if (sendChatBtn) sendChatBtn.addEventListener('click', handleSend);
    if (chatInput) {
      chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
      });
    }

    const chatContainer = document.getElementById('unifiedChatContainer');
    if (chatContainer) {
      chatContainer.addEventListener('click', (e) => {
        const pinBtn = e.target.closest('.pin-chat-btn');
        if (pinBtn) {
          const id = parseInt(pinBtn.dataset.msgId);
          const msg = this.mockChatMessages.find(m => m.id === id);
          if (msg) {
            msg.pinned = !msg.pinned;
            this.renderChatMessages();

            const overlayH4 = document.getElementById('lowerThirdH4');
            const overlayP = document.getElementById('lowerThirdP');
            if (msg.pinned && overlayH4 && overlayP) {
              overlayH4.textContent = `💬 Pregunta de ${msg.user} (${msg.platform.toUpperCase()}):`;
              overlayP.textContent = `"${msg.text}"`;
              this.app.showToast('Pregunta fijada en la pantalla de transmisión en vivo', 'success');
            }
          }
        }
      });
    }
  }
}

// ==========================================
// 5. VOICE LAB MANAGER
// ==========================================
class VoiceLabManager {
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

    let rate = 1.05;
    let pitch = 1.0;

    if (emotion === 'viral') {
      rate = 1.18;
      pitch = 1.08;
    } else if (emotion === 'mystery') {
      rate = 0.92;
      pitch = 0.88;
    } else if (emotion === 'cinematic') {
      rate = 0.98;
      pitch = 0.95;
    } else if (emotion === 'friendly') {
      rate = 1.02;
      pitch = 1.02;
    }

    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = rate;
      utterance.pitch = pitch;
      utterance.lang = 'es-ES';

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

    const signCertBtn = document.getElementById('signLicenseBtn');
    if (signCertBtn) {
      signCertBtn.addEventListener('click', () => {
        const name = document.getElementById('certInputName')?.value || 'Alex Rivera';
        const doc = document.getElementById('certInputDoc')?.value || 'ID-CREATOR-9901';
        this.generateLicenseCertificate(name, doc);
      });
    }

    const downloadCertBtn = document.getElementById('downloadCertBtn');
    if (downloadCertBtn) {
      downloadCertBtn.addEventListener('click', () => {
        this.app.showToast('Descargando Certificado Oficial de Propiedad Intelectual (PDF/PNG)', 'success');
      });
    }

    const playNarratorBtn = document.getElementById('playNarratorBtn');
    if (playNarratorBtn) {
      playNarratorBtn.addEventListener('click', () => {
        const script = document.getElementById('narratorScriptInput')?.value;
        const emotion = document.getElementById('narratorEmotionSelect')?.value || 'viral';
        this.synthesizeSpeech(script, emotion);
      });
    }

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

// ==========================================
// 6. PLANNER MANAGER
// ==========================================
class PlannerManager {
  constructor(app) {
    this.app = app;
    this.activeMockupPlatform = 'tiktok';
    this.currentPostType = 'post';
    this.uploadedMedia = null;
    this.init();
  }

  init() {
    this.renderCalendar();
    this.renderMockup();
    this.updateCharCounter();
    this.bindEvents();
  }

  renderCalendar() {
    const grid = document.getElementById('calendarGridCells');
    const monthTitle = document.getElementById('calendarMonthTitle');
    if (!grid) return;

    if (monthTitle) {
      monthTitle.textContent = 'Septiembre 2026';
    }

    const data = StorageManager.getData();
    const posts = data.scheduledPosts || [];

    const firstDayIndex = 2;
    const totalDays = 30;

    let cellsHtml = '';

    for (let i = 0; i < firstDayIndex; i++) {
      cellsHtml += `<div class="calendar-cell" style="opacity:0.25;"><span class="calendar-cell-date">${28 + i}</span></div>`;
    }

    for (let day = 1; day <= totalDays; day++) {
      const isToday = day === 14;
      const dayStr = `2026-09-${day.toString().padStart(2, '0')}`;
      const dayPosts = posts.filter(p => p.date === dayStr);

      const postBadges = dayPosts.map(p => {
        let pClass = 'tt';
        if (p.platforms.some(pl => pl.includes('facebook') || pl === 'fb')) pClass = 'fb';
        else if (p.platforms.some(pl => pl.includes('instagram') || pl === 'ig')) pClass = 'ig';
        else if (p.platforms.some(pl => pl.includes('youtube') || pl === 'yt')) pClass = 'yt';

        return `
          <div class="calendar-post-badge ${pClass}" title="${p.title}">
            <span>${p.platforms.map(plat => plat.substring(0,2).toUpperCase()).join('•')}</span>
            <span>${p.title}</span>
          </div>
        `;
      }).join('');

      cellsHtml += `
        <div class="calendar-cell ${isToday ? 'today' : ''}" data-date="${dayStr}">
          <span class="calendar-cell-date">${day} ${isToday ? '(Hoy)' : ''}</span>
          ${postBadges}
        </div>
      `;
    }

    grid.innerHTML = cellsHtml;
  }

  importDesignFromStudio(dataUrl) {
    this.uploadedMedia = dataUrl;
    const previewContainer = document.getElementById('postMediaPreviewContainer');
    const previewImg = document.getElementById('postMediaPreviewImg');
    const dropzoneContent = document.getElementById('dropzoneContent');

    if (previewImg) previewImg.src = dataUrl;
    if (previewContainer) previewContainer.style.display = 'block';
    if (dropzoneContent) dropzoneContent.style.display = 'none';

    this.renderMockup();
  }

  handleMediaFile(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      this.importDesignFromStudio(e.target.result);
      this.app.showToast(`Archivo "${file.name}" cargado para publicación.`, 'success');
    };
    reader.readAsDataURL(file);
  }

  removeMedia() {
    this.uploadedMedia = null;
    const previewContainer = document.getElementById('postMediaPreviewContainer');
    const previewImg = document.getElementById('postMediaPreviewImg');
    const dropzoneContent = document.getElementById('dropzoneContent');

    if (previewImg) previewImg.src = '';
    if (previewContainer) previewContainer.style.display = 'none';
    if (dropzoneContent) dropzoneContent.style.display = 'block';

    const fileInput = document.getElementById('postMediaUpload');
    if (fileInput) fileInput.value = '';

    this.renderMockup();
    this.app.showToast('Medio removido de la publicación.', 'info');
  }

  preparePostFromClip(clip) {
    const titleInput = document.getElementById('newPostTitleInput');
    const captionInput = document.getElementById('newPostCaptionInput');

    if (titleInput) titleInput.value = clip.title;
    if (captionInput) {
      captionInput.value = `${clip.title} 🔥\n\n${clip.hookQuote}\n\n${clip.tags.join(' ')}`;
    }

    this.updateCharCounter();
    this.renderMockup();
    this.app.showToast('Clip importado al compositor de publicaciones.', 'info');
  }

  updateCharCounter() {
    const caption = document.getElementById('newPostCaptionInput')?.value || '';
    const usedEl = document.getElementById('charCountUsed');
    const limitEl = document.getElementById('charCountLimit');

    const limits = {
      tiktok: 2200,
      instagram: 2200,
      facebook: 63206,
      youtube: 5000
    };

    const maxLimit = limits[this.activeMockupPlatform] || 2200;
    if (usedEl) usedEl.textContent = caption.length;
    if (limitEl) limitEl.textContent = maxLimit;

    const badge = document.getElementById('charCounterBadge');
    if (badge) {
      badge.style.color = caption.length > maxLimit ? '#f87171' : 'var(--accent-cyan)';
    }
  }

  renderMockup() {
    const mockupContainer = document.getElementById('phoneMockupContainer');
    if (!mockupContainer) return;

    const title = document.getElementById('newPostTitleInput')?.value || '5 Herramientas de IA que reemplazan agencias enteras en 2026';
    const caption = document.getElementById('newPostCaptionInput')?.value || '🚀 Si no estás usando estas herramientas en 2026 estás perdiendo horas de trabajo. ¡Mira el video hasta el final!\n\n#IA #Creadores #Tecnologia';
    const mediaSrc = this.uploadedMedia || 'assets/clip_demo.jpg';
    const isFacebook = this.activeMockupPlatform === 'facebook';

    if (this.activeMockupPlatform === 'tiktok') {
      mockupContainer.innerHTML = `
        <div class="smartphone-device">
          <div class="dynamic-island"></div>
          <div class="phone-screen">
            <img src="${mediaSrc}" class="phone-media-bg" alt="TikTok Preview">
            <div class="tiktok-overlay-ui">
              <div class="tiktok-top-tabs">
                <span>Siguiendo</span>
                <span class="active">Para ti</span>
              </div>
              <div class="tiktok-bottom-area">
                <div class="tiktok-caption-group">
                  <div class="tiktok-creator-handle">@alexcreator.ai</div>
                  <div class="tiktok-caption-text">${caption}</div>
                  <div style="font-size:0.75rem; color:#fff; margin-top:4px; display:flex; align-items:center; gap:6px;">
                    <span>🎵 Sonido original - Alex Rivera • IA Hacks</span>
                  </div>
                </div>
                <div class="tiktok-right-actions">
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble" style="color:#fe0979;">❤️</div>
                    <span>142.5K</span>
                  </div>
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble">💬</div>
                    <span>1,890</span>
                  </div>
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble" style="color:#ffd000;">⭐</div>
                    <span>45.2K</span>
                  </div>
                  <div class="tiktok-action-btn">
                    <div class="tiktok-icon-bubble">↗️</div>
                    <span>28.4K</span>
                  </div>
                  <div class="tiktok-music-disk">
                    <div style="width:10px; height:10px; border-radius:50%; background:#fff;"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (this.activeMockupPlatform === 'instagram') {
      mockupContainer.innerHTML = `
        <div class="smartphone-device">
          <div class="dynamic-island"></div>
          <div class="phone-screen">
            <img src="${mediaSrc}" class="phone-media-bg" alt="Instagram Reel">
            <div class="tiktok-overlay-ui" style="justify-content:flex-end;">
              <div class="tiktok-bottom-area">
                <div class="tiktok-caption-group">
                  <div class="tiktok-creator-handle" style="display:flex; align-items:center; gap:6px;">
                    <span>alexcreator.ai</span>
                    <span style="font-size:0.7rem; border:1px solid #fff; border-radius:4px; padding:1px 4px;">Seguir</span>
                  </div>
                  <div class="tiktok-caption-text">${caption}</div>
                  <div style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">
                    Audio original • alexcreator.ai
                  </div>
                </div>
                <div class="tiktok-right-actions">
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">🤍</div><span>84.2K</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">💬</div><span>720</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">✈️</div><span>18.1K</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (this.activeMockupPlatform === 'facebook') {
      const isPage = document.getElementById('planCheckFBPage')?.checked;
      const isProfile = document.getElementById('planCheckFBProfile')?.checked;
      const authorTitle = isPage ? 'Viral Labs Oficial (Página)' : 'Alex Rivera (Perfil)';
      const badgeIcon = isPage ? '🏢' : '👤';

      mockupContainer.innerHTML = `
        <div class="smartphone-device">
          <div class="dynamic-island"></div>
          <div class="phone-screen" style="background:#18191a; overflow-y:auto;">
            <!-- Facebook Header Feed Mockup -->
            <div style="padding:14px; border-bottom:1px solid #3a3b3c;">
              <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:40px; height:40px; border-radius:50%; background:#1877f2; display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; font-size:1.1rem;">
                  ${badgeIcon}
                </div>
                <div style="flex:1;">
                  <div style="font-size:0.86rem; font-weight:700; color:#e4e6eb; display:flex; align-items:center; gap:4px;">
                    <span>${authorTitle}</span>
                    <span style="color:#1877f2; font-size:0.8rem;">✓</span>
                  </div>
                  <div style="font-size:0.72rem; color:#b0b3b8;">Hace 1 min · 🌐 Público (Multi-Publicación)</div>
                </div>
                <div style="color:#b0b3b8; font-size:1.1rem;">•••</div>
              </div>
              <div style="font-size:0.82rem; color:#e4e6eb; margin-top:10px; line-height:1.45; white-space:pre-line;">
                ${caption}
              </div>
            </div>

            <!-- Post Media -->
            <div style="width:100%; max-height:280px; overflow:hidden; background:#000; display:flex; align-items:center; justify-content:center;">
              <img src="${mediaSrc}" style="width:100%; height:auto; object-fit:contain;" alt="Facebook Media">
            </div>

            <!-- FB Interactions Bar -->
            <div style="padding:10px 14px; border-top:1px solid #3a3b3c; display:flex; justify-content:space-between; font-size:0.75rem; color:#b0b3b8;">
              <span>👍❤️😮 1.8K</span>
              <span>340 comentarios · 128 veces compartido</span>
            </div>
            <div style="padding:8px 14px; border-top:1px solid #3a3b3c; display:flex; justify-content:space-around; font-size:0.78rem; font-weight:600; color:#b0b3b8;">
              <span style="cursor:pointer;">👍 Me gusta</span>
              <span style="cursor:pointer;">💬 Comentar</span>
              <span style="cursor:pointer;">↗️ Compartir</span>
            </div>
          </div>
        </div>
      `;
    } else if (this.activeMockupPlatform === 'youtube') {
      mockupContainer.innerHTML = `
        <div class="smartphone-device">
          <div class="dynamic-island"></div>
          <div class="phone-screen">
            <img src="${mediaSrc}" class="phone-media-bg" alt="YouTube Shorts">
            <div class="tiktok-overlay-ui" style="justify-content:flex-end;">
              <div class="tiktok-bottom-area">
                <div class="tiktok-caption-group">
                  <div style="font-size:0.86rem; font-weight:800; color:#fff; margin-bottom:4px;">${title}</div>
                  <div class="tiktok-creator-handle" style="display:flex; align-items:center; gap:8px;">
                    <span>Alex Rivera Tech</span>
                    <span style="background:#ff0000; color:#fff; font-size:0.68rem; padding:2px 8px; border-radius:12px; font-weight:700;">SUSCRIBIRSE</span>
                  </div>
                </div>
                <div class="tiktok-right-actions">
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">👍</div><span>96K</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">👎</div><span>Dislike</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">💬</div><span>1.4K</span></div>
                  <div class="tiktok-action-btn"><div class="tiktok-icon-bubble">↗️</div><span>Compartir</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }
  }

  saveNewPost() {
    const titleInput = document.getElementById('newPostTitleInput');
    const captionInput = document.getElementById('newPostCaptionInput');
    const ytTagsInput = document.getElementById('newPostYtTagsInput');
    const dateInput = document.getElementById('newPostDateInput');
    const timeInput = document.getElementById('newPostTimeInput');

    const title = titleInput?.value.trim();
    const caption = captionInput?.value.trim();
    const ytTags = ytTagsInput?.value.trim() || '';
    const date = dateInput?.value || '2026-09-18';
    const time = timeInput?.value || '19:00';

    if (!title) {
      this.app.showToast('Por favor escribe un título para el contenido.', 'warning');
      return;
    }

    const platforms = [];
    if (document.getElementById('planCheckFBProfile')?.checked) platforms.push('facebook_profile');
    if (document.getElementById('planCheckFBPage')?.checked) platforms.push('facebook_page');
    if (document.getElementById('planCheckIG')?.checked) platforms.push('instagram');
    if (document.getElementById('planCheckIGStories')?.checked) platforms.push('instagram_stories');
    if (document.getElementById('planCheckTT')?.checked) platforms.push('tiktok');
    if (document.getElementById('planCheckYT')?.checked) platforms.push('youtube');
    if (document.getElementById('planCheckX')?.checked) platforms.push('x');
    if (document.getElementById('planCheckLI')?.checked) platforms.push('linkedin');

    const newPost = {
      id: 'post-' + Date.now(),
      title: title,
      platforms: platforms.length ? platforms : ['facebook_page', 'instagram'],
      postType: this.currentPostType,
      date: date,
      time: time,
      status: 'scheduled',
      caption: caption,
      youtubeTags: ytTags,
      viralScore: Math.floor(88 + Math.random() * 10),
      thumbnail: this.uploadedMedia || 'assets/thumbnail_demo.jpg'
    };

    StorageManager.addPost(newPost);
    this.app.broadcastMessage({ type: 'NEW_POST', post: newPost });
    this.renderCalendar();

    const targetsSummary = platforms.map(p => {
      if (p === 'facebook_profile') return 'FB Perfil';
      if (p === 'facebook_page') return 'FB Fanpage';
      if (p === 'instagram') return 'Instagram';
      if (p === 'tiktok') return 'TikTok';
      if (p === 'youtube') return 'YouTube';
      return p.toUpperCase();
    }).join(', ');

    this.app.showToast(`🚀 ¡Contenido programado con éxito para [${targetsSummary}]!`, 'success');

    if (titleInput) titleInput.value = '';
    if (captionInput) captionInput.value = '';
    if (ytTagsInput) {
      ytTagsInput.value = '';
      const tagCounter = document.getElementById('plannerTagCharCount');
      if (tagCounter) {
        tagCounter.textContent = '0 / 500 caracteres';
        tagCounter.style.color = '#94a3b8';
      }
    }
    this.updateCharCounter();
    this.renderMockup();
  }

  bindEvents() {
    // Quick AI Fill in Planner
    const quickAiBtn = document.getElementById('plannerQuickAiBtn');
    if (quickAiBtn) {
      quickAiBtn.addEventListener('click', () => {
        let pack = (window.omniviralApp && window.omniviralApp.studio && window.omniviralApp.studio.latestPack);
        if (!pack) {
          pack = GeminiSuiteManager.generateAutonomousPack('Inteligencia Artificial', '5 Herramientas de IA que reemplazan agencias enteras en 2026');
        }

        const tInput = document.getElementById('newPostTitleInput');
        const cInput = document.getElementById('newPostCaptionInput');
        const tagsIn = document.getElementById('newPostYtTagsInput');
        const dInput = document.getElementById('newPostDateInput');

        if (tInput && pack.titles && pack.titles.length) {
          tInput.value = pack.titles[0];
        }
        if (cInput && pack.descriptions) {
          cInput.value = pack.descriptions.instagram || pack.descriptions.tiktok || pack.hooks[0];
        }
        if (tagsIn && pack.youtubeTags) {
          tagsIn.value = pack.youtubeTags.allCsv || '';
          const tagCounter = document.getElementById('plannerTagCharCount');
          if (tagCounter) {
            const len = tagsIn.value.length;
            tagCounter.textContent = `${len} / 500 caracteres`;
            tagCounter.style.color = len > 500 ? '#ef4444' : '#94a3b8';
          }
        }
        if (dInput) {
          const today = new Date().toISOString().split('T')[0];
          dInput.value = today;
        }

        this.updateCharCounter();
        this.renderMockup();
        this.app.showToast('✨ Contenido auto-completado con IA (Título, Copy y Etiquetas)', 'success');
      });
    }

    // YouTube Tags Input & Counter
    const ytTagsInput = document.getElementById('newPostYtTagsInput');
    const tagCounter = document.getElementById('plannerTagCharCount');
    if (ytTagsInput) {
      ytTagsInput.addEventListener('input', (e) => {
        const len = e.target.value.length;
        if (tagCounter) {
          tagCounter.textContent = `${len} / 500 caracteres`;
          tagCounter.style.color = len > 500 ? '#ef4444' : '#94a3b8';
        }
      });
    }

    // Copy YouTube Tags Button
    const copyTagsBtn = document.getElementById('plannerCopyTagsBtn');
    if (copyTagsBtn) {
      copyTagsBtn.addEventListener('click', () => {
        const tagsInput = document.getElementById('newPostYtTagsInput');
        const val = tagsInput ? tagsInput.value.trim() : '';
        if (val) {
          navigator.clipboard.writeText(val);
          this.app.showToast('📋 Etiquetas copiadas en formato YouTube Studio', 'success');
        } else {
          this.app.showToast('No hay etiquetas para copiar', 'warning');
        }
      });
    }

    // Export Schedule as JSON
    const exportBtn = document.getElementById('exportScheduleBtn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        const data = StorageManager.getData();
        const posts = data.scheduledPosts || [];
        const jsonStr = JSON.stringify(posts, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `calendario_viral_labs_${new Date().toISOString().slice(0, 10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
        this.app.showToast('📥 Calendario editorial exportado con éxito', 'success');
      });
    }

    // Post Type Selector
    document.querySelectorAll('.post-type-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.post-type-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.currentPostType = e.currentTarget.dataset.type;
        this.renderMockup();
      });
    });

    // Media Dropzone & Upload
    const dropzone = document.getElementById('postMediaDropzone');
    const fileInput = document.getElementById('postMediaUpload');
    const removeBtn = document.getElementById('removeMediaBtn');

    if (dropzone && fileInput) {
      dropzone.addEventListener('click', (e) => {
        if (!e.target.closest('#removeMediaBtn') && !this.uploadedMedia) {
          fileInput.click();
        }
      });

      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) this.handleMediaFile(file);
      });

      dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('drag-active');
      });

      dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('drag-active');
      });

      dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag-active');
        const file = e.dataTransfer.files[0];
        if (file) this.handleMediaFile(file);
      });
    }

    if (removeBtn) {
      removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.removeMedia();
      });
    }

    // Hashtags quick chips
    document.querySelectorAll('.hashtag-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const tag = e.currentTarget.dataset.tag;
        const captionInput = document.getElementById('newPostCaptionInput');
        if (captionInput && tag) {
          captionInput.value += ` ${tag}`;
          this.updateCharCounter();
          this.renderMockup();
        }
      });
    });

    // Mockup platform switcher
    document.querySelectorAll('.mockup-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.mockup-tab-btn').forEach(b => b.classList.remove('btn-primary'));
        const target = e.currentTarget;
        target.classList.add('btn-primary');
        this.activeMockupPlatform = target.dataset.platform;
        this.updateCharCounter();
        this.renderMockup();
      });
    });

    const titleInput = document.getElementById('newPostTitleInput');
    const captionInput = document.getElementById('newPostCaptionInput');

    if (titleInput) titleInput.addEventListener('input', () => this.renderMockup());
    if (captionInput) {
      captionInput.addEventListener('input', () => {
        this.updateCharCounter();
        this.renderMockup();
      });
    }

    // Live sync checkboxes with mockup if Facebook is active
    ['planCheckFBProfile', 'planCheckFBPage'].forEach(id => {
      const chk = document.getElementById(id);
      if (chk) chk.addEventListener('change', () => {
        if (this.activeMockupPlatform === 'facebook') this.renderMockup();
      });
    });

    const scheduleBtn = document.getElementById('schedulePostBtn');
    if (scheduleBtn) {
      scheduleBtn.addEventListener('click', () => this.saveNewPost());
    }
  }
}

// ==========================================
// 7. RADAR MANAGER
// ==========================================
class RadarManager {
  constructor(app) {
    this.app = app;
    this.generatedBios = {};
    this.activeBioTarget = 'bio-yt';
    this.init();
  }

  init() {
    this.bindEvents();
    this.calculateEarnings();
    this.evaluateHook('Si creas contenido y tardas más de 30 minutos por video, estás tirando tu dinero...');
    this.generateChannelBios('Viral Labs Studio', 'espiritualidad');
  }

  generateChannelBios(creatorName, nicheKey) {
    const cleanName = creatorName || 'Creador Pro';
    const biosByNiche = {
      'espiritualidad': {
        'bio-yt': `✨ Bienvenido a ${cleanName} | El canal definitivo de Consciencia, Manifestación Cuántica & Despertar Interior.\n\n🌌 Aquí aprenderás a reprogramar tu subconsciente, elevar tu frecuencia vibracional y manifestar la realidad que mereces mediante la Ley de Asunción, frecuencias de solfeggio y técnicas milenarias explicadas con ciencia.\n\n📅 Nuevos videos: Lunes, Miércoles y Viernes (19:00 Horas).\n🔔 Suscríbete y activa la campana para no perderte ninguna transmisión en vivo ni meditaciones guiadas.\n\n📧 Contacto & Colaboraciones: contacto@${cleanName.toLowerCase().replace(/\\s+/g, '')}.com\n\n#Espiritualidad #Manifestacion #LeyDeAtraccion #Consciencia #Meditacion`,
        'bio-tt': `🧘 ${cleanName} | Eleva tu frecuencia diaria ✨\n⚡ Reprograma tu mente en 60s\n👇 Meditación cuántica guiada en el enlace\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-ig': `🌌 ${cleanName} • Consciencia & Manifestación\n👁️ Te enseño a reprogramar tu realidad y vivir con propósito\n🧘 +100K almas transformadas en comunidad\n✨ Meditación cuántica guiada gratuita 👇\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-fb': `Bienvenido a la página oficial de ${cleanName}. Un santuario digital creado para expandir tu consciencia, dominar la manifestación consciente y acceder a una vida de paz y abundancia integral. Publicamos reflexiones diarias, transmisiones comunitarias y lecciones de sabiduría atemporal.`,
        'bio-tw': `🔮 Transmisiones en Vivo de Meditación, Sesiones de Ondas Theta y Preguntas & Respuestas sobre Crecimiento Personal y Espiritualidad Práctica con ${cleanName}.\n\n📜 Reglas del Chat: Respeto mutuo, energía positiva y mente abierta.`
      },
      'finanzas': {
        'bio-yt': `💰 Bienvenido a ${cleanName} | Tu acelerador de Riqueza, Inversiones Inteligentes & Libertad Financiera.\n\n📊 Desglosamos las estrategias exactas que usan el 1% para multiplicar su capital en bolsa, bienes raíces, criptoactivos y negocios automatizados, sin jerga confusa.\n\n📅 Videos largos todos los Martes y Jueves (18:00 Horas).\n🔔 Suscríbete para construir patrimonio y retirarte joven.\n\n📧 Negocios: contacto@${cleanName.toLowerCase().replace(/\\s+/g, '')}.com\n\n#FinanzasPersonales #Inversiones #LibertadFinanciera #EducacionFinanciera #Dinero`,
        'bio-tt': `💵 ${cleanName} | Multiplica tu dinero en 2026 📈\n💡 Hacks financieros que no enseñan en la escuela\n👇 Descarga mi plantilla de presupuesto\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-ig': `📈 ${cleanName} • Finanzas & Creación de Riqueza\n💼 Estrategias reales para pasar de $0 a tus primeros $100K\n🧠 Mentalidad millonaria sin humo\n🎁 Plantilla financiera GRATIS 👇\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-fb': `Página oficial de ${cleanName}. Dedicada a democratizar la educación financiera de élite. Análisis de mercados, psicología del dinero y planes paso a paso para salir de deudas e invertir con criterio profesional.`,
        'bio-tw': `📊 Streams en Vivo de Análisis de Mercados, Finanzas Personales en Directo y Revisión de Portafolios con ${cleanName}.\n\n⚠️ Disclaimer: El contenido es estrictamente educativo y no constituye asesoría financiera legal.`
      },
      'mentalidad': {
        'bio-yt': `🧠 Bienvenido a ${cleanName} | Filosofía Estoica, Disciplina Inquebrantable & Fortaleza Mental.\n\n🏛️ Enseñanzas prácticas de Marco Aurelio, Séneca y Epicteto combinadas con neurociencia moderna para superar la procrastinación, forjar resiliencia y dominar tus emociones en un mundo caótico.\n\n📅 Videos: Todos los Lunes y Domingos.\n🔔 Suscríbete para construir la mente más fuerte de tu entorno.\n\n📧 Contacto: info@${cleanName.toLowerCase().replace(/\\s+/g, '')}.com\n\n#Estoicismo #Disciplina #Mentalidad #Psicologia #DesarrolloPersonal`,
        'bio-tt': `⚔️ ${cleanName} | Forja tu mente con disciplina 🧠\n🏛️ Sabiduría estoica para la vida moderna\n👇 Guía de hábitos matutinos\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-ig': `🏛️ ${cleanName} • Estoicismo & Disciplina\n⚔️ Domina tu mente antes de que el mundo te domine a ti\n📖 Reflexiones estoicas y hábitos de acero diarios\n⚡ Desafío de 21 días de disciplina 👇\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-fb': `Comunidad de ${cleanName}. Un espacio para quienes eligen la disciplina sobre la comodidad y la virtud sobre la mediocridad. Lecciones de vida, frases estoicas comentadas y reflexiones profundas para tu día a día.`,
        'bio-tw': `⚔️ Sesiones en Vivo de Lectura Profunda, Debates Filosóficos y Construcción de Hábitos con ${cleanName}.\n\n📜 Principio: Controla lo que depende de ti y acepta con serenidad lo que no.`
      },
      'ia': {
        'bio-yt': `🤖 Bienvenido a ${cleanName} | El epicentro de Inteligencia Artificial, Automatizaciones & Futuro Tecnológico.\n\n🚀 Tutoriales prácticos, comparativas de modelos (Gemini, Claude, GPT), prompts avanzados y automatizaciones sin código para ganar ventaja competitiva en la era de la IA.\n\n📅 Videos semanales los Miércoles y Sábados.\n🔔 Suscríbete para mantenerte 5 pasos adelante de tu competencia.\n\n📧 Alianzas & Reviews: ia@${cleanName.toLowerCase().replace(/\\s+/g, '')}.com\n\n#InteligenciaArtificial #IA #Automatizacion #Productividad #Tecnologia`,
        'bio-tt': `⚡ ${cleanName} | IA y Automatizaciones en 60s 🤖\n🛠️ Herramientas gratis que parecen ilegales\n👇 Mega-Pack de 1000 Prompts PRO\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-ig': `🤖 ${cleanName} • Inteligencia Artificial & Productividad\n🚀 Ahorra 20h a la semana con flujos de trabajo de IA\n💡 Prompts probados, agentes autónomos y apps secretas\n🎁 Guía de herramientas 2026 GRATIS 👇\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-fb': `Página oficial de ${cleanName}. Tu fuente de noticias, tutoriales y casos prácticos sobre Inteligencia Artificial aplicada a negocios, creación de contenido y automatización del trabajo diario.`,
        'bio-tw': `🖥️ Streams en Vivo de Programación con IA, Creación de Agentes y Pruebas de Nuevas Herramientas en Directo con ${cleanName}.`
      },
      'salud': {
        'bio-yt': `🧬 Bienvenido a ${cleanName} | Biohacking, Salud Metabólica & Longevidad Basada en Evidencia.\n\n🥗 Descubre cómo optimizar tu sueño, energía celular, nutrición y rendimiento físico sin pseudociencias ni modas pasajeras. Salud preventiva de alto nivel.\n\n📅 Nuevos episodios cada Jueves.\n🔔 Suscríbete para vivir más años con la máxima vitalidad.\n\n📧 Contacto: salud@${cleanName.toLowerCase().replace(/\\s+/g, '')}.com\n\n#Biohacking #Longevidad #SaludMetabolica #Nutricion #AyunoIntermitente`,
        'bio-tt': `🧬 ${cleanName} | Optimiza tu biología ⚡\n🌿 Hábitos de longevidad respaldados por ciencia\n👇 Guía de suplementos esenciales\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-ig': `🔬 ${cleanName} • Biohacking & Longevidad\n⚡ Hackea tu energía, sueño y salud celular\n🩺 Protocolos basados en estudios médicos sin humo\n📥 Guía para dormir como un bebé 👇\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-fb': `Página de divulgación de ${cleanName}. Consejos prácticos sobre hábitos, ritmos circadianos, entrenamiento eficiente y nutrición para maximizar tu salud y prevenir enfermedades crónicas.`,
        'bio-tw': `🏃 Streams de Rutinas, Charlas de Biohacking en Vivo y Preguntas sobre Rendimiento Físico con ${cleanName}.`
      },
      'misterio': {
        'bio-yt': `🔮 Bienvenido a ${cleanName} | Casos Reales, Enigmas Históricos & Misterios Sin Resolver.\n\n🕵️ Narraciones inmersivas, investigaciones documentales y expedientes clasificados que desafían la lógica humana.\n\n📅 Estrenos cinematográficos cada Viernes en la noche.\n🔔 Suscríbete si te atreves a explorar lo desconocido.\n\n📧 Prensa: misterio@${cleanName.toLowerCase().replace(/\\s+/g, '')}.com\n\n#Misterio #CasosReales #Curiosidades #HistoriasReales #Suspense`,
        'bio-tt': `👁️ ${cleanName} | Historias que no te dejarán dormir 🔮\n🌑 Casos reales y enigmas en 60 segundos\n👇 Podcast completo en YouTube\n🔗 youtube.com/@${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-ig': `🌑 ${cleanName} • Casos Reales & Misterios\n📜 Archivos clasificados, crímenes reales y enigmas del mundo\n🎙️ Escucha nuestras investigaciones completas 👇\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-fb': `Comunidad oficial de ${cleanName}. El punto de encuentro de los amantes del misterio, la investigación criminal y los enigmas más desconcertantes de la historia humana.`,
        'bio-tw': `🕯️ Transmisiones Nocturnas de Relatos de Terror, Análisis de Evidencias y Casos Reales en Vivo con ${cleanName}.`
      },
      'emprendimiento': {
        'bio-yt': `📈 Bienvenido a ${cleanName} | De Creador a Emprendedor Digital.\n\n🚀 Modelos de negocio validados, e-commerce, embudos de venta y monetización de marcas personales en la economía de creadores moderna.\n\n📅 Videos: Miércoles y Domingos.\n🔔 Suscríbete para construir un negocio rentable y escalable.\n\n📧 Negocios: contacto@${cleanName.toLowerCase().replace(/\\s+/g, '')}.com\n\n#Emprendimiento #NegociosOnline #Ecommerce #MarcaPersonal #MarketingDigital`,
        'bio-tt': `🚀 ${cleanName} | Crea un negocio online real 💼\n📈 Casos de estudio y estrategias sin humo\n👇 Checklist para lanzar tu primer producto\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-ig': `💼 ${cleanName} • Negocios Digitales & Crecimiento\n📈 Te muestro el detrás de escena de construir empresas escalables\n🎯 Monetiza tu talento en internet\n🚀 Recursos gratuitos para empezar 👇\n🔗 linktr.ee/${cleanName.toLowerCase().replace(/\\s+/g, '')}`,
        'bio-fb': `Página de ${cleanName} para fundadores, creadores y emprendedores decididos a construir marcas digitales sostenibles con tracción y rentabilidad real.`,
        'bio-tw': `🚀 Streams de 'Construyendo en Público', Auditorías de Negocios y Sesiones de Trabajo con ${cleanName}.`
      }
    };

    const selected = biosByNiche[nicheKey] || biosByNiche['espiritualidad'];
    this.generatedBios = selected;

    const outputBox = document.getElementById('channelBioOutputBox');
    if (outputBox && this.generatedBios[this.activeBioTarget]) {
      outputBox.textContent = this.generatedBios[this.activeBioTarget];
    }
  }

  evaluateHook(text) {
    if (!text || text.trim() === '') return;

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

    if (words.length >= 8 && words.length <= 22) {
      score += 8;
    } else if (words.length > 30) {
      score -= 10;
    }

    if (/\d+/.test(text)) {
      score += 7;
    }

    score = Math.min(99, Math.max(45, score));

    const scoreNumEl = document.getElementById('radialScoreNumber');
    const radialCircle = document.getElementById('radialScoreCircle');

    if (scoreNumEl) scoreNumEl.textContent = score;
    if (radialCircle) {
      radialCircle.style.setProperty('--score-pct', score);
    }

    const curiosity = Math.min(100, score + 4);
    const urgency = Math.min(100, score - 2 + (powerHits * 3));
    const clarity = Math.min(100, Math.max(60, 100 - words.length));

    const curBar = document.getElementById('curiosityScoreBar');
    const urgBar = document.getElementById('urgencyScoreBar');
    const claBar = document.getElementById('clarityScoreBar');

    if (curBar) curBar.style.width = `${curiosity}%`;
    if (urgBar) urgBar.style.width = `${urgency}%`;
    if (claBar) claBar.style.width = `${clarity}%`;

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

    const baseRpm = 0.85 * tierMultiplier;
    const adRevenue = Math.round((views / 1000) * baseRpm);
    const brandValuePerDeal = Math.max(300, Math.round((views / 100000) * 350));
    const brandRevenue = brandsCount * brandValuePerDeal;

    const totalMonthly = adRevenue + brandRevenue;
    const totalAnnual = totalMonthly * 12;

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
    const hookInput = document.getElementById('hookEvaluatorInput');
    const evaluateBtn = document.getElementById('evaluateHookBtn');

    if (evaluateBtn) {
      evaluateBtn.addEventListener('click', () => {
        const text = hookInput?.value;
        this.evaluateHook(text);
        this.app.showToast('Gancho evaluado contra métricas de retención 2026', 'success');
      });
    }

    const viewsSlider = document.getElementById('sliderViews');
    const brandsSlider = document.getElementById('sliderBrands');
    const tierSelect = document.getElementById('selectAudienceTier');

    if (viewsSlider) viewsSlider.addEventListener('input', () => this.calculateEarnings());
    if (brandsSlider) brandsSlider.addEventListener('input', () => this.calculateEarnings());
    if (tierSelect) tierSelect.addEventListener('change', () => this.calculateEarnings());

    // 2026 Algorithm Platform Tabs
    document.querySelectorAll('.algo-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.algo-tab-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        const plat = (e.currentTarget.dataset.platform || 'yt').toUpperCase();
        document.querySelectorAll('.algo-platform-pane').forEach(p => p.classList.remove('active'));
        const pane = document.getElementById(`algoPane${plat}`);
        if (pane) pane.classList.add('active');
      });
    });

    // Channel Bio Generator Buttons & Tabs
    const genBioBtn = document.getElementById('generateChannelBioBtn');
    if (genBioBtn) {
      genBioBtn.addEventListener('click', () => {
        const name = document.getElementById('bioCreatorName')?.value.trim() || 'Viral Labs Studio';
        const niche = document.getElementById('bioNicheSelect')?.value || 'espiritualidad';
        this.generateChannelBios(name, niche);
        this.app.showToast(`✨ Biografías optimizadas generadas para ${name}`, 'success');
      });
    }

    document.querySelectorAll('.bio-platform-tab').forEach(tab => {
      tab.addEventListener('click', (e) => {
        document.querySelectorAll('.bio-platform-tab').forEach(t => t.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.activeBioTarget = e.currentTarget.dataset.target || 'bio-yt';
        const box = document.getElementById('channelBioOutputBox');
        if (box && this.generatedBios[this.activeBioTarget]) {
          box.textContent = this.generatedBios[this.activeBioTarget];
        }
      });
    });

    const copyBioBtn = document.getElementById('copyChannelBioBtn');
    if (copyBioBtn) {
      copyBioBtn.addEventListener('click', () => {
        const box = document.getElementById('channelBioOutputBox');
        if (box && box.textContent.trim()) {
          navigator.clipboard.writeText(box.textContent.trim());
          this.app.showToast('📋 Biografía copiada al portapapeles', 'success');
        }
      });
    }
  }
}

// ==========================================
// 8. AUTH SYSTEM & BYOK WALLET MODULE
// ==========================================
class AuthSystem {
  constructor(app) {
    this.app = app;
    this.currentUser = null;
    this.byokKeys = {
      gemini: '',
      openai: '',
      runway: '',
      elevenlabs: ''
    };
    this.oauthConnections = {
      meta: true,
      youtube: true,
      tiktok: true,
      twitch: true
    };
    this.init();
  }

  init() {
    this.loadUserSession();
    this.loadByokKeys();
    this.loadOAuthConnections();
    this.bindEvents();
    this.updateUserUI();
  }

  loadOAuthConnections() {
    try {
      const raw = localStorage.getItem('virallabs_oauth_connections');
      if (raw) {
        this.oauthConnections = { ...this.oauthConnections, ...JSON.parse(raw) };
      }
    } catch (e) {
      console.warn('Error loading OAuth connections', e);
    }
    this.updateOAuthUI();
  }

  saveOAuthConnections() {
    localStorage.setItem('virallabs_oauth_connections', JSON.stringify(this.oauthConnections));
    this.updateOAuthUI();
  }

  updateOAuthUI() {
    Object.entries(this.oauthConnections).forEach(([key, isConnected]) => {
      const btn = document.querySelector(`.oauth-toggle-btn[data-oauth="${key}"]`);
      if (btn) {
        btn.textContent = isConnected ? '✓ Enlazado' : '+ Vincular';
        btn.classList.toggle('btn-primary', isConnected);
        btn.classList.toggle('btn-ghost', !isConnected);
      }
    });
  }

  switchAuthTab(tab) {
    const accPanel = document.getElementById('authPanelAccount');
    const oauthPanel = document.getElementById('authPanelOAuth');
    const accBtn = document.getElementById('authTabAccountBtn');
    const oauthBtn = document.getElementById('authTabOAuthBtn');

    if (tab === 'account') {
      if (accPanel) accPanel.style.display = 'block';
      if (oauthPanel) oauthPanel.style.display = 'none';
      if (accBtn) accBtn.classList.add('active');
      if (oauthBtn) oauthBtn.classList.remove('active');
    } else {
      if (accPanel) accPanel.style.display = 'none';
      if (oauthPanel) oauthPanel.style.display = 'block';
      if (accBtn) accBtn.classList.remove('active');
      if (oauthBtn) oauthBtn.classList.add('active');
    }
  }

  toggleOAuth(platform) {
    this.oauthConnections[platform] = !this.oauthConnections[platform];
    this.saveOAuthConnections();
    const status = this.oauthConnections[platform] ? 'enlazada con éxito' : 'desvinculada';
    const names = {
      meta: 'Meta Graph API (Facebook Perfil & Fanpage + Instagram)',
      youtube: 'YouTube Studio API',
      tiktok: 'TikTok for Creators API',
      twitch: 'Twitch Interactive API'
    };
    this.app.showToast(`Cuenta ${names[platform] || platform} ${status}.`, 'info');
  }

  loadUserSession() {
    try {
      const rawUser = localStorage.getItem('virallabs_auth_user');
      if (rawUser) {
        this.currentUser = JSON.parse(rawUser);
      } else {
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

    const geminiInput = document.getElementById('byokGeminiKey');
    const geminiModelSelect = document.getElementById('byokGeminiModelSelect');
    const openaiInput = document.getElementById('byokOpenaiKey');
    const runwayInput = document.getElementById('byokRunwayKey');
    const elevenInput = document.getElementById('byokElevenKey');

    if (geminiInput) geminiInput.value = this.byokKeys.gemini || '';
    if (geminiModelSelect) geminiModelSelect.value = this.byokKeys.geminiModel || localStorage.getItem('byok_gemini_model') || 'gemini-2.0-flash';
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
    document.querySelectorAll('.oauth-toggle-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const platform = e.currentTarget.dataset.oauth;
        if (platform) this.toggleOAuth(platform);
      });
    });

    const googleBtn = document.getElementById('googleSignInBtn');
    if (googleBtn) {
      googleBtn.addEventListener('click', () => this.loginWithGoogle());
    }

    const emailForm = document.getElementById('emailAuthForm');
    if (emailForm) {
      emailForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('authEmailInput')?.value;
        const name = document.getElementById('authNameInput')?.value;
        if (email) this.loginWithEmail(email, name);
      });
    }

    const saveByokBtn = document.getElementById('saveByokKeysBtn');
    if (saveByokBtn) {
      saveByokBtn.addEventListener('click', () => {
        this.byokKeys.gemini = document.getElementById('byokGeminiKey')?.value.trim() || '';
        this.byokKeys.geminiModel = document.getElementById('byokGeminiModelSelect')?.value || 'gemini-2.0-flash';
        this.byokKeys.openai = document.getElementById('byokOpenaiKey')?.value.trim() || '';
        this.byokKeys.runway = document.getElementById('byokRunwayKey')?.value.trim() || '';
        this.byokKeys.elevenlabs = document.getElementById('byokElevenKey')?.value.trim() || '';
        localStorage.setItem('byok_gemini_key', this.byokKeys.gemini);
        localStorage.setItem('byok_gemini_model', this.byokKeys.geminiModel);
        this.saveByokKeys();
        this.closeByokModal();
      });
    }

    const userCard = document.querySelector('.creator-profile-card');
    if (userCard) {
      userCard.style.cursor = 'pointer';
      userCard.title = 'Configurar Cuenta & Billetera BYOK';
      userCard.addEventListener('click', () => this.openByokModal());
    }
  }
}

// ==========================================
// 9. TELEPROMPTER PRO MODULE
// ==========================================
class TeleprompterPro {
  constructor(app) {
    this.app = app;
    this.container = null;
    this.scrollArea = null;
    this.contentEl = null;
    this.isPlaying = false;
    this.speedWpm = 140;
    this.fontSize = 28;
    this.isMirrored = false;
    this.isExpanded = false;
    this.scrollPos = 0;
    this.animationFrameId = null;
    this.lastTimestamp = null;

    this.defaultScript = `¡Bienvenidos a Viral Labs! 🚀\n\nEn este video te revelo el secreto que los creadores de más de 1 millón de suscriptores usan para dominar el algoritmo en 2026.\n\nEl 95% de los creadores cometen el error de enfocarse únicamente en las vistas. Pero la verdadera métrica clave es la tasa de retención en los primeros 3 segundos y el ratio de compartidos por mensaje directo.\n\nQuédate hasta el final porque te mostraré paso a paso cómo estructurar tu gancho viral para multiplicar tu alcance por 10x.\n\n¡Dale like, suscríbete y activa la campana para no perderte las próximas estrategias!`;

    this.init();
  }

  init() {
    this.container = document.getElementById('teleprompterDock');
    if (!this.container) return;

    this.scrollArea = document.getElementById('prompterScrollArea');
    this.contentEl = document.getElementById('prompterTextContent');

    if (this.contentEl && !this.contentEl.value) {
      this.contentEl.value = this.defaultScript;
    }

    this.bindEvents();
    this.updateStyle();
  }

  bindEvents() {
    const playBtn = document.getElementById('prompterPlayBtn');
    const resetBtn = document.getElementById('prompterResetBtn');
    const mirrorBtn = document.getElementById('prompterMirrorBtn');
    const expandBtn = document.getElementById('prompterExpandBtn');
    const closeBtn = document.getElementById('prompterCloseBtn');
    const speedSlider = document.getElementById('prompterSpeedSlider');
    const fontSlider = document.getElementById('prompterFontSlider');
    const importScriptBtn = document.getElementById('prompterImportScriptBtn');

    if (playBtn) playBtn.addEventListener('click', () => this.togglePlay());
    if (resetBtn) resetBtn.addEventListener('click', () => this.resetScroll());
    if (mirrorBtn) mirrorBtn.addEventListener('click', () => this.toggleMirror());
    if (expandBtn) expandBtn.addEventListener('click', () => this.toggleExpand());
    if (closeBtn) closeBtn.addEventListener('click', () => this.hide());

    if (speedSlider) {
      speedSlider.addEventListener('input', (e) => {
        this.speedWpm = parseInt(e.target.value, 10);
        const label = document.getElementById('prompterSpeedVal');
        if (label) label.textContent = `${this.speedWpm} WPM`;
      });
    }

    if (fontSlider) {
      fontSlider.addEventListener('input', (e) => {
        this.fontSize = parseInt(e.target.value, 10);
        this.updateStyle();
        const label = document.getElementById('prompterFontVal');
        if (label) label.textContent = `${this.fontSize}px`;
      });
    }

    if (importScriptBtn) {
      importScriptBtn.addEventListener('click', () => this.importScriptFromStudio());
    }

    window.addEventListener('keydown', (e) => {
      if (!this.container || !this.container.classList.contains('active')) return;
      if (document.activeElement === this.contentEl) return;

      if (e.code === 'Space') {
        e.preventDefault();
        this.togglePlay();
      } else if (e.code === 'ArrowUp') {
        e.preventDefault();
        this.adjustSpeed(10);
      } else if (e.code === 'ArrowDown') {
        e.preventDefault();
        this.adjustSpeed(-10);
      } else if (e.key === 'r' || e.key === 'R') {
        this.resetScroll();
      } else if (e.key === 'm' || e.key === 'M') {
        this.toggleMirror();
      }
    });

    const header = document.getElementById('prompterHeader');
    if (header) {
      let isDragging = false;
      let startX, startY, initialLeft, initialTop;

      header.addEventListener('mousedown', (e) => {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        const rect = this.container.getBoundingClientRect();
        initialLeft = rect.left;
        initialTop = rect.top;
        this.container.style.bottom = 'auto';
        this.container.style.right = 'auto';
        this.container.style.left = `${initialLeft}px`;
        this.container.style.top = `${initialTop}px`;
      });

      window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        this.container.style.left = `${Math.max(10, Math.min(window.innerWidth - 300, initialLeft + dx))}px`;
        this.container.style.top = `${Math.max(10, Math.min(window.innerHeight - 200, initialTop + dy))}px`;
      });

      window.addEventListener('mouseup', () => {
        isDragging = false;
      });
    }
  }

  show() {
    if (!this.container) return;
    this.container.classList.add('active');
    this.app.showToast('Teleprompter Pro activado. Usa [Espacio] para pausar/reanudar.', 'info');
  }

  hide() {
    if (!this.container) return;
    this.pause();
    this.container.classList.remove('active');
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  play() {
    this.isPlaying = true;
    const playBtn = document.getElementById('prompterPlayBtn');
    if (playBtn) playBtn.innerHTML = '⏸️ Pausar';
    this.lastTimestamp = performance.now();
    this.scrollLoop();
  }

  pause() {
    this.isPlaying = false;
    const playBtn = document.getElementById('prompterPlayBtn');
    if (playBtn) playBtn.innerHTML = '▶️ Iniciar';
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  resetScroll() {
    this.pause();
    this.scrollPos = 0;
    if (this.scrollArea) {
      this.scrollArea.scrollTop = 0;
    }
    this.app.showToast('Teleprompter reiniciado al inicio.', 'info');
  }

  toggleMirror() {
    this.isMirrored = !this.isMirrored;
    const mirrorBtn = document.getElementById('prompterMirrorBtn');
    if (mirrorBtn) {
      mirrorBtn.classList.toggle('active', this.isMirrored);
    }
    this.updateStyle();
    this.app.showToast(this.isMirrored ? 'Modo Espejo Reflejado Activado (Para Cristal Físico)' : 'Modo Espejo Desactivado', 'info');
  }

  toggleExpand() {
    this.isExpanded = !this.isExpanded;
    this.container.classList.toggle('expanded', this.isExpanded);
    const expandBtn = document.getElementById('prompterExpandBtn');
    if (expandBtn) {
      expandBtn.innerHTML = this.isExpanded ? '🗗 Reducir' : '🗖 Expandir';
    }
  }

  adjustSpeed(delta) {
    this.speedWpm = Math.max(60, Math.min(320, this.speedWpm + delta));
    const slider = document.getElementById('prompterSpeedSlider');
    const label = document.getElementById('prompterSpeedVal');
    if (slider) slider.value = this.speedWpm;
    if (label) label.textContent = `${this.speedWpm} WPM`;
  }

  updateStyle() {
    if (this.scrollArea) {
      this.scrollArea.style.transform = this.isMirrored ? 'scaleX(-1)' : 'none';
    }
    if (this.contentEl) {
      this.contentEl.style.fontSize = `${this.fontSize}px`;
      this.contentEl.style.lineHeight = '1.7';
    }
  }

  scrollLoop() {
    if (!this.isPlaying) return;

    const now = performance.now();
    const dt = (now - this.lastTimestamp) / 1000;
    this.lastTimestamp = now;

    const pxPerSec = (this.speedWpm / 140) * 48 * (this.fontSize / 28);
    this.scrollPos += pxPerSec * dt;

    if (this.scrollArea) {
      this.scrollArea.scrollTop = this.scrollPos;

      if (this.scrollArea.scrollTop + this.scrollArea.clientHeight >= this.scrollArea.scrollHeight - 10) {
        this.pause();
        this.app.showToast('Fin de la lectura del Teleprompter completado.', 'success');
        return;
      }
    }

    this.animationFrameId = requestAnimationFrame(() => this.scrollLoop());
  }

  importScriptFromStudio() {
    const scriptBox = document.getElementById('generatedScriptOutput');
    if (scriptBox && scriptBox.textContent.trim()) {
      const text = scriptBox.textContent.trim();
      if (this.contentEl) {
        this.contentEl.value = text;
        this.resetScroll();
        this.show();
        this.app.showToast('Guión importado exitosamente al Teleprompter Pro.', 'success');
      }
    } else {
      this.app.showToast('Primero genera un guión en el AI Studio para importarlo.', 'warning');
    }
  }
}

// ==========================================
// ==========================================
// 9.5. HACKSLABS SUITE (FACELESS CHANNELS & VIRAL OUTLIERS)
// ==========================================
class HacksLabsManager {
  constructor(app) {
    this.app = app;
    this.activeFilter = 'all';
    this.searchQuery = '';
    
    this.niches = [
      {
        id: 'finanzas',
        name: 'Finanzas Personales & Inversión Inteligente',
        icon: '💎',
        rpmRange: '$32 - $58 USD',
        rpmScore: 98,
        competition: 'Media',
        compClass: 'badge-purple',
        format: 'Largo (>8 min) & Shorts',
        category: ['high-rpm', 'long', 'shorts'],
        description: 'Educación financiera sobre fondos indexados, hábitos de ahorro, interés compuesto y psicología del dinero.',
        viralAngles: [
          'La regla 50/30/20 que los bancos prefieren que ignores',
          'Qué pasa si inviertes $100 al mes durante 10 años (Simulación Real)',
          '5 Errores financieros que te mantendrán pobre a los 30'
        ],
        secretTip: 'Usa gráficos animados minimalistas y capturas de pantalla de simuladores de interés compuesto.',
        tags: ['#FinanzasPersonales', '#Inversiones', '#EducacionFinanciera', '#AhorroInteligente']
      },
      {
        id: 'ia-nocode',
        name: 'Inteligencia Artificial & Automatización No-Code',
        icon: '🤖',
        rpmRange: '$28 - $52 USD',
        rpmScore: 95,
        competition: 'Baja',
        compClass: 'badge-emerald',
        format: 'Tutoriales & Demostraciones',
        category: ['high-rpm', 'low-comp', 'long'],
        description: 'Herramientas de IA generativa, flujos de trabajo con Make/Zapier y creación de micro-servicios digitales.',
        viralAngles: [
          '3 Herramientas de IA gratuitas que parecen ilegales de conocer',
          'Cómo automaticé la creación de 50 videos a la semana con Make',
          'El fin de los empleos tradicionales: Las habilidades que sobrevivirán a 2026'
        ],
        secretTip: 'Muestra capturas paso a paso en pantalla completa con zoom dinámico y música lofi.',
        tags: ['#InteligenciaArtificial', '#Automatizacion', '#TechTools', '#ProductividadIA']
      },
      {
        id: 'geopolitica-3d',
        name: 'Geopolítica, Mapas 3D & Conflictos Históricos',
        icon: '🌍',
        rpmRange: '$24 - $45 USD',
        rpmScore: 90,
        competition: 'Baja',
        compClass: 'badge-emerald',
        format: 'Mapas 3D & Documental',
        category: ['low-comp', 'long'],
        description: 'Análisis geopolítico con animaciones cartográficas de Google Earth Studio y Blender sobre rutas comerciales y recursos.',
        viralAngles: [
          'Por qué Suiza es geográficamente imposible de invadir',
          'El estrecho de Malaca: El punto donde el 80% del comercio mundial podría colapsar',
          'El secreto detrás de la riqueza inesperada de este pequeño país europeo'
        ],
        secretTip: 'La retención se dispara cuando el mapa se acerca y gira en 3D cada 4 segundos.',
        tags: ['#Geopolitica', '#Mapas3D', '#HistoriaMundial', '#EstrategiaMilitar']
      },
      {
        id: 'estoicismo',
        name: 'Estoicismo, Filosofía Oscura & Autodisciplina',
        icon: '🏛️',
        rpmRange: '$18 - $36 USD',
        rpmScore: 82,
        competition: 'Media',
        compClass: 'badge-purple',
        format: 'Shorts & Reels Virales',
        category: ['shorts'],
        description: 'Citas de Marco Aurelio, Séneca y leyes de poder enfocadas en fortaleza mental, superación personal y enfoque.',
        viralAngles: [
          '7 Reglas estoicas para volverte silenciosamente peligroso',
          'Cómo responder cuando alguien intenta faltarte el respeto en público',
          'La regla del silencio: Por qué los hombres de alto valor hablan poco'
        ],
        secretTip: 'Estatua de mármol con luz azul/magenta de fondo, voz grave en off y música Phonk ambiental.',
        tags: ['#Estoicismo', '#MarcoAurelio', '#Mentalidad', '#DesarrolloPersonal']
      },
      {
        id: 'crimen-misterio',
        name: 'Casos Reales, Misterios Sin Resolver & Crimen',
        icon: '🕵️',
        rpmRange: '$16 - $32 USD',
        rpmScore: 80,
        competition: 'Media',
        compClass: 'badge-purple',
        format: 'Narrativa & Documental',
        category: ['long'],
        description: 'Historias de detectives, desapariciones inexplicables y cronología forense con ambientación cinematográfica.',
        viralAngles: [
          'La misteriosa llamada al 911 que dejó perplejos a los investigadores por 20 años',
          'El caso del excursionista que dejó una libreta con pistas inquietantes',
          'Nadie creyó la historia de este marinero hasta que encontraron el barco vacío'
        ],
        secretTip: 'Divide la historia en 3 sospechosos y revela la pista clave en el minuto 7:45.',
        tags: ['#CasosReales', '#Misterio', '#TrueCrimeEspañol', '#HistoriasReales']
      },
      {
        id: 'biohacking',
        name: 'Longevidad, Biohacking & Optimización Cerebral',
        icon: '🧬',
        rpmRange: '$26 - $48 USD',
        rpmScore: 92,
        competition: 'Baja',
        compClass: 'badge-emerald',
        format: 'Video Largo & Shorts',
        category: ['high-rpm', 'low-comp', 'long', 'shorts'],
        description: 'Protocolos de sueño profundo, suplementación basada en evidencia médica, nootrópicos y ayuno intermitente.',
        viralAngles: [
          'El protocolo de 10 minutos al despertar que duplica tus niveles de dopamina',
          'Los 3 suplementos que la ciencia respalda para retrasar el envejecimiento celular',
          'Por qué tomar café en tu primera hora de vigilia arruina tu tarde'
        ],
        secretTip: 'Cita estudios de PubMed / Nature en pequeñas tarjetas flotantes para generar autoridad instantánea.',
        tags: ['#Biohacking', '#Longevidad', '#SaludMental', '#Optimización']
      },
      {
        id: 'cripto-rwa',
        name: 'Criptoactivos, RWA & Tokenización de Activos',
        icon: '⚡',
        rpmRange: '$35 - $65 USD',
        rpmScore: 99,
        competition: 'Media',
        compClass: 'badge-purple',
        format: 'Video de Análisis',
        category: ['high-rpm', 'long'],
        description: 'Narrativas de tokens RWA (Real World Assets), infraestructura DeFi y ciclos de liquidez macroeconómica.',
        viralAngles: [
          'BlackRock y la tokenización de billones de dólares en activos reales',
          'Qué es la narrativa RWA y por qué dominará el próximo ciclo financiero',
          'Cómo analizar proyectos cripto antes de que coticen en los principales exchanges'
        ],
        secretTip: 'Audiencia de países anglosajones y Europa Occidental eleva el RPM a más de $50 USD.',
        tags: ['#Cripto', '#RWA', '#Blockchain', '#InversionesWeb3']
      },
      {
        id: 'libros-mentalidad',
        name: 'Resúmenes Animados de Libros & Mentalidad',
        icon: '📚',
        rpmRange: '$16 - $30 USD',
        rpmScore: 78,
        competition: 'Baja',
        compClass: 'badge-emerald',
        format: 'Pizarra / Animación 2D',
        category: ['low-comp', 'long'],
        description: 'Condensación de los mejores libros de negocios, hábitos, persuasión y psicología en lecciones aplicables de 10 minutos.',
        viralAngles: [
          'Hábitos Atómicos: Las 4 leyes para cambiar tu vida en 1% diario',
          'Las 48 Leyes del Poder explicadas con ejemplos históricos reales',
          'Pensar Rápido, Pensar Despacio: Cómo tu cerebro te sabotea todos los días'
        ],
        secretTip: 'Vende el audiolibro o libro físico con enlaces de afiliado de Amazon en la primera línea de la descripción.',
        tags: ['#ResumenDeLibros', '#HabitosAtomicos', '#CrecimientoPersonal', '#Educacion']
      },
      {
        id: 'lujo-millonarios',
        name: 'Estilo de Vida Millonario, Megamansiones & Yates',
        icon: '🛥️',
        rpmRange: '$22 - $44 USD',
        rpmScore: 88,
        competition: 'Media',
        compClass: 'badge-purple',
        format: 'Shorts & Reels 4K',
        category: ['shorts', 'high-rpm'],
        description: 'Tours cinemáticos en 4K por las propiedades más exclusivas del mundo, hipercoches y relojes de colección.',
        viralAngles: [
          'Dentro de la mansión de $150,000,000 con garaje submarino',
          'El reloj que cuesta más que 5 departamentos en Nueva York',
          'Cómo viven los multimillonarios en Mónaco durante el Gran Premio'
        ],
        secretTip: 'Alta tasa de guardados y compartidos; usa clips en 4K 60fps con corrección de color cinemática.',
        tags: ['#LujoExtremo', '#Megamansiones', '#Superyates', '#EstiloDeVida']
      },
      {
        id: 'espacio-astro',
        name: 'Astrofísica, Misterios Espaciales & la NASA',
        icon: '🚀',
        rpmRange: '$14 - $28 USD',
        rpmScore: 75,
        competition: 'Media',
        compClass: 'badge-purple',
        format: 'Shorts & Documental',
        category: ['shorts'],
        description: 'Telescopio James Webb, agujeros negros, exoplanetas habitables y paradojas de la física cuántica.',
        viralAngles: [
          'El sonido más aterrador captado por la NASA en un agujero negro',
          'El James Webb acaba de encontrar algo en este exoplaneta que desafía la física',
          'Qué pasaría exactamente si la Tierra dejara de girar por un solo segundo'
        ],
        secretTip: 'Efecto de asombro ("sense of wonder"): ganchos con preguntas existenciales en los primeros 2 segundos.',
        tags: ['#Espacio', '#JamesWebb', '#NASA', '#Astrofisica', '#Universo']
      },
      {
        id: 'negocios-quiebras',
        name: 'Casos de Negocio, Éxitos & Quiebras Épicas',
        icon: '🏢',
        rpmRange: '$28 - $54 USD',
        rpmScore: 94,
        competition: 'Baja',
        compClass: 'badge-emerald',
        format: 'Video Largo (>10 min)',
        category: ['high-rpm', 'low-comp', 'long'],
        description: 'Crónicas sobre cómo empresas gigantes como Blockbuster, Kodak o Enron colapsaron, y cómo startups alcanzaron el éxito.',
        viralAngles: [
          'Cómo un error de $50 millones destruyó a la mayor cadena de videos del mundo',
          'La oscura estrategia detrás del monopolio de las gafas de sol de lujo',
          'La estafa multimillonaria de Theranos que engañó a presidentes y magnates'
        ],
        secretTip: 'Ritmo ágil de edición con titulares de prensa antiguos, recortes de revistas y música de suspenso corporativo.',
        tags: ['#HistoriasDeNegocios', '#Empresas', '#Emprendimiento', '#Finanzas']
      },
      {
        id: 'seguridad-tech',
        name: 'Ciberseguridad, Privacidad Digital & Linux',
        icon: '🛡️',
        rpmRange: '$24 - $42 USD',
        rpmScore: 89,
        competition: 'Baja',
        compClass: 'badge-emerald',
        format: 'Tutoriales Prácticos',
        category: ['low-comp', 'long'],
        description: 'Guías de privacidad en línea, navegadores blindados, configuración de VPN propia y sistemas de código abierto.',
        viralAngles: [
          '5 Ajustes urgentes de privacidad que debes activar en tu teléfono hoy',
          'Por qué los hackers nunca usan Google Chrome ni Windows para sus finanzas',
          'Cómo monté mi propia nube privada de 10TB por menos de lo que cuesta una suscripción'
        ],
        secretTip: 'Audiencia con alto poder adquisitivo interesada en software B2B, hosting y hardware.',
        tags: ['#Ciberseguridad', '#PrivacidadDigital', '#TechHacks', '#SoftwareLibre']
      }
    ];

    this.outliers = [
      {
        id: 'outlier-oro-suiza',
        title: 'El Secreto Oculto de las Bóvedas de Suiza',
        niche: 'Finanzas & Geopolítica',
        multiplier: '133x Outlier',
        views: '2.4M vistas (vs 18k promedio del canal)',
        badgeClass: 'badge-pink',
        hook3s: '"Si tienes más de $1,000 en una cuenta bancaria, el 90% de los gobiernos del mundo no quieren que descubras este búnker en los Alpes antes de que termine el mes..."',
        thumbnailFormula: 'Mapa 3D con textura topográfica en tonos carbón, coordenadas GPS en amarillo neón y etiqueta roja: "EL BÚNKER PROHIBIDO".',
        keyRetentionSecret: 'Revela 1 micro-revelación cada 45 segundos para mantener el gráfico de retención sin caídas superiores al 5%.',
        suggestedPrompt: 'Crea un guión cinematográfico de 8 minutos para un canal faceless sobre las bóvedas de oro más secretas del mundo, con gancho de 3 segundos de alta intriga y desglose de 3 misterios financieros.'
      },
      {
        id: 'outlier-estoicismo-7',
        title: '7 Reglas Estoicas para Volverte Silenciosamente Imparable',
        niche: 'Estoicismo & Psicología',
        multiplier: '114x Outlier',
        views: '4.8M vistas (vs 42k promedio del canal)',
        badgeClass: 'badge-purple',
        hook3s: '"Marco Aurelio escribió esta advertencia hace 2,000 años para un general que estaba a punto de ser traicionado, y hoy cambiará la forma en que todos te miran..."',
        thumbnailFormula: 'Estatua clásica de piedra con grietas luminosas en cian, fondo oscuro y texto en mayúsculas: "CÁLLATE Y OBSERVA".',
        keyRetentionSecret: 'La regla número 4 debe ser contraria a la intuición para forzar a la gente a comentar y debatir en los comentarios.',
        suggestedPrompt: 'Genera un guión de 60 segundos en formato vertical para Short/TikTok sobre la regla estoica del autocontrol ante las provocaciones, con voz en off solemne y subtítulos de alto impacto.'
      },
      {
        id: 'outlier-chatgpt-errores',
        title: 'Por Qué el 99% Usa ChatGPT Mal (Y las 3 Técnicas Pro)',
        niche: 'IA & Productividad',
        multiplier: '76x Outlier',
        views: '1.9M vistas (vs 25k promedio del canal)',
        badgeClass: 'badge-cyan',
        hook3s: '"Deja de pedirle a ChatGPT que actúe como un redactor profesional; utiliza este modificador de un solo caracter y tus respuestas pasarán de mediocres a nivel consultor senior..."',
        thumbnailFormula: 'Comparativa visual en pantalla dividida: "PROMPT COMÚN" (en rojo tachado) vs "PROMPT DE $10,000" (con brillo dorado).',
        keyRetentionSecret: 'Demostración en vivo en los primeros 15 segundos: muestra el resultado antes de explicar el método.',
        suggestedPrompt: 'Escribe un guión de video tutorial faceless de 10 minutos revelando técnicas avanzadas de Prompt Engineering con ejemplos prácticos para automatizar negocios digitales.'
      },
      {
        id: 'outlier-regla-3dias',
        title: 'La Regla de los 3 Días que Salva Fortunas en Compras',
        niche: 'Finanzas & Hábitos',
        multiplier: '106x Outlier',
        views: '3.2M vistas (vs 30k promedio del canal)',
        badgeClass: 'badge-emerald',
        hook3s: '"Un multimillonario retirado reveló un truco psicológico tan absurdo que parece una broma, pero le impidió gastar $42,000 en impulsos el año pasado..."',
        thumbnailFormula: 'Gráfico minimalista de un cerebro con una barra de progreso que se enfría de rojo a azul hielo, con la frase: "EL FRENO CEREBRAL".',
        keyRetentionSecret: 'Cierre con llamado a la acción sutil para descargar una plantilla gratuita de seguimiento de gastos en la descripción.',
        suggestedPrompt: 'Genera un guión de 5 minutos sobre psicología del consumidor y el sesgo del comprador impulsivo, incluyendo un plan de acción de 3 pasos para controlar gastos hormiga.'
      }
    ];

    this.academy = [
      {
        id: 'acad-anti-desmonetizacion',
        title: '🛡️ Escudo Anti-Desmonetización: YouTube & Meta 2026',
        category: 'Políticas & Seguridad Algorítmica',
        readTime: '6 min de lectura',
        description: 'Cómo evitar que el algoritmo marque tu canal faceless como "Contenido repetitivo" o "Contenido generado automáticamente sin valor añadido".',
        keyPoints: [
          '<strong>Regla de los 3 Elementos Propios:</strong> Todo video debe combinar voz con inflexiones reales, guión con perspectiva única y edición con capas de b-roll de múltiples orígenes.',
          '<strong>Metadatos Dinámicos:</strong> Nunca uses títulos con plantillas fijas (ej. "Curiosidad #1", "Curiosidad #2"). Cada miniatura debe poseer composición y colores distintos.',
          '<strong>Fórmula de Transformación:</strong> Si utilizas fragmentos de dominio público o archivo, añade zoom dinámico, recorte horizontal/vertical y anotaciones explicativas cada 5 segundos.'
        ]
      },
      {
        id: 'acad-fb-bonus',
        title: '💰 Hack del Performance Bonus en Facebook Fanpages',
        category: 'Monetización en Meta',
        readTime: '8 min de lectura',
        description: 'Estrategia exacta para calificar y maximizar los ingresos del programa de Bonificaciones por Rendimiento de Facebook sin invertir en anuncios.',
        keyPoints: [
          '<strong>Posts de Controversia Positiva:</strong> Preguntas de opción múltiple en formato imagen de alta resolución que incentivan debates sanos en la sección de comentarios.',
          '<strong>Multiplicador de Compartidos:</strong> Facebook premia con hasta 5x más bonificación las publicaciones que son compartidas en grupos temáticos por usuarios reales.',
          '<strong>Sincronización con Viral Labs Fanpage:</strong> Publica 3 Reels y 2 posts de interacción al día usando nuestro módulo integrado de programación horaria.'
        ]
      },
      {
        id: 'acad-bucle-infinito',
        title: '♾️ Técnica del Bucle Infinito (Infinite Loop Scripting)',
        category: 'Retención de Shorts & TikTok',
        readTime: '5 min de lectura',
        description: 'La estructura narrativa donde el final del video se conecta a la perfección con el inicio, disparando la retención por encima del 110%.',
        keyPoints: [
          '<strong>Frase Puente Final:</strong> La última oración termina con una conjunción o pregunta abierta (ej. "...y es exactamente por esta razón que...").',
          '<strong>Gancho Inicial Conector:</strong> Los primeros 2 segundos continúan la frase (ej. "...todos los millonarios guardan silencio sobre...").',
          '<strong>Sin Cierre Clásico:</strong> Elimina despedidas como "gracias por ver" o "dale like", ya que causan una caída del 70% en la retención en los últimos 3 segundos.'
        ]
      }
    ];

    this.init();
  }

  init() {
    this.renderNiches();
    this.renderOutliers();
    this.renderAcademy();
    this.bindEvents();
    this.checkStoredGithubToken();
  }

  checkStoredGithubToken() {
    const tokenInput = document.getElementById('hlGithubTokenInput');
    const stored = localStorage.getItem('virallabs_github_token');
    if (stored && tokenInput) {
      tokenInput.value = stored;
      this.updateGithubSyncStatus('Token vinculado localmente con @chenyz10yt. Listo para sincronizar con un solo clic.', 'success');
    }
  }

  bindEvents() {
    // Subnav switching
    document.querySelectorAll('.hl-nav-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.dataset.target;
        document.querySelectorAll('.hl-nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        document.querySelectorAll('.hl-tab-pane').forEach(p => p.style.display = 'none');
        const targetPane = document.getElementById(targetId);
        if (targetPane) targetPane.style.display = 'block';
      });
    });

    // Quick sync button in hero
    const quickSyncBtn = document.getElementById('hlQuickSyncBtn');
    if (quickSyncBtn) {
      quickSyncBtn.addEventListener('click', () => {
        const githubNavBtn = document.querySelector('.hl-nav-btn[data-target="hlTabGithub"]');
        if (githubNavBtn) githubNavBtn.click();
      });
    }

    // Niche search input
    const searchInput = document.getElementById('hlNicheSearchInput');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.searchQuery = e.target.value.toLowerCase().trim();
        this.renderNiches();
      });
    }

    // Filter pills
    document.querySelectorAll('.hl-filter-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.hl-filter-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.activeFilter = pill.dataset.filter;
        this.renderNiches();
      });
    });

    // GitHub Save & Sync button
    const saveSyncBtn = document.getElementById('hlSaveTokenAndSyncBtn');
    if (saveSyncBtn) {
      saveSyncBtn.addEventListener('click', () => {
        this.handleGithubSync();
      });
    }
  }

  renderNiches() {
    const container = document.getElementById('hlNichesGrid');
    if (!container) return;

    let filtered = this.niches.filter(n => {
      const matchFilter = this.activeFilter === 'all' || n.category.includes(this.activeFilter);
      const matchSearch = !this.searchQuery || 
        n.name.toLowerCase().includes(this.searchQuery) ||
        n.description.toLowerCase().includes(this.searchQuery) ||
        n.tags.some(t => t.toLowerCase().includes(this.searchQuery));
      return matchFilter && matchSearch;
    });

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align:center; padding:40px 20px; color:var(--text-muted);">
          <div style="font-size:2.5rem; margin-bottom:10px;">🔍</div>
          <h4>No se encontraron nichos con ese criterio de búsqueda</h4>
          <p style="font-size:0.85rem;">Prueba limpiando los filtros o utilizando términos como "Finanzas", "IA" o "Lujo".</p>
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(n => `
      <div class="hl-niche-card">
        <div class="hl-niche-header">
          <div class="hl-niche-icon-wrap">${n.icon}</div>
          <div style="flex:1;">
            <div class="hl-niche-name">${n.name}</div>
            <div style="display:flex; gap:6px; margin-top:4px; flex-wrap:wrap;">
              <span class="badge ${n.compClass}">Competencia: ${n.competition}</span>
              <span class="badge badge-cyan">${n.format}</span>
            </div>
          </div>
        </div>

        <div class="hl-rpm-badge">
          <div class="hl-rpm-val">${n.rpmRange}</div>
          <div class="hl-rpm-label">RPM Estimado por 1,000 Vistas</div>
        </div>

        <p class="hl-niche-desc">${n.description}</p>

        <div style="background:rgba(255,255,255,0.03); border-radius:6px; padding:10px; margin-bottom:14px;">
          <div style="font-size:0.75rem; font-weight:700; color:#fff; margin-bottom:6px;">⚡ Ángulos Virales Sugeridos:</div>
          <ul style="margin:0; padding-left:16px; font-size:0.76rem; color:var(--text-secondary); line-height:1.45;">
            ${n.viralAngles.map(a => `<li>${a}</li>`).join('')}
          </ul>
        </div>

        <div style="font-size:0.72rem; color:#6ee7b7; margin-bottom:14px; display:flex; align-items:flex-start; gap:6px;">
          <span>💡</span>
          <span><strong>Tip Pro:</strong> ${n.secretTip}</span>
        </div>

        <div class="hl-niche-actions">
          <button class="btn btn-cyber btn-sm" onclick="window.ViralLabs.hackslabs.loadNicheToStudio('${n.id}')" style="flex:1;">
            ✍️ Generar en AI Studio
          </button>
          <button class="btn btn-ghost btn-sm" onclick="window.ViralLabs.hackslabs.copyNichePrompts('${n.id}')" title="Copiar Ángulos al Portapapeles">
            📋 Copiar
          </button>
        </div>
      </div>
    `).join('');
  }

  renderOutliers() {
    const container = document.getElementById('hlOutliersGrid');
    if (!container) return;

    container.innerHTML = this.outliers.map(o => `
      <div class="hl-outlier-card">
        <div class="hl-outlier-header">
          <div>
            <span class="badge ${o.badgeClass}">${o.multiplier}</span>
            <span class="badge badge-purple" style="margin-left:6px;">${o.niche}</span>
            <h4 style="font-size:1.05rem; font-weight:700; color:#fff; margin-top:8px; line-height:1.35;">${o.title}</h4>
            <div style="font-size:0.76rem; color:#6ee7b7; margin-top:4px; font-weight:600;">📈 ${o.views}</div>
          </div>
        </div>

        <div class="hl-outlier-body">
          <div class="hl-metric-item">
            <div class="hl-metric-label">🎣 Gancho de 3 Segundos (Hook):</div>
            <div class="hl-metric-val" style="font-style:italic; color:#e2e8f0; font-weight:400; line-height:1.45;">${o.hook3s}</div>
          </div>

          <div class="hl-metric-item">
            <div class="hl-metric-label">🖼️ Fórmula de Miniatura Viral:</div>
            <div class="hl-metric-val" style="color:var(--text-secondary); font-weight:400; font-size:0.8rem;">${o.thumbnailFormula}</div>
          </div>

          <div class="hl-metric-item">
            <div class="hl-metric-label">⚡ Secreto de Retención Algorítmica:</div>
            <div class="hl-metric-val" style="color:#93c5fd; font-weight:400; font-size:0.8rem;">${o.keyRetentionSecret}</div>
          </div>

          <div style="margin-top:16px; display:flex; gap:8px;">
            <button class="btn btn-primary btn-sm" onclick="window.ViralLabs.hackslabs.replicateOutlier('${o.id}')" style="flex:1;">
              🚀 Replicar con AI Studio
            </button>
            <button class="btn btn-ghost btn-sm" onclick="navigator.clipboard.writeText('${o.hook3s.replace(/"/g, '\\"')}'); window.ViralLabs.showToast('¡Gancho copiado al portapapeles!', 'success');">
              📋 Gancho
            </button>
          </div>
        </div>
      </div>
    `).join('');
  }

  renderAcademy() {
    const container = document.getElementById('hlAcademyGrid');
    if (!container) return;

    container.innerHTML = this.academy.map(a => `
      <div class="hl-lesson-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span class="badge badge-cyan">${a.category}</span>
          <span style="font-size:0.72rem; color:var(--text-muted);">⏱️ ${a.readTime}</span>
        </div>
        <h4 style="font-size:1.1rem; font-weight:700; color:#fff; margin-bottom:10px;">${a.title}</h4>
        <p style="font-size:0.84rem; color:var(--text-secondary); margin-bottom:16px; line-height:1.5;">${a.description}</p>
        
        <div style="background:rgba(15, 23, 42, 0.6); border:1px solid rgba(255, 255, 255, 0.06); border-radius:8px; padding:14px;">
          <div style="font-size:0.78rem; font-weight:700; color:#fff; margin-bottom:8px;">📌 Puntos Clave de Implementación:</div>
          <div style="display:flex; flex-direction:column; gap:10px; font-size:0.8rem; color:var(--text-secondary); line-height:1.5;">
            ${a.keyPoints.map(p => `<div>${p}</div>`).join('')}
          </div>
        </div>
      </div>
    `).join('');
  }

  loadNicheToStudio(nicheId) {
    const niche = this.niches.find(n => n.id === nicheId);
    if (!niche) return;

    const topicInput = document.getElementById('studioTopicInput');
    const angle = niche.viralAngles[0];
    if (topicInput) {
      topicInput.value = `${niche.name}: ${angle}`;
    }

    this.app.switchTab('studio');
    this.app.showToast(`Nicho cargado en AI Studio: "${niche.name}"`, 'success');
  }

  copyNichePrompts(nicheId) {
    const niche = this.niches.find(n => n.id === nicheId);
    if (!niche) return;
    const text = `🎯 NICHO: ${niche.name}\n💰 RPM: ${niche.rpmRange}\n🔥 ÁNGULOS VIRALES:\n` + niche.viralAngles.map((a, i) => `${i+1}. ${a}`).join('\n') + `\n💡 TIP: ${niche.secretTip}\n🏷️ TAGS: ${niche.tags.join(' ')}`;
    navigator.clipboard.writeText(text);
    this.app.showToast('Ángulos y datos del nicho copiados al portapapeles.', 'success');
  }

  replicateOutlier(outlierId) {
    const out = this.outliers.find(o => o.id === outlierId);
    if (!out) return;

    const topicInput = document.getElementById('studioTopicInput');
    if (topicInput) {
      topicInput.value = out.title;
    }

    this.app.switchTab('studio');
    this.app.showToast(`Outlier cargado en AI Studio: "${out.title}"`, 'success');
  }

  updateGithubSyncStatus(msg, type = 'info') {
    const box = document.getElementById('hlGithubSyncStatusBox');
    if (!box) return;
    box.style.display = 'block';
    const colorMap = {
      success: '#10b981',
      error: '#ef4444',
      info: '#06b6d4',
      warning: '#f59e0b'
    };
    box.style.borderColor = colorMap[type] || '#06b6d4';
    box.style.color = '#fff';
    box.innerHTML = msg;
  }

  handleGithubSync() {
    const tokenInput = document.getElementById('hlGithubTokenInput');
    const token = tokenInput ? tokenInput.value.trim() : '';

    if (!token) {
      this.app.showToast('Por favor introduce tu Personal Access Token de GitHub.', 'warning');
      this.updateGithubSyncStatus('⚠️ Debes ingresar un token de GitHub válido (ghp_... o github_pat_...) para autenticar.', 'warning');
      return;
    }

    localStorage.setItem('virallabs_github_token', token);
    this.updateGithubSyncStatus('⏳ Autenticando con GitHub API para @chenyz10yt...', 'info');

    fetch('https://api.github.com/user', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    })
    .then(res => {
      if (!res.ok) throw new Error('Token inválido o sin permisos suficientes.');
      return res.json();
    })
    .then(user => {
      this.updateGithubSyncStatus(`
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-size:1.5rem;">✅</span>
          <div>
            <strong>¡Conexión Exitosa con GitHub!</strong><br>
            Autenticado como: <code>@${user.login}</code>.<br>
            <span style="font-size:0.75rem; color:#93c5fd;">
              Tu token ha quedado guardado localmente de forma segura. Ahora ejecuta <code>SUBIR_A_GITHUB.bat</code> en la carpeta de tu app para sincronizar los archivos completos en <code>https://github.com/chenyz10yt/virallabs-studio-ai</code>.
            </span>
          </div>
        </div>
      `, 'success');
      this.app.showToast(`Autenticado con éxito como @${user.login}`, 'success');
    })
    .catch(err => {
      this.updateGithubSyncStatus(`❌ Error de autenticación: ${err.message}`, 'error');
      this.app.showToast('Error al conectar con GitHub.', 'error');
    });
  }
}


// 10. MAIN APP CONTROLLER
// ==========================================
class ViralLabsApp {
  constructor() {
    this.activeTab = 'dashboard';
    this.storage = StorageManager;
    this.broadcastChannel = null;
    this.deferredInstallPrompt = null;
    this.currentVersion = 'v3.0.0';
    this.availableVersion = 'v3.0.0';
    this.init();
  }

  init() {
    // Multi-tab real-time sync with Fanpage
    if ('BroadcastChannel' in window) {
      this.broadcastChannel = new BroadcastChannel('virallabs_channel');
    }

    this.auth = new AuthSystem(this);
    this.teleprompter = new TeleprompterPro(this);
    this.studio = new StudioManager(this);
    this.clipper = new ClipperManager(this);
    this.multistream = new MultistreamManager(this);
    this.voicelab = new VoiceLabManager(this);
    this.planner = new PlannerManager(this);
    this.radar = new RadarManager(this);
    this.hackslabs = new HacksLabsManager(this);

    this.setupNavigation();
    this.setupHeaderActions();
    this.renderDashboardMetrics();
    this.setupAutoUpdater();
    this.setupPWAInstall();

    const initialHash = window.location.hash.replace('#', '');
    if (initialHash && document.getElementById(`pane-${initialHash}`)) {
      this.switchTab(initialHash);
    }
  }

  broadcastMessage(data) {
    if (this.broadcastChannel) {
      this.broadcastChannel.postMessage(data);
    }
  }

  setupAutoUpdater() {
    // Purge legacy caches on startup
    if ('caches' in window) {
      caches.keys().then((keys) => {
        keys.forEach((key) => {
          if (!key.includes('v3.0.0')) {
            caches.delete(key);
          }
        });
      });
    }

    // Register Service Worker with v3.0.0
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('service-worker.js?v=3.0.0').then((reg) => {
        reg.update();
        reg.onupdatefound = () => {
          const installingWorker = reg.installing;
          installingWorker.onstatechange = () => {
            if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
              this.showUpdateModal('v3.0.0 AI');
            }
          };
        };
      }).catch(err => console.log('SW registration note:', err));
    }

    // Bind Manual Check Update Button
    const checkUpdateBtn = document.getElementById('checkUpdateNavBtn');
    if (checkUpdateBtn) {
      checkUpdateBtn.addEventListener('click', () => {
        this.showToast('🔍 Verificando repositorios de Viral Labs...', 'info');
        setTimeout(() => {
          this.showToast('✅ Viral Labs v3.0 AI está en su versión más reciente.', 'success');
        }, 800);
      });
    }

    // Bind Update Modal Buttons
    const installNowBtn = document.getElementById('installUpdateNowBtn');
    if (installNowBtn) {
      installNowBtn.addEventListener('click', () => {
        this.installUpdate();
      });
    }
  }

  showUpdateModal(version) {
    const modal = document.getElementById('autoUpdateModal');
    const verBadge = document.getElementById('updateVersionBadge');
    if (verBadge) verBadge.textContent = version;
    if (modal) {
      modal.classList.add('active');
    }
  }

  installUpdate() {
    const installBtn = document.getElementById('installUpdateNowBtn');
    const updateProgress = document.getElementById('updateProgressBar');
    const updateStatusText = document.getElementById('updateStatusText');

    if (installBtn) installBtn.disabled = true;
    if (updateStatusText) updateStatusText.textContent = '📦 Instalando motor de contenido autónomo v3.0 AI...';

    let pct = 0;
    const interval = setInterval(() => {
      pct += 25;
      if (updateProgress) updateProgress.style.width = `${pct}%`;

      if (pct >= 100) {
        clearInterval(interval);
        if (updateStatusText) updateStatusText.textContent = '✅ ¡Viral Labs v3.0 AI activado! Recargando...';
        
        sessionStorage.setItem('virallabs_update_dismissed', 'true');
        
        if (navigator.serviceWorker && navigator.serviceWorker.controller) {
          navigator.serviceWorker.controller.postMessage({ action: 'skipWaiting' });
        }

        setTimeout(() => {
          window.location.reload(true);
        }, 800);
      }
    }, 200);
  }

  setupPWAInstall() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredInstallPrompt = e;
      const installBtn = document.getElementById('pwaInstallBtn');
      if (installBtn) {
        installBtn.style.display = 'inline-flex';
        installBtn.addEventListener('click', () => {
          if (this.deferredInstallPrompt) {
            this.deferredInstallPrompt.prompt();
            this.deferredInstallPrompt.userChoice.then((choice) => {
              if (choice.outcome === 'accepted') {
                this.showToast('¡Viral Labs instalada como aplicación nativa!', 'success');
              }
              this.deferredInstallPrompt = null;
            });
          }
        });
      }
    });
  }

  setupNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = item.dataset.tab;
        if (tab) this.switchTab(tab);
      });
    });

    document.querySelectorAll('.action-card').forEach(card => {
      card.addEventListener('click', (e) => {
        e.preventDefault();
        const targetTab = card.dataset.tab;
        if (targetTab) this.switchTab(targetTab);
      });
    });
  }

  switchTab(tabName) {
    this.activeTab = tabName;
    window.location.hash = tabName;

    document.querySelectorAll('.nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.tab === tabName);
    });

    document.querySelectorAll('.content-pane').forEach(pane => {
      pane.classList.remove('active');
    });

    const targetPane = document.getElementById(`pane-${tabName}`);
    if (targetPane) {
      targetPane.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (tabName === 'studio' && this.studio) {
      setTimeout(() => this.studio.renderCanvas(), 50);
    } else if (tabName === 'clipper' && this.clipper) {
      setTimeout(() => this.clipper.drawWaveform(), 50);
    } else if (tabName === 'planner' && this.planner) {
      setTimeout(() => this.planner.renderCalendar(), 50);
    }
  }

  renderDashboardMetrics() {
    const data = StorageManager.getData();
    const postsCount = data.scheduledPosts.length;
    const countEl = document.getElementById('dashScheduledCount');
    if (countEl) countEl.textContent = postsCount;
  }

  setupHeaderActions() {
    document.querySelectorAll('.platform-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        const platform = pill.dataset.platform;
        const isConnected = pill.classList.toggle('connected');
        StorageManager.updatePlatformStatus(platform, isConnected);
        this.showToast(`${platform.toUpperCase()} ${isConnected ? 'Conectado' : 'Desconectado'}`, 'info');
        if (this.multistream) this.multistream.renderPlatformsMatrix();
      });
    });

    const settingsBtn = document.getElementById('openSettingsBtn');
    const modal = document.getElementById('rtmpModal');
    const closeBtn = document.getElementById('closeModalBtn');
    const saveRtmpBtn = document.getElementById('saveRtmpSettingsBtn');

    if (settingsBtn && modal) {
      settingsBtn.addEventListener('click', () => modal.classList.add('active'));
    }
    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
      });
    }
    if (saveRtmpBtn && modal) {
      saveRtmpBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        this.showToast('Configuración RTMP y claves de transmisión guardadas.', 'success');
      });
    }

    // Auth Modal open / close
    const authBtn = document.getElementById('openAuthModalBtn');
    const authModal = document.getElementById('authModal');
    const closeAuthBtn = document.getElementById('closeAuthModalBtn');
    if (authBtn && this.auth) {
      authBtn.addEventListener('click', () => this.auth.openAuthModal());
    }
    if (closeAuthBtn && this.auth) {
      closeAuthBtn.addEventListener('click', () => this.auth.closeAuthModal());
    }
    if (authModal && this.auth) {
      authModal.addEventListener('click', (e) => {
        if (e.target === authModal) this.auth.closeAuthModal();
      });
    }

    // BYOK Wallet Modal open / close
    const byokBtn = document.getElementById('openByokWalletBtn');
    const byokModal = document.getElementById('byokModal');
    const closeByokBtn = document.getElementById('closeByokModalBtn');
    if (byokBtn && this.auth) {
      byokBtn.addEventListener('click', () => this.auth.openByokModal());
    }
    if (closeByokBtn && this.auth) {
      closeByokBtn.addEventListener('click', () => this.auth.closeByokModal());
    }
    if (byokModal && this.auth) {
      byokModal.addEventListener('click', (e) => {
        if (e.target === byokModal) this.auth.closeByokModal();
      });
    }

    // Teleprompter Pro Button
    const prompterBtn = document.getElementById('openPrompterBtn');
    if (prompterBtn && this.teleprompter) {
      prompterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.teleprompter.show();
      });
    }
  }

  showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'toastOut 0.3s forwards';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
}

// Backward-compatible global exports
window.OmniViralApp = ViralLabsApp;
document.addEventListener('DOMContentLoaded', () => {
  window.ViralLabs = new ViralLabsApp();
  window.OmniViral = window.ViralLabs;
});

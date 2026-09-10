/**
 * assets/js/main.js
 * Quiktalk AI Core Application & Interactive Script
 * Encapsulates: Preloader, Accessible Nav & FAQ, ROI Calculator, Call Simulator & Audio Stub,
 * WebGL Scene with performance guards, and Real Lead Form Submission.
 */

(function () {
  'use strict';

  // =============================================================
  // 1. Preloader & Load Awareness (QTK-018)
  // =============================================================
  function dismissPreloader() {
    const preEl = document.getElementById('pre');
    if (preEl && !preEl.classList.contains('done')) {
      const preNum = document.getElementById('pre-num');
      const preFill = document.getElementById('pre-bar-fill');
      if (preNum) preNum.innerText = '100%';
      if (preFill) preFill.style.right = '0%';
      setTimeout(() => {
        preEl.classList.add('done');
      }, 150);
    }
  }

  // Fade out on real load or after maximum fallback timeout (1.5s)
  if (document.readyState === 'complete') {
    dismissPreloader();
  } else {
    window.addEventListener('load', dismissPreloader);
    setTimeout(dismissPreloader, 1500);
  }

  // =============================================================
  // 2. Accessible Navigation & Mobile Menu (QTK-010)
  // =============================================================
  const burgerBtn = document.getElementById('burgerBtn');
  const mobileMenu = document.getElementById('mobile-menu');

  function openMenu() {
    if (!mobileMenu) return;
    mobileMenu.classList.add('open');
    if (burgerBtn) {
      burgerBtn.setAttribute('aria-expanded', 'true');
      burgerBtn.classList.add('active');
    }
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    if (!mobileMenu) return;
    mobileMenu.classList.remove('open');
    if (burgerBtn) {
      burgerBtn.setAttribute('aria-expanded', 'false');
      burgerBtn.classList.remove('active');
    }
    document.body.style.overflow = '';
  }

  function toggleMenu() {
    if (mobileMenu && mobileMenu.classList.contains('open')) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  if (burgerBtn) {
    burgerBtn.addEventListener('click', toggleMenu);
  }

  // Close mobile menu on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('open')) {
      closeMenu();
      if (burgerBtn) burgerBtn.focus();
    }
  });

  // Navigation scroll helper with precise offset
  function scrollToSec(id) {
    const el = document.getElementById(id);
    if (el) {
      const navHeight = 74;
      const paddingOffset = (id === 'process' || id === 'workflow') ? 40 : 24;
      const targetTop = el.getBoundingClientRect().top + window.pageYOffset - navHeight - paddingOffset;
      window.scrollTo({ top: Math.max(0, targetTop), behavior: 'smooth' });
    }
  }

  // Smooth scroll for anchor links
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href && href.length > 1) {
          const targetId = href.substring(1);
          const targetEl = document.getElementById(targetId);
          if (targetEl) {
            e.preventDefault();
            closeMenu();
            scrollToSec(targetId);
            // Update URL hash without jump
            if (history.pushState) {
              history.pushState(null, null, href);
            }
          }
        }
      });
    });

    // Close mobile menu when clicking menu links
    if (mobileMenu) {
      mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          closeMenu();
        });
      });
    }

    // Scroll spy for navigation sticky state and rail indicator
    const mainNav = document.getElementById('main-nav');
    const railBtns = document.querySelectorAll('#rail button');
    const sections = ['hero', 'workflow', 'industries', 'comparison', 'integrations', 'about', 'faq', 'demo'];

    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      if (mainNav) {
        if (scrollY > 40) {
          mainNav.classList.add('stuck');
        } else {
          mainNav.classList.remove('stuck');
        }
      }

      // Update active indicator on rail
      if (railBtns.length > 0) {
        sections.forEach((secId, idx) => {
          const el = document.getElementById(secId);
          if (el) {
            const rect = el.getBoundingClientRect();
            if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 3) {
              railBtns.forEach(b => b.classList.remove('on'));
              if (railBtns[idx]) railBtns[idx].classList.add('on');
            }
          }
        });
      }
    }, { passive: true });
  });

  // =============================================================
  // 3. Accessible FAQ Accordion (QTK-010)
  // =============================================================
  function initFaq() {
    const faqButtons = document.querySelectorAll('.faq-q');
    faqButtons.forEach(btn => {
      btn.addEventListener('click', function () {
        const item = this.closest('.faq-item');
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        
        // Close others for clean single-expand behavior
        faqButtons.forEach(otherBtn => {
          if (otherBtn !== this) {
            otherBtn.setAttribute('aria-expanded', 'false');
            const otherItem = otherBtn.closest('.faq-item');
            if (otherItem) otherItem.classList.remove('open');
          }
        });

        if (isExpanded) {
          this.setAttribute('aria-expanded', 'false');
          if (item) item.classList.remove('open');
        } else {
          this.setAttribute('aria-expanded', 'true');
          if (item) item.classList.add('open');
        }
      });
    });
  }

  // =============================================================
  // 4. Call Simulator & Audio Demo Stub (QTK-017)
  // =============================================================
  const simDialogs = [
    {
      industry: 'Roofing & Trades',
      text: '"Kia ora! Thank you for calling Acme Roofing. I can help dispatch an emergency technician for leaks or book a quote with Dave this week. What is the address of the property?"'
    },
    {
      industry: 'Dental & Medical',
      text: '"Thanks for calling North Shore Dental! I have an opening this Thursday at 10:00 AM with Dr. Smith for an emergency toothache check. May I have your full name to reserve that slot?"'
    },
    {
      industry: 'Legal & Accounting',
      text: '"Welcome to Apex Legal. I can take down the details of your inquiry and schedule an initial 20-minute consultation with our commercial partner. What legal matter can we assist with today?"'
    },
    {
      industry: 'Automotive',
      text: '"Hi there, thanks for calling Central Mechanics! Are you calling for a WOF inspection, emergency breakdown towing, or general vehicle service?"'
    }
  ];

  let currentSimIdx = 0;

  function runCallSimulation(idx) {
    if (typeof idx === 'number') {
      currentSimIdx = idx % simDialogs.length;
    } else {
      currentSimIdx = (currentSimIdx + 1) % simDialogs.length;
    }

    const textEl = document.getElementById('simText');
    const indEl = document.getElementById('simIndustry');
    if (textEl) {
      textEl.style.opacity = '0';
      setTimeout(() => {
        textEl.innerText = simDialogs[currentSimIdx].text;
        if (indEl) indEl.innerText = simDialogs[currentSimIdx].industry.toUpperCase();
        textEl.style.opacity = '1';
      }, 200);
    }

    if (window.QuiktalkAnalytics) {
      window.QuiktalkAnalytics.trackSimulatorPlay(simDialogs[currentSimIdx].industry);
    }
  }

  // Audio stub preview handler (PH-05)
  function initAudioStub() {
    const audioButtons = document.querySelectorAll('.audio-stub-btn');
    audioButtons.forEach(btn => {
      btn.addEventListener('click', function () {
        const slot = this.getAttribute('data-slot') || 'emergency-plumbing.mp3';
        const noticeEl = document.getElementById('audioStubNotice');
        if (noticeEl) {
          noticeEl.style.display = 'block';
          noticeEl.innerText = `Sample slot [${slot}] — real recording pending Stage 2 verification (PH-05).`;
        }
        if (window.QuiktalkAnalytics) {
          window.QuiktalkAnalytics.trackSimulatorPlay('audio_stub_' + slot);
        }
      });
    });
  }

  // =============================================================
  // 5. ROI & Revenue Calculator (QTK-008)
  // =============================================================
  function updateRoiCalc() {
    const slider = document.getElementById('roiSlider');
    if (!slider) return;

    const calls = parseInt(slider.value, 10) || 120;
    const callCountLabel = document.getElementById('callCountLabel');
    if (callCountLabel) callCountLabel.innerText = calls + ' calls / mo';

    // Disclosed methodology: 30% missed calls
    const missedCalls = Math.round(calls * 0.3);
    const missedLabel = document.getElementById('missedLabel');
    if (missedLabel) missedLabel.innerText = missedCalls + ' missed';

    // 70% recapture rate via instant 24/7 answer
    const recapturedLeads = Math.round(missedCalls * 0.7);
    const recapturedLeadsEl = document.getElementById('recapturedLeads');
    if (recapturedLeadsEl) recapturedLeadsEl.innerText = recapturedLeads + ' Leads Recaptured';

    // Editable or default $500 avg job value
    const jobValInput = document.getElementById('avgJobValueInput');
    const avgJobValue = jobValInput ? (parseInt(jobValInput.value, 10) || 500) : 500;

    const revenue = Math.round(recapturedLeads * avgJobValue).toLocaleString();
    const recapturedRevEl = document.getElementById('recapturedRevenue');
    if (recapturedRevEl) recapturedRevEl.innerText = '$' + revenue + ' NZD';
  }

  // =============================================================
  // 6. Real Lead Form Submission (QTK-001)
  // =============================================================
  async function handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = document.getElementById('submitBtn');
    const statusBox = document.getElementById('formStatus');

    if (!form || !submitBtn) return;

    // Build payload
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    payload._page = window.location.href;
    payload.userAgent = navigator.userAgent;

    // Track submission attempt
    if (window.QuiktalkAnalytics) {
      window.QuiktalkAnalytics.trackFormSubmitAttempt();
    }

    // Visual loading state
    submitBtn.disabled = true;
    const originalText = submitBtn.innerText;
    submitBtn.innerText = 'RECEIVING DEMO REQUEST...';
    submitBtn.style.opacity = '0.75';

    if (statusBox) {
      statusBox.className = 'form-status info';
      statusBox.innerText = 'Connecting to Quiktalk AI secure server...';
      statusBox.style.display = 'block';
    }

    try {
      const response = await fetch('/api/lead', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok || !data.success) {
        throw new Error(data.message || (data.errors && data.errors[0]) || 'Server could not process request.');
      }

      // SUCCESS CONFIRMED BY SERVER
      submitBtn.innerText = '✓ DEMO REQUEST RECEIVED';
      submitBtn.style.background = '#34d399';
      submitBtn.style.color = '#000';
      submitBtn.style.opacity = '1';

      if (statusBox) {
        statusBox.className = 'form-status success';
        statusBox.innerText = data.message || 'Demo request confirmed! Our Auckland team will configure your voice agent and email you within 1 business day.';
      }

      // Analytics conversion trigger
      if (window.QuiktalkAnalytics) {
        window.QuiktalkAnalytics.trackFormSubmitSuccess(data.leadId);
      }

      // Custom event for downstream hooks
      window.dispatchEvent(new CustomEvent('lead:success', { detail: data }));

      // Reset form fields
      form.reset();

    } catch (err) {
      // ERROR HANDLING - Do not fake success
      console.error('[Lead Form] Submission failed:', err);
      submitBtn.disabled = false;
      submitBtn.innerText = 'TRY AGAIN';
      submitBtn.style.background = '';
      submitBtn.style.color = '';
      submitBtn.style.opacity = '1';

      if (statusBox) {
        statusBox.className = 'form-status error';
        statusBox.innerText = err.message || 'Something went wrong while submitting. Please email admin@quiktalkai.com directly.';
      }

      if (window.QuiktalkAnalytics) {
        window.QuiktalkAnalytics.trackFormSubmitError(err.message);
      }
    }
  }

  // =============================================================
  // 7. Three.js WebGL Scene with Performance Guards (QTK-013)
  // =============================================================
  function initWebGLScene() {
    const canvas = document.getElementById('gl');
    if (!canvas || typeof THREE === 'undefined') return;

    // Check reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      canvas.style.display = 'none';
      return;
    }

    // WebGL capability check with try/catch
    let glContext = null;
    try {
      glContext = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (!glContext) {
        console.warn('[Three.js] WebGL not supported on this device. Graceful fallback active.');
        canvas.style.display = 'none';
        return;
      }
    } catch (e) {
      console.warn('[Three.js] WebGL context initialization error:', e);
      canvas.style.display = 'none';
      return;
    }

    try {
      const scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x060608, 0.012);

      const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.set(0, 2, 22);

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: window.devicePixelRatio < 2, // antialias on low-DPI only to save GPU
        alpha: true,
        powerPreference: 'high-performance'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));

      // PMREM Generator
      const pmremGenerator = new THREE.PMREMGenerator(renderer);
      pmremGenerator.compileEquirectangularShader();
      const envScene = new THREE.Scene();
      envScene.background = new THREE.Color(0x020204);

      const topLight = new THREE.Mesh(
        new THREE.PlaneGeometry(60, 30),
        new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide })
      );
      topLight.position.set(0, 25, 5);
      topLight.rotation.x = Math.PI / 2.2;
      envScene.add(topLight);

      const rimStrip = new THREE.Mesh(
        new THREE.PlaneGeometry(10, 60),
        new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide })
      );
      rimStrip.position.set(25, 0, 10);
      rimStrip.rotation.y = Math.PI / 2.5;
      envScene.add(rimStrip);

      const renderTarget = pmremGenerator.fromScene(envScene);
      pmremGenerator.dispose();
      const chromeEnvMap = renderTarget.texture;

      // Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 2.2);
      scene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xffffff, 8.0);
      keyLight.position.set(10, 20, 15);
      scene.add(keyLight);

      const rimLight = new THREE.SpotLight(0xffffff, 10.0);
      rimLight.position.set(-10, -10, 20);
      scene.add(rimLight);

      const bgCyanLight = new THREE.PointLight(0xe5c158, 4.0, 70);
      bgCyanLight.position.set(25, -12, -15);
      scene.add(bgCyanLight);

      // Headset Group
      const headsetGroup = new THREE.Group();
      const chromeMat = new THREE.MeshStandardMaterial({
        color: 0x666677,
        metalness: 1.0,
        roughness: 0.02,
        envMap: chromeEnvMap,
        envMapIntensity: 10.0
      });

      // Mic Head
      const micHeadGroup = new THREE.Group();
      const micFoamGeo = new THREE.SphereGeometry(0.58, 24, 18);
      const micFoamMat = new THREE.MeshStandardMaterial({ color: 0x181820, roughness: 0.8 });
      const micFoamMesh = new THREE.Mesh(micFoamGeo, micFoamMat);
      micHeadGroup.add(micFoamMesh);

      const micRingGeo = new THREE.TorusGeometry(0.59, 0.05, 12, 24);
      const micRingMesh = new THREE.Mesh(micRingGeo, chromeMat);
      micHeadGroup.add(micRingMesh);

      micHeadGroup.position.set(-1.2, -3.4, 2.8);
      headsetGroup.add(micHeadGroup);

      // Gyro Rings
      const gyro1Geo = new THREE.TorusGeometry(5.2, 0.04, 12, 64);
      const gyro1Mat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.65 });
      const gyro1Mesh = new THREE.Mesh(gyro1Geo, gyro1Mat);
      headsetGroup.add(gyro1Mesh);

      const gyro2Geo = new THREE.TorusGeometry(6.2, 0.03, 12, 64);
      const gyro2Mat = new THREE.MeshBasicMaterial({ color: 0xe5c158, transparent: true, opacity: 0.45 });
      const gyro2Mesh = new THREE.Mesh(gyro2Geo, gyro2Mat);
      gyro2Mesh.rotation.x = Math.PI / 3;
      headsetGroup.add(gyro2Mesh);

      // Responsive layout placement
      function updateLayout() {
        if (window.innerWidth < 768) {
          headsetGroup.position.set(0, 1, -2);
          headsetGroup.scale.set(0.75, 0.75, 0.75);
        } else {
          headsetGroup.position.set(8, 2, 2);
          headsetGroup.scale.set(1.0, 1.0, 1.0);
        }
      }
      updateLayout();
      scene.add(headsetGroup);

      // Sound Particle Cloud
      const particleCount = 600; // optimized count
      const particleGeo = new THREE.BufferGeometry();
      const particlePos = new Float32Array(particleCount * 3);
      const particleColors = new Float32Array(particleCount * 3);
      const colorCyan = new THREE.Color(0xe5c158);
      const colorViolet = new THREE.Color(0xf3d998);

      for (let i = 0; i < particleCount; i++) {
        particlePos[i * 3] = (Math.random() - 0.5) * 80;
        particlePos[i * 3 + 1] = (Math.random() - 0.5) * 40;
        particlePos[i * 3 + 2] = (Math.random() - 0.5) * 80;
        const mixed = colorCyan.clone().lerp(colorViolet, Math.random());
        particleColors[i * 3] = mixed.r;
        particleColors[i * 3 + 1] = mixed.g;
        particleColors[i * 3 + 2] = mixed.b;
      }

      particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
      particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
      const particleMat = new THREE.PointsMaterial({ size: 0.24, vertexColors: true, transparent: true, opacity: 0.6 });
      const particleSystem = new THREE.Points(particleGeo, particleMat);
      scene.add(particleSystem);

      // Dynamic animation controls & performance throttling
      let isRunning = true;
      let isHeroInView = true;
      let isTabActive = true;
      let targetScrollY = 0;
      let scrollY = 0;
      let mouseX = 0, mouseY = 0;
      let targetMouseX = 0, targetMouseY = 0;
      let cachedDocHeight = document.body.scrollHeight || 3000;

      // Cache document height on resize instead of every animation frame
      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        updateLayout();
        cachedDocHeight = document.body.scrollHeight || 3000;
      }, { passive: true });

      window.addEventListener('mousemove', (e) => {
        targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
      }, { passive: true });

      window.addEventListener('scroll', () => {
        targetScrollY = window.scrollY;
      }, { passive: true });

      // Pause rendering when browser tab is hidden (visibilitychange)
      document.addEventListener('visibilitychange', () => {
        isTabActive = !document.hidden;
        if (isTabActive && isHeroInView && !isRunning) {
          isRunning = true;
          requestAnimationFrame(animate);
        }
      });

      // Pause rendering when hero section is out of viewport (IntersectionObserver)
      const heroSection = document.getElementById('hero');
      if (window.IntersectionObserver && heroSection) {
        const heroObserver = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            isHeroInView = entry.isIntersecting;
            if (isHeroInView && isTabActive && !isRunning) {
              isRunning = true;
              requestAnimationFrame(animate);
            }
          });
        }, { threshold: 0.05 });
        heroObserver.observe(heroSection);
      }

      const clock = new THREE.Clock();

      function animate() {
        if (!isTabActive || !isHeroInView) {
          isRunning = false;
          return;
        }

        requestAnimationFrame(animate);
        const time = clock.getElapsedTime();

        scrollY += (targetScrollY - scrollY) * 0.05;
        mouseX += (targetMouseX - mouseX) * 0.05;
        mouseY += (targetMouseY - mouseY) * 0.05;

        const scrollFraction = scrollY / (cachedDocHeight - window.innerHeight || 1);

        headsetGroup.rotation.y = time * 0.35 + mouseX * 0.45;
        headsetGroup.rotation.x = Math.sin(time * 0.5) * 0.18 + mouseY * 0.35;
        headsetGroup.position.y = 2 + Math.sin(time * 1.5) * 0.5;

        gyro1Mesh.rotation.z = time * 0.6;
        gyro2Mesh.rotation.z = -time * 0.4;

        particleSystem.rotation.y = time * 0.03;

        camera.position.z = 22 - scrollFraction * 8;
        camera.position.y = 2 - scrollFraction * 3;
        camera.position.x = Math.sin(scrollFraction * Math.PI * 2) * 5;
        camera.lookAt(headsetGroup.position.x * 0.3, headsetGroup.position.y * 0.3, 0);

        renderer.render(scene, camera);
      }

      animate();

    } catch (err) {
      console.warn('[Three.js] Initialization exception caught:', err);
      if (canvas) canvas.style.display = 'none';
    }
  }

  // =============================================================
  // 8. Lifecycle Initialization
  // =============================================================
  document.addEventListener('DOMContentLoaded', () => {
    initFaq();
    initAudioStub();

    // Wire Simulator buttons
    const simPills = document.querySelectorAll('.sim-pill');
    simPills.forEach((pill, idx) => {
      pill.addEventListener('click', function () {
        simPills.forEach(p => p.classList.remove('active'));
        this.classList.add('active');
        runCallSimulation(idx);
      });
    });

    // Wire Simulator Next button
    const simNextBtn = document.getElementById('simNextBtn');
    if (simNextBtn) {
      simNextBtn.addEventListener('click', () => runCallSimulation());
    }

    // Wire ROI Slider
    const roiSlider = document.getElementById('roiSlider');
    if (roiSlider) {
      roiSlider.addEventListener('input', updateRoiCalc);
      updateRoiCalc();
    }

    const jobValInput = document.getElementById('avgJobValueInput');
    if (jobValInput) {
      jobValInput.addEventListener('input', updateRoiCalc);
    }

    // Wire Lead Form
    const leadForm = document.getElementById('leadForm');
    if (leadForm) {
      leadForm.addEventListener('submit', handleFormSubmit);
    }

    // Initialize 3D scene after idle or frame
    if (window.requestIdleCallback) {
      window.requestIdleCallback(initWebGLScene);
    } else {
      setTimeout(initWebGLScene, 100);
    }
  });

  // Export functions to window for any required legacy calls
  window.QuiktalkApp = {
    toggleMenu,
    scrollToSec,
    runCallSimulation,
    updateRoiCalc,
    handleFormSubmit
  };
})();

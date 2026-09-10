/**
 * assets/js/analytics.js
 * Privacy-First Analytics & Conversion Event Dispatcher for Quiktalk AI (QTK-003)
 * Tracks essential CRO events locally without third-party cookies or intrusive scripts.
 */

(function () {
  'use strict';

  window.QuiktalkAnalytics = {
    // Event buffer for local debugging
    events: [],

    /**
     * Track a custom conversion or engagement event
     * @param {string} eventName Event name (e.g. 'form_submit_success', 'demo_cta_click')
     * @param {object} [eventParams={}] Optional metadata
     */
    track: function (eventName, eventParams = {}) {
      const payload = {
        event: eventName,
        timestamp: new Date().toISOString(),
        url: window.location.pathname,
        params: eventParams
      };

      this.events.push(payload);

      // Dispatch native custom DOM event for any listening integrations
      try {
        const customEvent = new CustomEvent('quiktalk:analytics', { detail: payload });
        window.dispatchEvent(customEvent);
      } catch (e) {
        // Fallback for older browsers
      }

      // If GA4 gtag is present and configured
      if (typeof window.gtag === 'function') {
        window.gtag('event', eventName, eventParams);
      }

      // If Plausible is present
      if (typeof window.plausible === 'function') {
        window.plausible(eventName, { props: eventParams });
      }

      // Safe console logging in local development
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log(`[Quiktalk Analytics] Event: ${eventName}`, eventParams);
      }
    },

    /**
     * Convenience methods for core audit-specified tracking actions
     */
    trackDemoCtaClick: function (source) {
      this.track('demo_cta_click', { cta_source: source || 'unknown' });
    },

    trackSimulatorPlay: function (industry) {
      this.track('simulator_play', { industry: industry || 'default' });
    },

    trackFormSubmitAttempt: function () {
      this.track('form_submit_attempt');
    },

    trackFormSubmitSuccess: function (leadId) {
      this.track('form_submit_success', { lead_id: leadId });
    },

    trackFormSubmitError: function (reason) {
      this.track('form_submit_error', { error_reason: reason });
    },

    trackEmailClick: function () {
      this.track('email_click', { destination: 'admin@quiktalkai.com' });
    },

    trackPhoneClick: function (phoneNumber) {
      this.track('phone_click', { phone: phoneNumber || 'direct' });
    },

    trackPricingView: function (tier) {
      this.track('pricing_view', { tier: tier || 'all' });
    }
  };

  // Wire automatic click delegation for tracked elements
  document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', function (e) {
      const target = e.target.closest('a, button');
      if (!target) return;

      const href = target.getAttribute('href') || '';
      const text = (target.textContent || '').trim().toUpperCase();

      if (href.startsWith('mailto:')) {
        window.QuiktalkAnalytics.trackEmailClick();
      } else if (href.startsWith('tel:')) {
        window.QuiktalkAnalytics.trackPhoneClick(href.replace('tel:', ''));
      } else if (href === '#demo' || text.includes('DEMO') || text.includes('GET MY DEMO')) {
        window.QuiktalkAnalytics.trackDemoCtaClick(target.className || 'button');
      }
    });
  });
})();

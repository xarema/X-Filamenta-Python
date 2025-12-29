/*
 * Purpose: HTMX Utilities
 * Description: Helper functions and event handlers for HTMX interactions
 *
 * File: frontend/static/js/plugins/htmx-utils.js | Repository: X-Filamenta-Python
 * Created: 2025-12-27T00:00:00+00:00
 * Last modified (Git): TBD | Commit: TBD
 *
 * Distributed by: XAREMA | Coder: AleGabMar
 * App version: 0.0.1-Alpha | File version: 0.0.1-Alpha
 *
 * License: AGPL-3.0-or-later
 * SPDX-License-Identifier: AGPL-3.0-or-later
 *
 * Copyright (c) 2025 XAREMA. All rights reserved.
 *
 * Metadata:
 * - Status: Draft
 * - Classification: Public
 *
 * Notes:
 * - ES6+ JavaScript
 * - HTMX 1.9+ compatible
 * - Event handlers for HTMX lifecycle
 * - Notification and error handling
 */

/**
 * HTMX Utilities
 * Helper functions pour HTMX
 */

// Initialisation HTMX
document.addEventListener('DOMContentLoaded', function() {
  console.log('HTMX utilities loaded');

  // Ajouter des événements HTMX personnalisés si nécessaire
  document.body.addEventListener('htmx:afterSwap', function(event) {
    // Callback après un swap HTMX
    console.log('HTMX swap completed');
  });

  document.body.addEventListener('htmx:responseError', function(event) {
    // Gérer les erreurs HTMX
    console.error('HTMX error:', event.detail);
  });
});

// Helper pour afficher des notifications
function showNotification(message, type = 'info') {
  // Simple notification toast
  const toast = document.createElement('div');
  toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
  toast.style.zIndex = '9999';
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

// Export pour utilisation globale
window.htmxUtils = {
  showNotification
};

